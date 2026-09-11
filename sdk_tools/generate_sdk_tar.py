import os
import tarfile

import pick

import constants
import github_utils
import utils


def __select_macos_sdk(options: list[str]) -> int:
    picker = pick.Picker(
        options=[os.path.basename(op) for op in options],
        title="Select an SDK (Enter to confirm):",
        multiselect=False,
        min_selection_count=1,
    )

    result = picker.start()
    return result[1]


def __compress_macos_sdk(sdk_path: str) -> str:
    if not os.path.exists(sdk_path):
        raise FileNotFoundError(f"{sdk_path} does not exists")

    sdk_name = os.path.basename(sdk_path)
    output_path = os.path.join("/tmp", f"{sdk_name}.tar.gz")

    with tarfile.open(output_path, "w:gz", dereference=True) as tar:

        def verbose_filter(tarinfo):
            # Skip the circular symlink loop in Ruby.framework
            if "Ruby.framework" in tarinfo.name:
                return None

            print(f"a {tarinfo.name}")
            return tarinfo

        tar.add(sdk_path, filter=verbose_filter)

    if not os.path.exists(output_path):
        raise FileNotFoundError(f"Tar file {output_path} does not exist.")

    return output_path


def main():
    sdks = utils.find_macos_sdks()
    if not sdks:
        raise ValueError("No SDKs available")

    selected_index = __select_macos_sdk(options=sdks)
    sdk_to_prepare = sdks[selected_index]
    compressed_sdk_path = __compress_macos_sdk(sdk_path=sdk_to_prepare)
    utils.split_file_in_chunks(file_path=compressed_sdk_path)

    # gh_repo = github_utils.GitHubFactory.get_repo()
    # github_utils.upload_sdk_to_repo(repo=gh_repo, file_path=output_path)

    # os.remove(output_path)


if __name__ == "__main__":
    main()
