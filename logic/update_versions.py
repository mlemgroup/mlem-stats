import json
import os
from typing import TypedDict

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


class VersionCount(TypedDict):
    time: int
    count: int


class SingleVersionData(TypedDict):
    """
    The schema of output/version/*.json
    """

    per_day: list[VersionCount]
    per_week: list[VersionCount]


def write_all(
    versions: list["MajorVersion"],
    time: int,
) -> None:
    """
    Write data from the given list of MajorVersion instances to the files stored under the output/versions directory
    """

    write_short_list_file(versions, time)
    write_full_list_file(versions, time)
    write_single_version_files(versions, time)


def write_short_list_file(versions: list["MajorVersion"], time: int) -> None:
    versions.sort(key=lambda x: x.value, reverse=True)
    with open("output/versions/short_list.json", "w") as f:
        data = ShortVersionList(
            time=time,
            versions=[i.to_short_dict() for i in versions],
        )
        json.dump(data, f, indent=4)
    print("Wrote to output/versions/short_list.json")


def write_full_list_file(versions: list["MajorVersion"], time: int) -> None:
    versions.sort(key=lambda x: x.value, reverse=True)
    with open("output/versions/full_list.json", "w") as f:
        data = FullVersionList(
            time=time,
            versions=[i.to_full_dict() for i in versions],
        )
        json.dump(data, f)
    print("Wrote to output/versions/full_list.json")


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
