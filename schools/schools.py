""" Tool to update the school database."""

import datetime
import os
import pathlib
import json
import socket
import sys
import time

import bs4
import geopy
import requests

SLEEP_TIME = 5 # seconds

directory = pathlib.Path(__file__).parent.resolve()
parent = pathlib.Path(__file__).parent.parent.resolve()
path_html: str = os.path.join(directory, "schools.html")
path_json: str = os.path.join(directory, "schools.json")
path_md: str = os.path.join(directory, "SCHOOLS.md")
path_py: str = os.path.join(parent, "src", "pyelternportal", "schools.py")

year_month = datetime.date.today().isoformat()[:8]
geolocator = geopy.geocoders.Nominatim(user_agent="pyelternportal")

with open(path_json, mode="r", encoding="utf-8") as read_file:
    data = json.load(read_file)

for school in sys.argv[1:]:
    if next((s for s in data if s["school"] == school), None) is None:
        data.append({"school": school})

data.sort(key=lambda s: s["school"])

for s in data:
    if "domain" not in s and s["school"] is not None:
        s["domain"] = f"{s["school"]}.eltern-portal.org"

    if "url" not in s and s["domain"] is not None:
        s["url"] = f"https://{s["domain"]}"

    ipcheck = (
        "ip" not in s or "ip_lastcheck" not in s or year_month not in s["ip_lastcheck"]
    )
    if ipcheck and s["domain"] is not None:
        hostname = s["domain"]
        ip = socket.gethostbyname(hostname)
        print(f"resolve {hostname} to {ip}")
        s["ip"] = ip
        s["ip_lastcheck"] = datetime.date.today().isoformat()

    namecheck = (
        "name" not in s
        or "exists" not in s
        or "name_lastcheck" not in s
        or year_month not in s["name_lastcheck"]
    )
    if namecheck and s["url"] is not None:
        response = requests.get(url=s["url"], timeout=30)
        html = response.text
        if "Dieses Eltern-Portal existiert nicht" in html:
            print(f"resolve {s["url"]} to 'Eltern-Portal existiert nicht'")
            s["exists"] = False
            s["name"] = None
        else:
            soup = bs4.BeautifulSoup(html, "html5lib")
            tag = soup.find("h2", {"id": "schule"})
            name = tag.get_text() if tag is not None else None
            print(f"resolve {s["url"]} to {name}")
            s["exists"] = True
            s["name"] = name
        s["name_lastcheck"] = datetime.date.today().isoformat()
        time.sleep(SLEEP_TIME)

    geocheck = (
        "geo" not in s
        or "geo_lastcheck" not in s
        or year_month not in s["geo_lastcheck"]
    )
    if geocheck and s["name"] is not None:
        name_geo = s["name_geo"] if "name_geo" in s else s["name"]
        location = geolocator.geocode(
            name_geo, addressdetails=True, language="de", country_codes="de"
        )
        if location is None:
            print(f"resolve {name_geo} to None")
            s["geo"] = None
        else:
            geotype = location.raw["type"]
            address = location.raw["address"]
            if geotype == "school":
                postcode = address["postcode"]
                city =  address["city"] if "city" in address else address.get("town")
                print(f"resolve {name_geo} to {postcode} {city}")
                s["geo"] = {
                    "type": geotype,
                    "lat": location.raw["lat"],
                    "lon": location.raw["lon"],
                    "name": location.raw["name"],
                    "road": address["road"],
                    "house_number": address.get("house_number"),
                    "postcode": postcode,
                    "city": city,
                    "country": address["country"],
                }
            else:
                print(f"resolve {name_geo} to {geotype}")
                s["geo"] = {
                    "type": geotype,
                }
        s["geo_lastcheck"] = datetime.date.today().isoformat()
        time.sleep(SLEEP_TIME)


with open(path_md, mode="w", encoding="utf-8") as fh:
    fh.write("# Known instances of Eltern-Portal\n")
    fh.write("\n")
    fh.write("Identifier | Url                                   | School\n")
    fh.write(":--------- | :------------------------------------ | :-----\n")
    for s in data:
        if s.get("exists", False):
            identifier = s["school"]
            url = s.get("url")
            school = s.get("name")
            if "geo" in s and s["geo"] is not None:
                geo = s["geo"]
                if "postcode" in geo and geo["postcode"] is not None:
                    school += ", " + geo["postcode"]
                    if "city" in geo and geo["city"] is not None:
                        school += " " + geo["city"]
                else:
                    if "city" in geo and geo["city"] is not None:
                        school += ", " + geo["city"]

            fh.write(f"{identifier:<10} | {url:<37} | {school}\n")

with open(file=path_py, mode="w", encoding="utf-8") as fh:
    fh.write('""" Known instances of eltern-portal.org """\n\n')
    fh.write("# pylint: disable=too-many-lines\n\n")
    fh.write("from .school import School\n\n")
    fh.write("SCHOOLS = [\n")
    for s in data:
        if s.get("exists", False):
            fh.write("    School(\n")
            fh.write('        school="' + s["school"] + '",\n')
            if "name" in s and s["name"]:
                fh.write('        name="' + s["name"] + '",\n')
            if "geo" in s and s["geo"] and s["geo"]["type"] == "school":
                if s["geo"]["postcode"]:
                    fh.write('        postcode="' + s["geo"]["postcode"] + '",\n')
                if s["geo"]["city"]:
                    fh.write('        city="' + s["geo"]["city"] + '",\n')
            fh.write("    ),\n")
    fh.write("]\n")

with open(file=path_json, mode="w", encoding="utf-8") as fh:
    json.dump(obj=data, fp=fh, indent=2, sort_keys=True)


with open(file=path_html, mode="w", encoding="utf-8") as fh:
    fh.writelines('<!DOCTYPE html>')
    fh.writelines('<html lang="en">')
    fh.writelines('<head>')
    fh.writelines('    <base target="_top">')
    fh.writelines('    <meta charset="utf-8">')
    fh.writelines('    <meta name="viewport" content="width=device-width, initial-scale=1">')
    fh.writelines('    <title>Schools</title>')
    fh.writelines('    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />')
    fh.writelines('    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>')
    fh.writelines('    <style>')
    fh.writelines('        html, body {')
    fh.writelines('            height: 100%;')
    fh.writelines('            margin: 0;')
    fh.writelines('        }')
    fh.writelines('    </style>')
    fh.writelines('</head>')
    fh.writelines('<body>')
    fh.writelines('    <div id="map" style="width: 100%; height: 100%;"></div>')
    fh.writelines('    <script>')
    fh.writelines("        const map = L.map('map').setView([51.163361, 10.447683], 7);")
    fh.writelines("        const tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {")
    fh.writelines("            maxZoom: 19,")
    fh.writelines("            attribution: '&copy; <a href=\"http://www.openstreetmap.org/copyright\">OpenStreetMap</a>'")
    fh.writelines("        }).addTo(map);")
    for s in data:
        if "geo" in s and s["geo"]:
            geo = s["geo"]
            if "lat" in geo and geo["lat"] and "lon" in geo and geo["lon"]:
                fh.writelines(f"        const m_{s["school"]} = L.marker([{geo["lat"]}, {geo["lon"]}]).bindTooltip('{s["school"]}: {s["name"]}').addTo(map);")
    fh.writelines('    </script>')
    fh.writelines('</body>')
    fh.writelines('</html>')
