import os

CONTEXT_FILE = os.getenv("AIWRITER_CONTEXT_FILE", "context.txt")
CONTEXT_FULL_FILE = os.getenv("AIWRITER_CONTEXT_FULL_FILE", "full_context.txt")
CONTEXT_DIR = os.getenv("AIWRITER_CONTEXT_DIR", "context")

MODEL = os.getenv("AIWRITER_MODEL", "anthropic/claude-3-7-sonnet-latest")
ESSAY_FILE = os.getenv("AIWRITER_ESSAY_FILE", "essay.txt")

CRITERIA_FILE = os.getenv("AIWRITER_CRITERIA", "criteria.txt")
SCORES_FILE = os.getenv("AIWRITER_SCORES", "scores.txt")

DRAFTS_DIR = os.getenv("AIWRITER_DRAFTS_DIR", "drafts")