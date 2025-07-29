# azure-storage-helper

Azure의 storage 서비스를 사용하기 위한 Python SDK를 좀 더 쉽게 사용할 수 있도록 도와줍니다.  
현재 지원하고 있는 SDK는 다음 2개 라이브러리이며, Blob container만 지원하고 있습니다.

- Blob Storage (azure-storage-blob)
- Datalake Storage Gen2 (azure-storage-file-datalake)

## 목차

- [azure-storage-helper](#azure-storage-helper)
  - [목차](#목차)
  - [Getting started](#getting-started)
    - [Installation](#installation)
    - [Package overview](#package-overview)
  - [User Guide](#user-guide)
    - [StorageClient](#storageclient)
      - [Example](#example)
      - [Property](#property)
      - [Method](#method)
    - [ContainerClient](#containerclient)
      - [Example](#example-1)
      - [Property](#property-1)
      - [Method](#method-1)
    - [DirectoryClient](#directoryclient)
      - [Example](#example-2)
      - [Property](#property-2)
      - [Method](#method-2)
    - [BlobClient](#blobclient)
      - [Example](#example-3)
      - [Property](#property-3)
      - [Method](#method-3)
    - [helper](#helper)

## Getting started

### Installation

azure-storage-helper는 pip 명령어를 통해 PyPI으로부터 설치할 수 있습니다.

```cmd
pip install azure-storage-helper
```

### Package overview

본 패키지에서는 4개의 Client를 제공합니다.

> StorageClient > ContainerClient > DirectoryClient(gen2만 해당) > BlobClient

`helper`에서는 BlobClient를 이용하여 파일 업로드/다운로드 등 자주 수행하는 작업을 함수로 제공합니다.

## User Guide

본 가이드는 `gen2`를 기준으로 작성되었습니다.  
`gen1`은 `DirectoryClient`가 없으며, 일부 기능에 제한이 있을 수 있습니다.

### StorageClient

Azure Storage Account에 대한 클라이언트입니다.  
다음 두 개의 인자를 이용해 생성할 수 있습니다.

- `account_name` : Storage Account의 이름
- `account_key` : Storage Account에 접근하기 위한 key

#### Example

```python
from azure.gen2 import StorageClient

account_name = "account_name"
account_key = "account_key"

storage = StorageClient(account_name=account_name, account_key=account_key)
```

#### Property

- `client`
  - Original SDK의 client(azure.storage.filedatalake.DataLakeServiceClient)를 반환합니다. 본 패키지에서 제공하지 않는 기능이 필요한 경우 사용할 수 있습니다.
  - *gen1에서는 azure.storage.blob.BlobServiceClient*

#### Method

- `containers(name_starts_with: str = None) -> list[ContainerClient]`
  - 현재 스토리지 계정에 존재하는 컨테이너 리스트를 반환합니다.
- `get_container(name: str) -> ContainerClient`
  - 특정 이름의 컨테이너를 반환합니다.
- `get_directory(path: str) -> DirectoryClient`
  - 특정 경로의 디렉토리를 반환합니다.
  - 경로는 `<container>/<directory-path>`로 나타냅니다.
  - *gen1에서는 제공하지 않습니다.*
- `get_blob(path: str) -> BlobClient`
  - 특정 경로의 블랍을 반환합니다.
  - 경로는 `<container>/<directory-path>/<blob-name>`으로 나타냅니다.

### ContainerClient

Container에 대한 클라이언트입니다.  
다음 두 개의 인자를 이용해 생성할 수 있습니다.

- `name` : 컨테이너 이름
- `storage` : StorageClient

#### Example

```python
from azure.gen2 import ContainerClient

container = ContainerClient("raw", storage)

if not container.exists():
    container.create()
```

#### Property

- `name`
  - 컨테이너 이름
- `client`
  - Original SDK의 client(azure.storage.filedatalake.FileSystemClient)를 반환합니다. 본 패키지에서 제공하지 않는 기능이 필요한 경우 사용할 수 있습니다.
  - *gen1에서는 azure.storage.blob.ContainerClient*

#### Method

- `exists() -> bool`
  - 컨테이너의 존재 유무를 반환합니다.
- `create(exist_ok=False, **kwargs) -> None`
  - 컨테이너를 생성합니다.
  - `exist_ok`가 `True`이면 컨테이너가 이미 존재할 시 에러가 발생하지 않습니다.
- `delete(**kwargs) -> None`
  - 컨테이너를 삭제합니다.
- `glob(path: str = None, name_starts_with: str = None, recursive: bool = True) -> list[BlobClient]`
  - 현재 컨테이너에 존재하는 조건에 부합하는 모든 blob을 반환합니다.
  - `path`는 현재 컨테이너로부터 검색하려는 디렉토리의 상대 경로입니다.
  - `name_starts_with`는 blob 이름의 접두사입니다.
  - `recursive`는 재귀적으로 하위 디렉토리에 대한 검색 여부를 나타냅니다.
  - *gen1에서는 `recursive` 옵션 기능을 제공하지 않습니다.*
- `get_directory(path: str) -> DirectoryClient`
  - 현재 컨테이너로부터 특정 경로에 있는 DirectoryClient를 반환합니다.
  - 경로는 컨테이너 이름을 제외한 현재 컨테이너로부터 디렉토리의 상대 경로입니다.
  - *gen1에서는 제공하지 않습니다.*
- `get_blob(path: str) -> BlobClient`
  - 현재 컨테이너로부터 특정 경로의 BlobClient를 반환합니다.
  - 경로는 컨테이너 이름을 제외한 현재 컨테이너로부터 blob의 상대 경로입니다.

### DirectoryClient

Directory에 대한 클라이언트입니다.  
다음 두 개의 인자를 이용해 생성할 수 있습니다.  
*※ gen1에서는 제공하지 않습니다.*

- `path` : 컨테이너를 포함하는 디렉토리의 절대 경로
- `storage` : StorageClient

#### Example

```python
from azure.gen2 import DirectoryClient

directory = DirectoryClient("raw/folder/subfolder", storage)

if not directory.exists():
    directory.create()
```

#### Property

- `name`
  - 디렉토리 이름
- `path`
  - 컨테이너를 포함하는 디렉토리의 절대 경로
- `client`
  - Original SDK의 client(azure.storage.filedatalake.DataLakeDirectoryClient)를 반환합니다. 본 패키지에서 제공하지 않는 기능이 필요한 경우 사용할 수 있습니다.
- `container`
  - 현재 디렉토리의 상위 컨테이너에 대한 ContainerClient
- `parent`
  - 현재 디렉토리의 상위 클라이언트
  - DirectoryClient 또는 ContainerClient

#### Method

- `exists() -> bool`
  - 디렉토리의 존재 유무를 반환합니다.
- `create(exist_ok=False, **kwargs) -> None`
  - 디렉토리를 생성합니다.
  - `exist_ok`가 `True`이면 디렉토리가 이미 존재할 시 에러가 발생하지 않습니다.
- `delete(**kwargs) -> None`
  - 디렉토리를 삭제합니다.
- `glob(name_starts_with: str = None, recursive: bool = True) -> list[BlobClient]`
  - 현재 디렉토리에 존재하는 조건에 부합하는 모든 blob을 반환합니다.
  - `name_starts_with`는 blob 이름의 접두사입니다.
  - `recursive`는 재귀적으로 하위 디렉토리에 대한 검색 여부를 나타냅니다.
- `get_directory(path: str) -> DirectoryClient`
  - 현재 디렉토리로부터 특정 경로에 있는 DirectoryClient를 반환합니다.
  - 경로는 현재 디렉토리로부터 해당 디렉토리의 상대 경로입니다.
- `get_blob(path: str) -> BlobClient`
  - 현재 디렉토리로부터 특정 경로의 BlobClient를 반환합니다.
  - 경로는 현재 디렉토리로부터 blob의 상대 경로입니다.

### BlobClient

Blob에 대한 클라이언트입니다.  
다음 두 개의 인자를 이용해 생성할 수 있습니다.

- `path` : 컨테이너를 포함하는 디렉토리의 절대 경로
- `storage` : StorageClient

#### Example

```python
from azure.gen2 import BlobClient

blob = BlobClient("raw/folder/blob.txt", storage)

if not blob.exists():
    blob.create()
```

#### Property

- `name`
  - Blob 이름
- `path`
  - 컨테이너를 포함하는 Blob의 절대 경로
- `client`
  - Original SDK의 client(azure.storage.filedatalake.DataLakeFileClient)를 반환합니다. 본 패키지에서 제공하지 않는 기능이 필요한 경우 사용할 수 있습니다.
  - *gen1에서는 azure.storage.blob.BLobClient*
- `container`
  - 현재 Blob의 상위 컨테이너에 대한 ContainerClient
- `parent`
  - 현재 Blob의 상위 클라이언트
  - DirectoryClient 또는 ContainerClient
  - *gen1에서는 제공하지 않습니다.*

#### Method

- `exists() -> bool`
  - Blob의 존재 유무를 반환합니다.
- `create(exist_ok=False, **kwargs) -> None`
  - Blob를 생성합니다.
  - `exist_ok`가 `True`이면 Blob이 이미 존재할 시 에러가 발생하지 않습니다.
  - *gen1에서는 제공하지 않습니다.*
- `delete(**kwargs) -> None`
  - Blob을 삭제합니다.
- `upload(bytes: BytesIO, overwrite: bool = True) -> None`
  - 현재 blob에 바이트 스트림의 내용을 작성합니다.
- `download() -> BytesIO`
  - 현재 blob의 내용을 바이트 스트림으로 받아옵니다.

### helper

- `load_yaml(blob: BlobClient) -> dict`
- `load_csv(blob: BlobClient, **kwargs) -> DataFrame`
- `load_jobib(blob: BlobClient) -> Any`
- `upload_to_csv(blob: BlobClient, data: DataFrame, encode: str = "utf-8", **kwargs)`
- `upload_to_parquet(blob: BlobClient, data: DataFrame, **kwargs)`
- `upload_file(blob: BlobClient, local_path: str, overwrite: bool = True)`
- `download_file(blob: BlobClient, local_path: str, file_name: str = None) -> str`
