import os
import pathlib

CHROMIUM_SRC_PATH = "CHROMIUM_SRC_PATH"
GITHUB_REPO = "GITHUB_REPO"
GITHUB_TOKEN = "GITHUB_TOKEN"
GITHUB_USERNAME = "GITHUB_USERNAME"
LINUX_MACOS_SDKS_PATH = "LINUX_MACOS_SDKS_PATH"
SDK_PATH = "SDK_PATH"


def _load_env(filepath=".env", valid_keys: set[str] = None):
    try:
        with open(filepath, "r") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                if "=" not in line:
                    continue

                key, value = line.split("=", 1)
                key = key.strip()
                if valid_keys and key not in valid_keys:
                    continue

                value = value.strip().strip("'\"")
                if value:
                    os.environ[key] = value
    except FileNotFoundError:
        print(f"Warning: {filepath} file not found.")


class Constants:
    _load_env(
        valid_keys={
            CHROMIUM_SRC_PATH,
            GITHUB_REPO,
            GITHUB_TOKEN,
            GITHUB_USERNAME,
            LINUX_MACOS_SDKS_PATH,
            SDK_PATH,
        }
    )

    @classmethod
    def github_username(cls) -> str:
        username = os.environ.get(GITHUB_USERNAME)
        if not username:
            raise ValueError(f"{GITHUB_USERNAME} is not set in .env file")

        return username

    @classmethod
    def github_token(cls) -> str:
        token = os.environ.get(GITHUB_TOKEN)
        if not token:
            raise ValueError(f"{GITHUB_TOKEN} is not set in .env file")

        return token

    @classmethod
    def github_repo(cls) -> str:
        repo = os.environ.get(GITHUB_REPO)
        if not repo:
            raise ValueError(f"{GITHUB_REPO} is not set in .env file")

        return repo

    @classmethod
    def sdk_path(cls) -> str:
        default_path = os.path.join("/Library", "Developer", "CommandLineTools", "SDKs")
        return os.environ.get(SDK_PATH, default_path)

    @classmethod
    def linux_macos_sdks_path(cls) -> str:
        home = str(pathlib.Path.home())
        default_path = os.path.join(home, "MacOS_SDKs")

        return os.environ.get(LINUX_MACOS_SDKS_PATH, default_path)

    @classmethod
    def chromium_src_path(cls) -> str:
        return os.environ.get(CHROMIUM_SRC_PATH)
