import os
from typing import Optional

import github

from chromium_osx_tools import constants

RELEASE_NAME = "macOS SDKs Release"


class GitHubFactory:
    __instance: Optional[github.Github] = None
    __repos: dict[str, github.Repository.Repository] = {}

    @classmethod
    def get_instance(cls) -> github.Github:
        if cls.__instance:
            return cls.__instance

        auth = github.Auth.Token(constants.Constants.github_token())
        gh = github.Github(auth=auth)
        cls.__instance = gh
        return gh

    @classmethod
    def get_repo(cls, repo_name: Optional[str] = None) -> github.Repository.Repository:
        if repo_name in cls.__repos:
            return cls.__repos[repo_name]

        if not repo_name:
            repo_name = constants.Constants.github_repo()

        username = constants.Constants.github_username()
        repo = cls.get_instance().get_repo(f"{username}/{repo_name}")
        cls.__repos[repo_name] = repo

        return repo


def get_release(
    repo: github.Repository.Repository, release_tag: str = "macOS_SDKs_tag"
) -> github.GitRelease.GitRelease:
    try:
        release = repo.get_release(release_tag)
        return release
    except github.UnknownObjectException:
        release = repo.create_git_release(
            tag=release_tag,
            name=RELEASE_NAME,
            message="Automated toolchain upload.",
            draft=False,
            prerelease=False,
        )
        return release


def find_sdk_in_release(
    release: github.GitRelease.GitRelease, sdk_name: str
) -> Optional[github.GitReleaseAsset]:
    for asset in release.get_assets():
        if sdk_name in asset.name:
            return asset

    return None


def __delete_file_from_release_if_exists(
    release: github.GitRelease.GitRelease, file_name: str
):
    for existing_asset in release.get_assets():
        if existing_asset.name == file_name:
            existing_asset.delete_asset()
            return


def upload_sdk_to_repo(
    repo: github.Repository.Repository,
    sdk_name: str,
    sdk_path: str,
    release_tag: str = "macOS_SDKs_tag",
) -> None:
    if not os.path.exists(sdk_path):
        raise FileNotFoundError(f"{sdk_path} does not exists")

    release = get_release(repo=repo, release_tag=release_tag)
    __delete_file_from_release_if_exists(release=release, file_name=sdk_name)
    asset = release.upload_asset(
        path=sdk_path, content_type="application/gzip", name=sdk_name
    )

    print(
        f"Success! The new file is uploaded and available at: {asset.browser_download_url}"
    )


def download_sdk_from_repo(
    repo: github.Repository.Repository,
    sdk_name: str,
    release_tag: str = "macOS_SDKs_tag",
) -> None:
    sdks_path = constants.Constants().linux_macos_sdks_path()
    if not os.exists(sdks_path):
        os.makedirs(sdks_path, exist_ok=True)
