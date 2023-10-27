import genanki
import os
import base64
import json
import click
import requests
from collections import defaultdict

# Constants
NAME_FORMAT = "{FormattedName}"


def format_name(colleague):
    return colleague.get("name", "")


def fetch_image_as_base64(url):
    response = requests.get(url)
    image_data = base64.b64encode(response.content).decode("utf-8")
    return f"data:image/jpeg;base64,{image_data}"


def generate_single_deck(colleagues, output_filename):
    # Define the Anki model with two card types
    model_id = 2380120066
    model_name = "Colleague Flashcards"
    templates = [
        {
            "name": "Card 1: Name to Image",
            "qfmt": "{{Name}}<br><i>{{Title}}</i>",
            "afmt": '{{FrontSide}}<hr id="answer">{{Image}}',
        },
        {
            "name": "Card 2: Image to Name",
            "qfmt": "{{Image}}",
            "afmt": '{{FrontSide}}<hr id="answer">{{Name}}<br><i>{{Title}}</i>',
        },
    ]

    my_model = genanki.Model(
        model_id,
        model_name,
        fields=[{"name": "Name"}, {"name": "Image"}, {"name": "Title"}],
        templates=templates,
        css="""
            .card {
                font-family: Arial;
                font-size: 20px;
                text-align: center;
                color: black;
                background-color: white;
            }
            img {
                height: 300px;
                width: 300px;
            }
            i {
                color: darkblue;
                font-size: 16px;
            }
        """,
    )

    # Create the Anki deck
    deck_id = 1234567890  # Arbitrary deck ID
    deck_title = "Colleagues"
    my_deck = genanki.Deck(deck_id, deck_title)

    # Process the colleagues to generate notes for the Anki deck
    for colleague in colleagues:
        if "name" not in colleague or "image_url" not in colleague:
            print(f"Skipping colleague entry due to missing key: {colleague}")
            continue

        # Calculate the formatted name and add it to the colleague dictionary
        colleague["FormattedName"] = format_name(colleague)

        # Use the formatted name in the note
        formatted_name = NAME_FORMAT.format(**colleague)
        titles = (
            "<br>".join(colleague["titles"])
            if "titles" in colleague
            else colleague.get("title", "")
        )
        image = f'<img src="{fetch_image_as_base64(colleague["image_url"])}" />'

        my_note = genanki.Note(
            model=my_model,
            # build a GUID based on "anki deck generator colleague flashcards" and the colleague name
            guid="adgcf.{name}".format(**colleague),
            fields=[formatted_name, image, titles],
        )
        my_deck.add_note(my_note)

    # Generate the Anki package
    my_package = genanki.Package(my_deck)
    my_package.write_to_file(output_filename)

    click.secho(
        f"Anki package generated successfully at {output_filename}!", fg="green"
    )


@click.command()
@click.argument(
    "json_files",
    nargs=-1,
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
)
@click.option(
    "--output",
    default=None,
    type=click.Path(file_okay=True, dir_okay=False, writable=True),
    help="Path to save the generated Anki deck.",
)
def generate_anki_deck(json_files, output):
    # Check if input files are provided
    if not json_files:
        click.secho("Error: No input files provided.", fg="red")
        click.secho(
            "Use '--help' for information on how to use this tool.", fg="yellow"
        )
        return

    all_colleagues = []
    for json_file in json_files:
        with open(json_file, "r") as f:
            data = json.load(f)
            all_colleagues.extend(data)

    if output:
        output_filename = output
    else:
        output_filename = "colleagues.apkg"
    generate_single_deck(all_colleagues, output_filename)


if __name__ == "__main__":
    try:
        generate_anki_deck()
    except Exception as e:
        click.secho(f"An unexpected error occurred: {e}", fg="red")
