from dataclasses import dataclass

from datetime import tzinfo


@dataclass
class SecretConfig:


    hash: str = None
    

    @classmethod
    def from_dict(cls, data: dict) -> "SecretConfig":
        return cls(
            hash=data["checksum"]
        )