import typer
import httpx
from rich import print

app = typer.Typer()
API_BASE = "http://localhost:8000"

@app.command(help="Greetings")
def hello(name: str = typer.Option(..., help="Name")):
    print(f"Hello, {name}!")

@app.command(help="Create a note")
def create(title: str = typer.Option(..., prompt=True, help="Title of the note"),
    content: str = typer.Option("", prompt=True, help="Content of the note")):
    response = httpx.post(f"{API_BASE}/create", json={"title": title, "content": content})
    print(response.json())

@app.command(help="List all notes")
def list():
    response = httpx.get(f"{API_BASE}/list")
    print(response.json())

@app.command(help="Get a note by its ID")
def get_one_note(id: int = typer.Option(..., prompt=True, help="ID of the note")):
    try:
        response = httpx.get(f"{API_BASE}/get/{id}")
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        print(f"[red] HTTP error {e.response.status_code}: {e.response.text}[/red]")
        raise typer.Exit(code=1)
    except httpx.RequestError as e:
        print(f"[red] Network error: {e}[/red]")
        raise typer.Exit(code=1)

    print(response.json())

@app.command(help="Delete a note")
def delete(id: int = typer.Option(..., prompt=True, help="ID of the note")):
    confirm = typer.confirm(f"Are you sure you want to delete the note with id {id}")
    if not confirm:
        print("[yellow]Deletion cancelled [/yellow]")
        raise typer.Exit()
    try:
        response = httpx.delete(f"{API_BASE}/delete/{id}")
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        print(f"[red] HTTP error {e.response.status_code}: {e.response.text}[/red]")
        raise typer.Exit(code=1)
    except httpx.RequestError as e:
        print(f"[red] Network error: {e}[/red]")
        raise typer.Exit(code=1)

    print("[green]Note deleted successfully[/green]")

if __name__ == '__main__':
    app()