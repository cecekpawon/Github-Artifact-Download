#!/usr/bin/env python

import json, re, sys, time

try:
  from urllib.request import Request,urlopen
except ImportError:
  from urllib2 import Request,urlopen

banner = """\
-
GITHUB ////////////////////////////////////////////////////
///////// ARTIFACT | @cecekpawon - Mon Feb  8 14:57:06 2021
DOWNLOAD //////////////////////////////////////////////////
"""

print(banner)

if len(sys.argv) != 6:
  print("{:10s}: {} <owner> <repo> <jobs> <pattern> <token>".format("Usage", sys.argv[0]))
  print("{:10s}: Owner name".format(" <owner>"))
  print("{:10s}: Repo name".format(" <repo>"))
  print("{:10s}: Total jobs in workflow to fetch".format(" <jobs>"))
  print("{:10s}: Pattern to match artifact name".format(" <pattern>"))
  print("{:10s}: Github secret token".format(" <token>"))
  print("{:10s}: {} acidanthera OpenCorePkg 4 xcode xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx".format("Ex", sys.argv[0]))
  sys.exit(1)

owner   = sys.argv[1]
repo    = sys.argv[2]
jobs    = sys.argv[3]
pattern = sys.argv[4]
token   = sys.argv[5]

url_api = "https://api.github.com/repos/{}/{}/actions/artifacts?per_page={}&page=1"
url_str = url_api.format(owner, repo, jobs)

try:
  url = urlopen(url_str)
except:
  print("Failed to open url")
  sys.exit(1)

try:
  data = json.loads(url.read().decode())
except ValueError:
  print("Invalid JSON data")
  sys.exit(1)

if not "artifacts" in data:
  print("Key 'artifacts' doesn't exist in JSON data")
  sys.exit(1)

for item in data["artifacts"]:
  if re.search(pattern, item["name"], re.IGNORECASE):
    id = item["id"]
    name = item["name"]
    url = item["archive_download_url"]
    size_in_bytes = item["size_in_bytes"]
    filename = "{}-{}.zip".format(name, id);

    print("Found artifact with: id ({}) name ({}) size ({}) output ({})".format(id, name, size_in_bytes, filename))

    request = Request(url)
    request.add_header("Authorization", "Bearer " + token)
    response = urlopen(request)

    with open(filename, "wb") as f:
      total=0
      while True:
        data = response.read(1024)
        if not len(data):
          sys.stdout.write("\n")
          #sys.stdout.flush()
          break
        f.write(data)
        total += len(data)
        block = int((50 * total) // size_in_bytes) + 1
        percents = int((100 * total) // size_in_bytes) + 1
        sys.stdout.write("\r")
        sys.stdout.write("[{}{}] {}%".format("#" * block, " " * (50 - block), percents))
        sys.stdout.flush()
        #time.sleep(0.002)
