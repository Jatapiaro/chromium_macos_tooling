import os
import pathlib
import dataclasses
import subprocess
from typing import Optional

from chromium_osx_tools import constants

MAC_SDK_GNI_PATH = "build/config/mac/mac_sdk.gni"
MAC_SDK_OFFICIAL_BUILD_VERSION_STRING = "mac_sdk_official_build_version"
MAC_SDK_OFFICIAL_UNIVERSAL_BUILD_VERSION_STRING = (
    "mac_sdk_official_universal_build_version"
)
MAC_SDK_OFFICIAL_UNIVERSAL_STRING = "mac_sdk_official_universal_version"
MAC_SDK_OFFICIAL_VERSION_STRING = "mac_sdk_official_version"
MAC_SDK_STRING = "mac_sdk_official"


@dataclasses.dataclass(frozen=True)
class CommandOutput:
    return_code: int
    std_out: list[str]
    std_err: str
    command: str


@dataclasses.dataclass(frozen=True)
class SupportedSDK:
    sdk_version: str
    build_version: str
    is_universal: bool

    def __str__(self):
        prefix = "Universal " if self.is_universal else ""
        return (
            f"{prefix}SDK Version: {self.sdk_version} => "
            f"{prefix}Build Version: {self.build_version}"
        )


def run_command(command: list[str]) -> CommandOutput:
    command_str = " ".join(command)
    result = subprocess.run(command, capture_output=True, text=True)
    return CommandOutput(
        return_code=result.returncode,
        std_out=[s.strip() for s in result.stdout.splitlines()],
        std_err=result.stderr,
        command=command_str,
    )


def find_macos_sdks(sdk_path: Optional[str] = None) -> list[str]:
    if not sdk_path:
        sdk_path = constants.Constants.sdk_path()

    if not os.path.exists(sdk_path):
        raise FileNotFoundError(f"{sdk_path} does not exists.")

    result = set()
    for sdk in os.listdir(sdk_path):
        result.add(str(pathlib.Path(os.path.join(sdk_path, sdk)).resolve()))

    return sorted(list(result))


def find_chromium_supported_sdks(
    chromium_src_path: Optional[str] = None,
) -> list[SupportedSDK]:
    if not chromium_src_path:
        chromium_src_path = constants.Constants.chromium_src_path()

    if not os.path.exists(chromium_src_path):
        error = f"Chromium source path {chromium_src_path} doesn't exists"
        raise FileNotFoundError(error)

    result = run_command(
        command=[
            "grep",
            MAC_SDK_STRING,
            os.path.join(chromium_src_path, MAC_SDK_GNI_PATH),
        ]
    )
    if result.return_code != 0:
        raise Exception(f"Something went wrong while running {result.command}")

    parsed_vars = {}
    for line in result.std_out:
        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"')

        if any(char.isdigit() for char in value):
            parsed_vars[key] = value

    supported_sdks = []
    for key, value in parsed_vars.items():
        if not key.endswith("_version") or key.endswith("_build_version"):
            continue

        base_name = key[:-8]
        build_key = f"{base_name}_build_version"
        if build_key in parsed_vars:
            supported_sdks.append(
                SupportedSDK(
                    sdk_version=value,
                    build_version=parsed_vars[build_key],
                    is_universal="universal" in key,
                )
            )

    return supported_sdks
