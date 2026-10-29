from dataclasses import dataclass


@dataclass(frozen=True)
class Storage:


    name: str
    path: str
    warning_percent: int
    critical_percent: int


    @classmethod
    def from_dict(cls, data: dict) -> "Storage":
        return cls(
            name=data["name"],
            path=data["path"],
            warning_percent=data["warning_percent"],
            critical_percent=data["critical_percent"]
        )