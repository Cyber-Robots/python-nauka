# python-nauka

Moje projekty z nauki Pythona, Gita i GitHub Actions. Każdy projekt to osobny program w terminalu z własnymi testami.

## Projekty

| Projekt | Co robi | Czego uczy |
|---|---|---|
| [Kalkulator](src/kalkulator/README.md) | Liczy wyrażenia z nawiasami, potęgami i pierwiastkiem, z historią w pliku | parser metodą zejść rekurencyjnych, obsługa błędów, testy parametryzowane |
| [To-do](src/todo/README.md) | Lista zadań zapisywana w pliku JSON | `argparse`, praca z plikami JSON, oddzielenie logiki od interfejsu |
| [Bot pogodowy](src/pogoda/README.md) | Pokazuje aktualną pogodę dla wybranej miejscowości | zapytania HTTP, zewnętrzne API, testy z atrapą zamiast internetu |

## Szybki start

Wymagany jest Python 3.9 lub nowszy.

```
git clone https://github.com/Cyber-Robots/python-nauka.git
cd python-nauka
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Uruchamianie projektów:

```
python3 src/kalkulator/kalkulator.py
python3 src/todo/todo.py list
python3 src/pogoda/pogoda.py Warszawa
```

## Testy

```
python -m pytest
```

Testy nie wymagają internetu. Zapytania sieciowe bota pogodowego są w nich zastępowane atrapą, a pliki z danymi powstają w katalogach tymczasowych. Po każdym pushu i Pull Requeście testy uruchamia GitHub Actions.

## Struktura

```
python-nauka/
├── src/
│   ├── kalkulator/
│   ├── todo/
│   └── pogoda/
├── tests/
├── pytest.ini
├── requirements.txt
└── README.md
```

## Jak pracuję z repozytorium

- Każda zmiana powstaje na osobnej gałęzi i trafia do `main` przez Pull Request.
- Commity są małe i opisują, co się zmieniło.
- Hasła, klucze i pliki z danymi osobistymi nie trafiają do repozytorium (patrz `.gitignore`).
