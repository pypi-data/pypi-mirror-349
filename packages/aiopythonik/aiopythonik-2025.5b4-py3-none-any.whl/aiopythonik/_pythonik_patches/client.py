from pythonik.client import PythonikClient as _PythonikClient


__all__ = ["PythonikClient"]

from .specs import (
    AssetSpec,
    CollectionSpec,
    FilesSpec,
    JobSpec,
    MetadataSpec,
    SearchSpec,
)


class PythonikClient(_PythonikClient):

    def assets(self) -> AssetSpec:
        return AssetSpec(self.session, self.timeout, self.base_url)

    def collections(self) -> CollectionSpec:
        return CollectionSpec(self.session, self.timeout, self.base_url)

    def files(self) -> FilesSpec:
        return FilesSpec(self.session, self.timeout, self.base_url)

    def jobs(self) -> JobSpec:
        return JobSpec(self.session, self.timeout, self.base_url)

    def metadata(self) -> MetadataSpec:
        return MetadataSpec(self.session, self.timeout, self.base_url)

    def search(self) -> SearchSpec:
        return SearchSpec(self.session, self.timeout, self.base_url)
