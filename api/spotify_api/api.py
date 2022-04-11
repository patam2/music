import os

from flask import Blueprint, request, abort
from utils import cookies, spotify


spotify_api_BP = Blueprint('spotify_api', __name__)
cookieSession = cookies.Cookies()


@spotify_api_BP.route("/api/spotify/get_playlists")
def get_spotify_playlists():
    spot = spotify.Spotify()
    if "session" in request.cookies:
        cookie = request.cookies.get("session")
        temp_token = cookieSession.decode_cookie(cookie)["spotify_access_token"]
        if not temp_token:
            return abort(403)
        return {"playlists": spot.get_user_playlists(temp_token, playlists=[])}
    return abort(403)


@spotify_api_BP.route("/api/spotify/get_liked_songs")
def get_spotify_likes():
    spot = spotify.Spotify()
    if "session" in request.cookies:
        cookie = request.cookies.get("session")
        temp_token = cookieSession.decode_cookie(cookie)["spotify_access_token"]
        if not temp_token:
            return abort(403)
        tracks = spot.get_user_liked_tracks(temp_token, tracks=[])
        return {"total": tracks[1], "tracks": tracks[0]}
    return abort(403)


@spotify_api_BP.route("/api/spotify/get_tracks_from_playlist")
def get_playlist_tracks():
    spot = spotify.Spotify()
    if "session" in request.cookies:
        cookie = request.cookies.get("session")
        temp_token = cookieSession.decode_cookie(cookie)["spotify_access_token"]
        if not temp_token:
            return abort(403)
        tracks = spot.get_playlist_tracks(
            temp_token, request.args.get("playlist_id"), tracks=[]
        )
        return {"tracks": tracks}