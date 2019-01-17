#!/usr/bin/python3
from urllib import request, parse
import json

serverUrl = "https://gitlab.com/api/v4"
projectId = input("Project: (e.g. mynamespace/myproject)\n> ")
token = "your_api_token_here"


def make_req(url, data=None, method="GET"):
    req = request.Request(url, data, method=method)
    req.add_header('PRIVATE-TOKEN', token)
    resp = request.urlopen(req).read().decode()
    return json.loads(resp or '{}')


numIgnore = int(input("Leave this many pipelines (0):\n> ") or "0")
erased_pipelines = 0

print()
print("Working...")

while True:
    pipelines = make_req(
        f"{serverUrl}/projects/{parse.quote_plus(projectId)}/pipelines")
    if len(pipelines) <= numIgnore:
        break
    for pl in pipelines[numIgnore:]:
        make_req(
            f"{serverUrl}/projects/{parse.quote_plus(projectId)}/pipelines/{pl['id']}", method="DELETE")
        erased_pipelines += 1

print(f"Done! Erased {erased_pipelines} pipelines.")
