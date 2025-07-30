import ollama

PROMPT_FOR_LORA = """
Please explain the input image. Describe as many detailed elements as possible. 
Absolutely do not output or mention the following elements:
- Eyes color
- Features reminiscent of an animal
- Has a tail (and a description of its appearance)
- Description of the ears (e.g., "with pointed ears like a fox", "animal traits such as large ears")
- Hair color
- Hairstyle
- Yellow streaked hair and ahoge (cowlick)

Absolutely add output or mention the following elements:
- 3dcg
- polygon
- vr avatar
- not furry
"""

PROMPT_SIMPLE = """
Please explain the input image. Describe as many detailed elements as possible. 
"""

CANCELED = "sorry"


def image2text(image, model, for_lora=False):
    if for_lora:
        prompt = PROMPT_FOR_LORA
    else:
        prompt = PROMPT_SIMPLE
    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt, "images": [image]}],
    )
    #
    if CANCELED in response["message"]["content"]:
        print(f"Analysis rejected: {image}")
    return response["message"]["content"]
