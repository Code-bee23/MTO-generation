import json
import base64
import requests
import re

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llava:latest"


def build_prompt(ocr_text: str):

    return f"""
You are a professional piping engineer.

Analyze the piping isometric drawing image together with the OCR text.

Extract the information below.

Return ONLY valid JSON.

Do NOT explain anything.
Do NOT use markdown.
Do NOT wrap the JSON inside ```.

JSON:

{{
  "line_number":"",
  "pipe_size":"",
  "material":"",
  "pipe_length":"",
  "pipe_schedule":"",
  "valves":[],
  "elbows":0,
  "tees":0,
  "reducers":0,
  "flanges":0,
  "supports":0,
  "remarks":""
}}

OCR TEXT:

{ocr_text}
"""


def image_to_base64(image_path):

    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def call_ollama(prompt, image_path):

    image = image_to_base64(image_path)

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "images": [image],
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=300
    )

    response.raise_for_status()

    result = response.json()

    print("\n================ RAW LLaVA RESPONSE ================\n")
    print(result["response"])
    print("\n====================================================\n")

    return result["response"]


def extract_json(text):

    # Remove markdown fences
    text = text.replace("```json", "")
    text = text.replace("```", "")

    # Find first JSON object
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise Exception("No JSON found in LLaVA response.")

    json_text = match.group(0)

    print("\n================ JSON FOUND ================\n")
    print(json_text)
    print("\n============================================\n")

    return json.loads(json_text)


def validate_json(data):

    defaults = {
        "line_number": "",
        "pipe_size": "",
        "material": "",
        "pipe_length": "",
        "pipe_schedule": "",
        "valves": [],
        "elbows": 0,
        "tees": 0,
        "reducers": 0,
        "flanges": 0,
        "supports": 0,
        "remarks": ""
    }

    for key, value in defaults.items():
        if key not in data:
            data[key] = value

    return data


def extract_components(ocr_text, image_path):

    prompt = build_prompt(ocr_text)

    response = call_ollama(prompt, image_path)

    try:
        data = extract_json(response)

        data = validate_json(data)

        print("\n================ FINAL AI DATA ================\n")
        print(data)
        print("\n===============================================\n")

        return data

    except Exception as e:

        print("JSON Parsing Failed")
        print(e)

        return {
            "line_number": "",
            "pipe_size": "Unknown",
            "material": "Unknown",
            "pipe_length": "Unknown",
            "pipe_schedule": "",
            "valves": [],
            "elbows": 0,
            "tees": 0,
            "reducers": 0,
            "flanges": 0,
            "supports": 0,
            "remarks": "AI could not extract structured data"
        }