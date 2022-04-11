from flask import Flask, request, abort, make_response, redirect
import json
from utils import (spotify, postgres, cookies, Youtube, settings)
from spotify_api import spotify_api_BP
from google_api import youtube_api_BP


cookieSession = cookies.Cookies()
conn = postgres.Auth()

app = Flask(__name__)
app.register_blueprint(spotify_api_BP)
app.register_blueprint(youtube_api_BP)

@app.route("/api/login/spotify")
def log_in_with_spotify():
    spot = spotify.Spotify()
    if "code" in request.args:
        resp = json.loads(spot.get_tokens(request.args.get("code")))
        data = spot.get_userinfo(resp)

        curr_cookie = request.cookies.get('session', "e30=")
        result = conn.log_in(data, scope='spotify', cookie=cookieSession.decode_cookie(curr_cookie))
        flask_response = make_response(redirect(f'{settings.host["hostname"]}/transfer'))
        flask_response.set_cookie("session", cookieSession.add_params(curr_cookie, result), max_age=3600)
        return flask_response
    return abort(403)


@app.route("/api/login/google")
def log_in_with_google():
    if "code" not in request.args:
        return redirect(f'https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id={Youtube.CLIENT_ID}&redirect_uri={settings.host["hostname"]}/api/login/google&scope=email https://www.googleapis.com/auth/youtube&access_type=offline')
    else:
        yt = Youtube.Youtube()

        #Get cookie
        code = yt.authenticate_with_code(request.args.get('code')) #sealt tuleb refresh token
        cookie = request.cookies.get("session", "e30=")

        #Get email
        email = yt.get_user_email(code['id_token'])
        #print(code)
        result = conn.log_in({'email':email, 'google_refresh_token':code['refresh_token']}, scope='google', cookie=cookieSession.decode_cookie(cookie))
        #print(result)
        cookie = cookieSession.add_params(cookie, result)
        print(cookieSession.decode_cookie(cookie))

        flask_response = make_response(redirect(f'{settings.host["hostname"]}/transfer'))
        flask_response.set_cookie("session", cookie, max_age=3600)
        return flask_response


@app.route('/api/google/create_playlist', methods=['POST'])
def create_playlist():
    #Get user auth
    curr_cookie = request.cookies.get('session')
    user_data = cookieSession.decode_cookie(curr_cookie)

    #Get data
    post_data = request.get_json()

    yt = Youtube.Youtube()
    r = yt.create_user_playlist(user_data['google_access_token'], post_data['title'])
    return r


if __name__ == "__main__":
    app.run(debug=True)