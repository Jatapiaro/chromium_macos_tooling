import os
import shutil
import tarfile


def remove_path(path: str) -> None:
    if not os.path.exists(path):
        return

    if os.path.isdir(path):
        shutil.rmtree(path)

    os.remove(path)


def compress_macos_sdk(sdk_path: str) -> str:
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

        tar.add(sdk_path, arcname=sdk_name, filter=verbose_filter)

    if not os.path.exists(output_path):
        raise FileNotFoundError(f"Tar file {output_path} does not exist.")

    return output_path
