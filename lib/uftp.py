"""
Based on micropython-ftplib 0.1.0 by SpotlightKid:
    https://github.com/SpotlightKid/micropython-ftplib

Which was based on on CPython's ftplib by Guido van Rossum, et al.:
    https://github.com/python/cpython/blob/3.7/Lib/ftplib.py

Python Software Foundation License
"""

import usocket as socket

MAXLINE = 2048
CRLF = '\r\n'
B_CRLF = b'\r\n'
_GLOBAL_DEFAULT_TIMEOUT = object()

class Error(Exception): pass
class ReplyError(Error): pass
class TempError(Error): pass
class PermError(Error): pass
class ProtoError(Error): pass
class FTP:

    sock = None
    file = None
    encoding = "latin-1"

    def __init__(self, host=None, port=21, user=None, passwd=None, acct=None,
                 timeout=_GLOBAL_DEFAULT_TIMEOUT):
        self.host = host
        self.port = port
        self.timeout = timeout
        if host:
            self.connect(host, port)
            if user:
                self.login(user, passwd, acct)
                self.sendcmd("TYPE I")

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if self.sock is not None:
            try:
                self.quit()
            except (OSError, EOFError):
                pass
            finally:
                if self.sock is not None:
                    self.close()

    def _create_connection(self, addr, timeout=None):
        sock = socket.socket(socket.AF_INET)
        sock.connect(addr)
        if timeout not in [None, _GLOBAL_DEFAULT_TIMEOUT]:
            sock.settimeout(timeout)
        return sock

    def connect(self, host=None, port=None, timeout=None):
        self.host = host if host else self.host
        self.port = port if port else self.port
        self.timeout = timeout if timeout else self.timeout
        self.sock = self._create_connection((self.host, self.port), timeout)
        return self.getresp()

    def login(self, user='anonymous', passwd='anonymous@', acct=''):
        resp = self.sendcmd('USER ' + user)
        if resp[0] == '3':
            resp = self.sendcmd('PASS ' + passwd)
        if resp[0] == '3':
            resp = self.sendcmd('ACCT ' + acct)
        if resp[0] != '2':
            raise ReplyError(resp)
        return resp

    def quit(self):
        resp = self.voidcmd('QUIT')
        self.close()
        return resp

    def close(self):
        sock = self.sock
        self.sock = None
        if sock is not None:
            sock.close()

    def getline(self):
        line = str(self.sock.recv(MAXLINE), self.encoding)
        if len(line) > MAXLINE:
            raise Error("got more than %d bytes" % MAXLINE)
        if not line:
            raise EOFError
        return line.rstrip('\r\n')

    def getmultiline(self):
        line = self.getline()
        if line[3:4] == '-':
            code = line[:3]
            while 1:
                nextline = self.getline()
                line = line + ('\n' + nextline)
                if nextline[:3] == code and \
                        nextline[3:4] != '-':
                    break
        return line

    def getresp(self):
        resp = self.getmultiline()
        c = resp[:1]
        if c in ['1', '2', '3']:
            return resp
        if c == '4':
            raise TempError(resp)
        if c == '5':
            raise PermError(resp)
        raise ProtoError(resp)

    def voidresp(self):
        resp = self.getresp()
        if not resp.startswith('2'):
            raise ReplyError(resp)
        return resp

    def sendcmd(self, cmd):
        cmd += CRLF
        self.sock.send(cmd.encode(self.encoding))
        return self.getresp()

    def voidcmd(self, cmd):
        resp = self.sendcmd(cmd)
        if not resp.startswith('2'):
            raise ReplyError(resp)
        return resp

    def makepasv(self):
        host, port = parse227(self.sendcmd('PASV'))
        return host, port

    def transfercmd(self, cmd, fp=None, callback=print, blocksize=MAXLINE, rest=None):
        host, port = self.makepasv()
        conn = self._create_connection((host, port), self.timeout)
        try:
            if rest is not None:
                self.sendcmd("REST %s" % rest)

            resp = self.sendcmd(cmd)
            if resp[0] == '2':
                resp = self.getresp()
            if resp[0] != '1':
                raise ReplyError(resp)
        except:
            conn.close()
            raise
        while 1:
            if 'STOR' in cmd:
                data = fp.read(blocksize)
            elif 'LIST' in cmd or 'RETR' in cmd or 'NLST' in cmd:
                data = conn.recv(blocksize)
            else:
                raise ValueError('Unknown Command')
            if not data:
                break
            if 'STOR' in cmd:
                conn.send(data)
            callback(data)
        conn.close()
        return self.voidresp()

    def stor(self, localname, remotename=None, **kw):
        remotename = localname if not remotename else remotename
        return self.transfercmd('STOR ' + remotename, fp=open(localname, 'rb'), **kw)

    def retr(self, filename, **kw):
        return self.transfercmd('RETR ' + filename, **kw)

    def list(self, *args, **kw):
        return self.transfercmd(" ".join(['LIST'] + list(args)), **kw)

    def abort(self):
        line = b'ABOR' + B_CRLF
        self.sock.send(line, 0x1)
        resp = self.getmultiline()
        if resp[:3] not in ['426', '225', '226']:
            raise ProtoError(resp)
        return resp

    def rename(self, fromname, toname):
        resp = self.sendcmd('RNFR ' + fromname)
        if resp[0] != '3':
            raise ReplyError(resp)
        return self.voidcmd('RNTO ' + toname)

    def delete(self, filename):
        resp = self.sendcmd('DELE ' + filename)
        if resp[:3] in ['250', '200']:
            return resp
        else:
            raise ReplyError(resp)

    def cwd(self, dirname):
        cmd = 'CWD ' + dirname if dirname != '..' else 'CDUP'
        return self.voidcmd(cmd)

    def size(self, filename):
        resp = self.sendcmd('SIZE ' + filename)
        if resp[:3] == '213':
            s = resp[3:].strip()
            return int(s)
        return 0

    def mkd(self, dirname):
        resp = self.voidcmd('MKD ' + dirname)
        return parse257(resp) if resp.startswith('257') else ''

    def rmd(self, dirname):
        return self.voidcmd('RMD ' + dirname)

    def pwd(self):
        resp = self.sendcmd('PWD')
        return '' if not resp.startswith('257') else parse257(resp)


def parse227(resp):
    if not resp.startswith('227'):
        raise ReplyError("Unexpected response: %s" % resp)
    try:
        left = resp.find('(')
        if left < 0:
            raise ValueError("missing left delimiter")
        right = resp.find(')', left + 1)
        if right < 0:
            raise ValueError("missing right delimiter")
        numbers = tuple(int(i) for i in resp[left+1:right].split(',', 6))
        host = '%i.%i.%i.%i' % numbers[:4]
        port = (numbers[4] << 8) + numbers[5]
    except Exception as exc:
        raise ProtoError("Error parsing response '%s': %s" % (resp, exc))

    return host, port

def parse257(resp):
    if resp[3:5] != ' "':
        return ''
    resp = resp.replace('257', '')
    resp = resp.replace('"', '')
    return resp.strip()
