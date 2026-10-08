# Kalkulator CLI

Prosty kalkulator w terminalu napisany w Pythonie. Projekt do nauki Gita, testów i GitHub Actions.

## Funkcje

- Dodawanie, odejmowanie, mnożenie i dzielenie
- Obsługa błędów (dzielenie przez zero, zły format, litery zamiast liczb)
- Przecinek lub kropka jako separator dziesiętny
- Historia obliczeń w trakcie sesji

## Uruchomienie

```
git clone https://github.com/Cyber-Robots/python-nauka.git
cd python-nauka
python3 kalkulator.py
```

Przykładowa sesja:

```
> 2 + 3
5
> 9 / 2
4.5
> 5 / 0
Błąd: Nie można dzielić przez zero.
> historia
2 + 3 = 5
9 / 2 = 4.5
> q
```

## Testy

```
pip install pytest
python -m pytest
```

## Pomysły na rozwój

- [ ] Potęgowanie i pierwiastek
- [ ] Wyrażenia z wieloma działaniami (`2 + 3 * 4`)
- [ ] Zapis historii do pliku
