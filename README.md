# Basic Agent Loop

Companion code for the article **[The Agent Loop Is Simpler Than You Think](#)**.

The article walks through what an agent loop actually is, where the idea came from (the 2022 [MRKL Systems paper](https://arxiv.org/abs/2205.00445) by AI21 Labs), and how to implement one yourself in about 40 lines of Python.

This repo contains that implementation.

## What It Does

`agent_loop.py` runs a minimal agent loop against a local model via [LM Studio](https://lmstudio.ai). The loop has two steps:

1. **Observe** — invoke the model with the current context
2. **Act or end** — if the model returns a tool call, run it and loop; if it returns a stop token, return the final answer

The only tool wired up is a calculator — a nod to the MRKL paper, which used the same example to show that LLMs don't need to compute, they just need to know *when* to call something that can.

## Setup

**Requirements:** Python 3.9+, [LM Studio](https://lmstudio.ai) running locally with a tool-capable model loaded (Llama 3, Mistral, or Qwen recommended).

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Start LM Studio's local server, then run:

```bash
python agent_loop.py
```

## Adapting to Other Providers

The code uses the OpenAI SDK, which is supported by most model providers. To point it at a different provider, update the `base_url` and `api_key` in the client:

```python
client = OpenAI(base_url="https://your-provider/v1", api_key="your-key")
```

## Tested On

13-inch MacBook Air, M4, 32GB — macOS Tahoe
