import argparse
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments, 
    Trainer
)

def parse_args():
    parser = argparse.ArgumentParser(description="Fine-tuning GPT2 model")

    parser.add_argument(
        "--run_name",
        type=str,
        required=True,
        help="Name of the current run",
    )
    args = parser.parse_args()
    return args

args = parse_args()

CHECKPOINT = "distilgpt2"
DATA_FP = "data/flows_formatted.jsonl"
SAVE_LOCATION = "model/saved_model/run_1"

def tokenize_data():
    tokenizer = AutoTokenizer.from_pretrained(CHECKPOINT)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.add_special_tokens({"eos_token": "<END>"})

    dataset = load_dataset("json", data_files=DATA_FP, split="train")

    def format(example):
        prompt = example["prompt"]
        response = example["response"]
        full_text = f"<PROMPT>\n{prompt}\n\n<RESPONSE>\n{response}<END>"
        tokens = tokenizer(
            full_text,
            truncation=True,
            padding="max_length",
            max_length=1000,
        )
        tokens["labels"] = tokens["input_ids"].copy()
        return tokens

    tokenized_dataset = dataset.map(format, batched=False)
    return tokenized_dataset.train_test_split(test_size=0.1), tokenizer

def training(data, tokenizer):
    model = AutoModelForCausalLM.from_pretrained(CHECKPOINT)

    # Hyperparameters
    training_args = TrainingArguments(
        # "test-trainer",
        evaluation_strategy="epoch",
        # logging_strategy="epoch",
        # save_strategy="epoch",
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        num_train_epochs=3,
        learning_rate=5e-5,
        weight_decay=0.01,
        # save_total_limit=2,
        # logging_dir="logs",
        fp16=True,
        # report_to="none",


        # gradient_accumulation_steps=4,
        # lr_scheduler_type="cosine",
    )

    # Actual training
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=data["train"],
        eval_dataset=data["test"],
        tokenizer=tokenizer,
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