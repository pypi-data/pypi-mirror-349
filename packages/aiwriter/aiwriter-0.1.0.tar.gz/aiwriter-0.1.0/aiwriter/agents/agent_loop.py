import os
from aiwriter.agents.context_builder import build_context
from aiwriter.agents.writer import write_essay
from aiwriter.agents.ranker import rank_essay
from aiwriter.env import DRAFTS_DIR

SCORE_THRESHOLD = 8

def iteration_prompt(essay, scores, threshold):
    return f"Given the following essay and scores, please improve all aspects of the essay at or below {threshold}. \n\nEssay:\n\n{essay}\n\nScores:\n\n{scores}"

def all_scores_greater_than_threshold(scores, threshold=SCORE_THRESHOLD):
    return all(float(v) > threshold for v in scores.__dict__.values() if isinstance(v, (int, float)))

def agent_loop(prompt: str, max_iters: int = 6):
    os.makedirs(DRAFTS_DIR, exist_ok=True)
    essay_text = None
    scores = None
    for i in range(1, max_iters + 1):
        if i == 1:
            context = build_context(prompt)
            essay = write_essay(context)
        else:
            essay = write_essay(iteration_prompt(essay_text, scores, SCORE_THRESHOLD))
        essay_text = essay
        draft_path = f"{DRAFTS_DIR}/draft_{i}.md"
        with open(draft_path, "w") as f:
            f.write(str(essay))

        scores = rank_essay(str(essay))
        score_path = f"{DRAFTS_DIR}/draft_score_{i}.md"
        with open(score_path, "w") as f:
            f.write(str(scores))

        print(f"Draft #{i}")
        print(f"Essay: {essay_text.title}")
        print(f"Scores:\n\n{scores}")

        if all_scores_greater_than_threshold(scores, threshold=SCORE_THRESHOLD):
            print(f"All scores above {SCORE_THRESHOLD} at iteration {i}. Exiting loop.")
            break

def cli():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python agent_loop.py <prompt>")
        return
    prompt = sys.argv[1]
    agent_loop(prompt)

if __name__ == "__main__":
    cli()