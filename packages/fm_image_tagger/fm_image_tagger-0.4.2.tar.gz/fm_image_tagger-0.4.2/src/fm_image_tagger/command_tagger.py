import os
import sys

import fm_image_tagger.ollama_caption as Caption
import fm_image_tagger.tagger as Tagger


def createTagFiles(path, threshold=0.35):
    if not os.path.isdir(path):
        print(f"The specified path is not a directory: {path}")
        sys.exit(1)

    tagger = Tagger.WD14Tagger(Tagger.SWINV2_MODEL_DSV3_REPO)
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg"):
                file_path = os.path.join(root, file)
                tags = tagger.image_tag(file_path, threshold=threshold)
                # create tag file
                base = os.path.splitext(file_path)[0]
                with open(f"{base}.txt", "w", encoding="utf-8") as f:
                    f.write(tags)
    print("Done.")


def createCaptionFiles(path, model, for_lora):
    if not os.path.isdir(path):
        print(f"The specified path is not a directory: {path}")
        sys.exit(1)

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg"):
                file_path = os.path.join(root, file)
                caption = Caption.image2text(file_path, model, for_lora)
                # create tag file
                base = os.path.splitext(file_path)[0]
                with open(f"{base}.txt", "w", encoding="utf-8") as f:
                    f.write(caption)
    print("Done.")
