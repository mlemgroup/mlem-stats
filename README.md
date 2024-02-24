A script that fetches instance data from https://data.lemmyverse.net/ and proccesses it into JSON files stored under the `output` directory. The script is executed every 24h by a Github Action. The Mlem client fetches the JSON files from the repo to display in-app data.

# Data Schema

Output files always store instances with the following properties.

```json
{
  "name": "Lemmy.World",
  "host": "lemmy.world",
  "user_count": 149400,
  "avatar": "https://lemmy.world/pictrs/image/0fc7f14b-ffcb-43d0-bef1-cf759b76d821.png",
  "version": "0.18.5"
}
```

# Output Files

## `instances_by_score.json`

This list is used by Mlem for the instance-searching feature. It is a list of instances (stored in the format described above).
The list of instances is sorted by a 'score' value, which is determined by data.lemmyverse.net. 

An instance is excluded from the list if:
- It has a negative score.
- It has less than 20 users.
- It has a `susReason`.
- It is listed in the `input/blacklist.json` file.

## `versions/short_list.json`

A list of Lemmy versions, with the number of instances running each version. This counts all Lemmy instances, and isn't filtered like `instances_by_score.json` is. This isn't currently used in Mlem yet.

```json
{
  "timestamp": 1708776308.0,
  "versions": [
    {
      "name": "0.19.3",
      "count": 352,
      "count_including_variations": 354,
      "variations": [
        {
          "name": "0.19.3-rc.4",
          "count": 1
        },
        {
          "name": "0.19.3-rc.3",
          "count": 1
        }
      ]
    }
  ]
}
```

## `versions/full_list.json`

Similar to `versions/short_list.json`, but adds an additional `instances` property that stores a list of all instances running that version. Each instance in the list uses the format described under Data Schema above.

## `versions/version/*.json`

Stores the number of instances running a version or any variations of that version for each day over the last 30 days, and each week since the version was first seen. Data isn't guaranteed to be recorded exactly every day/week - no data will be recorded if zero instances were running that version on a given day.