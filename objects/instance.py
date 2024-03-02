from typing import Any
import urllib.request
import json

from objects.instance_stub import InstanceStub


class Instance:
    """
    The instance data received from data.lemmyverse.net.
    """

    @classmethod
    def load_all(cls) -> list["Instance"]:
        print("Reading instances...")
        with urllib.request.urlopen(
            "https://data.lemmyverse.net/data/instance.full.json"
        ) as f:
            instances: list[Instance] = []
            raw_instances: list[dict[str, Any]] = json.load(f)
            for instance_data in raw_instances:
                try:
                    instances.append(Instance(instance_data))
                except KeyError:
                    print(
                        f"    Failed to read instance data for {instance_data['baseurl']}"
                    )

        instances.sort(key=lambda x: x.score, reverse=True)
        print(
            f"Successfully read {len(instances)} of {len(raw_instances)} instances, "
            f"unable to read {len(raw_instances) - len(instances)}"
        )
        return instances

    def __init__(self, data: dict[str, Any]) -> None:
        # This isn't all properties we have available
        self.baseurl: str = data["baseurl"]  # lemmy.world
        self.url: str = data["url"]  # https://lemmy.world/
        self.name: str = data["name"]
        self.desc: str = data["desc"]
        self.downvotes_enabled: bool = data["downvotes"]
        self.nsfw_content_allowed: bool = data["nsfw"]
        self.private: bool = data["private"]
        self.federated: bool = data["fed"]
        self.version: str = data["version"]
        self.registration_open: bool = data["open"]
        self.user_count = data["counts"]["users"]
        self.score: int = data["score"]
        self.sus_reason: str | None = data.get("sus_reason")
        self.avatar: str | None = data.get("icon")

    @property
    def host(self) -> str:
        return (
            self.url.removeprefix("https://").removeprefix("http://").removesuffix("/")
        )

    def to_dict(self, include_version: bool = True) -> "InstanceStub":
        if include_version:
            return InstanceStub(
                name=self.name,
                host=self.host,
                user_count=self.user_count,
                avatar=self.avatar,
                version=self.version,
            )
        else:
            return InstanceStub(
                name=self.name,
                host=self.host,
                user_count=self.user_count,
                avatar=self.avatar,
            )
