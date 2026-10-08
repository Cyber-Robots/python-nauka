# Kalkulator CLI

Kalkulator w terminalu napisany w Pythonie. Projekt do nauki Gita, testów i GitHub Actions.

## Funkcje

- Działania `+`, `-`, `*`, `/`, potęgowanie `**` i pierwiastek `sqrt(...)`
- Prawidłowa kolejność działań i nawiasy: `2 + 3 * 4` daje 14, a `(2 + 3) * 4` daje 20
- Własny parser zamiast `eval()`, więc program nie wykona obcego kodu
- Obsługa błędów (dzielenie przez zero, niedomknięty nawias, pierwiastek z liczby ujemnej)
- Przecinek lub kropka jako separator dziesiętny
- Historia obliczeń zapisywana w pliku `historia.txt` i wczytywana przy starcie

## Uruchomienie

```
git clone https://github.com/Cyber-Robots/python-nauka.git
cd python-nauka
python3 src/kalkulator/kalkulator.py
```

Przykładowa sesja:

```
> 2 + 3 * 4
14
> (2 + 3) ** 2
25
> sqrt(16) + 1
5
> 5 / 0
Błąd: Nie można dzielić przez zero.
> historia
2 + 3 * 4 = 14
(2 + 3) ** 2 = 25
sqrt(16) + 1 = 5
> q
```

Komendy: `historia`, `wyczysc`, `q`.

## Testy

```
pip install pytest
python -m pytest
```

## Jak to działa

Wyrażenie jest dzielone na tokeny, a potem liczone parserem metodą zejść rekurencyjnych. Każdy poziom gramatyki odpowiada jednemu priorytetowi działań (dodawanie, mnożenie, minus unarny, potęga, nawiasy), dzięki czemu kolejność działań wynika ze struktury kodu, a nie z dodatkowych reguł.

## Pomysły na rozwój

- [ ] Wynik poprzedniego działania jako `ans`
- [ ] Funkcje `abs()`, `sin()`, `cos()`
- [ ] Stałe `pi` i `e`
