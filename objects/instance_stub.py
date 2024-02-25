from typing import TypedDict


class InstanceStub(TypedDict, total=False):
    """
    Used in instances_by_score.json.
    """

    name: str
    host: str
    user_count: int
    avatar: str | None
    version: str
