import json

import pytest

from src.todo.todo import (
    dodaj,
    formatuj,
    main,
    oznacz_wykonane,
    usun,
    wczytaj,
    zapisz,
)


def test_dodaj():
    zadania = []
    dodaj(zadania, "kupić mleko")
    assert zadania == [{"tresc": "kupić mleko", "wykonane": False}]


def test_dodaj_obcina_spacje():
    zadania = []
    dodaj(zadania, "  nauka Pythona  ")
    assert zadania[0]["tresc"] == "nauka Pythona"


@pytest.mark.parametrize("tresc", ["", "   "])
def test_dodaj_pusta_tresc(tresc):
    with pytest.raises(ValueError):
        dodaj([], tresc)


def test_oznacz_wykonane():
    zadania = [{"tresc": "a", "wykonane": False}]
    oznacz_wykonane(zadania, 1)
    assert zadania[0]["wykonane"] is True


def test_usun():
    zadania = [{"tresc": "a", "wykonane": False}, {"tresc": "b", "wykonane": False}]
    usun(zadania, 1)
    assert [z["tresc"] for z in zadania] == ["b"]


@pytest.mark.parametrize("numer", [0, 2, -1])
def test_zly_numer(numer):
    zadania = [{"tresc": "a", "wykonane": False}]
    with pytest.raises(IndexError):
        oznacz_wykonane(zadania, numer)
    with pytest.raises(IndexError):
        usun(zadania, numer)


def test_zapis_i_odczyt(tmp_path):
    plik = tmp_path / "zadania.json"
    zadania = [{"tresc": "zażółć gęślą jaźń", "wykonane": True}]
    zapisz(zadania, plik)
    assert wczytaj(plik) == zadania


def test_polskie_znaki_nie_sa_escapowane(tmp_path):
    plik = tmp_path / "zadania.json"
    zapisz([{"tresc": "łódź", "wykonane": False}], plik)
    assert "łódź" in plik.read_text(encoding="utf-8")


def test_wczytaj_brak_pliku(tmp_path):
    assert wczytaj(tmp_path / "nie_ma.json") == []


def test_wczytaj_uszkodzony_plik(tmp_path):
    plik = tmp_path / "zadania.json"
    plik.write_text("{to nie jest json", encoding="utf-8")
    with pytest.raises(ValueError):
        wczytaj(plik)


def test_formatuj():
    zadania = [
        {"tresc": "a", "wykonane": False},
        {"tresc": "b", "wykonane": True},
    ]
    assert formatuj(zadania) == "1. [ ] a\n2. [x] b"


def test_formatuj_pusta_lista():
    assert formatuj([]) == "Brak zadań."


def test_cli_caly_przebieg(tmp_path, capsys):
    plik = str(tmp_path / "zadania.json")

    assert main(["--plik", plik, "add", "pierwsze"]) == 0
    assert main(["--plik", plik, "add", "drugie"]) == 0
    assert main(["--plik", plik, "done", "1"]) == 0
    assert main(["--plik", plik, "delete", "2"]) == 0
    capsys.readouterr()

    assert main(["--plik", plik, "list"]) == 0
    assert capsys.readouterr().out.strip() == "1. [x] pierwsze"

    zapisane = json.loads((tmp_path / "zadania.json").read_text(encoding="utf-8"))
    assert zapisane == [{"tresc": "pierwsze", "wykonane": True}]


def test_cli_zly_numer_zwraca_kod_bledu(tmp_path, capsys):
    plik = str(tmp_path / "zadania.json")
    assert main(["--plik", plik, "done", "5"]) == 1
    assert "Błąd" in capsys.readouterr().err
