# AI PR Review Tool

A command-line tool that reviews Git diffs using a locally running Ollama model.

## Features

- Reviews local Git diffs
- Runs through Ollama
- Uses a local model instead of an external API
- Prints review feedback in the terminal
- Installs as a `git-review` command

## Requirements

- Python 3.8+
- Git
- Ollama
- An Ollama model such as `qwen2.5-coder:7b`

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Luke-Melendy/ai-pr-review.git
cd ai-pr-review
```

2. Install Ollama

Follow install instructions from [Ollama](https://ollama.com/)

3. Pull the model:

```bash
ollama pull qwen2.5-coder:7b
```

4. Install project locally

```bash
pip install -e
```

## Usage

Simply run the tool from inside a git repo:
```bash
git-review
```

## Notes

 - Larger diffs may take longer time to process
 - Issues may get repeated in output since this is a prototype
 - This is meant to assist with code review and not replace it entirely

 ## Author
 Luke Melendy - [Connect](www.linkedin.com/in/)
