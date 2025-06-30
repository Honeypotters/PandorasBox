from transformers import AutoModelForCausalLM, AutoTokenizer
import time
import torch
from flask import Flask, jsonify, request
import json
import datetime

MODEL_FP = "aillm/model/saved_model/run_6"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = AutoModelForCausalLM.from_pretrained(MODEL_FP).to(device)
tokenizer = AutoTokenizer.from_pretrained(MODEL_FP)

def convert_http_to_json(http_string: str) -> dict:
    """
    Parses a raw HTTP request and response string into a structured dictionary.
    """
    # Separate the main prompt and response sections
    try:
        prompt_section, response_section = http_string.strip().split("<RESPONSE>", 1)
    except ValueError:
        raise ValueError("Input string must contain '<RESPONSE>' separator.")

    # Clean up the prompt section from its tag
    prompt_section = prompt_section.replace("<PROMPT>", "").strip()

    # Process the Response
    response_parts = response_section.strip().split("\n\n", 1)
    response_header_lines = response_parts[0].split("\n")
    status_line = response_header_lines[0].split(None, 2)

    response_data = {
        "protocol": status_line[0],
        "status_code": int(status_line[1]),
        "status_message": status_line[2],
        "headers": {},
    }

    # Add body to response_data if it exists
    if len(response_parts) > 1:
        response_data["body"] = response_parts[1]

    # Parse response headers
    for line in response_header_lines[1:]:
        if line.strip():
            parts = line.split(":", 1)
            if len(parts) == 2:
                key, value = parts
                response_data["headers"][key.strip().lower()] = value.strip()

    # Combine into the final structure
    final_structure = {"response": response_data}

    # Return the dictionary
    return final_structure

def json_to_http_request_string(json_data):
    """
    Converts a JSON object representing an HTTP request into a formatted string.
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
    if "prompt" not in data or not isinstance(data["prompt"], dict):
        return "Error: Input JSON must have a 'prompt' key containing the request data."

    prompt = data["prompt"]

    # Extract the main components for the first line
    method = prompt.get("method", "GET")
    url = prompt.get("url", "/")
    protocol = prompt.get("protocol", "HTTP/1.1")
    request_line = f"{method} {url} {protocol}"

    # Create a list to hold the formatted header strings
    headers = []

    # Define the desired order of headers to match the user's request
    header_order = ["User-Agent", "Accept", "Accept-Language", "Accept-Encoding"]

    # Add headers to the list in the specified order, if they exist
    for key in header_order:
        if key in prompt:
            headers.append(f"{key}: {prompt[key]}")

    for key, value in prompt.items():
        if key not in ["method", "url", "protocol"] and key not in header_order:
            headers.append(f"{key}: {value}")

    # Join the request line and all header lines to form the request details
    request_details = "\n".join([request_line] + headers)

    return f"<PROMPT>\n{request_details}\n\n<RESPONSE>"


# Generate response
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

def log_request(response_txt):
    timestamp = datetime.datetime.now().isoformat()
    log_entry = f"[{timestamp}]\n{response_txt}\n{'-'*80}\n"
    with open("aillm/data/request_logs.txt", "a", encoding="utf-8") as log_file:
        log_file.write(log_entry)

app = Flask(__name__)

# Process request
@app.route("/api", methods=["POST"])
def get_response():
    data = request.get_json()
    response_txt = reciever(json_to_http_request_string(data))
    response_json = convert_http_to_json(response_txt)

    log_request(response_txt)

    if not response_json:
        return jsonify({"error": "Invalid HTTP response format"}), 400

    return jsonify({"response": response_json}), 201

if __name__ == "__main__":
    app.run(debug=True)
