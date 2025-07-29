from typing import Optional
import instructor
from pydantic import create_model, Field, ConfigDict, BaseModel
from aiwriter.env import MODEL


class BaseScore(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)


def rank_essay(essay: str, criteria: Optional[list[str]] = None):
    """This function takes an essay and returns a score based on the criteria."""
    from typing import cast, Any

    if criteria is None:
        criteria = [
            "clarity",
            "conciseness",
            "relevance",
            "engagement",
            "accuracy",
        ]  # default criteria
        try:
            from aiwriter.env import CRITERIA_FILE
            import os

            if os.path.exists(CRITERIA_FILE):
                with open(CRITERIA_FILE) as cf:
                    criteria = [c.strip() for c in cf.read().split(",") if c.strip()]
        except Exception:
            pass

    RANKER_PROMPT = (
        "Score the essay based on the following criteria: "
        + ", ".join(criteria)
        + ".\n\nEach criteria should be scored from 0 to 10.\n\nEssay:\n\n"
    )

    criteria_dict = {key: Field(ge=0, le=10) for key in criteria}
    ScoreModel = create_model("ScoreModel", __base__=BaseScore, **criteria_dict)
    llm = instructor.from_provider(MODEL)
    response = cast(
        Any,
        llm.chat.completions.create(
            messages=[{"role": "user", "content": RANKER_PROMPT + essay}],
            response_model=ScoreModel,
        ),
    )

    return response


def cli():
    """Command line interface for the essay ranker."""
    from aiwriter.env import SCORES_FILE, CRITERIA_FILE, ESSAY_FILE

    try:
        criteria = open(CRITERIA_FILE, "r").read()
    except FileNotFoundError:
        criteria = "clarity,conciseness,relevance,engagement,accuracy"
    try:
        essay = open(ESSAY_FILE, "r").read()
    except FileNotFoundError:
        print(f"No essay found in {ESSAY_FILE}. Please provide an essay to rank.")
        return

    criteria = criteria.split(",")
    scores = rank_essay(essay, criteria)
    print(f"Scores:\n\n{scores}")

    with open(SCORES_FILE, "w") as scores_file:
        scores_file.write(str(scores))


if __name__ == "__main__":
    cli()
