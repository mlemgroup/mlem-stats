import urllib.request
import json

import ssl

ssl._create_default_https_context = ssl._create_unverified_context

with urllib.request.urlopen("https://data.lemmyverse.net/data/instance.full.json") as f:
    instances: list[dict] = json.load(f)

instances.sort(key=lambda x: x["score"], reverse=True)

output = []

for i in instances:
    if i["score"] <= 0 or i["counts"]["users"] < 10 or i["susReason"]:
        continue

    new = {
        "display_name": i["name"],
        "name": i["baseurl"],
        "user_count": i["counts"]["users"],
        "avatar": i.get("icon"),
        "version": i["version"]
    }

    output.append(new)

print(f"Saved {len(output)} of {len(instances)} instances")
with open("output/instances_by_score.json", "w") as f:
    json.dump(output, f)
