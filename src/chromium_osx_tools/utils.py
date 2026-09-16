import os
import pathlib
from typing import Optional

from chromium_osx_tools import constants


def find_macos_sdks(sdk_path: Optional[str] = None) -> list[str]:
    if not sdk_path:
        sdk_path = constants.Constants.sdk_path()

    if not os.path.exists(sdk_path):
        raise FileNotFoundError(f"{sdk_path} does not exists.")

    result = set()
    for sdk in os.listdir(sdk_path):
        result.add(str(pathlib.Path(os.path.join(sdk_path, sdk)).resolve()))

    return sorted(list(result))
