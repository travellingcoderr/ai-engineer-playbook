import argparse
import json
from pathlib import Path

import torch
from datasets import load_dataset
from peft import LoraConfig
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
)
from trl import SFTConfig, SFTTrainer


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train a LoRA adapter on chat-format JSONL data.")
    parser.add_argument("--model-name", required=True, help="Base model from Hugging Face.")
    parser.add_argument("--train-file", required=True, help="Path to training JSONL file.")
    parser.add_argument("--eval-file", help="Optional path to evaluation JSONL file.")
    parser.add_argument("--output-dir", required=True, help="Where adapter checkpoints will be saved.")
    parser.add_argument("--max-seq-length", type=int, default=1024)
    parser.add_argument("--num-train-epochs", type=float, default=2.0)
    parser.add_argument("--per-device-train-batch-size", type=int, default=1)
    parser.add_argument("--per-device-eval-batch-size", type=int, default=1)
    parser.add_argument("--gradient-accumulation-steps", type=int, default=8)
    parser.add_argument("--learning-rate", type=float, default=2e-4)
    parser.add_argument("--logging-steps", type=int, default=10)
    parser.add_argument("--save-steps", type=int, default=50)
    parser.add_argument("--eval-steps", type=int, default=50)
    parser.add_argument("--warmup-ratio", type=float, default=0.03)
    parser.add_argument("--lora-r", type=int, default=16)
    parser.add_argument("--lora-alpha", type=int, default=32)
    parser.add_argument("--lora-dropout", type=float, default=0.05)
    parser.add_argument(
        "--target-modules",
        nargs="+",
        default=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        help="Transformer modules to adapt with LoRA.",
    )
    parser.add_argument(
        "--load-in-4bit",
        action="store_true",
        help="Use QLoRA-style 4-bit loading. Best on Linux with a compatible NVIDIA GPU.",
    )
    return parser.parse_args()


def render_chat_example(messages: list[dict], tokenizer) -> str:
    # We render each training example into the model's native chat format so
    # the adapter learns the exact conversation structure used at inference time.
    return tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)


def load_chat_dataset(path: str, tokenizer):
    dataset = load_dataset("json", data_files=path, split="train")

    def _format(example: dict) -> dict:
        if "messages" not in example:
            raise ValueError("Each JSONL row must include a 'messages' field.")
        text = render_chat_example(example["messages"], tokenizer)
        return {"text": text}

    return dataset.map(_format)


def build_model(args: argparse.Namespace):
    quantization_config = None
    model_kwargs = {"device_map": "auto"}

    if args.load_in_4bit:
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
        )
        model_kwargs["quantization_config"] = quantization_config
    else:
        if torch.cuda.is_available():
            model_kwargs["torch_dtype"] = torch.float16

    model = AutoModelForCausalLM.from_pretrained(args.model_name, **model_kwargs)
    model.config.use_cache = False
    return model


def main():
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    tokenizer = AutoTokenizer.from_pretrained(args.model_name, use_fast=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    train_dataset = load_chat_dataset(args.train_file, tokenizer)
    eval_dataset = load_chat_dataset(args.eval_file, tokenizer) if args.eval_file else None

    model = build_model(args)

    peft_config = LoraConfig(
        r=args.lora_r,
        lora_alpha=args.lora_alpha,
        lora_dropout=args.lora_dropout,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=args.target_modules,
    )

    training_args = SFTConfig(
        output_dir=str(output_dir),
        num_train_epochs=args.num_train_epochs,
        per_device_train_batch_size=args.per_device_train_batch_size,
        per_device_eval_batch_size=args.per_device_eval_batch_size,
        gradient_accumulation_steps=args.gradient_accumulation_steps,
        learning_rate=args.learning_rate,
        logging_steps=args.logging_steps,
        save_steps=args.save_steps,
        eval_steps=args.eval_steps if eval_dataset is not None else None,
        evaluation_strategy="steps" if eval_dataset is not None else "no",
        warmup_ratio=args.warmup_ratio,
        lr_scheduler_type="cosine",
        bf16=torch.cuda.is_available() and torch.cuda.is_bf16_supported(),
        fp16=torch.cuda.is_available() and not torch.cuda.is_bf16_supported(),
        max_seq_length=args.max_seq_length,
        packing=False,
        report_to="none",
    )

    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        peft_config=peft_config,
        processing_class=tokenizer,
        dataset_text_field="text",
    )

    trainer.train()
    trainer.save_model(str(output_dir))
    tokenizer.save_pretrained(str(output_dir))

    summary = {
        "base_model": args.model_name,
        "train_file": args.train_file,
        "eval_file": args.eval_file,
        "output_dir": str(output_dir),
        "load_in_4bit": args.load_in_4bit,
    }
    (output_dir / "run_summary.json").write_text(json.dumps(summary, indent=2))
    print(f"Saved LoRA adapter to {output_dir}")


if __name__ == "__main__":
    main()
