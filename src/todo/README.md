# To-do CLI

Lista zadań w terminalu, napisana w Pythonie. Zadania są zapisywane w pliku JSON, więc zostają między uruchomieniami.

## Użycie

```
python3 src/todo/todo.py add "kupić mleko"
python3 src/todo/todo.py add "napisać testy"
python3 src/todo/todo.py list
python3 src/todo/todo.py done 1
python3 src/todo/todo.py delete 2
```

Przykładowy wynik `list`:

```
1. [x] kupić mleko
2. [ ] napisać testy
```

Domyślnie zadania trafiają do pliku `zadania.json` w bieżącym folderze. Inny plik wskażesz opcją `--plik`:

```
python3 src/todo/todo.py --plik praca.json add "wysłać raport"
```

## Instalacja

```
git clone https://github.com/Cyber-Robots/python-nauka.git
cd python-nauka
```

Projekt używa tylko biblioteki standardowej Pythona, więc nie trzeba niczego doinstalowywać.

## Testy

```
pip install pytest
python -m pytest
```

## Pomysły na rozwój

- [ ] Termin wykonania zadania i sortowanie po dacie
- [ ] Priorytety (`--priorytet wysoki`)
- [ ] Komenda `clear` usuwająca wszystkie wykonane zadania
- [ ] Zamiana `argparse` na bibliotekę `typer`
