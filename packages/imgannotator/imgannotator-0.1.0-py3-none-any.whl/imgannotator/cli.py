# src/imgannotator/cli.py
import typer
from .filters import apply_filter
from .metadata import embed_metadata

app = typer.Typer(help="Image Annotator CLI")

@app.command()
def annotate(
    folder: str = typer.Argument(..., help="Folder containing images"),
    filter: str = typer.Option("BLUR", "--filter", "-f", help="Pillow/OpenCV filter name"),
    label: str = typer.Option(None, "--label", "-l", help="Label to embed"),
):
    """
    Apply FILTER to all images in FOLDER and embed optional LABEL as EXIF.
    """
    apply_filter(folder, filter)  # turn0search7
    if label:
        embed_metadata(folder, label)  # turn0search1

if __name__ == "__main__":
    app()
