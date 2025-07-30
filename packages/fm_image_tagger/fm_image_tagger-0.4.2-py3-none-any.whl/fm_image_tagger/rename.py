import os


def rename_files(directory, suffix):
    try:
        # Ensure the provided directory exists
        if not os.path.isdir(directory):
            print(f"The directory {directory} does not exist.")
            return

        files = os.listdir(directory)
        files.sort()  # Ensure a consistent ordering

        for index, filename in enumerate(files):
            old_path = os.path.join(directory, filename)
            if os.path.isfile(old_path):
                name, ext = os.path.splitext(filename)
                new_filename = f"{suffix}_{index + 1:04}{ext}"
                new_path = os.path.join(directory, new_filename)
                os.rename(old_path, new_path)
                print(f"Renamed {old_path} to {new_path}")

    except Exception as e:
        print(f"An error occurred: {e}")
