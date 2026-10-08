import pytest
import requests

from src.pogoda import pogoda as modul
from src.pogoda.pogoda import (
    BladPogody,
    formatuj,
    main,
    opis_pogody,
    pobierz_pogode,
    znajdz_miejscowosc,
)

WARSZAWA = {
    "results": [
        {
            "id": 756135,
            "name": "Warszawa",
            "latitude": 52.22977,
            "longitude": 21.01178,
            "country": "Polska",
            "country_code": "PL",
        }
    ]
}

POGODA = {
    "current": {
        "time": "2026-10-08T16:45",
        "interval": 900,
        "temperature_2m": 12.34,
        "apparent_temperature": 10.1,
        "relative_humidity_2m": 78,
        "wind_speed_10m": 14.4,
        "weather_code": 3,
    }
}


class FalszywaOdpowiedz:
    """Udaje odpowiedź z biblioteki requests, bez łączenia się z internetem."""

    def __init__(self, dane, blad_http=False):
        self._dane = dane
        self._blad_http = blad_http

    def raise_for_status(self):
        if self._blad_http:
            raise requests.HTTPError("500 Server Error")

    def json(self):
        if isinstance(self._dane, Exception):
            raise self._dane
        return self._dane


@pytest.fixture
def falszywe_api(monkeypatch):
    """Podmienia requests.get; zapamiętuje zapytania, żeby można je sprawdzić."""
    odpowiedzi = {
        modul.GEOCODING_URL: FalszywaOdpowiedz(WARSZAWA),
        modul.FORECAST_URL: FalszywaOdpowiedz(POGODA),
    }
    zapytania = []

    def falszywe_get(url, params=None, timeout=None):
        zapytania.append({"url": url, "params": params, "timeout": timeout})
        return odpowiedzi[url]

    monkeypatch.setattr(modul.requests, "get", falszywe_get)
    return odpowiedzi, zapytania


# --- opis_pogody ----------------------------------------------------------

def test_opis_pogody_znany_kod():
    assert opis_pogody(0) == "bezchmurnie"
    assert opis_pogody(95) == "burza"


def test_opis_pogody_nieznany_kod():
    assert "nieznany" in opis_pogody(1234)


# --- znajdz_miejscowosc ---------------------------------------------------

def test_znajdz_miejscowosc(falszywe_api):
    miejsce = znajdz_miejscowosc("Warszawa")
    assert miejsce == {
        "nazwa": "Warszawa",
        "kraj": "Polska",
        "szerokosc": 52.22977,
        "dlugosc": 21.01178,
    }


def test_znajdz_miejscowosc_wysyla_nazwe_i_limit_czasu(falszywe_api):
    _, zapytania = falszywe_api
    znajdz_miejscowosc("  Nowy Sącz ")
    assert zapytania[0]["params"]["name"] == "Nowy Sącz"
    assert zapytania[0]["timeout"] == modul.TIMEOUT


def test_znajdz_miejscowosc_brak_wynikow(falszywe_api):
    odpowiedzi, _ = falszywe_api
    # Tak API odpowiada, gdy nic nie znajdzie: brak klucza "results".
    odpowiedzi[modul.GEOCODING_URL] = FalszywaOdpowiedz({"generationtime_ms": 0.3})
    with pytest.raises(BladPogody, match="Nie znaleziono"):
        znajdz_miejscowosc("Xyzxyz")


@pytest.mark.parametrize("nazwa", ["", "   "])
def test_znajdz_miejscowosc_pusta_nazwa(nazwa, falszywe_api):
    _, zapytania = falszywe_api
    with pytest.raises(BladPogody):
        znajdz_miejscowosc(nazwa)
    assert zapytania == []  # nie ma sensu pytać serwera o pustą nazwę


def test_znajdz_miejscowosc_niepelna_odpowiedz(falszywe_api):
    odpowiedzi, _ = falszywe_api
    odpowiedzi[modul.GEOCODING_URL] = FalszywaOdpowiedz({"results": [{"name": "X"}]})
    with pytest.raises(BladPogody, match="niepełne"):
        znajdz_miejscowosc("X")


# --- pobierz_pogode -------------------------------------------------------

def test_pobierz_pogode(falszywe_api):
    pogoda = pobierz_pogode(52.2, 21.0)
    assert pogoda == {
        "temperatura": 12.34,
        "odczuwalna": 10.1,
        "wilgotnosc": 78,
        "wiatr": 14.4,
        "kod": 3,
    }


def test_pobierz_pogode_wysyla_wspolrzedne(falszywe_api):
    _, zapytania = falszywe_api
    pobierz_pogode(52.2, 21.0)
    params = zapytania[0]["params"]
    assert params["latitude"] == 52.2
    assert params["longitude"] == 21.0
    assert "temperature_2m" in params["current"]


@pytest.mark.parametrize("dane", [{}, {"current": {}}, {"current": {"temperature_2m": 1}}])
def test_pobierz_pogode_zle_dane(dane, falszywe_api):
    odpowiedzi, _ = falszywe_api
    odpowiedzi[modul.FORECAST_URL] = FalszywaOdpowiedz(dane)
    with pytest.raises(BladPogody):
        pobierz_pogode(52.2, 21.0)


# --- błędy sieci ----------------------------------------------------------

@pytest.mark.parametrize(
    "wyjatek, fragment",
    [
        (requests.Timeout(), "na czas"),
        (requests.ConnectionError(), "Brak połączenia"),
    ],
)
def test_bledy_sieci(monkeypatch, wyjatek, fragment):
    def get_z_bledem(*args, **kwargs):
        raise wyjatek

    monkeypatch.setattr(modul.requests, "get", get_z_bledem)
    with pytest.raises(BladPogody, match=fragment):
        znajdz_miejscowosc("Warszawa")


def test_blad_http(falszywe_api):
    odpowiedzi, _ = falszywe_api
    odpowiedzi[modul.GEOCODING_URL] = FalszywaOdpowiedz({}, blad_http=True)
    with pytest.raises(BladPogody, match="zwrócił błąd"):
        znajdz_miejscowosc("Warszawa")


def test_nieczytelny_json(falszywe_api):
    odpowiedzi, _ = falszywe_api
    odpowiedzi[modul.GEOCODING_URL] = FalszywaOdpowiedz(ValueError("zły json"))
    with pytest.raises(BladPogody, match="nieczytelną"):
        znajdz_miejscowosc("Warszawa")


# --- formatowanie i main --------------------------------------------------

def test_formatuj():
    miejsce = {"nazwa": "Warszawa", "kraj": "Polska", "szerokosc": 0, "dlugosc": 0}
    pogoda = {"temperatura": 12.34, "odczuwalna": 10.1, "wilgotnosc": 78, "wiatr": 14.4, "kod": 3}
    tekst = formatuj(miejsce, pogoda)
    assert "Warszawa, Polska" in tekst
    assert "Pochmurno" in tekst
    assert "12.3 °C" in tekst
    assert "78%" in tekst
    assert "14.4 km/h" in tekst
    assert "Open-Meteo.com" in tekst


def test_formatuj_bez_kraju():
    miejsce = {"nazwa": "Gdzieś", "kraj": "", "szerokosc": 0, "dlugosc": 0}
    pogoda = {"temperatura": 0, "odczuwalna": 0, "wilgotnosc": 0, "wiatr": 0, "kod": 0}
    assert "Pogoda: Gdzieś\n" in formatuj(miejsce, pogoda)


def test_main_caly_przebieg(falszywe_api, capsys):
    assert main(["Warszawa"]) == 0
    wyjscie = capsys.readouterr().out
    assert "Warszawa, Polska" in wyjscie
    assert "Pochmurno" in wyjscie


def test_main_nazwa_z_kilku_slow(falszywe_api):
    _, zapytania = falszywe_api
    assert main(["Nowy", "Sącz"]) == 0
    assert zapytania[0]["params"]["name"] == "Nowy Sącz"


def test_main_blad_zwraca_kod_1(falszywe_api, capsys):
    odpowiedzi, _ = falszywe_api
    odpowiedzi[modul.GEOCODING_URL] = FalszywaOdpowiedz({})
    assert main(["Xyzxyz"]) == 1
    assert "Błąd" in capsys.readouterr().err
