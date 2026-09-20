from dataclasses import dataclass


@dataclass
class RepositoryReport:
    incompatible: bool = False
    integrity: bool | None = None