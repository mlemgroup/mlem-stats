import json
import os
from typing import TypedDict

from objects.instance import Instance
from objects.major_version import MajorVersion

PER_DAY_CACHE_LENGTH = 30
"""
The length of time, in days, for which per-day version counts are maintained in output/versions/version/*.json
"""


class ShortVersionList(TypedDict):
    """
    The schema of output/versions/short_list.json
    """

    time: int
    versions: list[MajorVersion.ShortData]


class FullVersionList(TypedDict):
    """
    The schema of output/versions/full_list.json
    """

    time: int
    versions: list[MajorVersion.FullData]


class TopInstancesVersions(TypedDict):
    time: int
    instances: dict[str, str]


class VersionCount(TypedDict):
    time: int
    count: int


class SingleVersionData(TypedDict):
    """
    The schema of output/version/*.json
    """

    per_day: list[VersionCount]
    per_week: list[VersionCount]


class UpdateEvent(TypedDict):
    host: str
    precise_time: int | None
    old_version: str
    new_version: str


class EventGroup(TypedDict):
    time: int
    events: list[UpdateEvent]


def write_all(
    instances: list[Instance],
    versions: list[MajorVersion],
    time: int,
) -> None:
    """
    Write data from the given list of MajorVersion instances to the files stored under the output/versions directory
    """
    write_events_and_instance_versions(instances, time)
    write_short_list_file(versions, time)
    write_full_list_file(versions, time)
    write_single_version_files(versions, time)


def write_events_and_instance_versions(instances: list["Instance"], time: int) -> None:
    with open("output/versions/instance_versions.json", "r") as f:
        yesterday_data: TopInstancesVersions = json.load(f)

    if yesterday_data["time"] == time:
        print(
            "Yesterday's instance_versions.json has matching timestamp. Not updating instance_versions.json"
        )
        return

    today_data = TopInstancesVersions(
        time=time, instances={i.baseurl: i.version for i in instances}
    )

    with open("output/versions/instance_versions.json", "w") as f:
        json.dump(today_data, f, indent=4)
    print("Wrote to output/versions/instance_versions.json")

    today_events: list[UpdateEvent] = []
    for instance, today_value in today_data["instances"].items():
        yesterday_value = yesterday_data["instances"].get(instance)
        if yesterday_value is not None and today_value != yesterday_value:
            today_events.append(
                UpdateEvent(
                    host=instance,
                    precise_time=None,
                    old_version=yesterday_value,
                    new_version=today_value,
                )
            )

    if today_events:
        print(f"Saving {len(today_events)} recent version changes...")
        with open("output/versions/recent_events.json", "r") as f:
            event_groups: list[EventGroup] = json.load(f)

        event_groups.append(EventGroup(time=time, events=today_events))

        if len(event_groups) > 30:
            del event_groups[0]

        with open("output/versions/recent_events.json", "w") as f:
            json.dump(event_groups, f)

        print("Wrote to output/versions/recent_events.json")
    else:
        print("There were no recent version changes.")


def write_short_list_file(versions: list["MajorVersion"], time: int) -> None:
    versions.sort(key=lambda x: x.value, reverse=True)
    with open("output/versions/version_list_short.json", "w") as f:
        data = ShortVersionList(
            time=time,
            versions=[i.to_short_dict() for i in versions],
        )
        json.dump(data, f, indent=4)
    print("Wrote to output/versions/version_list_short.json")


def write_full_list_file(versions: list["MajorVersion"], time: int) -> None:
    versions.sort(key=lambda x: x.value, reverse=True)
    with open("output/versions/version_list_full.json", "w") as f:
        data = FullVersionList(
            time=time,
            versions=[i.to_full_dict() for i in versions],
        )
        json.dump(data, f)
    print("Wrote to output/versions/version_list_full.json")


def write_single_version_files(versions: list["MajorVersion"], time: int) -> None:
    existing_files = os.listdir("output/versions/version")
    for version in versions:
        filename = f"output/versions/version/{version.name}.json"
        data: SingleVersionData
        if f"{version.name}.json" in existing_files:
            with open(filename, "r") as f:
                data = json.load(f)
            existing_files.remove(f"{version.name}.json")
        else:
            data = SingleVersionData(per_day=[], per_week=[])

        new_count = VersionCount(time=time, count=version.count_including_variations)

        if (not data["per_day"]) or data["per_day"][-1]["time"] != time:
            data["per_day"].append(new_count)
            if len(data["per_day"]) > PER_DAY_CACHE_LENGTH:
                del data["per_day"][0]

        if (not data["per_week"]) or (
            time - data["per_week"][-1]["time"]
        ) >= 6.9 * 24 * 60 * 60:
            data["per_week"].append(new_count)

        with open(filename, "w") as f:
            json.dump(data, f)

    print("Wrote to files under output/versions/version directory")
    if existing_files:
        print(f"There are {len(existing_files)} dead version files:")
        for file in existing_files:
            print(f"- {file}")
        print()
