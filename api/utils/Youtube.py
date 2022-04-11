import requests
from utils import cookies, settings
from utils.Exceptions import YoutubeAccountNotMade


CLIENT_ID = settings.secrets['youtube']['client_id']
CLIENT_SECRET = settings.secrets['youtube']['client_secret']

# https://developers.google.com/identity/protocols/oauth2/scopes#youtube
# https://developers.google.com/identity/protocols/oauth2/web-server?hl=en#httprest_5


class YoutubeAuth:
    def __init__(self) -> None:
        self.api_key = settings.secrets['youtube']['api_key']
        self.cookies = cookies.Cookies()
        self.session = requests.session()

    def authenticate_with_code(self, code):
        req = requests.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uri": f'{settings.host["hostname"]}/api/login/google',
                "grant_type": "authorization_code",
            },
        ).json()

        return req

    def get_access_token(self, code):
        return self.session.post(
            "https://oauth2.googleapis.com/token",
            data={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "refresh_token": code,
                "grant_type": "refresh_token",
            },
        ).json()["access_token"]

    def get_user_email(self, openid_auth):
        return self.session.get(
            f"https://oauth2.googleapis.com/tokeninfo?id_token={openid_auth}"
        ).json()["email"]


class Youtube(YoutubeAuth):
    def __init__(self) -> None:
        super().__init__()

    def create_user_playlist(self, access_token, title) -> str:
        req = self.session.post(
            url=f"https://youtube.googleapis.com/youtube/v3/playlists?part=snippet&key={self.api_key}",
            headers={"Authorization": f"Bearer {access_token}"},
            json={"snippet": {"title": title}},
        ).json()
        #print(req)
        if 'error' in req:
            if req['error']['code'] == 401:
                raise YoutubeAccountNotMade('Youtube account not created. Sign in with your brand account.')
        return req["id"]

    def search_for_first_result(self, access_token, query) -> dict:
        req = self.session.get(
            url=f"https://youtube.googleapis.com/youtube/v3/search?part=snippet&q={query}&key={self.api_key}",
            headers={"Authorization": f"Bearer {access_token}"},
        ).json()
        #print(req)
        return req["items"][0]

    def add_to_playlist(self, access_token, playlist_id, video_id):
        return self.session.post(
            url=f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet&key={self.api_key}",
            headers={"Authorization": f"Bearer {access_token}"},
            json={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {"videoId": video_id, "kind": "youtube#video"},
                }
            },
        ).json()
