A script that fetches instance data from https://data.lemmyverse.net/ and proccesses it into JSON files stored under the `output` directory. The script is executed every 24h by a Github Action. The Mlem client fetches the JSON files from the repo to display in-app data.

# Output Files

## `output/instances_by_score.json`

This list is used by Mlem for the instance-searching feature. Instances are stored in the following format:

```json
{
  "name": "Lemmy.World",
  "host": "lemmy.world",
  "user_count": 149400,
  "avatar": "https://lemmy.world/pictrs/image/0fc7f14b-ffcb-43d0-bef1-cf759b76d821.png",
  "version": "0.18.5"
}
```

The list of instances is sorted by a 'score' value. This value is determined by data.lemmyverse.net. It roughly (but not exactly) corresponds to the size of the instance. 

An instance is excluded from the list if:
- It has a negative score.
- It has less than 20 users.
- It has a `susReason`.
- It is listed in the `input/blacklist.json` file.
