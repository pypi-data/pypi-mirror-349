#!/usr/bin/env python3

import subprocess
import sys
import os


def get_git_diff(path="."):
    """Get the output of git diff in the given path."""
    try:
        diff = subprocess.check_output(['git', '-C', path, 'diff']).decode('utf-8')
        if not diff.strip():
            print("No changes detected (git diff is empty). Please stage or modify files.")
            sys.exit(1)
        return diff
    except subprocess.CalledProcessError:
        print("Error: Make sure this path is a git repository with changes.")
        sys.exit(1)


def query_ollama(prompt, model="llama2"):
    """Send the prompt to Ollama and return the result."""
    try:
        result = subprocess.check_output(['ollama', 'run', model], input=prompt.encode())
        return result.decode('utf-8').strip()
    except subprocess.CalledProcessError as e:
        print("Error calling Ollama:", e)
        sys.exit(1)


def generate_pr_text(diff_text):
    """Generate PR title and description using the provided git diff."""
    prompt = (
        "Summarize the following git diff into a concise Pull Request title and detailed description:\n\n"
        f"{diff_text}\n\n"
        "PR title:\nPR description:"
    )
    return query_ollama(prompt)


def main():
    """Main entry point for the CLI."""
    path = os.getcwd()
    diff = get_git_diff(path)

    print("\nGenerating PR title and description using Ollama AI...\n")
    pr_text = generate_pr_text(diff)

    print("\n=== Generated Pull Request ===\n")
    print(pr_text)


if __name__ == '__main__':
    main()