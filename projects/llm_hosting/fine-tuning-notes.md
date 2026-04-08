# Fine-Tuning Notes For This Project

This note captures the reasoning behind the fine-tuning path recommended for this repository.

## 1. The Core Decision

If you want to customize an open-weight LLM, the first question is not "how do I fine-tune it?"

The first question is:

- do I need **better knowledge at runtime**
- or do I need **different model behavior**

Use **RAG** when you need:

- fresh or changing internal documents
- grounded answers from a knowledge base
- citations or source-aware answers
- minimal change to the underlying model

Use **fine-tuning** when you need:

- a consistent style or tone
- better formatting or structured outputs
- domain-specific behavior
- more reliable task performance for a narrow use case

## 2. Recommended Fine-Tuning Method

For a first project, the recommended path is:

- keep the same base model
- fine-tune a **LoRA adapter**
- evaluate it against the base model
- deploy base model plus adapter

Why this path:

- cheaper than full fine-tuning
- easier to iterate
- smaller artifacts
- simpler rollback
- easier to compare against the untuned model

## 3. Typical Workflow

The practical flow is:

1. choose a small instruct base model
2. prepare a narrow, high-quality dataset
3. train a LoRA adapter
4. evaluate behavior on held-out prompts
5. deploy the adapter

The deployment artifact is usually one of:

- base model + adapter
- merged model if your serving stack needs a single export

## 4. Training Stack

The most standard route is:

- `transformers`
- `trl`
- `peft`
- `datasets`
- `accelerate`

This project uses that route because it teaches the core concepts without hiding too much of the workflow.

## 5. Deployment Options

### Ollama

Best if you want:

- the simplest path from local experimentation to serving
- to stay close to your current local stack
- quick demo deployment

High-level deployment idea:

- keep the same base model
- attach the LoRA adapter in an Ollama `Modelfile`
- create and run the tuned model

### vLLM

Best if you want:

- a more production-like inference server
- better serving ergonomics for future scale
- easier migration toward hosted GPU deployment

High-level deployment idea:

- serve the base model with vLLM
- enable LoRA support
- load the adapter at serve time

## 6. Where To Deploy

Recommended by stage:

- learning only: local machine or Colab
- public demo: Runpod or single GPU VM
- managed serving: Hugging Face Inference Endpoints
- enterprise alignment: Azure AI Foundry, Vertex AI, or SageMaker

If you are learning fine-tuning for the first time, the best sequence is:

1. train on Colab or a GPU host
2. compare outputs against the base model
3. deploy to Ollama or vLLM

## 7. What A Good First Fine-Tuning Project Looks Like

Good first projects are narrow:

- consistent consulting tone
- structured JSON output
- domain explanation style
- custom classifier behavior

Bad first projects are vague:

- make the model smarter
- make it know all my documents
- make it better at everything

## 8. Practical Recommendation For This Repository

The best default path for this repo is:

- keep using the existing inference bridge for serving
- train a LoRA adapter in the new `finetuning` folder
- start with a small instruct model
- validate the adapter on a simple eval file
- then decide whether to serve it with Ollama or vLLM

If you are optimizing for simplicity, choose Ollama first.

If you are optimizing for a more production-style deployment path, choose vLLM.
