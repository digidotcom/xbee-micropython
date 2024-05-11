"""
Based on micropython-urequests 0.6 from micropython-lib:
    https://github.com/micropython/micropython-lib/tree/master/urequests

Copyright (c) 2013, 2014 micropython-lib contributors
MIT License

NOTE: Added support for HTTP/1.1, which will be used, if specified by setting
      request_1_1 to True in the options for the request() command.

NOTE: Due to the extremely small amount of memory available for use on the
      XBee Cellular products, it is not always possible to fit the entire
      payload of a given request in the resulting content/text variable.
      Because of this, a read() function has been added to the Response.
      Using read(), you can receive data in specified sized data chunks,
      so as to not run out of memory.
      When this functionality is used, the content and text values on
      the Response class are not longer valid.
"""

import usocket

class Response:

    def __init__(self, f, chunked_response):
        self.raw = f
        self.encoding = "utf-8"
        self._cached = None
        self._chunked_response = chunked_response
        self._chunk_size = 0

    def close(self):
        if self.raw:
            self.raw.close()
            self.raw = None
        self._cached = None

    def read(self, sz=16 * 1024):
        if self._chunked_response:
            if self._chunk_size == 0:
                l = self.raw.readline()
                #print("chunk line:", l)
                if l == b"":
                    return b""
                l = l.split(b";", 1)[0]
                self._chunk_size = int(l, 16)
                #print("chunk size:", self._chunk_size)
                if self._chunk_size == 0:
                    # End of message
                    sep = self.raw.read(2)
                    assert sep == b"\r\n"
                    return b""
            data = self.raw.read(min(sz, self._chunk_size))
            self._chunk_size -= len(data)
            if self._chunk_size == 0:
                sep = self.raw.read(2)
                assert sep == b"\r\n"
        else:
            data = self.raw.read(sz)
        return data

    @property
    def content(self):
        if self._cached is None:
            try:
                if self._chunked_response:
                    while True:
                        data = self.read()
                        if data == b"":
                            break
                        if self._cached is None:
                            self._cached = data
                        else:
                            self._cached += data
                else:
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
            verify=None, cert=None, request_1_1=False):
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
        if request_1_1:
            s.write(b"%s /%s HTTP/1.1\r\n" % (method, path))
        else:
            s.write(b"%s /%s HTTP/1.0\r\n" % (method, path))
        if not "Host" in headers:
            s.write(b"Host: %s\r\n" % host)
        s.write(b"Connection: close\r\n")
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
        chunked = False
        while True:
            l = s.readline()
            if not l or l == b"\r\n":
                break
            #print(l)
            if l.startswith(b"Transfer-Encoding:"):
                if b"chunked" in l:
                    chunked = True
            elif l.startswith(b"Location:") and not 200 <= status <= 299:
                raise NotImplementedError("Redirects not yet supported")
    except OSError:
        s.close()
        raise

    resp = Response(s, chunked)
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
