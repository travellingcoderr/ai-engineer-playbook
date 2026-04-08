import argparse
import json

import torch
from datasets import load_dataset
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare a base model and LoRA adapter on eval prompts.")
    parser.add_argument("--base-model", required=True, help="Base model used for the adapter.")
    parser.add_argument("--adapter-path", required=True, help="Path to saved LoRA adapter directory.")
    parser.add_argument("--eval-file", required=True, help="JSONL file with chat-format messages.")
    parser.add_argument("--max-new-tokens", type=int, default=200)
    return parser.parse_args()


def load_generator(model_name: str, adapter_path: str | None = None):
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map="auto",
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    )

    if adapter_path:
        model = PeftModel.from_pretrained(model, adapter_path)

    model.eval()
    return model, tokenizer


def generate_response(model, tokenizer, messages: list[dict], max_new_tokens: int) -> str:
    # For evaluation we remove the assistant answer, then ask the model to continue.
    prompt_messages = [m for m in messages if m["role"] != "assistant"]
    prompt = tokenizer.apply_chat_template(prompt_messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            temperature=None,
            pad_token_id=tokenizer.eos_token_id,
        )

    generated_tokens = outputs[0][inputs["input_ids"].shape[1]:]
    return tokenizer.decode(generated_tokens, skip_special_tokens=True).strip()


def main():
    args = parse_args()
    dataset = load_dataset("json", data_files=args.eval_file, split="train")

    base_model, base_tokenizer = load_generator(args.base_model)
    tuned_model, tuned_tokenizer = load_generator(args.base_model, args.adapter_path)

    for index, example in enumerate(dataset, start=1):
        messages = example["messages"]
        expected = next((m["content"] for m in messages if m["role"] == "assistant"), "")
        user_prompt = next((m["content"] for m in messages if m["role"] == "user"), "")

        base_output = generate_response(base_model, base_tokenizer, messages, args.max_new_tokens)
        tuned_output = generate_response(tuned_model, tuned_tokenizer, messages, args.max_new_tokens)

        print("=" * 80)
        print(f"Example {index}")
        print(f"User: {user_prompt}")
        print(f"Expected: {expected}")
        print(f"Base model: {base_output}")
        print(f"Tuned model: {tuned_output}")

    print("=" * 80)
    print(
        json.dumps(
            {
                "base_model": args.base_model,
                "adapter_path": args.adapter_path,
                "eval_file": args.eval_file,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
