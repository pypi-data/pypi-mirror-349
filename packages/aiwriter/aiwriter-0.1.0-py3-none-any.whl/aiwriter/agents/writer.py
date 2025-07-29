import instructor
from pydantic import BaseModel
from aiwriter.env import MODEL

class Essay(BaseModel):
    title: str
    content: str

    def __str__(self):
        return f"Title: {self.title}\n\nContent:\n{self.content}"


def write_essay(prompt: str):
    """Pass prompt to LLM and return the response."""
    from typing import cast

    llm = instructor.from_provider(MODEL)
    response = cast(Essay, llm.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        response_model=Essay,
    ))
    return response

def cli():
    """Command line interface for the essay writer."""
    import sys
    import os
    from aiwriter.env import CONTEXT_DIR, CONTEXT_FULL_FILE, ESSAY_FILE
    from context_builder import build_context

    if len(sys.argv) < 2:
        print("Usage: python writer.py <prompt>")
        sys.exit(1)

    prompt = sys.argv[1]
    try:
        context_file = open(os.path.join(CONTEXT_DIR, CONTEXT_FULL_FILE), "r")
        print("\n\nContext file already exists, reading it...\n\n")
        context = context_file.read()
    except FileNotFoundError:
        context = build_context(prompt)
    
    try:
        response_file = open(os.path.join(CONTEXT_DIR, ESSAY_FILE), "r")
        print("\n\nResponse file already exists, reading it...\n\n")
        essay = response_file.read()
        print(essay)
        return
    except FileNotFoundError:
        essay = write_essay(context)
        open(ESSAY_FILE, "w").write(str(essay))
        print(essay)

if __name__ == "__main__":
    cli()