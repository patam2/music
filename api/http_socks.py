import socket
import ssl
import json
import logging


logging.basicConfig(filename='httprequests.log', encoding='utf-8', level=logging.DEBUG)

class Https_socket:
    def __init__(self, host) -> None:
        self.host = host
        #self.socket_conn = self.create_sock()

    def _apply_headers(self, method, headers, data):
        h = (
            f"Host: {self.host}\r\n"
            "Accept: application/json\r\n"
            "Content-Type: %s"
            f"Content-Length: {0 if not data else len(json.dumps(data))}\r\n"
            % (
                "application/x-www-form-urlencoded\r\n"
                if method == "POST" and self.host == "accounts.spotify.com"
                else "application/json\r\n"
            )
        )
        for key, item in headers.items():
            h += f"{key}: {item}\r\n"
        return h

    def _get_content_length(self, data):
        data = data.lower()
        if b"content-length" in data:
            return int(data.split(b"content-length: ")[1].split(b"\r\n")[0])
        else:
            return 0

    def create_sock(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock = ssl.create_default_context().wrap_socket(
            sock,
            server_side=False,
            server_hostname=self.host,
            do_handshake_on_connect=True,
        )
        sock.connect((self.host, 443))
        return sock

    def request(self, method, url, headers={}, data=None, tries=1):
        self.socket_conn = self.create_sock()
        logging.debug("%s %s HTTP/1.1\r\n%s\r\n%s\r\n\r\n"
            % (
                method,
                url,
                self._apply_headers(method, headers, data),
                (json.dumps(data) if data else ""),
        ))
        if tries >= 3:
            print("Tried 3 times!")
            return None
        try:
            self.socket_conn.sendall(
                str.encode(
                    "%s %s HTTP/1.1\r\n%s\r\n%s\r\n\r\n"
                    % (
                        method,
                        url,
                        self._apply_headers(method, headers, data),
                        (json.dumps(data) if data else ""),
                    )
                )
            )
            data = self.socket_conn.recv(4048)
            data, body = data.split(b"\r\n\r\n")
            content_length = self._get_content_length(data)
            while content_length > len(body) or body.endswith(b"\r\n"):
                body += self.socket_conn.recv(4048)
            self.socket_conn.shutdown(2)
            logging.debug(body[:270])
            return body
        except WindowsError:
            self.socket_conn.shutdown(2)
            self.socket_conn = self.create_sock()
            return self.request(tries + 1)