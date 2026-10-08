# Bot pogodowy

Program w terminalu, który pokazuje aktualną pogodę dla wybranej miejscowości. Dane pochodzą z darmowego API [Open-Meteo](https://open-meteo.com/), które nie wymaga klucza.

## Użycie

```
python3 src/pogoda/pogoda.py Warszawa
python3 src/pogoda/pogoda.py "Nowy Sącz"
```

Przykładowy wynik:

```
Pogoda: Warszawa, Polska
Pochmurno
Temperatura: 12.3 °C (odczuwalna 10.1 °C)
Wilgotność: 78%
Wiatr: 14.4 km/h
Dane: Open-Meteo.com
```

## Instalacja

```
git clone https://github.com/Cyber-Robots/python-nauka.git
cd python-nauka
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Biblioteka `requests` musi być na liście w `requirements.txt`.

## Jak to działa

1. Nazwa miejscowości trafia do **API geokodowania**, które zwraca współrzędne geograficzne.
2. Współrzędne trafiają do **API prognozy**, które zwraca aktualną pogodę jako kod WMO (np. `3`) oraz liczby.
3. Kod zamieniany jest na opis po polsku, a całość formatowana do czytelnego tekstu.

Każde zapytanie ma limit czasu 10 sekund, a błędy (brak internetu, nieznane miasto, błąd serwera) kończą się czytelnym komunikatem zamiast śladu stosu.

## Testy

```
python -m pytest
```

Testy **nie łączą się z internetem**. Funkcja `requests.get` jest w nich podmieniana na atrapę, która zwraca przygotowane odpowiedzi. Dzięki temu są szybkie, działają offline i przechodzą tak samo w GitHub Actions.

## Dane i licencja

Dane pogodowe: [Open-Meteo.com](https://open-meteo.com/), licencja CC BY 4.0. Darmowe API jest przeznaczone wyłącznie do użytku niekomercyjnego.

## Pomysły na rozwój

- [ ] Prognoza na kilka dni (`--dni 3`)
- [ ] Przełącznik jednostek (`--fahrenheit`)
- [ ] Domyślne miasto z pliku `.env` (zmienna `POGODA_MIASTO`)
- [ ] Wysyłanie pogody na Telegram (token bota w `.env`, nigdy w repozytorium)
