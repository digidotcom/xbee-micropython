"""
Based on micropython-urequests 0.6 from micropython-lib:
    https://github.com/micropython/micropython-lib/tree/master/urequests

Copyright (c) 2013, 2014 micropython-lib contributors
MIT License
"""

import usocket

class Response:

    def __init__(self, f):
        self.raw = f
        self.encoding = "utf-8"
        self._cached = None

    def close(self):
        if self.raw:
            self.raw.close()
            self.raw = None
        self._cached = None

    @property
    def content(self):
        if self._cached is None:
            try:
                self._cached = self.raw.read()
            finally:
                self.raw.close()
                self.raw = None
        return self._cached

    @property
    def text(self):
        return str(self.content, self.encoding)

    def json(self):
        import ujson
        return ujson.loads(self.content)


def request(method, url, data=None, json=None, headers={}, stream=None,
            verify=None, cert=None):
    try:
        scheme, _, host, path = url.split("/", 3)
    except ValueError:
        scheme, _, host = url.split("/", 2)
        path = ""
    if scheme == "http:":
        port = 80
        proto = usocket.IPPROTO_TCP
    elif scheme == "https:":
        import ussl
        port = 443
        proto = usocket.IPPROTO_SEC
    else:
        raise ValueError("Unsupported scheme: " + scheme)

    if ":" in host:
        host, port = host.split(":", 1)
        port = int(port)

    s = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM, proto)
    try:
        if proto == usocket.IPPROTO_SEC:
            wrap_params = {'server_hostname':host}
            if cert is not None:
                wrap_params['certfile'] = cert[0]
                wrap_params['keyfile'] = cert[1]
            if verify is not None:
                wrap_params['ca_certs'] = verify
            s = ussl.wrap_socket(s, **wrap_params)
        s.connect((host, port))
        s.write(b"%s /%s HTTP/1.0\r\n" % (method, path))
        if not "Host" in headers:
            s.write(b"Host: %s\r\n" % host)
        # Iterate over keys to avoid tuple alloc
        for k in headers:
            s.write(k)
            s.write(b": ")
            s.write(headers[k])
            s.write(b"\r\n")
        if json is not None:
            assert data is None
            import ujson
            data = ujson.dumps(json)
            s.write(b"Content-Type: application/json\r\n")
        if data:
            s.write(b"Content-Length: %d\r\n" % len(data))
        s.write(b"\r\n")
        if data:
            s.write(data)

        l = s.readline()
        #print(l)
        l = l.split(None, 2)
        status = int(l[1])
        reason = ""
        if len(l) > 2:
            reason = l[2].rstrip()
        while True:
            l = s.readline()
            if not l or l == b"\r\n":
                break
            #print(l)
            if l.startswith(b"Transfer-Encoding:"):
                if b"chunked" in l:
                    raise ValueError("Unsupported " + l)
            elif l.startswith(b"Location:") and not 200 <= status <= 299:
                raise NotImplementedError("Redirects not yet supported")
    except OSError:
        s.close()
        raise

    resp = Response(s)
    resp.status_code = status
    resp.reason = reason
    return resp


def head(url, **kw):
    return request("HEAD", url, **kw)

def get(url, **kw):
    return request("GET", url, **kw)

def post(url, **kw):
    return request("POST", url, **kw)

def put(url, **kw):
    return request("PUT", url, **kw)

def patch(url, **kw):
    return request("PATCH", url, **kw)

def delete(url, **kw):
    return request("DELETE", url, **kw)
