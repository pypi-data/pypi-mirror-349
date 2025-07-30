from PIL import Image

import fm_image_tagger.ollama_caption as Caption
import fm_image_tagger.tagger as Tagger


def get_meta(image_path):
    positive = ""
    negative = ""
    try:
        with Image.open(image_path) as img:
            meta_data = img.text
            if "parameters" in meta_data:
                prompt = meta_data["parameters"].split("\n")
                positive = prompt[0]
                negative = prompt[1]
    except Exception as e:
        print(f"An error occurred: {e}")
    negative = negative.replace("Negative prompt: ", "")
    return (positive, negative)


def display(image_path, meta_flag, threshold=0.35):
    if meta_flag:
        (positive, negative) = get_meta(image_path)
        print(f"Positive prompt:\n{positive}")
        print(f"Negative prompt:\n{negative}")
    else:
        tagger = Tagger.WD14Tagger(Tagger.MOAT_MODEL_DSV2_REPO)
        tags = tagger.image_tag(image_path, threshold=threshold)
        print(f"Tags:\n{tags}")


def caption(image_path, model, for_lora):
    text = Caption.image2text(image_path, model, for_lora)
    print(f"Caption:\n{text}")
