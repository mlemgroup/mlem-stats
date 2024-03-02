import json
import ssl
import datetime
import urllib.request
import re

from objects.instance import Instance
from objects.instance_stub import InstanceStub
from objects.major_version import MajorVersion

from logic import update_versions

ssl._create_default_https_context = ssl._create_unverified_context

with urllib.request.urlopen("https://data.lemmyverse.net/data/meta.json") as f:
    data = json.load(f)
    lemmyverse_last_updated = datetime.datetime.fromtimestamp(data["time"] // 1000)
    last_updated_timestamp = int(lemmyverse_last_updated.timestamp())
    print(
        f"{lemmyverse_last_updated:Lemmyverse was last updated on %m/%d/%Y at %H:%M:%S}"
    )


instances = Instance.load_all()

with open("input/blacklist.json", "r") as f:
    blacklist: list[str] = json.load(f)

print("\nProcessing instances...")
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

print(
    f"Wrote {len(instances_by_score)} of {len(instances)} instances to instances_by_score.json"
)

update_versions.write_all(list(instance_versions.values()), time=last_updated_timestamp)
