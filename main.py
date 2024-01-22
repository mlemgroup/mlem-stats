import urllib.request
import json

import ssl

ssl._create_default_https_context = ssl._create_unverified_context

with urllib.request.urlopen("https://data.lemmyverse.net/data/instance.full.json") as f:
    instances: list[dict] = json.load(f)

instances.sort(key=lambda x: x["score"], reverse=True)

print(instances[0])
output = []

for i in instances:
    if i["score"] <= 0 or i["counts"]["users"] < 10 or i["susReason"]:
        continue

    new = {
        "name": i["name"],
        "url": i["url"],
        "user_count": i["counts"]["users"],
        "avatar": i.get("icon"),
        "version": i["version"]
    }

    output.append(new)

with open("output/instances_by_score.json", "w") as f:
    json.dump(output, f)


print(f"Saved {len(output)} of {len(instances)} instances")