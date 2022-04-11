import json
import base64
from utils import spotify


spotClient = spotify.Spotify()

class Cookies:
    def __init__(self, **kwargs) -> None:
        cookies = {**kwargs}

    def create_cookie(self, result) -> str:
        return base64.b64encode(
            str.encode(
                json.dumps(
                    result
                )
            )
        ).decode()
    
    def decode_cookie(self, cookie) -> dict:
        return json.loads(base64.b64decode(
            cookie
        ).decode())

    def add_params(self, cookie, dictionary={}) -> str:
        if isinstance(cookie, dict): cookie = self.decode_cookie()
        if not cookie: cookie = b'e30='
        return self.create_cookie(self.decode_cookie(cookie) | dictionary)
