import click
from managment.commands import InitialDBCommand

@click.group()
def cli():
    pass


@cli.command()
def create_initial_db():
    command = InitialDBCommand()
    command.execute()

if __name__ == "__main__":
    cli()