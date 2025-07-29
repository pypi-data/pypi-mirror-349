import os
import tempfile
from io import BytesIO
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
import yaml
from pandas import DataFrame

from .gen2 import BlobClient


def load_yaml(blob: BlobClient) -> dict:
    """YAML 파일을 불러옵니다.

    Args:
        blob (BlobClient): BlobClient.

    Returns:
        dict: YAML contents.
    """
    stream = blob.download()
    config = yaml.safe_load(stream)
    return config


def load_csv(blob: BlobClient, **kwargs) -> DataFrame:
    """CSV 파일을 읽어 DataFrame으로 반환합니다.

    Args:
        blob (BlobClient): BlobClient.

    Returns:
        DataFrame: Data.
    """
    stream = blob.download()
    return pd.read_csv(stream, low_memory=False, **kwargs)


def load_jobib(blob: BlobClient) -> Any:
    """joblib으로 저장된 객체를 불러옵니다.

    Args:
        blob (BlobClient): BlobClient.

    Returns:
        Any: Object.
    """
    stream = blob.download()

    with tempfile.NamedTemporaryFile("wb+", suffix=".pkl") as file:
        file.write(stream.read())
        file.seek(os.SEEK_SET)

        obj = joblib.load(file.name)

    return obj


def load_stream(blob: BlobClient, **kwargs) -> BytesIO:
    """파일을 읽어 스트림을 반환합니다.

    Args:
        blob (BlobClient): BlobClient.

    Returns:
        BytesIO: Stream.
    """
    stream = blob.download()
    return stream


def upload_to_csv(
    blob: BlobClient, data: DataFrame, encode: str = "utf-8", **kwargs
):
    """DataFrame을 CSV 파일로 저장합니다.

    Args:
        blob (BlobClient): BlobClient.
        data (DataFrame): Data.
        encode (str): Encoding option.
        **kwargs : pandas.DataFrame.to_csv(**kwargs) e.g. index, header, ...
    """
    blob.container.create(exist_ok=True)
    blob.create(exist_ok=True)

    stream = BytesIO(data.to_csv(**kwargs).encode(encode))
    blob.upload(stream)


def upload_to_parquet(blob: BlobClient, data: DataFrame, **kwargs):
    """DataFrame을 Parquet 파일로 저장합니다.

    Args:
        blob (BlobClient): BlobClient.
        data (DataFrame): Data.
        **kwargs : pandas.DataFrame.to_parquet(**kwargs) e.g. index, ..
    """
    blob.container.create(exist_ok=True)
    blob.create(exist_ok=True)

    stream = BytesIO(data.to_parquet(**kwargs))
    blob.upload(stream)


def upload_file(blob: BlobClient, local_path: str, overwrite: bool = True):
    """파일을 저장합니다.

    Args:
        blob (BlobClient): BlobClient.
        local_path (str): 로컬 파일 경로.
        overwrite (bool, optional): 덮어쓰기 옵션. Defaults to True.
    """
    blob.container.create(exist_ok=True)
    blob.create(exist_ok=True)

    with open(local_path, "rb") as file:
        stream = BytesIO(file.read())
        blob.upload(stream, overwrite=overwrite)


def download_file(
    blob: BlobClient, local_path: str, file_name: str = None
) -> str:
    """파일을 다운로드합니다.

    Args:
        blob (BlobClient): BlobClient.
        local_path (str): 파일이 저장될 로컬 위치(디렉토리 경로).
        file_name (str, optional): 파일명. 없으면 blob명으로 저장함. Defaults to None.

    Returns:
        str: 로컬 파일 경로.
    """
    if not file_name:
        file_name = blob.name

    stream = blob.download()

    file_path = Path(local_path)
    file_path.mkdir(exist_ok=True, parents=True)

    file_path = file_path / file_name

    with open(file_path, "wb+") as file:
        file.write(stream.read())
        file.seek(os.SEEK_SET)

    return str(file_path)
