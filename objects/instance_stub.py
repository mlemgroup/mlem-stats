from typing import TypedDict


class InstanceStub(TypedDict):
    """
    Used in instances_by_score.json.
    """

    name: str
    host: str
    user_count: int
    avatar: str | None
    version: str
