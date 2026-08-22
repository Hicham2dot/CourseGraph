"""Tests unitaires — à implémenter au fil des semaines."""


def test_import_config() -> None:
    """Vérifie que la config s'importe et retourne un objet Settings."""
    from coursegraph.config import get_settings

    settings = get_settings()
    assert settings.api_port == 8000
    assert settings.qdrant_collection == "coursegraph"


def test_import_api() -> None:
    """Vérifie que l'app FastAPI s'instancie sans erreur."""
    from coursegraph.api.main import app

    assert app.title == "CourseGraph API"
