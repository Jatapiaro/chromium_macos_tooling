import pick
from chromium_osx_tools import utils, github_utils


def __select_supported_macos_sdk(options: list[utils.SupportedSDK]) -> int:
    picker = pick.Picker(
        options=[str(op) for op in options],
        title="Select an SDK (Enter to confirm):",
        multiselect=False,
        min_selection_count=1,
    )

    result = picker.start()
    return result[1]


def main():
    supported_sdks = utils.find_chromium_supported_sdks()
    selected_index = __select_supported_macos_sdk(supported_sdks)
    selected_sdk = supported_sdks[selected_index]

    repo = github_utils.GitHubFactory.get_repo()
    release = github_utils.get_release(repo=repo)
    sdk_name = f"MacOSX{selected_sdk.sdk_version}.sdk"
    gh_sdk_asset = github_utils.find_sdk_in_release(
        release=release,
        sdk_name=sdk_name,
    )


if __name__ == "__main__":
    main()
