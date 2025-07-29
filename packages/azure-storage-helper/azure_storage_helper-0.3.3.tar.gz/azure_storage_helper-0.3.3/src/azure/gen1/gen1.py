from __future__ import annotations

from io import BytesIO
from pathlib import Path

from azure.core.exceptions import ResourceExistsError
from azure.storage.blob import BlobServiceClient
from azure.storage.blob import ContainerClient as OriginalContainerClient
from azure.storage.blob import BlobClient as OriginalBlobClient


class StorageClient:
    def __init__(self, account_name: str, account_key: str) -> None:
        """Storage 사용을 도와주는 BlobServiceClient wrapper class.

        Args:
            account_name (str): Name of StorageClient Account.
            account_key (str): Access key of StorageClient Account.
        """
        self.account_name = account_name
        self.account_key = account_key

        self._client: BlobServiceClient = None
        self.__init_storage_client(account_name, account_key)

    @property
    def client(self) -> BlobServiceClient:
        """azure.storage.blob.BlobServiceClient을 반환합니다.

        Returns:
            BlobServiceClient: A client to interact with the Storage Account,
            even if the directory may not yet exist.
        """
        return self._client

    def containers(self, name_starts_with: str = None) -> list:
        """현재 스토리지 계정에 존재하는 컨테이너 리스트를 반환합니다. 리스트의 아이템은
        azure.storage.blob.ContainerClient의 wrapper 클래스인 ContainerClient입니다.

        Args:
            name_starts_with (str, optional): 특정 접두사로 시작하는 컨테이너만 반환하기
            위한 필터. Defaults to None.

        Returns:
            list: 현재 스토리지 계정에 존재하는 컨테이너 리스트.
        """
        containers = self.client.list_containers(
            name_starts_with=name_starts_with
        )
        return list(
            map(
                lambda container: ContainerClient(container.name, self),
                containers,
            )
        )

    def get_container(self, name: str) -> ContainerClient:
        """`name` 이름의 컨테이너를 azure.storage.blob.ContainerClient의 wrapper 클래스인
        ContainerClient의 인스턴스로 반환합니다.

        Args:
            name (str): 컨테이너 이름.

        Returns:
            ContainerClient: ContainerClient.
        """
        return ContainerClient(name, self)

    def get_blob(self, path: str) -> BlobClient:
        """`path` 경로의 blob을 azure.storage.blob.BlobServiceClient의 wrapper 클래스인
        BlobClient의 인스턴스를 반환합니다.

        Args:
            path (str): 컨테이너를 포함하는 Blob의 절대 경로.

        Returns:
            BlobClient: BlobClient.
        """
        return BlobClient(path, self)

    def __init_storage_client(
        self, account_name: str, account_key: str
    ) -> BlobServiceClient:
        """StorageClient Account와 상호작용 가능한 client를 설정합니다.

        Args:
            account_name (str): Name of StorageClient Account.
            account_key (str): Access key of StorageClient Account.

        Returns:
            BlobServiceClient: Client to interact with Blob Storage Service at
            the account level.
        """
        connection_str = (
            f"DefaultEndpointsProtocol=https;AccountName={account_name};"
            f"AccountKey={account_key};EndpointSuffix=core.windows.net"
        )

        self.account_name = account_name
        self.account_key = account_key
        self._client = BlobServiceClient.from_connection_string(connection_str)


class ContainerClient:
    def __init__(self, name: str, storage: StorageClient) -> None:
        """Container 사용을 도와주는 azure.storage.blob.ContainerClient의 wrapper
        class.

        Args:
            name (str): 컨테이너 이름.
            storage (StorageClient): 스토리지 계정에 대한 Helper class.
        """
        self._storage: StorageClient = storage
        self._name: str = name

    @property
    def name(self) -> str:
        """컨테이너 이름을 반환합니다.

        Returns:
            str: 컨테이너 이름.
        """
        return self._name

    @property
    def client(self) -> OriginalContainerClient:
        """컨테이너에 대한 azure.storage.blob.ContainerClient 반환합니다.

        Returns:
            ContainerClient: A client to interact with a specific file system,
            even if that file system may not yet exist.
        """
        return self._storage.client.get_container_client(self._name)

    def exists(self) -> bool:
        """컨테이너의 존재 유무를 반환합니다.

        Returns:
            bool: 해당 컨테이너가 존재하면 `True`, 아니면 `False`를 반환.
        """
        return self.client.exists()

    def create(self, exist_ok=False, **kwargs) -> None:
        """컨테이너를 생성합니다.

        Args:
            exist_ok (bool, optional): 컨테이너가 이미 존재하는 경우 에러 발생 여부.
            `True`면 에러가 발생하지 않으나 `False`이면 `ResourceExistsError`가 발생함.
            Defaults to False.

        Raises:
            err: ResourceExistsError
        """
        try:
            self.client.create_container(**kwargs)
        except ResourceExistsError as err:
            if not exist_ok:
                raise err

    def delete(self, **kwargs) -> None:
        """현재 container를 삭제합니다.
        """
        self.client.delete_container(**kwargs)

    def glob(self, path: str = None, name_starts_with: str = None) -> list:
        """컨테이너에 존재하는 Blob을 검색합니다.

        Args:
            path (str, optional): 현재 컨테이너로부터 검색하려는 디렉토리의 상대 경로.
            Defaults to None.
            name_starts_with (str, optional): Blob 이름의 접두사. Defaults to None.
            Defaults to True.

        Returns:
            list: Blob 검색 결과.
        """
        if name_starts_with is None:
            name_starts_with = ""

        paths = self.client.list_blobs(name_starts_with=path)

        results = []
        for path in paths:
            if not path.size:
                continue

            file_path = path.name
            file_name = Path(file_path).name
            if file_name.startswith(name_starts_with):
                full_path = f"{self.name}/{file_path}"
                results.append(full_path)

        return list(map(lambda path: BlobClient(path, self._storage), results))

    def get_blob(self, path: str) -> BlobClient:
        """`path` 경로의 blob을 azure.storage.blob.BlobClient의 wrapper 클래스인
        BlobClient의 인스턴스로 반환합니다.

        Args:
            path (str): 현재 컨테이너로부터 Blob 경로.

        Returns:
            BlobClient: BlobClient.
        """
        full_path = f"{self.name}/{path}"
        return BlobClient(full_path, self._storage)

    def __str__(self) -> str:
        return self.name


class BlobClient:
    def __init__(self, path: str, storage: StorageClient) -> None:
        """Blob 사용을 도와주는 azure.storage.blob.BlobClient의 wrapper class.

        Args:
            path (Union[str, Path]): 컨테이너를 포함하는 Blob 절대 경로.
            storage (StorageClient): 스토리지 계정에 대한 Helper class.
        """
        self._storage: StorageClient = storage
        self._sub_path: Path = Path(path)
        self._container: ContainerClient
        self.__init()

    @property
    def name(self) -> str:
        """Blob 이름을 반환합니다.

        Returns:
            str: Blob name
        """
        return self._sub_path.name

    @property
    def path(self) -> str:
        """컨테이너를 포함하는 Blob의 절대 경로를 반환합니다.

        Returns:
            str: Blob의 절대 경로
        """
        return str(self)

    @property
    def client(self) -> OriginalBlobClient:
        """azure.storage.blob.BlobServiceClient를 반환합니다.

        Returns:
            BlobServiceClient: A client to interact with the DataLake file,
            even if the file may not yet exist.
        """
        return self._storage.client.get_blob_client(
            self.container.name, str(self._sub_path)
        )

    @property
    def container(self) -> ContainerClient:
        """컨테이너에 대한 helper 클래스인 ContainerClient를 반환합니다.

        Returns:
            ContainerClient: 컨테이너에 대한 helper class.
        """
        return self._container

    def upload(self, bytes: BytesIO, overwrite: bool = True) -> None:
        """현재 blob에 바이트 스트림의 내용을 작성합니다.

        Args:
            bytes (BytesIO): 바이트 스트림.
            overwrite (bool, optional): 덮어쓰기 옵션. Defaults to True.
        """
        self.client.upload_blob(bytes, overwrite=overwrite)

    def download(self) -> BytesIO:
        """현재 blob의 내용을 바이트 스트림으로 받아옵니다.

        Returns:
            BytesIO: 바이트 스트림.
        """
        download = self.client.download_blob()
        downloaded_bytes = download.readall()

        return BytesIO(downloaded_bytes)

    def exists(self) -> bool:
        """Blob의 존재 유무를 반환합니다.

        Returns:
            bool: 해당 blob이 존재하면 `True`, 아니면 `False`를 반환.
        """
        return self.client.exists()

    def delete(self, delete_snapshots: str = "include") -> None:
        """현재 blob을 삭제합니다.

        Args:
            delete_snapshots (str, optional): 스냅샷 삭제 여부.\n
            스냅샷만 삭제하고 blob은 남기고 싶다면 `delete_snapshots="only"`\n
            Defaults to "include".\n
        """
        self.client.delete_blob(delete_snapshots=delete_snapshots)

    def __init(self) -> None:
        """인스턴스 초기화"""
        container_name, *others = self._sub_path.parts
        self._container = ContainerClient(container_name, self._storage)
        self._sub_path = Path("/".join(others))

    def __str__(self) -> str:
        return f"{self._container}/{self._sub_path}"
