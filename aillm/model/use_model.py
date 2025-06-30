from transformers import AutoModelForCausalLM, AutoTokenizer
import time
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

MODEL_FP = "model/saved_model/checkpoint-999"

# Load in pretrained model
model = AutoModelForCausalLM.from_pretrained(MODEL_FP).to(device)
tokenizer = AutoTokenizer.from_pretrained(MODEL_FP)

# Example inputs to test model
input_text = [
    """<PROMPT>
GET https://po.smp46.me/api/settings HTTP/1.1
user-agent: Mozilla/5.0 (X11; Linux x86_64; rv:139.0) Gecko/20100101 Firefox/139.0
accept: application/json, text/plain, */*
accept-language: en-US,en;q=0.5
accept-encoding: gzip, deflate, br, zstd
x-csrf-token: TEST_TOKEN
referer: https://po.smp46.me/

<RESPONSE>
""", 
"""<PROMPT>
POST https://example.com/api/login HTTP/1.1
content-type: application/json
user-agent: CustomClient/1.0
cookie: session=abc123

<RESPONSE>
""", 
"""<PROMPT>
POST https://example.com/api/data HTTP/1.1
content-type: application/json
authorization: Bearer XYZ123
user-agent: ExampleClient/2.0
cookie: auth_token=abc.def.ghi

<RESPONSE>
""",
"""<PROMPT>
GET https://api.example.com/v1/config HTTP/1.1
user-agent: Mozilla/5.0 (X11; Linux x86_64; rv:139.0) Gecko/20100101 Firefox/139.0
accept: application/json
accept-language: en-US,en;q=0.5
authorization: Bearer VALID_TOKEN_ABC123
referer: https://example.com/dashboard

<RESPONSE>
"""
]

start = time.time()
inputs = tokenizer(input_text[0], return_tensors="pt").to(device)
with torch.no_grad(): # Skip overhead
    outputs = model.generate(
        **inputs,
        do_sample=True,
        penalty_alpha=0.6, # To reduce repeated headers
        top_k=20,
        max_new_tokens=200, # Stop model from generating more responses
    )
end = time.time()
print("Time to tokenize and generate prompt: ", end - start)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))