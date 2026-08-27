import os
import shutil


def copy_directory(src: str, dest: str):
    try:
        if not os.path.exists(dest):
            os.mkdir(dest)

        for item in os.listdir(src):
            src_path = os.path.join(src, item)
            dest_path = os.path.join(dest, item)

            if os.path.isfile(src_path):
                shutil.copy(src_path, dest_path)
                print(f"Copied: {src_path} -> {dest_path}")

            elif os.path.isdir(src_path):
                if not os.path.exists(dest_path):
                    os.mkdir(dest_path)

                copy_directory(src_path, dest_path)

    except OSError as e:
        print(f"Error copying {src} to {dest}: {e}")


def copy_files(src: str, dest: str):
    try:
        if os.path.exists(dest):
            shutil.rmtree(dest)
            print(f"Deleted: {dest}")

        os.mkdir(dest)
        print(f"Created: {dest}")

        copy_directory(src, dest)

    except OSError as e:
        print(f"Error preparing destination: {e}")
