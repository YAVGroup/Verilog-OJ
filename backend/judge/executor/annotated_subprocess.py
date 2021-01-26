r"""Subprocess with timestamp annotations

Order between stdout and stderr is not guarantee to be preserved.

Not design for heavy stdout and stderr I/O environment.

Ref: https://gist.github.com/smoser/6714b6c741a6f658b41e
"""

import datetime, os, threading
import subprocess

__all__ = ['Popen']

def fp_readlines(fp, sizehint=None):
    if sizehint is None:
        sizehint = 1024

    leftover = bytes()
    while True:
        buf = os.read(fp, sizehint)
        eof = buf == b''

        if leftover:
            buf = leftover + buf
            leftover = bytes()

        while True:
            end = buf.find(b'\n')
            if end != -1:
                yield buf[0:end+1]
                buf = buf[end+1:]
            else:
                leftover = buf
                break

        if eof:
            if len(leftover) > 0:
                yield leftover
            break

def ftime(fmt, ts=None):
    if ts is None:
        ts = datetime.datetime.now()
    return datetime.datetime.strftime(ts, fmt)

def addtime(fh_in, buf_out, buf_mutex, fmt='%H:%M:%S '):
    fmtfunc = ftime
    for line in fp_readlines(fh_in):
        with buf_mutex:
            print(line)
            buf_out += fmtfunc(fmt).encode() + line

# TODO: implement me
def run(*args, **kwargs):
    pass

class Popen(subprocess.Popen):
    def __init__(self, args, shell=False, env=None):
        """Only support some args for now"""
        
        self.out_r, self.out_w = os.pipe()
        self.err_r, self.err_w = os.pipe()

        super().__init__(args, shell=shell, env=env, stdout=self.out_w, stderr=self.err_w)

    def communicate(self):
        """The data is buffered in memory
        Returns a large buffer
        """
        threads = []
        buffer = bytearray()

        # Ensures I/O by line
        buffer_mutex = threading.Lock()

        try:
            t = threading.Thread(
                target=addtime, args=(self.out_r, buffer, buffer_mutex, '[%H:%M:%S] '))
            t.start()
            threads.append(t)

            t = threading.Thread(
                target=addtime, args=(self.err_r, buffer, buffer_mutex, '[ERR %H:%M:%S] '))
            t.start()
            threads.append(t)

            super().communicate()

        finally:
            os.close(self.out_w)
            os.close(self.err_w)

            for t in threads:
                t.join()

            os.close(self.out_r)
            os.close(self.err_r)

            return buffer


