import os
import pathlib
import uuid
from typing import Optional

import constants


def find_macos_sdks(sdk_path: Optional[str] = None) -> list[str]:
    if not sdk_path:
        sdk_path = constants.Constants.sdk_path()

    if not os.path.exists(sdk_path):
        raise FileNotFoundError(f"{sdk_path} does not exists.")

    result = set()
    for sdk in os.listdir(sdk_path):
        result.add(str(pathlib.Path(os.path.join(sdk_path, sdk)).resolve()))

    return sorted(list(result))


def split_file_in_chunks(
    file_path: str, mb_chunk_size: int = 32, output_path: Optional[str] = None
) -> str:
    if not output_path:
        dir_name = str(uuid.uuid4())
        output_path = os.path.join("/tmp", dir_name)
    os.makedirs(output_path, exist_ok=True)

    file_name = os.path.basename(file_path)
    chunk_size = mb_chunk_size * 1024 * 1024

    with open(file_path, "rb") as file_in:
        idx = 1
        while True:
            data = file_in.read(chunk_size)
            if not data:
                break

            chunk_filename = os.path.join(output_path, f"{file_name}.part{idx:03d}")
            with open(chunk_filename, "wb") as f_out:
                f_out.write(data)
            idx += 1

    return output_path