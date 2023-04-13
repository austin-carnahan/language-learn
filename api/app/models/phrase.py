from app import db
from app.models.language import Language

class Phrase(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    primary_language_id = db.Column(db.Integer, db.ForeignKey('language.id'), nullable=False)
    secondary_language_id = db.Column(db.Integer, db.ForeignKey('language.id'), nullable=False)
    primary_language = db.relationship('Language', backref='primary_phrases', lazy=True)
    secondary_language = db.relationship('Language', backref='secondary_phrases', lazy=True)
    primary = db.Column(db.String(50), unique=True, nullable=False)
    secondary = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f'<Phrase {self.primary} {self.secondary}>'