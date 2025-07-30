from normalize_tools.countries import search_country_name, unique_languages, lookup_index
import pytest


def test_el_salvador():
    assert search_country_name("El Salvador") == "El Salvador"

def test_particulas():
    assert search_country_name("De La Administracion") == ""


@pytest.mark.parametrize("input_str,expected", [
    # Español - exactos
    ("España", "España"),
    ("México", "México"),
    ("Estados Unidos", "Estados Unidos"),
    ("República Dominicana", "República Dominicana"),
    ("Reino Unido", "Reino Unido"),
    ("Guinea Ecuatorial", "Guinea Ecuatorial"),
    
    # Español - normalizados
    ("españa", "España"),
    ("MEXICO", "México"),
    ("republica dominicana", "República Dominicana"),
    ("reino unido", "Reino Unido"),
    
    # Inglés - comunes
    ("Spain", "España"),
    ("Mexico", "México"),
    ("United States", "Estados Unidos"),
    ("Dominican Republic", "República Dominicana"),
    ("United Kingdom", "Reino Unido"),
    ("Equatorial Guinea", "Guinea Ecuatorial"),

    # Mixtos - variantes válidas
    ("colombia", "Colombia"),
    ("COLOMBIA", "Colombia"),
    ("Venezuela", "Venezuela, República Bolivariana de"),
    ("venezuela", "Venezuela, República Bolivariana de"),
    ("Republic of Ireland", "Irlanda"),

    # Falsos positivos y negativos esperados
    ("", ""),
    ("   ", ""),
    ("LATAM", ""),
    ("Financiero", ""),
    ("Tecnológico", ""),
    ("Comercial", ""),
    ("Transylvania", ""),
    ("Moon", ""),
    ("Gotham", "")
])
def test_search_country_name(input_str, expected):
    country_name = search_country_name(input_str, lookup_index)
    assert country_name == expected
