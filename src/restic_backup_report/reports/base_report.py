from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from restic_backup_report.models.repository import Repository
from restic_backup_report.models.repository_report import RepositoryReport
from restic_backup_report.models.snapshot_report import SnapshotReport
from restic_backup_report.models.storage import Storage
from restic_backup_report.models.storage_report import StorageReport, UsageState


class Report(ABC):


    def __init__(self) -> None:
        super().__init__()

        self.repositories: dict[Repository, RepositoryReport] = {}
        self.storages: dict[Storage, StorageReport] = {}

    # Repository

    def append_repository(self, repo: Repository) -> None:
        self.repositories[repo] = RepositoryReport()


    def set_repository_incompatible(self, repo: Repository) -> None:
        self.repositories[repo].incompatible = True
    

    def set_repository_integrity(self, repo: Repository, status: bool) -> None:
        self.repositories[repo].integrity = status


    def set_repository_snapshot_reports(self, repo: Repository, snapshot_reports: dict[datetime, list[SnapshotReport]]) -> None:
        self.repositories[repo].snapshots = snapshot_reports


    def finish_repository(self, repo: Repository, success: bool = True) -> None:
        self.repositories[repo].success = success

    # Storage

    def append_storage(self, storage: Storage) -> None:
        self.storages[storage] = StorageReport()


    def set_storage_folder(self, storage: Storage, folder: str) -> None:
        self.storages[storage].path = folder


    def set_storage_folder_size(self, storage: Storage, size: str) -> None:
        self.storages[storage].folder_size = size


    def set_storage_partition(self, storage: Storage, partition: str) -> None:
        self.storages[storage].partition = partition


    def set_storage_mountpoint(self, storage: Storage, mountpoint: str) -> None:
        self.storages[storage].mountpoint = mountpoint


    def set_storage_partition_size(self, storage: Storage, partitionSize: str) -> None:
        self.storages[storage].partition_size = partitionSize


    def set_storage_usage(self, storage: Storage, usage: float) -> None:
        self.storages[storage].usage = usage


    def set_storage_usage_state(self, storage: Storage, usageState: UsageState) -> None:
        self.storages[storage].usageState = usageState


    def finish_storage(self, storage: Storage, success: bool = True) -> None:
        self.storages[storage].success = success


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