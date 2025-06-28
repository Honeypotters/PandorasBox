from datasets import load_dataset
from transformers import AutoTokenizer

checkpoint = "distilgpt2"
data_fp = "data/flows_formatted.jsonl"

tokenizer = AutoTokenizer.from_pretrained(checkpoint)

dataset = load_dataset("json", data_files=data_fp, split="train")

tokenizer.save_pretrained("model/full_tokenizer")