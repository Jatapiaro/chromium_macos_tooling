import os
import tarfile

import constants
import github_utils


def main():
    sdk_path = constants.Constants.sdk_path()
    if not os.path.exists(sdk_path):
        raise FileNotFoundError(f"{sdk_path} does not exists.")

    sdk_name = os.path.basename(sdk_path)
    output_path = os.path.join("/tmp", sdk_name)
    with tarfile.open(output_path, "w:xz") as tar:
        tar.add(sdk_path, arcname=sdk_name)

    if not os.path.exists(output_path):
        raise FileNotFoundError(f"Tar file {output_path} does not exists.")

    gh_repo = github_utils.GitHubFactory.get_repo()
    github_utils.upload_sdk_to_repo(repo=gh_repo, file_path=output_path)

    os.remove(output_path)


if __name__ == "__main__":
    main()
