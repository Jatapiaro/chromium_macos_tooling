import os

import github
import pick

from chromium_osx_tools import files, github_utils, utils


def __select_macos_sdk(options: list[str]) -> int:
    picker = pick.Picker(
        options=[os.path.basename(op) for op in options],
        title="Select an SDK (Enter to confirm):",
        multiselect=False,
        min_selection_count=1,
    )

    result = picker.start()
    return result[1]


def main():
    sdks = utils.find_macos_sdks()
    if not sdks:
        raise ValueError("No SDKs available")

    selected_index = __select_macos_sdk(options=sdks)
    sdk_to_prepare = sdks[selected_index]
    compressed_sdk_path = files.compress_macos_sdk(sdk_path=sdk_to_prepare)

    sdk_name = os.path.basename(compressed_sdk_path)
    gh_repo = github_utils.GitHubFactory.get_repo()
    try:
        github_utils.upload_sdk_to_repo(
            repo=gh_repo, sdk_name=sdk_name, sdk_path=compressed_sdk_path
        )
    except github.GithubException as e:
        raise e
    except FileNotFoundError as e:
        raise e
    finally:
        os.remove(compressed_sdk_path)


if __name__ == "__main__":
    main()
