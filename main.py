import os

from objects.instance import Instance
from objects.instance_stub import InstanceStub
from objects.major_version import MajorVersion
import json
import ssl
import datetime
import urllib.request
import re

ssl._create_default_https_context = ssl._create_unverified_context

with urllib.request.urlopen("https://data.lemmyverse.net/data/meta.json") as f:
    data = json.load(f)
    lemmyverse_last_updated = datetime.datetime.fromtimestamp(data["time"] // 1000)
    last_updated_timestamp = int(lemmyverse_last_updated.timestamp())
    print(
        f"{lemmyverse_last_updated:Lemmyverse was last updated on %m/%d/%Y at %H:%M:%S.}"
    )


instances = Instance.load_all()

with open("input/blacklist.json", "r") as f:
    blacklist: list[str] = json.load(f)

print("Processing instances...")
instances_by_score: list[InstanceStub] = []
instance_versions: dict[str, MajorVersion] = {}

for instance in instances:
    if (
        match := re.match(r"(?P<main>\d+\.\d+\.\d)(?:[+-].+)?", instance.version)
    ) is not None:
        main = match.group("main")
        instance_versions.setdefault(main, MajorVersion(name=main))
        instance_versions[main].add(instance)

    if (
        instance.score > 0
        and instance.user_count >= 20
        and instance.sus_reason is None
        and instance.baseurl not in blacklist
    ):
        instances_by_score.append(instance.to_dict())

with open("output/instances_by_score.json", "w") as f:
    json.dump(instances_by_score, f)

versions = list(instance_versions.values())
versions.sort(key=lambda x: x.value, reverse=True)

with open("output/versions/short_list.json", "w") as f:
    data = {
        "timestamp": last_updated_timestamp,
        "versions": [i.to_short_dict() for i in versions],
    }
    json.dump(data, f, indent=4)

with open("output/versions/full_list.json", "w") as f:
    data = {
        "timestamp": last_updated_timestamp,
        "versions": [i.to_full_dict() for i in versions],
    }
    json.dump(data, f)

existing_files = os.listdir("output/versions/version")
for version in versions:
    filename = f"output/versions/version/{version.name}.json"
    if f"{version.name}.json" in existing_files:
        with open(filename, "r") as f:
            data = json.load(f)
    else:
        data = {"per_day": [], "per_week": []}

    new_count = {
        "time": last_updated_timestamp,
        "count": version.count_including_variations,
    }

    if (not data["per_day"]) or data["per_day"][-1]["time"] != last_updated_timestamp:
        data["per_day"].append(new_count)
        if len(data["per_day"]) > 30:
            del data["per_day"][0]

    if (not data["per_week"]) or (
        last_updated_timestamp - data["per_week"][-1]["time"]
    ) >= 6.9 * 24 * 60 * 60:
        data["per_week"].append(new_count)

    with open(filename, "w") as f:
        json.dump(data, f)


print(
    f"Saved {len(instances_by_score)} of {len(instances)} instances to instances_by_score.json"
)
