from transformers import AutoModelForCausalLM, AutoTokenizer

checkpoint = "distilgpt2"
tokenizer = "model/full_tokenizer"

model = AutoModelForCausalLM.from_pretrained(checkpoint)
tokenizer = AutoTokenizer.from_pretrained()

raw_inputs = [
    "GET /api/user?id=42 HTTP/1.1\nHost: honeypot.net\n\n",
    "POST /api/login HTTP/1.1\nHost: honeypot.net\n\nusername=admin&password=1234"
]

inputs = tokenizer(raw_inputs, return_tensors="pt", padding=True, truncation=True)

outputs = model(**inputs)

print("Logits shape:", outputs.logits.shape)