from transformers import AutoModelForCausalLM, AutoTokenizer
import time
import torch
from flask import Flask, jsonify, request
import json
import re

MODEL_FP = "model/saved_model/checkpoint-999"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = AutoModelForCausalLM.from_pretrained(MODEL_FP).to(device)
tokenizer = AutoTokenizer.from_pretrained(MODEL_FP)

def http_to_json(raw_http_string):
    """
    Converts a raw HTTP request and response string into a JSON object.

    Args:
        raw_http_string: A string containing the raw HTTP request and response.

    Returns:
        A JSON formatted string representing the parsed HTTP data,
        or None if the input format is invalid.
    """
    prompt_match = re.search(r"<PROMPT>(.*?)<RESPONSE>", raw_http_string, re.DOTALL)
    response_match = re.search(r"<RESPONSE>(.*?)", raw_http_string, re.DOTALL)

    if not prompt_match or not response_match:
        return None

    prompt_text = prompt_match.group(1).strip()
    response_text = response_match.group(1).strip()

    def parse_headers(text_block):
        headers = {}
        lines = text_block.split('\n')
        if not lines:
            return None, None

        first_line = lines[0]
        header_lines = lines[1:]

        for line in header_lines:
            if ':' in line:
                key, value = line.split(':', 1)
                headers[key.strip()] = value.strip()

        return first_line.strip(), headers

    prompt_line, prompt_headers = parse_headers(prompt_text)
    response_line, response_headers = parse_headers(response_text)

    if prompt_line is None or response_line is None:
        return None

    try:
        method, url, protocol = prompt_line.split()
    except ValueError:
        return None

    try:
        response_protocol, status_code, status_message = response_line.split(None, 2)
    except ValueError:
        return None


    output_data = {
        "prompt": {
            "method": method,
            "url": url,
            "protocol": protocol,
            "headers": prompt_headers
        },
        "response": {
            "protocol": response_protocol,
            "status_code": int(status_code),
            "status_message": status_message,
            "headers": response_headers
        }
    }

    return json.dumps(output_data, indent=2)

def json_to_http_request_string(json_data):
    """
    Converts a JSON object representing an HTTP request into a formatted string.

    Args:
        json_data (dict or str): A dictionary or a JSON string containing
                                 the request details under a "prompt" key.

    Returns:
        str: A string formatted as an HTTP request, or an error message
             if the input format is incorrect.
    """
    # If the input is a JSON string, parse it into a dictionary
    if isinstance(json_data, str):
        try:
            data = json.loads(json_data)
        except json.JSONDecodeError:
            return "Error: Invalid JSON string provided."
    else:
        data = json_data

    # Check if the 'prompt' key exists and is a dictionary
    if 'prompt' not in data or not isinstance(data['prompt'], dict):
        return "Error: Input JSON must have a 'prompt' key containing the request data."

    prompt = data['prompt']

    # --- Build the Request Line ---
    # Extract the main components for the first line
    method = prompt.get('method', 'GET')
    url = prompt.get('url', '/')
    protocol = prompt.get('protocol', 'HTTP/1.1')
    request_line = f"{method} {url} {protocol}"

    # --- Build the Header Lines ---
    # Create a list to hold the formatted header strings
    headers = []
    
    # Define the desired order of headers to match the user's request
    header_order = [
        "User-Agent",
        "Accept",
        "Accept-Language",
        "Accept-Encoding"
    ]
    
    # Add headers to the list in the specified order, if they exist
    for key in header_order:
        if key in prompt:
            headers.append(f"{key}: {prompt[key]}")
            
    # Also add any other headers from the prompt that weren't in the specified order
    # This makes the function more robust for different inputs.
    for key, value in prompt.items():
        # We've already processed these, so skip them
        if key not in ['method', 'url', 'protocol'] and key not in header_order:
            headers.append(f"{key}: {value}")


    # Join the request line and all header lines with a newline character
    full_request = [request_line] + headers
    return "\n".join(full_request) + "\n<RESPONSE>"

def reciever(input):
    start = time.time()
    inputs = tokenizer(input, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            do_sample=True,
            penalty_alpha=0.6,
            top_k=20,
            max_new_tokens=200,
        )
    end = time.time()
    print(end - start)
    return tokenizer.decode(outputs[0])

app = Flask(__name__)

def format(example):
    prompt = example["prompt"]
    full_text = f"<PROMPT>\n{prompt}\n\n<RESPONSE>"
    tokens = tokenizer(
        full_text,
        truncation=True,
        padding="max_length",
        max_length=1000,
    )
    tokens["labels"] = tokens["input_ids"].copy()
    return tokens

@app.route('/request', methods=['POST'])
def get_response():
    data = request.get_json()
    response_txt = reciever(json_to_http_request_string(data))
    response_json = http_to_json(response_txt)

    if not response_json:
        return jsonify({"error": "Invalid HTTP response format"}), 400

    return jsonify({"response": response_json}), 201

if __name__ == '__main__':
    app.run(debug=True)

# Invoke-WebRequest -Uri 'http://127.0.0.1:5000/request' -Method POST -ContentType 'application/json' -Body '{
# "prompt": {
# "method": "GET",
# "url": "/",
# "protocol": "HTTP/1.1",
# "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8",
# "Accept-Language": "en-GB,en;q=0.5",
# "Accept-Encoding": "gzip, deflate, br, zstd",
# "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0"
# }
# }'
