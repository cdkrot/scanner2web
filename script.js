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

function document_loaded() {
    document.getElementById("btn0").hidden = "false"
}

function do_reload_image(elem) {
    if (typeof elem.potential == "undefined")
        elem.potential = 10;

    if (elem.potential != 0) {
        elem.potential -= 1;
        elem.alt = "Waiting for the server" + "..".repeat(3 - elem.potential % 3);
        window.setTimeout(function(elem) {
            elem.src = "/image.png?rnd=" + Math.floor(Math.random() * 10000);
        }, 900, elem);
    } else {
        elem.alt = "Waiting for the server. No image recieved. Try reloading page or pressing rescan button.";
    }
}

function rescan_requested() {
    var req = new XMLHttpRequest()
    req.onreadystatechange = function() {
        if (req.readyState == 4 && req.status == 200) {
            var elem = document.getElementById("scan");
            elem.potential = 20;
            elem.src = "/image.png?rnd=" + Math.floor(Math.random() * 10000);
        }
    }
    req.open("GET", "/rescan", true);
    req.send(null);
}
