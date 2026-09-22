from dataclasses import dataclass


@dataclass
class RepositoryReport:

    
    success: bool = True
    incompatible: bool = False
    integrity: bool | None = None