import os
import sys


def process_add(file_path, keyword):
    try:
        new_tags = []
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            tags = content.split(",")
            for tag in tags:
                check_tag = tag.strip()
                new_tags.append(check_tag)
            new_tags.append(keyword)
        output_tags = ", ".join(new_tags).replace("\n", " ") + "\n"
        with open(file_path, "w+", encoding="utf-8") as file:
            file.write(output_tags)
    except Exception as e:
        print(f"Failed to process {file_path}: {e}")


def process_remove(file_path, keywords):
    try:
        new_tags = []
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            tags = content.split(",")
            for tag in tags:
                check_tag = tag.strip()
                if check_tag not in keywords:
                    new_tags.append(check_tag)
        output_tags = ", ".join(new_tags).replace("\n", " ") + "\n"
        with open(file_path, "w+", encoding="utf-8") as file:
            file.write(output_tags)
    except Exception as e:
        print(f"Failed to process {file_path}: {e}")


def process_trigger(file_path, keyword):
    try:
        new_tags = [keyword]
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            tags = content.split(",")
            for tag in tags:
                check_tag = tag.strip()
                if not check_tag == keyword:
                    new_tags.append(check_tag)
        output_tags = ", ".join(new_tags).replace("\n", " ") + "\n"
        with open(file_path, "w+", encoding="utf-8") as file:
            file.write(output_tags)
    except Exception as e:
        print(f"Failed to process {file_path}: {e}")


def add(dir, word, trigger=False):
    if not os.path.isdir(dir):
        print(f"The specified path is not a directory: {dir}")
        sys.exit(1)

    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                if trigger:
                    process_trigger(file_path, word)
                else:
                    process_add(file_path, word)


def remove(dir, words):
    if not os.path.isdir(dir):
        print(f"The specified path is not a directory: {dir}")
        sys.exit(1)

    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                process_remove(file_path, words)
