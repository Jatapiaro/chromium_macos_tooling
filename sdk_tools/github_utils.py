import os
from typing import Optional

import github

import constants


class GitHubFactory:
    __instance: Optional[github.Github] = None
    __repos: dict[str, github.Repository.Repository] = {}

    @classmethod
    def get_instance(cls) -> github.Github:
        if cls.__instance:
            return cls.__instance

        gh = github.Github(constants.Constants.github_token())
        cls.__instance = gh
        return gh

    @classmethod
    def get_repo(cls, repo_name: Optional[str] = None) -> github.Repository.Repository:
        if repo_name in cls.__repos:
            return cls.__repos[repo_name]

        if not repo_name:
            repo_name = constants.Constants.github_repo()

        username = constants.Constants.github_username()
        return cls.get_instance().get_repo(f"{username}/{repo_name}")


def upload_sdk_to_repo(repo: github.Repository.Repository, file_path: str) -> bool:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} does not exists")

    with open(file_path, "rb") as f:
        content = f.read()

    path_in_repo = os.path.basename(file_path)
    try:
        file = repo.get_contents(path_in_repo)
        print("Overwriting file in repo")
        repo.update_file(
            path=file.path,
            message="Automatic SDK Update",
            content=content,
            sha=file.sha,
        )
    except Exception:
        print("Initial SDK Upload")
        repo.create_file(
            path=path_in_repo, message="Initial SDK Upload", content=content
        )
