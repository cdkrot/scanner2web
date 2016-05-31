# Copyright (C) 2016 Sayutin Dmitry.
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; If not, see <http://www.gnu.org/licenses/>.


from functools import partial
import subprocess
import os
import threading
from time import sleep

codes = {
    200: "200 OK",
    301: "301 Moved Permanently",
    404: "404 Not Found",
    503: "503 Service Temporary Unavailable"
}

def acquire_lock():
    for ret in range(5):
        try:
            os.open('image.lock', os.O_EXCL | os.O_CREAT)
            return True
        except:
            sleep(0.5)
    return False

def free_lock():
    os.unlink('image.lock')

# should be called in new thread.
def start_scanning():
    if not acquire_lock():
        return
    
    p1 = subprocess.Popen(['scanimage'], stdout=subprocess.PIPE);
    p2 = subprocess.Popen(['convert', 'pnm:-', 'png:image.png'], stdin=p1.stdout)
    p1.stdout.close() # somehow important for SIGPIPE's.
    p2.communicate()

    free_lock()

def request_rescan(env, start_response):
    threading.Thread(target=start_scanning, daemon=False).start()
    
    headers = [('Content-Type', 'text/plain'), ('Cache-Control', 'no-cache, no-store')]
    start_response(codes[200], headers)
    return [b"scan"]
    
def serve_static(filpath, conttype, env, start_response):
    start_response(codes[200], [('Content-Type', conttype)])
    return [open(filpath, 'rb').read()]

def image_server(env, start_response):
    if not acquire_lock():
        start_response(codes[503], [])
        return []

    headers = [('Content-Type', 'image/png'), ('Cache-Control', 'no-cache, no-store')]
    res = []
    try:
        res = [open('image.png', 'rb').read()]
        start_response(codes[200], headers)
    except:
        start_response(codes[503], headers)

    free_lock()
    return res

def get_redirect(path):
    if path != '/' and path.endswith('/'):
        return path[:len(path) - 1]
    return None

routing = {
    '/': partial(serve_static, filpath='index.html', conttype='text/html'),
    '/style.css': partial(serve_static, filpath='style.css', conttype='text/css'),
    '/script.js': partial(serve_static, filpath='script.js', conttype='text/javascript'),
    '/image.png': image_server,
    '/rescan': request_rescan
}

def application(env, start_response):
    path = env['PATH_INFO']
    host = env['HTTP_HOST']
    redir = get_redirect(path)
    
    if redir != None:
        headers = [('Content-Type', 'text/html'), ('Location', host + redir)]
        start_response(codes[301], headers)

        res = "Moved permanently to {}".format(host + redir)
        return [res.encode()]
        
    if path in routing:
        return routing[path](env=env, start_response=start_response)
    else:
        start_response(codes[404], [('Content-Type', 'text/html')])
        return ['404. Sorry, this page doesn\'t exist'.encode()]
