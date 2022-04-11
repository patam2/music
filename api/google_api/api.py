from flask import Blueprint, request, abort
from utils import cookies, Youtube, spotify
import threading


youtube_api_BP = Blueprint('youtube', __name__)

cookieSession = cookies.Cookies()
spotifySession = spotify.Spotify()
youtubeSession = Youtube.Youtube()


def add_songs(all_spotify_tracks, session_data, youtube_playlist):
    for spotify_track in all_spotify_tracks:
        q = ', '.join(artist['name'] for artist in spotify_track['track']['artists'])
        q += f' - {spotify_track["track"]["name"]}'

        search = youtubeSession.search_for_first_result(session_data['google_access_token'], q)
        youtubeSession.add_to_playlist(session_data['google_access_token'], youtube_playlist, search['id']['videoId'])


@youtube_api_BP.route('/api/youtube/transfer', methods=['POST'])
def transfer_playlist():
    #return {'url': 'https://www.youtube.com/watch?v=879ysA4h9r4&list=PLmNwLlfxZxG3VA5Vi1U0phKRfnno0klVL'}
    session_data = cookieSession.decode_cookie(request.cookies['session'])
    if "google_access_token" not in session_data or "spotify_access_token" not in session_data:
        return abort(403)
    
    if request.json.get('playlist_id') == 'LIKED':
        all_spotify_tracks = spotifySession.get_user_liked_tracks(
            access_token=session_data['spotify_access_token'],
            tracks=[],
            limit=3
        )[0]
    else:
        all_spotify_tracks = spotifySession.get_playlist_tracks(
            access_token=session_data['spotify_access_token'],
            playlist_id=request.json.get('playlist_id'),
            tracks=[],
            limit=3
        )

    youtube_playlist = youtubeSession.create_user_playlist(session_data['google_access_token'], request.json.get('playlist_name'))

    threading.Thread(
        target = add_songs,
        args = (all_spotify_tracks, session_data, youtube_playlist,)
    ).start()

    return {'url': f'https://youtube.com/playlist?list={youtube_playlist}'}