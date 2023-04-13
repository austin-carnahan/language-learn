import sys
import csv
from app import create_app, db
from app.models.language import Language
from app.models.phrase import Phrase


def insert_phrases_from_tsv(filename):
    # Load the Flask app
    app = create_app()

    # Read the contents of the TSV file
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        header = next(reader)  # Skip the header row
        primary_index = header.index(header[0])
        secondary_index = header.index(header[1])
        rows = [(row[primary_index], row[secondary_index]) for row in reader]

    # Connect to the database and insert the phrases
    with app.app_context():
        # Create the languages if they do not exist in the database
        primary_lang = Language.query.filter_by(name=header[0].lower()).first()
        if not primary_lang:
            primary_lang = Language(name=header[0].lower())
            db.session.add(primary_lang)
        secondary_lang = Language.query.filter_by(name=header[1].lower()).first()
        if not secondary_lang:
            secondary_lang = Language(name=header[1].lower())
            db.session.add(secondary_lang)

        # Insert the phrases into the database
        for primary, secondary in rows:
            # Check if the phrase already exists in the database (case-insensitive)
            existing_phrase = Phrase.query.filter(
                db.func.lower(Phrase.primary) == primary.lower(),
                db.func.lower(Phrase.secondary) == secondary.lower(),
                Phrase.primary_language == primary_lang,
                Phrase.secondary_language == secondary_lang
            ).first()

            if existing_phrase:
                # Skip the phrase if it already exists in the database
                continue

            phrase = Phrase(
                primary_language=primary_lang,
                secondary_language=secondary_lang,
                primary=primary,
                secondary=secondary
            )
            db.session.add(phrase)

        db.session.commit()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python insert_phrases.py <filename>')
        sys.exit(1)

    filename = sys.argv[1]
    insert_phrases_from_tsv(filename)