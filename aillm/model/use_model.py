from transformers import pipeline
from transformers import AutoModelForCausalLM, AutoTokenizer
import time
import torch

MODEL_FP = "model/saved_model/checkpoint-999"

# model = AutoModelForCausalLM.from_pretrained(MODEL_FP).to("cuda")
model = AutoModelForCausalLM.from_pretrained(MODEL_FP)
tokenizer = AutoTokenizer.from_pretrained(MODEL_FP)

# generator = pipeline("text-generation", model=model, tokenizer=tokenizer, device=0)

input_text = """<PROMPT>
GET https://po.smp46.me/api/settings HTTP/1.1
user-agent: Mozilla/5.0 (X11; Linux x86_64; rv:139.0) Gecko/20100101 Firefox/139.0
accept: application/json, text/plain, */*
accept-language: en-US,en;q=0.5
accept-encoding: gzip, deflate, br, zstd
x-csrf-token: TEST_TOKEN
referer: https://po.smp46.me/

<RESPONSE>
"""

# input_text = """<PROMPT>
# POST https://example.com/api/login HTTP/1.1
# content-type: application/json
# user-agent: CustomClient/1.0
# cookie: session=abc123

# <RESPONSE>
# """

# input_text = """<PROMPT>
# POST https://example.com/api/data HTTP/1.1
# content-type: application/json
# authorization: Bearer XYZ123
# user-agent: ExampleClient/2.0
# cookie: auth_token=abc.def.ghi

# <RESPONSE>
# """

start = time.time()
# inputs = tokenizer(input_text, return_tensors="pt").to("cuda")
inputs = tokenizer(input_text, return_tensors="pt")
with torch.no_grad(): # skip overhead
    outputs = model.generate(
        **inputs,
        do_sample=True,
        penalty_alpha=0.6,
        top_k=20,
        max_new_tokens=200,
        num_beams=3,
    )

# output = generator(
#     input_text,
#     do_sample=True,
#     top_k=50, 
#     top_p=0.95,
#     max_new_tokens=200,
# )
end = time.time()
print(end - start)
# print(output[0]["generated_text"])
print(tokenizer.decode(outputs[0], skip_special_tokens=True))

