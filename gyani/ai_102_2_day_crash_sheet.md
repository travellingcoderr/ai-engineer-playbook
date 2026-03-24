# AI-102 Two-Day Crash Sheet

This sheet is optimized for speed, not completeness. The goal is to get you exam-ready fast by focusing on the highest-yield areas for `AI-102`.

Official exam page:
- <https://learn.microsoft.com/en-us/learn/certifications/exams/ai-102>

## Strategy

- Do not try to master everything.
- Learn the Azure AI service map first.
- Focus on Azure OpenAI, Azure AI Search, document intelligence, language services, vision basics, responsible AI, and security.
- Use Microsoft Learn practice assessments after each study block.
- Memorize service selection and architecture patterns, because many questions are scenario-based.

## What To Prioritize

### Highest priority

- Azure OpenAI Service
- Azure AI Search
- Retrieval-Augmented Generation
- Prompt engineering basics
- Responsible AI
- Language service capabilities
- Document intelligence basics
- Security and authentication patterns

### Medium priority

- Computer Vision service overview
- Speech service overview
- Bot/service integration concepts
- Knowledge mining patterns

### Lower priority for a crash plan

- Deep SDK coding details
- Rare edge-case configurations
- Full implementation syntax

## Service Map You Must Know

### Azure OpenAI

Use for:
- chat completions
- embeddings
- generative AI apps
- assistants and agent-style solutions

Know:
- prompts
- system messages
- temperature
- max tokens
- content filtering basics
- RAG pairing with Azure AI Search

### Azure AI Search

Use for:
- indexing enterprise data
- full text search
- vector search
- hybrid search
- semantic ranking

Know:
- index
- documents
- chunks
- embeddings
- vector fields
- hybrid retrieval
- semantic search improves relevance

### Azure AI Document Intelligence

Use for:
- forms
- invoices
- receipts
- mortgage and business documents
- extracting structured fields from documents

Know:
- prebuilt models
- custom models
- OCR plus field extraction

### Azure AI Language

Use for:
- sentiment analysis
- key phrase extraction
- named entity recognition
- summarization
- question answering
- conversational language understanding

Know when to choose Language service versus Azure OpenAI:
- use Language service for standard NLP tasks
- use Azure OpenAI for generative and flexible reasoning tasks

### Azure AI Vision

Use for:
- image analysis
- OCR
- captioning
- object detection basics

### Speech

Use for:
- speech to text
- text to speech
- translation speech scenarios

## Fast Architecture Patterns To Memorize

### Pattern 1: Enterprise RAG

Flow:
1. Ingest documents
2. Chunk content
3. Generate embeddings
4. Store in Azure AI Search or vector-capable store
5. Retrieve relevant chunks
6. Send retrieved context plus prompt to Azure OpenAI
7. Return grounded response

Why use it:
- current enterprise data
- lower hallucination risk
- easy content updates without retraining

### Pattern 2: Document Processing

Flow:
1. Upload document
2. OCR and field extraction with Document Intelligence
3. Store structured results
4. Optionally send extracted text into Language service or Azure OpenAI

### Pattern 3: Guarded AI Application

Flow:
1. User prompt enters application
2. Validate input
3. Retrieve enterprise context if needed
4. Send to Azure OpenAI
5. Filter or validate output
6. Log usage, latency, and safety events

### Pattern 4: Search + Chat

Use Azure AI Search when:
- data changes frequently
- you need citations or grounded answers
- enterprise content must be indexed and retrieved

## What Microsoft Usually Tests

- choosing the correct Azure AI service for a scenario
- building generative AI solutions with Azure OpenAI
- implementing retrieval with Azure AI Search
- processing documents and text with the right Azure service
- responsible AI and content safety
- authentication and secure access patterns
- monitoring and deployment awareness

## Day 1 Plan

### Block 1: 2 hours

Study:
- Azure OpenAI basics
- prompts, completions, embeddings
- temperature, tokens, grounding
- RAG basics

Memorize:
- embeddings are for search and similarity, not final answer generation
- RAG is preferred for private and frequently changing data
- system messages shape assistant behavior

### Block 2: 2 hours

Study:
- Azure AI Search
- vector search
- semantic ranking
- hybrid retrieval
- indexing documents

Memorize:
- keyword search alone is weaker for semantic retrieval
- vector search improves meaning-based retrieval
- hybrid search combines vector and keyword methods

### Block 3: 90 minutes

Study:
- Document Intelligence
- Language service
- when to choose each one

Memorize:
- invoices/forms/receipts -> Document Intelligence
- sentiment/entities/key phrases -> Language service
- flexible generated text -> Azure OpenAI

### Block 4: 60 minutes

Take practice questions and review only incorrect answers.

## Day 2 Plan

### Block 1: 90 minutes

Study:
- Responsible AI
- content filtering
- safe deployment
- human oversight
- transparency and privacy basics

Memorize:
- fairness
- reliability and safety
- privacy and security
- inclusiveness
- transparency
- accountability

### Block 2: 90 minutes

Study:
- Vision overview
- Speech overview
- security/authentication basics
- managed identities
- key handling

Memorize:
- use managed identity and secure secret storage patterns where possible
- do not hardcode keys

### Block 3: 2 hours

Do full practice assessment.

Rules:
- flag every weak area
- review only weak areas
- do not reread everything

### Block 4: 60 minutes

Final revision:
- service selection table
- RAG architecture
- responsible AI principles
- search vs language vs openai vs document intelligence

## Service Selection Cheat Sheet

### If the question says

`Need grounded answers from private enterprise documents`

Choose:
- Azure OpenAI + Azure AI Search

`Need invoice or form field extraction`

Choose:
- Azure AI Document Intelligence

`Need sentiment, entities, key phrases, summarization`

Choose:
- Azure AI Language

`Need image analysis or OCR from images`

Choose:
- Azure AI Vision

`Need speech transcription or speech synthesis`

Choose:
- Azure AI Speech

`Need flexible chat, generation, prompt-based reasoning`

Choose:
- Azure OpenAI

## Terms To Be Ready To Explain

- token
- embedding
- vector search
- semantic ranker
- hybrid search
- chunking
- grounding
- hallucination
- prompt engineering
- content filtering
- responsible AI

## Exam-Day Tactics

- Read the scenario first, then identify the required capability.
- Eliminate answers that use the wrong service family.
- When data is private and changing, think RAG.
- When extraction from documents is required, think Document Intelligence.
- When classic NLP analysis is required, think Language service.
- Do not overthink with custom ML unless the question clearly requires it.

## Last-Minute Memory List

- Azure OpenAI = generation, chat, embeddings
- Azure AI Search = retrieval, vector, hybrid, semantic ranking
- Document Intelligence = forms and structured extraction
- Language = NLP analysis tasks
- Vision = image analysis and OCR
- Speech = speech to text and text to speech
- RAG = retrieve first, generate second

## Best Use Of Your Background

Because you already know RAG, agents, observability, and Azure-oriented architecture, your fastest path is not memorizing code. Your fastest path is mapping what you already know to Microsoft service names and exam-style scenario wording.

## Final Advice

- If your practice scores are weak after two days, delay the exam slightly rather than rushing.
- If your goal is job-search credibility, passing `AI-102` matters much more than over-preparing for `AI-900`.
