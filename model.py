import yaml

from PIL import Image
from google import genai
from yaml.loader import SafeLoader


def send(img: Image, keys: list):
    with open("config.yml") as cfg:
        data = yaml.load(cfg, Loader=SafeLoader)

    key = data["models"]["Google"]["key"]

    client = genai.Client(api_key=key)

    prompt = (
        "Imagine you're a secretary in a big company. I've sent you an image of a document. "
        "I'm going to give you a set of keys, divided by commas, and I want you to provide me with corresponding values for those keys. "
        "Assuming that the corresponding value for key1 would be value1 I want you to respond with a json format like this: {{key1: value1, key2: value2 ...}}. "
        "keys: {}".format(", ".join(keys))
    )

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=[prompt, img],
    )

    print(response.text)

    return response.text
