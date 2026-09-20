from abc import ABC, abstractmethod
from dataclasses import dataclass

from restic_backup_report.models.repository import Repository
from restic_backup_report.models.repository_report import RepositoryReport


class Report(ABC):


    def __init__(self) -> None:
        super().__init__()

        self.repositories: dict[Repository, RepositoryReport] = {}


    def append_repository(self, repo: Repository) -> None:
        self.repositories[repo] = RepositoryReport()


    def set_repository_incompatible(self, repo: Repository) -> None:
        self.repositories[repo].incompatible = True
    

    def set_repository_integrity(self, repo: Repository, status: bool) -> None:
        self.repositories[repo].integrity = status


    def finish(self, repo: Repository, success: bool = True) -> None:
        self.repositories[repo] = success


    @abstractmethod
    def render(self) -> str:
        pass


class ReportFormatRegister():


    _formats: dict[str, type[Report]] = {}
    
    
    @classmethod
    def register(cls, name: str, format: type[Report]) -> None:
        if name in cls._formats:
            raise ValueError(f"Format '{name}' is already registered")

        if format in cls._formats.values():
            raise ValueError(
                f"Format '{format.__name__}' is already registered"
            )

        cls._formats[name] = format


    @classmethod
    def register_formats(cls, formats: dict[str, type[Report]]):
        for key in formats.keys():
            cls.register(key, formats[key])


    @classmethod
    def get(cls, name: str) -> type[Report]:
        try:
            return cls._formats[name]
        except KeyError:
            raise KeyError(f"Format '{name}' is not registered")


    @classmethod
    def get_name(cls, format: type[Report]) -> str:
        for name, registered_target in cls._formats.items():
            if registered_target is format:
                return name

        raise KeyError(
            f"Format '{format.__name__}' is not registered"
        )


    @classmethod
    def names(cls) -> list[str]:
        return list(cls._formats)


    @classmethod
    def has(cls, name: str) -> bool:
        return name in cls._formats