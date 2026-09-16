import os

import pick

from chromium_osx_tools import files, utils


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
    files.split_file_in_chunks(file_path=compressed_sdk_path)

    # gh_repo = github_utils.GitHubFactory.get_repo()
    # github_utils.upload_sdk_to_repo(repo=gh_repo, file_path=output_path)

    # os.remove(output_path)


if __name__ == "__main__":
    main()
