// Copyright (C) 2016 Sayutin Dmitry.
// This program is free software; you can redistribute it and/or
// modify it under the terms of the GNU General Public License as
// published by the Free Software Foundation; version 3.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
// 
// You should have received a copy of the GNU General Public License
// along with this program; If not, see <http://www.gnu.org/licenses/>. -->

function do_reload_image(elem) {
    if (typeof elem.potential == "undefined")
        elem.potential = 5;

    if (elem.potential != 0) {
        elem.potential -= 1;
        window.setTimeout(function(elem) {
            elem.src = "/image.png?rnd=" + Math.floor(Math.random() * 10000);
        }, 1000, elem);
    }
}

function rescan_requested() {
    var req = new XMLHttpRequest()
    req.onreadystatechange = function() {
        if (req.readyState == 4 && req.status == 200) {
            elem = document.getElementById("scan");
            elem.potential = 30;
            elem.src = "/image.png?rnd=" + Math.floor(Math.random() * 10000);
        }
    }
    req.open("GET", "/rescan", true);
    req.send(null);
}
