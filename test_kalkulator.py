import pytest

from kalkulator import dodaj, formatuj, oblicz, odejmij, podziel, pomnoz


def test_dodaj():
    assert dodaj(2, 3) == 5


def test_odejmij():
    assert odejmij(5, 3) == 2


def test_pomnoz():
    assert pomnoz(4, 3) == 12


def test_podziel():
    assert podziel(10, 4) == 2.5


def test_dzielenie_przez_zero():
    with pytest.raises(ZeroDivisionError):
        podziel(1, 0)


@pytest.mark.parametrize(
    "wyrazenie, oczekiwany",
    [
        ("2 + 3", 5),
        ("10 - 4", 6),
        ("3 * 7", 21),
        ("9 / 2", 4.5),
        ("1,5 + 1,5", 3),
    ],
)
def test_oblicz(wyrazenie, oczekiwany):
    assert oblicz(wyrazenie) == oczekiwany


@pytest.mark.parametrize(
    "wyrazenie",
    ["", "2 +", "2 ^ 3", "a + b", "1 + 2 + 3"],
)
def test_oblicz_bledne_wyrazenie(wyrazenie):
    with pytest.raises(ValueError):
        oblicz(wyrazenie)


def test_oblicz_dzielenie_przez_zero():
    with pytest.raises(ZeroDivisionError):
        oblicz("5 / 0")


def test_formatuj():
    assert formatuj(5.0) == "5"
    assert formatuj(2.5) == "2.5"
