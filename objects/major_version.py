from objects.instance import Instance
from objects.version import Version


class MajorVersion(Version):
    class ShortData(Version.ShortData):
        variations: list[Version.ShortData]
        count_including_variations: int

    class FullData(Version.FullData):
        variations: list[Version.FullData]
        count_including_variations: int

    def __init__(self, name: str) -> None:
        super().__init__(name=name)
        self.variations: dict[str, "Version"] = {}

    def add(self, instance: Instance) -> None:
        if instance.version == self.name:
            super().add(instance)
        else:
            self.variations.setdefault(instance.version, Version(name=instance.version))
            self.variations[instance.version].add(instance)

    @property
    def count_including_variations(self) -> int:
        return len(self.instances) + sum(len(i.instances) for i in self.variations.values())

    def to_short_dict(self) -> ShortData:
        variations = self.variations.values()

        return MajorVersion.ShortData(
            name=self.name,
            count=len(self.instances),
            count_including_variations=self.count_including_variations,
            variations=[i.to_short_dict() for i in variations],
        )

    def to_full_dict(self) -> FullData:
        variations = list(self.variations.values())
        variations.sort(key=lambda x: x.value, reverse=True)

        return MajorVersion.FullData(
            name=self.name,
            count=len(self.instances),
            count_including_variations=self.count_including_variations,
            instances=self.sort_instances(),
            variations=[i.to_full_dict() for i in variations],
        )
