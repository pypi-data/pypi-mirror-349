import os
import sys


def read_tag(file_path, totals):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            print(f"Processing {file_path}:")
            tags = content.split(",")
            for tag in tags:
                check_tag = tag.strip()
                if check_tag in totals:
                    totals[check_tag] += 1
                else:
                    totals[check_tag] = 1  # Initialize new tag with count as zero
    except Exception as e:
        print(f"Failed to process {file_path}: {e}")


def total(dir):
    if not os.path.isdir(dir):
        print(f"The specified path is not a directory: {dir}")
        sys.exit(1)

    tags = {}
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                read_tag(file_path, tags)
    sorted_tags = sorted(
        tags.items(), key=lambda x: -x[1]
    )  # Sorting by count in descending order (most common first).
    print(f"tags: {sorted_tags}")
