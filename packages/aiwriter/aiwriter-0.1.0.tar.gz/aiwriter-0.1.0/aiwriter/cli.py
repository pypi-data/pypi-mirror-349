import click


from aiwriter.agents.agent_loop import agent_loop
from aiwriter.agents.writer import write_essay
from aiwriter.agents.ranker import rank_essay
from aiwriter.agents.context_builder import build_context


@click.group()
def main():
    """CLI for the AI Writer."""
    pass


@main.command()
@click.argument("prompt")
def write(prompt):
    """Write an essay based on the given prompt."""
    essay = write_essay(prompt)
    click.echo(essay)


@main.command()
@click.argument("prompt")
def build(prompt):
    """Build context for the given prompt."""
    context = build_context(prompt)
    click.echo(context)


@main.command()
@click.argument("essay")
@click.argument("criteria", required=False)
def rank(essay, criteria):
    """Rank an essay based on the given criteria."""
    criteria = criteria.split(",") if criteria else None
    scores = rank_essay(essay, criteria)
    click.echo(scores)


DEFAULT_MAX_ITERS = 6


@main.command()
@click.argument("prompt")
@click.option(
    "--max-iters",
    default=DEFAULT_MAX_ITERS,
    help=f"Maximum number of iterations for the agent loop. Default is {DEFAULT_MAX_ITERS}.",
)
def agent(prompt, max_iters):
    """Run the agent loop for the given prompt."""
    agent_loop(prompt, max_iters)
    click.echo(f"Agent loop completed for prompt: {prompt}")


if __name__ == "__main__":
    main()
