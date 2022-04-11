import json
import http_socks
import os
import base64
from utils import settings
#import requests


class SpotifyAuthentication:
    def __init__(self) -> None:
        self.quick_socket = http_socks.Https_socket('accounts.spotify.com')
        self.api_socket = http_socks.Https_socket('api.spotify.com')
        #self.quick_socket = requests.Session()
        self.token = (
            "Basic "
            + base64.b64encode(
                f"{settings.secrets['spotify']['client_id']}:{settings.secrets['spotify']['client_secret']}".encode()
            ).decode()
        )


    def get_tokens(self, authCode):
        return self.quick_socket.request(
            "POST", 
            f'/api/token?grant_type=authorization_code&code={authCode}&redirect_uri={settings.host["hostname"]}/api/login/spotify',
            headers = {'Authorization': self.token}
        )

    def get_token_from_refresh_token(self, refreshToken):
        return json.loads(self.quick_socket.request(
            "POST",
            f'/api/token?grant_type=refresh_token&refresh_token={refreshToken}',
            headers = {'Authorization': self.token}
        ))['access_token']

class Spotify(SpotifyAuthentication):
    def __init__(self) -> None:
        super().__init__()
    
    def get_userinfo(self, data):
        req = json.loads(
            self.api_socket.request(
                "GET",
                '/v1/me',
                headers = {'Authorization': 'Bearer ' + data['access_token']}
            )
        )
        if 'error' not in req:
            return {'email': req['email'], 'id': req['id'], 'refresh_token': data['refresh_token']}
    
    def get_user_playlists(self, access_token, offset=0, playlists=[]):
        req = json.loads(self.api_socket.request(
            'GET',
            f"/v1/me/playlists?offset={offset}&limit=50",
            headers = {'Authorization': 'Bearer ' + access_token}
        ))
        playlists += req['items']
        if req['total'] > len(playlists):
            return self.get_user_playlists(access_token, offset + 50, playlists)
        return playlists

    def get_user_liked_tracks(self, access_token, offset=0, tracks = [], limit=10):
        req = json.loads(self.api_socket.request(
            'GET',
            f'/v1/me/tracks?offset={offset}&limit={limit}',
            headers = {'Authorization': 'Bearer ' + access_token}
        ))
        tracks += req['items']
        if req['total'] > len(tracks) and len(tracks) < limit:
            return self.get_user_liked_tracks(access_token, offset + 10, tracks)
        return tracks, req['total']
    
    def get_playlist_tracks(self, access_token, playlist_id, offset=0, tracks = [], limit=10):
        req = json.loads(self.api_socket.request(
            'GET',
            f'/v1/playlists/{playlist_id}/tracks?offset={offset}&limit={limit}',
            headers = {'Authorization': 'Bearer ' + access_token}
        ))
        tracks += req['items']
        if req['total'] > len(tracks) and len(tracks) < limit:
            return self.get_playlist_tracks(access_token, offset + 10, tracks)
        return tracks