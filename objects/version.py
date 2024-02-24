import re
from typing import TypedDict

from objects.instance import Instance
from objects.instance_stub import InstanceStub


class Version:
    class ShortData(TypedDict):
        name: str
        count: int

    class FullData(ShortData):
        instances: list[InstanceStub]

    def __init__(self, name: str) -> None:
        self.name: str = name
        self.instances: list[InstanceStub] = []

    def add(self, instance: Instance) -> None:
        self.instances.append(instance.to_dict())

    def to_short_dict(self) -> ShortData:
        return Version.ShortData(name=self.name, count=len(self.instances))

    def to_full_dict(self) -> FullData:
        return Version.FullData(name=self.name, instances=self.instances)

    @property
    def value(self) -> tuple[int, ...]:
        value: list[int] = [0, 0, 0, 0, 0]
        match = re.match(
            r"(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)(?P<suffix>[+-].+)?",
            self.name,
        )
        value[0] = match.group("major")
        value[1] = match.group("minor")
        value[2] = match.group("patch")
        suffix = match.group("suffix")
        if suffix is not None:
            if suffix.startswith("-rc."):
                try:
                    value[3] = 2
                    value[4] = int(suffix.removeprefix("-rc.").split(".")[0])
                except ValueError:
                    pass
            elif suffix.startswith("-beta."):
                try:
                    value[3] = 1
                    value[4] = int(suffix.removeprefix("-beta.").split(".")[0])
                except ValueError:
                    pass
        return tuple(value)
