from dataclasses import dataclass

from datetime import tzinfo


@dataclass
class GeneralConfig:


    timezone: str = None


    @classmethod
    def from_dict(cls, data: dict) -> "GeneralConfig":
        return cls(
            timezone=data["timezone"]
        )