# src/aiopythonik/_pythonik_patches/client.pyi

from requests import Session

from .specs import (
    AssetSpec,
    CollectionSpec,
    FilesSpec,
    JobSpec,
    MetadataSpec,
    SearchSpec,
)


class PythonikClient:
    session: Session
    timeout: int
    base_url: str

    def __init__(
        self,
        app_id: str,
        auth_token: str,
        timeout: int = 3,
        base_url: str = "https://app.iconik.io",
    ) -> None:
        ...

    def assets(self) -> AssetSpec:
        ...

    def collections(self) -> CollectionSpec:
        ...

    def files(self) -> FilesSpec:
        ...

    def jobs(self) -> JobSpec:
        ...

    def metadata(self) -> MetadataSpec:
        ...

    def search(self) -> SearchSpec:
        ...
