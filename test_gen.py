import sys
import ast
import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("HF_TOKEN")

client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    token=os.getenv("HF_TOKEN")
)


def is_function_empty(func_node):
    for node in func_node.body:
        if isinstance(node, ast.Pass):
            continue

        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant):
            continue

        # Found real logic like Return, Assign, Call, etc.
        return False

    return True


def validate_function(source_code):
    try:
        tree = ast.parse(source_code)

        # Collect all top-level function definitions
        functions = []
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                functions.append(node)

        # We only support testing a single function at a time
        if len(functions) != 1:
            return False, "Error: This tool only generates unit tests for a single function."

        func = functions[0]

        # No point generating tests for an empty function
        if is_function_empty(func):
            return False, "Error: The provided function is empty and does not require tests."

        return True, func

    except SyntaxError:
        return False, "Error: This tool only generates unit tests for functions."


def generate_tests(function_node):
    # Strip comments by unparsing the AST node back to clean source code
    func_source = ast.unparse(function_node)

    system_instruction = (
        "You are a specialized unit test generator tool. "
        "Your sole purpose is to output valid, runnable Python unit tests using the 'unittest' framework. "

        "STRICT: Output raw Python code only. "
        "STRICT: No markdown blocks (no ```python or ```). "
        "STRICT: No explanations, comments, headers, or any text outside of Python code. "
        "STRICT: Always place the original function definition BEFORE the test class, not after. "

        "STRICT: Always copy the original function exactly as given into the output file. "
        "STRICT: Include all necessary imports at the top — this means 'unittest' plus any module "
        "the function uses, such as 'math', 'json', 'datetime', 'os', 're', or any other dependency. "
        "If the function uses 'random', import 'random'. If it uses 'collections', import 'collections'. "
        "Never assume a module is already imported. "

        "STRICT: End the file with: if __name__ == '__main__': unittest.main() "

        "REQUIREMENT: Write descriptive test method names following the pattern: test_<scenario>. "
        "REQUIREMENT: Cover all branches — every if/else path, every exception, and boundary values. "
        "REQUIREMENT: Test normal inputs, edge cases (empty, None, zero, negative), and expected exceptions. "
        "REQUIREMENT: Each test method should test exactly one behavior. "
        "REQUIREMENT: Never hardcode expected values by guessing. "
        "Always derive expected values by manually tracing through the function logic step by step. "
    )

    messages = [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": f"Function to test:\n{func_source}"}
    ]

    try:
        response = client.chat_completion(
            messages=messages,
            max_tokens=1500,
            temperature=0.1
        )

        test_code = response.choices[0].message.content

        # Clean up any markdown the model accidentally added
        clean_code = test_code.replace("```python", "").replace("```", "").strip()
        return clean_code

    except Exception as e:
        return f"Hugging Face API Error: {str(e)}"


def get_source_code():
    print("\n--- AI Unit Test Generator ---")
    print("1. Provide a file path")
    print("2. Input source code manually")

    choice = input("\nSelect an option (1 or 2): ").strip()

    if choice == "1":
        file_path = input("Enter the path to your .py file: ").strip()
        try:
            with open(file_path, "r") as f:
                return f.read().strip()
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            sys.exit(1)

    elif choice == "2":
        print("\nInput your Python function below.")
        print("Press Ctrl+D (Mac/Linux) or Ctrl+Z then Enter (Windows) to finish:")
        return sys.stdin.read().strip()

    else:
        print("Invalid choice. Please run the script again and select 1 or 2.")
        sys.exit(1)


def main():
    source_code = ""

    # Check if input is being piped in (e.g. cat file.py | python app.py)
    if not sys.stdin.isatty():
        source_code = sys.stdin.read().strip()
    else:
        source_code = get_source_code()

    if not source_code:
        print("Error: No input provided.")
        sys.exit(1)

    is_valid, result = validate_function(source_code)

    if not is_valid:
        print(result)
        sys.exit(1)

    test_code = generate_tests(result)
    print(test_code)


if __name__ == "__main__":
    main()