"""Bot pogodowy w terminalu.

Pobiera aktualną pogodę z darmowego API Open-Meteo (nie wymaga klucza).

Użycie:
    python3 src/pogoda/pogoda.py Warszawa
    python3 src/pogoda/pogoda.py "Nowy Sącz"
"""

import argparse
import sys

import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
TIMEOUT = 10  # sekundy; bez limitu program mógłby wisieć w nieskończoność

# Kody pogody WMO używane przez Open-Meteo.
OPISY_POGODY = {
    0: "bezchmurnie",
    1: "głównie bezchmurnie",
    2: "częściowe zachmurzenie",
    3: "pochmurno",
    45: "mgła",
    48: "mgła osadzająca szron",
    51: "lekka mżawka",
    53: "mżawka",
    55: "gęsta mżawka",
    56: "lekka marznąca mżawka",
    57: "gęsta marznąca mżawka",
    61: "słaby deszcz",
    63: "deszcz",
    65: "silny deszcz",
    66: "lekki marznący deszcz",
    67: "silny marznący deszcz",
    71: "słaby śnieg",
    73: "śnieg",
    75: "silny śnieg",
    77: "ziarna śniegu",
    80: "słabe przelotne opady deszczu",
    81: "przelotne opady deszczu",
    82: "gwałtowne opady deszczu",
    85: "słabe przelotne opady śniegu",
    86: "silne przelotne opady śniegu",
    95: "burza",
    96: "burza z lekkim gradem",
    97: "silna burza",
    99: "burza z silnym gradem",
}


class BladPogody(Exception):
    """Błąd, który można pokazać użytkownikowi (sieć, brak miasta, zła odpowiedź)."""


def _zapytaj(url, parametry):
    """Wysyła zapytanie GET i zwraca odpowiedź jako słownik."""
    try:
        odpowiedz = requests.get(url, params=parametry, timeout=TIMEOUT)
        odpowiedz.raise_for_status()
        return odpowiedz.json()
    except requests.Timeout:
        raise BladPogody("Serwer pogody nie odpowiedział na czas.") from None
    except requests.HTTPError as blad:
        raise BladPogody(f"Serwer pogody zwrócił błąd: {blad}") from None
    except requests.RequestException:
        raise BladPogody("Brak połączenia z serwerem pogody.") from None
    except ValueError:
        raise BladPogody("Serwer pogody zwrócił nieczytelną odpowiedź.") from None


def znajdz_miejscowosc(nazwa):
    """Zamienia nazwę miejscowości na współrzędne geograficzne."""
    nazwa = nazwa.strip()
    if not nazwa:
        raise BladPogody("Podaj nazwę miejscowości.")

    dane = _zapytaj(
        GEOCODING_URL,
        {"name": nazwa, "count": 1, "language": "pl", "format": "json"},
    )
    # Gdy nic nie znaleziono, API w ogóle nie zwraca klucza "results".
    wyniki = dane.get("results") if isinstance(dane, dict) else None
    if not wyniki:
        raise BladPogody(f"Nie znaleziono miejscowości: {nazwa}")

    wynik = wyniki[0]
    try:
        return {
            "nazwa": wynik["name"],
            "kraj": wynik.get("country", ""),
            "szerokosc": wynik["latitude"],
            "dlugosc": wynik["longitude"],
        }
    except KeyError:
        raise BladPogody("Serwer pogody zwrócił niepełne dane o miejscowości.") from None


def pobierz_pogode(szerokosc, dlugosc):
    """Pobiera aktualną pogodę dla podanych współrzędnych."""
    dane = _zapytaj(
        FORECAST_URL,
        {
            "latitude": szerokosc,
            "longitude": dlugosc,
            "current": "temperature_2m,apparent_temperature,relative_humidity_2m,"
            "wind_speed_10m,weather_code",
            "timezone": "auto",
        },
    )
    biezaca = dane.get("current") if isinstance(dane, dict) else None
    if not biezaca:
        raise BladPogody("Serwer pogody nie zwrócił aktualnych danych.")

    try:
        return {
            "temperatura": biezaca["temperature_2m"],
            "odczuwalna": biezaca["apparent_temperature"],
            "wilgotnosc": biezaca["relative_humidity_2m"],
            "wiatr": biezaca["wind_speed_10m"],
            "kod": biezaca["weather_code"],
        }
    except KeyError:
        raise BladPogody("Serwer pogody zwrócił niepełne dane pogodowe.") from None


def opis_pogody(kod):
    """Zamienia kod WMO na opis po polsku."""
    return OPISY_POGODY.get(kod, f"nieznany kod pogody ({kod})")


def formatuj(miejsce, pogoda):
    """Składa gotowy tekst do wyświetlenia."""
    etykieta = miejsce["nazwa"]
    if miejsce["kraj"]:
        etykieta += f", {miejsce['kraj']}"

    return (
        f"Pogoda: {etykieta}\n"
        f"{opis_pogody(pogoda['kod']).capitalize()}\n"
        f"Temperatura: {pogoda['temperatura']:.1f} °C "
        f"(odczuwalna {pogoda['odczuwalna']:.1f} °C)\n"
        f"Wilgotność: {pogoda['wilgotnosc']:.0f}%\n"
        f"Wiatr: {pogoda['wiatr']:.1f} km/h\n"
        "Dane: Open-Meteo.com"
    )


def main(argv=None):
    parser = argparse.ArgumentParser(description="Aktualna pogoda dla miejscowości.")
    parser.add_argument("miasto", nargs="+", help='nazwa miejscowości, np. Warszawa lub "Nowy Sącz"')
    args = parser.parse_args(argv)

    try:
        miejsce = znajdz_miejscowosc(" ".join(args.miasto))
        pogoda = pobierz_pogode(miejsce["szerokosc"], miejsce["dlugosc"])
    except BladPogody as blad:
        print(f"Błąd: {blad}", file=sys.stderr)
        return 1

    print(formatuj(miejsce, pogoda))
    return 0


if __name__ == "__main__":
    sys.exit(main())
