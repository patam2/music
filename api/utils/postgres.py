import os
import psycopg2
import psycopg2.extras
from utils import cookies, spotify, Youtube, settings


class Postgres:
    def __init__(self) -> None:
        self.conn = psycopg2.connect(
            (
                f"dbname={settings.database['dbname']} "
                f"user={settings.database['user']} "
                f"password={settings.secrets['postgres']['secret']}"
            )
        )
        self.cookies = cookies.Cookies()
        self.spot_conn = spotify.Spotify()
        self.google_conn = Youtube.YoutubeAuth()

class Auth(Postgres):
    def __init__(self) -> None:
        super().__init__()


    def __google_log_in(self, cursor, data, cookie={}):
        if "spotify_access_token" in cookie:
            cursor.execute(
                ("UPDATE public.users "
                    "SET google_email = %s, google_refresh_token = %s "
                    "WHERE email = %s;"
                    "SELECT * FROM public.users WHERE google_email = %s;"),
                (data["email"], data['google_refresh_token'], cookie['email'], data['email'],),
            )
        else:
            cursor.execute(
                ("INSERT INTO public.users (google_email, google_refresh_token)"
                    "SELECT %s, %s"
                    "WHERE NOT EXISTS (SELECT * FROM public.users WHERE google_email = %s);"
                    "SELECT * FROM public.users WHERE google_email = %s;"),
                (data['email'], data['google_refresh_token'], data["email"], data['email'],),
            )
        r = cursor.fetchone()
        self.conn.commit()
        if not r:
            return {}
        return dict(r)

    def __spotify_log_in(self, cursor, data, cookie={}):
        if 'google_access_token' in cookie:
            cursor.execute(
                ("UPDATE public.users "
                    "SET email = %s, refresh_token = %s "
                    "WHERE google_email = %s;"
                    "SELECT * FROM public.users WHERE email = %s;"),
                (data["email"], data['refresh_token'], cookie['google_email'], data['email'],),
            )

        else:
            cursor.execute(
                ("INSERT INTO public.users (id, email, refresh_token)"
                    "SELECT %s, %s, %s"
                    "WHERE NOT EXISTS (SELECT * FROM public.users WHERE email = %s);"
                    "SELECT * FROM public.users WHERE email = %s;"),
                (data["id"], data['email'], data['refresh_token'], data['email'],data['email'],),
            )
        r = cursor.fetchone()
        self.conn.commit()
        return r
    def log_in(self, data, scope, cookie={}):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as curs:
            if scope == "spotify":
                result = self.__spotify_log_in(curs, data, cookie)
    
            if scope == "google":
                result = self.__google_log_in(curs, data, cookie)

        if result.get('refresh_token', None):
            result["spotify_access_token"] = self.spot_conn.get_token_from_refresh_token(result["refresh_token"])
            del result["refresh_token"]
        if result.get('google_refresh_token', None):
            result["google_access_token"] = self.google_conn.get_access_token(result["google_refresh_token"])
            del result["google_refresh_token"]

        return result
