#!/usr/bin/python3
from urllib import request, parse
import json

serverUrl = "https://gitlab.com/api/v4"
projectId = input("Project: (e.g. gitlab/myproject)\n> ")
token = "your_api_token_here"

erased_pipelines = 0
erased_jobs = 0


def make_req(url, data=None, method="GET"):
    req = request.Request(url, data, method=method)
    req.add_header('PRIVATE-TOKEN', token)
    return json.loads(request.urlopen(req).read().decode())


def erase_jobs(pl):
    global erased_jobs
    jobs = make_req(
        f"{serverUrl}/projects/{parse.quote_plus(projectId)}/pipelines/{pl['id']}/jobs")
    for job in jobs:
        try:
            make_req(
                f"{serverUrl}/projects/{parse.quote_plus(projectId)}/jobs/{job['id']}/erase", None, "POST")
        except:
            pass
        erased_jobs += 1


print()
print("Working...")

pipelines = make_req(
    f"{serverUrl}/projects/{parse.quote_plus(projectId)}/pipelines")

if len(pipelines) > 1:
    for pl in pipelines[1:]:
        erase_jobs(pl)
        erased_pipelines += 1

print("Done!")
print(f"Erased {erased_pipelines} pipelines and {erased_jobs} jobs.")
