A script that fetches instance data from https://data.lemmyverse.net/ and proccesses it into JSON files stored under the `output` directory. The script is executed every 24h by a Github Action. The Mlem client fetches the JSON files from the repo to display in-app data.

# Output Files

## `output/instances_by_score.json`

A list of instances sorted by score, and filtered to exclude certain instances. This list is used by Mlem for the instance-searching feature. Instances are stored in the following format:

```json
{
  "name": "Lemmy.World",
  "host": "lemmy.world",
  "user_count": 149400,
  "avatar": "https://lemmy.world/pictrs/image/0fc7f14b-ffcb-43d0-bef1-cf759b76d821.png",
  "version": "0.18.5"
}
```
