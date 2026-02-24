# 🧪 AI Unit Test Generator

A command-line tool that automatically generates Python unit tests for your functions using a Large Language Model (LLM) via the Hugging Face Inference API.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [How to Run](#how-to-run)
- [Usage Examples](#usage-examples)
- [Limitations](#limitations)

---

## Overview

This tool takes a single Python function as input, validates it, and sends it to an LLM (`mistralai/Mistral-7B-Instruct-v0.2`) to generate a complete, runnable `unittest` test file — including imports, edge cases, exception handling, and branch coverage.

---

## Features

- ✅ Accepts input via **file path**, **manual paste**, or **stdin pipe**
- ✅ Validates that the input contains **exactly one non-empty function**
- ✅ Automatically strips comments before sending to the AI
- ✅ Generates tests covering **all branches, edge cases, and exceptions**
- ✅ Outputs a **clean, runnable** Python test file with no markdown

---

## Prerequisites

Before running this tool, make sure you have the following installed:

- **Python 3.8+**
- A **Hugging Face account** with an API token → [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

---

## Installation

**1. Clone the repository:**

```bash
git clone https://github.com/your-username/ai-unit-test-generator.git
cd ai-unit-test-generator
```

**2. Install dependencies:**

```bash
pip install huggingface-hub python-dotenv
```

---

## Configuration

**1. Create a `.env` file** in the root of the project:

```bash
touch .env
```

**2. Add your Hugging Face token to the `.env` file:**

```env
HF_TOKEN=your_huggingface_token_here
```

> ⚠️ Never commit your `.env` file to GitHub. Make sure `.env` is listed in your `.gitignore`.

**3. Add `.env` to `.gitignore`:**

```bash
echo ".env" >> .gitignore
```

---

## How to Run

The tool supports three input methods:

### Option 1: Provide a file path (recommended)

```bash
python app.py
```

Then select option `1` and enter the path to your `.py` file:

```
--- AI Unit Test Generator ---
1. Provide a file path
2. Input source code manually

Select an option (1 or 2): 1
Enter the path to your .py file: my_function.py
```

### Option 2: Paste source code manually

```bash
python app.py
```

Then select option `2` and paste your function, then press:
- `Ctrl+D` on **Mac/Linux**
- `Ctrl+Z` then `Enter` on **Windows**

### Option 3: Pipe input via stdin

```bash
cat my_function.py | python app.py
```

### Saving the output to a file

```bash
cat my_function.py | python app.py > test_my_function.py
```

Then run the generated tests:

```bash
python test_my_function.py
```

---

## Usage Examples

**Example input (`my_function.py`):**

```python
import math

def calculate_circle_area(radius):
    if radius < 0:
        raise ValueError("Radius cannot be negative.")
    if radius == 0:
        return 0.0
    return math.pi * (radius ** 2)
```

**Run the tool:**

```bash
cat my_function.py | python app.py > test_circle.py
python test_circle.py
```

**Expected output:**

```
......
----------------------------------------------------------------------
Ran 6 tests in 0.001s

OK
```

---

## Limitations

- Only supports **one function per input** — multiple functions will be rejected
- Empty functions (only `pass`, `...`, or docstrings) are rejected
- Generated expected values for **math-heavy functions** should be manually verified, as LLMs can occasionally produce incorrect calculations
- Requires an active internet connection to reach the Hugging Face Inference API
- Free Hugging Face accounts may experience **rate limiting** on heavy usage
