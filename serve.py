#!/usr/bin/python3

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

# !! This is very simple server, mostly for testing.
# !! However you can use in small networks.
# !! Make sure that it will not be visible in global internet.

from wsgiref.simple_server import make_server
import main
import os

try:
    # in case of forced stop
    os.unlink('image.lock')
except:
    pass

httpd = make_server('', 8080, main.application);
print("Serving on port 8080")
httpd.serve_forever()
