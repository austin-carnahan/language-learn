from app.utils.insert_phrases import insert_phrases_from_tsv
from app.models.language import Language
from app.models.phrase import Phrase

def test_insert_phrases_from_tsv(app, client):
    # Insert phrases from the test TSV file
    filename = 'data/english_spanish_phrases_01.tsv'
    insert_phrases_from_tsv(filename)

    # Verify that the phrases were inserted into the database
    with app.app_context():
        # Verify that the primary and secondary languages exist
        assert len(Language.query.all()) == 2
        assert Language.query.filter_by(name='english').first() is not None
        assert Language.query.filter_by(name='spanish').first() is not None

        # Verify that the phrases were inserted
        assert len(Phrase.query.all()) == 4
        assert Phrase.query.filter_by(primary='walk').first() is not None
        assert Phrase.query.filter_by(primary='run').first() is not None
        assert Phrase.query.filter_by(primary='swim').first() is not None
        assert Phrase.query.filter_by(primary='fly').first() is not None

        # Verify that the Spanish translations were inserted
        assert Phrase.query.filter_by(secondary='caminar').first() is not None
        assert Phrase.query.filter_by(secondary='correr').first() is not None
        assert Phrase.query.filter_by(secondary='nadar').first() is not None
        assert Phrase.query.filter_by(secondary='volar').first() is not None