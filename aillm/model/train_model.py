import argparse
import torch
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments, 
    Trainer,
    DataCollatorForLanguageModeling
)

# Get the name of the run
def parse_args():
    parser = argparse.ArgumentParser(description="Fine-tuning model")

    parser.add_argument(
        "--run_name",
        type=str,
        required=True,
        help="Name of the current run",
    )
    parser.add_argument(
        "--checkpoint",
        type=str,
        required=False,
        help="Model to train from (default: distilgpt2)",
    )
    args = parser.parse_args()
    return args

args = parse_args()

CHECKPOINT = args.checkpoint if args.checkpoint else "distilgpt2"
DATA_FP = "data/synthetic_http_traffic_skewed.jsonl"
SAVE_LOCATION = "model/saved_model/{args.run_name}"

def tokenize_data():
    tokenizer = AutoTokenizer.from_pretrained(CHECKPOINT)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.add_special_tokens({"eos_token": "<END>"})

    dataset = load_dataset("json", data_files=DATA_FP, split="train")

    # Fromat the token correctly for the model
    def format(example):
        prompt = example["prompt"]
        response = example["response"]
        full_text = f"<PROMPT>\n{prompt}\n\n<RESPONSE>\n{response}<END>"
        
        tokens = tokenizer(
            full_text,
            truncation=True,
            padding="max_length",
            max_length=1024,
        )
        return {
            "input_ids": tokens["input_ids"],
            "attention_mask": tokens["attention_mask"],
            "labels": tokens["input_ids"]
        }
    
    # Format all of the dataset, from jsonl to txt
    tokenized_dataset = dataset.map(format, remove_columns=dataset.column_names, batched=False)
    return tokenized_dataset.train_test_split(test_size=0.1), tokenizer

def training(data, tokenizer):
    model = AutoModelForCausalLM.from_pretrained(CHECKPOINT)

    # Hyperparameters
    training_args = TrainingArguments(
        output_dir=SAVE_LOCATION,
        eval_strategy="epoch",
        logging_strategy="epoch",
        save_strategy="epoch",
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        num_train_epochs=5,
        learning_rate=5e-4,
        weight_decay=0.01,
        logging_dir=f"{SAVE_LOCATION}/logs",
        bf16=torch.cuda.is_available(), # other choice is fp16, since 5070ti gpu can use bf16
        report_to="none",
        lr_scheduler_type="cosine",
        gradient_accumulation_steps=8,
        warmup_steps=100,
        eval_steps=100,
        logging_steps=50,
    )

    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False, # to change it for text-gen instead of classification
        pad_to_multiple_of=8,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=data["train"],
        eval_dataset=data["test"],
        data_collator=data_collator,
    )

    trainer.train()
    return trainer

def main():
    tokenized_dataset, tokenizer = tokenize_data()
    trainer = training(data=tokenized_dataset, tokenizer=tokenizer)

    # Save the trained model and tokenizer
    trainer.save_model(SAVE_LOCATION)
    tokenizer.save_pretrained(SAVE_LOCATION)

if __name__ == "__main__":
    main()