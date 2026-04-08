# Fine-Tuning Starter Project

This folder is a beginner-friendly starting point for fine-tuning an open-weight LLM with **LoRA** using the Hugging Face stack.

If you have worked with RAG but not with fine-tuning, the right mental model is:

- **RAG** gives the model better facts at runtime
- **fine-tuning** changes the model's behavior

Use fine-tuning when you want the model to:

- follow a house style consistently
- speak in a domain-specific tone
- return outputs in a specific structure
- perform a repeated task more reliably than prompt-only approaches

Do not fine-tune first if your main problem is:

- "the model needs access to my documents"
- "the model needs fresh business knowledge"
- "the answers need citations from my knowledge base"

That is usually a RAG problem, not a fine-tuning problem.

## What This Starter Includes

- `train_lora.py`: trains a LoRA adapter on chat-format JSONL data
- `eval_lora.py`: runs quick side-by-side evaluation prompts
- `requirements.txt`: Python dependencies
- `data/sample_train.jsonl`: tiny training dataset example
- `data/sample_eval.jsonl`: tiny eval dataset example

## Recommended Path For A Beginner

1. Start with a small instruct model.
2. Prepare a clean dataset of prompt/response examples.
3. Train a LoRA adapter, not the full model.
4. Evaluate it against the untuned base model.
5. Deploy the adapter with either Ollama or vLLM.

## Training Stack Used Here

- `transformers`
- `datasets`
- `trl`
- `peft`
- `accelerate`

This is the standard Hugging Face ecosystem route. It keeps the workflow understandable and transferable.

## Hardware Expectations

Real fine-tuning works best on Linux with an NVIDIA GPU.

Typical options:

- local Linux box with CUDA GPU
- Colab
- Runpod
- cloud VM with GPU

Mac can be useful for inference and app integration, but it is usually not the best place to learn QLoRA fine-tuning first.

## Dataset Format

The scripts expect chat-format JSONL like this:

```json
{"messages":[
  {"role":"system","content":"You are a concise enterprise AI assistant."},
  {"role":"user","content":"Explain RAG in one paragraph."},
  {"role":"assistant","content":"RAG retrieves relevant external context at query time and includes it in the prompt so the LLM can answer with fresher and more grounded information."}
]}
```

Each line is one training example.

## Install

Create a virtual environment, then install requirements:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r finetuning/requirements.txt
```

## Train

Example command:

```bash
python finetuning/train_lora.py \
  --model-name Qwen/Qwen2.5-3B-Instruct \
  --train-file finetuning/data/sample_train.jsonl \
  --eval-file finetuning/data/sample_eval.jsonl \
  --output-dir finetuning/output/qwen2.5-3b-lora \
  --num-train-epochs 2 \
  --per-device-train-batch-size 1 \
  --gradient-accumulation-steps 8 \
  --learning-rate 2e-4 \
  --max-seq-length 1024
```

Notes:

- Start small and prove the workflow first.
- If you are on a compatible Linux GPU and want QLoRA, add `--load-in-4bit`.
- Keep your first dataset tiny and high quality.

## Evaluate

After training, compare the base model and adapter:

```bash
python finetuning/eval_lora.py \
  --base-model Qwen/Qwen2.5-3B-Instruct \
  --adapter-path finetuning/output/qwen2.5-3b-lora \
  --eval-file finetuning/data/sample_eval.jsonl \
  --max-new-tokens 200
```

This is not a full benchmark. It is a simple starter script so you can inspect whether the tuned model is behaving more like you want.

## How To Think About Good Training Data

Good fine-tuning data is:

- small but high quality to begin with
- consistent in style
- realistic to the production task
- narrow in purpose

Bad first datasets are:

- scraped and noisy
- internally inconsistent
- trying to teach ten tasks at once
- mostly prompt engineering experiments copied into a dataset

## What To Tune First

For a first project, choose only one of these goals:

- answer in a specific business tone
- output a fixed JSON structure
- classify requests into a custom taxonomy
- rewrite content in a company style

Do not try to tune "general intelligence" into the model.

## Deployment Options After Training

### Option 1: Ollama

This is the simplest next step if you want to stay close to your current setup.

High-level flow:

1. train LoRA adapter
2. create an Ollama `Modelfile`
3. point `FROM` to the same base model
4. attach the adapter with `ADAPTER`
5. create and run the model in Ollama

### Option 2: vLLM

This is a better production-style path if you want a scalable HTTP server and easier future deployment.

High-level flow:

1. train LoRA adapter
2. serve the base model with vLLM
3. enable LoRA support
4. load the adapter at serve time

## Where To Deploy

Recommended deployment path:

- learning and iteration: local or Colab
- public demo: Runpod or a single GPU VM
- more managed deployment: Hugging Face Inference Endpoints
- enterprise cloud alignment: Azure AI Foundry, Vertex AI, or SageMaker

For your stage, the best default is:

- train the adapter in Colab or Runpod
- test it locally or on the same GPU host
- deploy with Ollama if you want simplicity
- deploy with vLLM if you want a more production-like serving path

## First Project Idea

If you want a practical first fine-tuning project, fine-tune a small model to behave like an "enterprise AI solutions architect" that:

- answers in a concise consulting tone
- explains AI architecture clearly
- uses business-safe wording
- returns short, structured answers

That is easier to validate than a broad open-ended tuning goal.
