import json
from datasets import Dataset

# Load the mitmproxy output
with open("data/flows.json", "r") as f:
    raw_data = json.load(f)

def make_prompt_response(entry):
    # Format the request
    req_line = f"{entry['method']} {entry['url']} HTTP/1.1"
    req_headers = "\n".join([f"{k}: {v}" for k, v in entry["request_headers"].items() if v])
    req_body = entry["request_body"] or ""
    prompt = f"{req_line}\n{req_headers}\n\n{req_body}"

    # Format the response
    status_line = f"HTTP/1.1 {entry['status_code']} STATUS"
    res_headers = "\n".join([f"{k}: {v}" for k, v in entry["response_headers"].items() if v])
    res_body = entry["response_body"] or ""
    response = f"{status_line}\n{res_headers}\n\n{res_body}"

    return {"prompt": prompt, "response": response}

# Convert all entries
converted = [make_prompt_response(entry) for entry in raw_data]

# Save for inspection (optional)
with open("flows_formatted.jsonl", "w") as f:
    for item in converted:
        f.write(json.dumps(item) + "\n")