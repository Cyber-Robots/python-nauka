import pytest

from src.kalkulator.kalkulator import (
    dodaj,
    formatuj,
    main,
    oblicz,
    odejmij,
    pierwiastek,
    podziel,
    pomnoz,
    potega,
    wczytaj_historie,
    wyczysc_historie,
    zapisz_wpis,
)


# --- Działania podstawowe -------------------------------------------------

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


def test_potega():
    assert potega(2, 10) == 1024
    assert potega(2, -1) == 0.5


def test_potega_zero_do_ujemnej():
    with pytest.raises(ZeroDivisionError):
        potega(0, -1)


def test_potega_wynik_zespolony():
    with pytest.raises(ValueError):
        potega(-8, 0.5)


def test_pierwiastek():
    assert pierwiastek(16) == 4


def test_pierwiastek_z_ujemnej():
    with pytest.raises(ValueError):
        pierwiastek(-1)


# --- Wyrażenia i kolejność działań ----------------------------------------

@pytest.mark.parametrize(
    "wyrazenie, oczekiwany",
    [
        ("2 + 3", 5),
        ("10 - 4", 6),
        ("3 * 7", 21),
        ("9 / 2", 4.5),
        ("1,5 + 1,5", 3),
        ("1 + 2 + 3", 6),
        ("2 + 3 * 4", 14),
        ("(2 + 3) * 4", 20),
        ("10 - 2 - 3", 5),
        ("8 / 4 / 2", 1),
        ("2 ** 3", 8),
        ("2 ** 3 ** 2", 512),
        ("-2 ** 2", -4),
        ("2 ** -1", 0.5),
        ("2 * -3", -6),
        ("-(2 + 3)", -5),
        ("sqrt(16)", 4),
        ("sqrt(9) + 1", 4),
        ("sqrt(2 + 2) * 3", 6),
        ("2 * (3 + (4 - 1))", 12),
    ],
)
def test_oblicz(wyrazenie, oczekiwany):
    assert oblicz(wyrazenie) == oczekiwany


@pytest.mark.parametrize(
    "wyrazenie",
    [
        "",
        "   ",
        "2 +",
        "2 ^ 3",
        "a + b",
        "2 3",
        "(2 + 3",
        "2 + 3)",
        "sqrt 4",
        "sqrt(4",
        "foo(2)",
        "sqrt(-1)",
        "(-8) ** 0.5",
        "10 ** 1000",
        "(" * 5000,
    ],
)
def test_oblicz_bledne_wyrazenie(wyrazenie):
    with pytest.raises(ValueError):
        oblicz(wyrazenie)


@pytest.mark.parametrize("wyrazenie", ["5 / 0", "1 / (2 - 2)", "0 ** -1"])
def test_oblicz_dzielenie_przez_zero(wyrazenie):
    with pytest.raises(ZeroDivisionError):
        oblicz(wyrazenie)


def test_formatuj():
    assert formatuj(5.0) == "5"
    assert formatuj(-0.0) == "0"
    assert formatuj(2.5) == "2.5"


def test_bledy_zmiennoprzecinkowe_sa_zaokraglane():
    assert formatuj(oblicz("0.1 + 0.2")) == "0.3"


# --- Historia w pliku -----------------------------------------------------

def test_wczytaj_historie_brak_pliku(tmp_path):
    assert wczytaj_historie(tmp_path / "brak.txt") == []


def test_zapis_i_odczyt_historii(tmp_path):
    plik = tmp_path / "historia.txt"
    zapisz_wpis("2 + 3 = 5", plik)
    zapisz_wpis("9 / 2 = 4.5", plik)
    assert wczytaj_historie(plik) == ["2 + 3 = 5", "9 / 2 = 4.5"]


def test_wyczysc_historie(tmp_path):
    plik = tmp_path / "historia.txt"
    zapisz_wpis("2 + 3 = 5", plik)
    wyczysc_historie(plik)
    assert wczytaj_historie(plik) == []


# --- Pętla programu -------------------------------------------------------

def uruchom_main(monkeypatch, plik, wejscia):
    polecenia = iter(wejscia)
    monkeypatch.setattr("builtins.input", lambda _: next(polecenia))
    main(plik)


def test_main_zapisuje_historie(monkeypatch, capsys, tmp_path):
    plik = tmp_path / "historia.txt"
    uruchom_main(monkeypatch, plik, ["2 + 3 * 4", "historia", "q"])
    wyjscie = capsys.readouterr().out
    assert "14" in wyjscie
    assert "2 + 3 * 4 = 14" in wyjscie
    assert wczytaj_historie(plik) == ["2 + 3 * 4 = 14"]


def test_main_wczytuje_historie_przy_starcie(monkeypatch, capsys, tmp_path):
    plik = tmp_path / "historia.txt"
    zapisz_wpis("1 + 1 = 2", plik)
    uruchom_main(monkeypatch, plik, ["historia", "q"])
    assert "1 + 1 = 2" in capsys.readouterr().out


def test_main_wyswietla_bledy_bez_zapisu(monkeypatch, capsys, tmp_path):
    plik = tmp_path / "historia.txt"
    uruchom_main(monkeypatch, plik, ["5 / 0", "q"])
    assert "Błąd" in capsys.readouterr().out
    assert wczytaj_historie(plik) == []
