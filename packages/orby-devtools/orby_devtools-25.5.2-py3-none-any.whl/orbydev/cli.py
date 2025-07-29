import click
from .project import Projects
from .templates import Templates
from textwrap import shorten

def _format_path(path, max_length=50):
    return shorten(path, width=max_length, placeholder="...")


class Colors:
    PROJECT = "cyan"
    PATH = "yellow"
    TEMPLATE = "green"
    ERROR = "red"
    WARNING = "magenta"


@click.group()
def main():
    """Orby DevTools CLI."""
    pass


@main.command()
@click.argument("name", default="Orby app")
@click.argument("path", default="")
@click.option("--template", default="default", help="Project template.")
def new(name, path, template):
    """Create a new Orby project."""
    status, exception = Projects.new(name, path, template)
    if status:
        click.echo(click.style(f"Project '{name}' created!", "green"))
    else:
        click.echo(f"Error when creating project: {click.style(str(exception), 'red')}", err=True)


@main.command()
@click.argument("path")
@click.argument("save_at", default="")
def build(path, save_at):
    """Build a ready Orby project."""
    status, exception = Projects.build(path, save_at)
    if status:
        click.echo(click.style(f"Project builded!", "green"))
    else:
        click.echo(f"Error when building project: {click.style(str(exception), 'red')}", err=True)


@main.command()
def projects():
    """List of all projects."""
    projects_list, exception = Projects.projects_list()

    if exception is not None:
        click.echo(f"Error when getting projects list: {click.style(str(exception), 'red')}", err=True)
    
    if not projects_list:
        click.echo(click.style("You have no projects.", "blue"))
        return
    
    header = f"{'Project':<20} │ {'Path':<50} │ {'Template':<10}"
    click.echo(click.style("Projects list", bold=True))
    click.echo("=" * 85)
    click.echo(click.style(header, underline=True))
    click.echo("-" * 85)
    
    for name, data in sorted(projects_list.items()):
        click.echo(
            f"{click.style(name, fg=Colors.PROJECT):<20} │ "
            f"{click.style(_format_path(data['path']), fg=Colors.PATH):<50} │ "
            f"{click.style(data['template'], fg=Colors.TEMPLATE):<10}"
        )
    
    click.echo("=" * 85)
    click.echo(f"Projects: {click.style(str(len(projects_list)), fg='green', bold=True)}")


@main.command()
@click.argument("name")
@click.argument("rmdir", default="f")
def rmproject(name: str, rmdir: str):
    """Delete a project."""
    rmdir = rmdir.lower() == "t"

    status, exception = Projects.remove(name, rmdir)
    if status:
        click.echo(click.style(f"Project deleted!", "green"))
    else:
        click.echo(f"Error when deleting project: {click.style(str(exception), 'red')}", err=True)


@main.command()
def templates():
    """List of all templates."""
    templates_list, exception = Templates.templates_list()

    if exception is not None:
        click.echo(f"Error when getting templates list: {click.style(str(exception), 'red')}", err=True)
    
    if not templates_list:
        click.echo(click.style("You have no templates.", "blue"))
        return
    
    header = f"{'Template':<20} │ {'Description':<60}"
    click.echo(click.style("Templates list", bold=True))
    click.echo("=" * 85)
    click.echo(click.style(header, underline=True))
    click.echo("-" * 85)
    
    for name, data in sorted(templates_list.items()):
        click.echo(
            f"{click.style(name, fg=Colors.PROJECT):<20} │ "
            f"{click.style(data, fg=Colors.PATH):<60}"
        )
    
    click.echo("=" * 85)
    click.echo(f"Templates: {click.style(str(len(templates_list)), fg='green', bold=True)}")


@main.command()
@click.argument("name")
@click.argument("path")
def savetemplate(name, path):
    """Saves the project as a template."""
    status, exception = Templates.savetemplate(name, path)
    if status:
        click.echo(click.style(f"Template '{name}' saved!", "green"))
    else:
        click.echo(f"Error when saving template: {click.style(str(exception), 'red')}", err=True)


@main.command()
@click.argument("name")
def rmtemplate(name: str):
    """Delete template."""
    status, exception = Templates.remove(name)
    if status:
        click.echo(click.style(f"Template deleted!", "green"))
    else:
        click.echo(f"Error when deleting template: {click.style(str(exception), 'red')}", err=True)


if __name__ == "__main__":
    main()