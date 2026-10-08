"""Kalkulator w terminalu: działania, potęgi, pierwiastek, nawiasy i historia w pliku."""

import math
import re
from pathlib import Path

PLIK_HISTORII = Path("historia.txt")


# --- Działania podstawowe -------------------------------------------------

def dodaj(a, b):
    return a + b


def odejmij(a, b):
    return a - b


def pomnoz(a, b):
    return a * b


def podziel(a, b):
    if b == 0:
        raise ZeroDivisionError("Nie można dzielić przez zero.")
    return a / b


def potega(a, b):
    try:
        wynik = a**b
    except OverflowError:
        raise ValueError("Wynik jest zbyt duży.") from None
    except ZeroDivisionError:
        raise ZeroDivisionError(
            "Zero nie może być podniesione do ujemnej potęgi."
        ) from None
    if isinstance(wynik, complex):
        raise ValueError("Wynik nie jest liczbą rzeczywistą.")
    return wynik


def pierwiastek(a):
    if a < 0:
        raise ValueError("Nie można liczyć pierwiastka z liczby ujemnej.")
    return math.sqrt(a)


OPERACJE = {
    "+": dodaj,
    "-": odejmij,
    "*": pomnoz,
    "/": podziel,
}


# --- Tokenizer i parser (zachowuje kolejność działań) ---------------------

TOKENY = re.compile(r"\s*(\d+(?:[.,]\d+)?|\*\*|[-+*/()]|[a-zA-Z]+)")


def tokenizuj(wyrazenie):
    """Dzieli tekst na tokeny: liczby, operatory, nawiasy, nazwy funkcji."""
    tekst = wyrazenie.strip()
    tokeny = []
    pozycja = 0
    while pozycja < len(tekst):
        dopasowanie = TOKENY.match(tekst, pozycja)
        if not dopasowanie:
            raise ValueError(f"Nieprawidłowy znak: {tekst[pozycja]!r}")
        tokeny.append(dopasowanie.group(1))
        pozycja = dopasowanie.end()
    return tokeny


class Parser:
    """Parser metodą zejść rekurencyjnych.

    Gramatyka (od najniższego do najwyższego priorytetu):
        wyrazenie := skladnik (('+' | '-') skladnik)*
        skladnik  := unarny (('*' | '/') unarny)*
        unarny    := ('+' | '-') unarny | potega
        potega    := atom ('**' unarny)?
        atom      := LICZBA | '(' wyrazenie ')' | 'sqrt' '(' wyrazenie ')'
    """

    def __init__(self, tokeny):
        self.tokeny = tokeny
        self.pozycja = 0

    def podglad(self):
        if self.pozycja < len(self.tokeny):
            return self.tokeny[self.pozycja]
        return None

    def pobierz(self):
        token = self.podglad()
        if token is None:
            raise ValueError("Niepełne wyrażenie.")
        self.pozycja += 1
        return token

    def zamknij_nawias(self):
        if self.pobierz() != ")":
            raise ValueError("Brakuje nawiasu zamykającego.")

    def parsuj(self):
        if not self.tokeny:
            raise ValueError("Puste wyrażenie.")
        wynik = self.wyrazenie()
        if self.podglad() is not None:
            raise ValueError(f"Nieoczekiwany element: {self.podglad()}")
        return wynik

    def wyrazenie(self):
        wynik = self.skladnik()
        while self.podglad() in ("+", "-"):
            operator = self.pobierz()
            wynik = OPERACJE[operator](wynik, self.skladnik())
        return wynik

    def skladnik(self):
        wynik = self.unarny()
        while self.podglad() in ("*", "/"):
            operator = self.pobierz()
            wynik = OPERACJE[operator](wynik, self.unarny())
        return wynik

    def unarny(self):
        if self.podglad() in ("+", "-"):
            operator = self.pobierz()
            wartosc = self.unarny()
            return -wartosc if operator == "-" else wartosc
        return self.potega()

    def potega(self):
        baza = self.atom()
        if self.podglad() == "**":
            self.pobierz()
            return potega(baza, self.unarny())
        return baza

    def atom(self):
        token = self.pobierz()

        if token == "(":
            wynik = self.wyrazenie()
            self.zamknij_nawias()
            return wynik

        if token == "sqrt":
            if self.pobierz() != "(":
                raise ValueError("Użyj formatu: sqrt(liczba)")
            wynik = self.wyrazenie()
            self.zamknij_nawias()
            return pierwiastek(wynik)

        if token[0].isdigit():
            return float(token.replace(",", "."))

        raise ValueError(f"Nieznany element: {token}")


def oblicz(wyrazenie):
    """Liczy wyrażenie, np. '2 + 3 * 4', '(2 + 3) ** 2', 'sqrt(16)'."""
    try:
        wynik = Parser(tokenizuj(wyrazenie)).parsuj()
    except RecursionError:
        raise ValueError("Wyrażenie jest zbyt zagnieżdżone.") from None
    if not math.isfinite(wynik):
        raise ValueError("Wynik jest zbyt duży.")
    return wynik


def formatuj(wynik):
    """Zamienia 5.0 na '5', a 2.5 zostawia jako '2.5'."""
    if wynik.is_integer():
        return str(int(wynik))
    return str(round(wynik, 10))


# --- Historia w pliku -----------------------------------------------------

def wczytaj_historie(plik=PLIK_HISTORII):
    plik = Path(plik)
    if not plik.exists():
        return []
    tresc = plik.read_text(encoding="utf-8")
    return [linia for linia in tresc.splitlines() if linia.strip()]


def zapisz_wpis(wpis, plik=PLIK_HISTORII):
    with open(plik, "a", encoding="utf-8") as f:
        f.write(wpis + "\n")


def wyczysc_historie(plik=PLIK_HISTORII):
    Path(plik).write_text("", encoding="utf-8")


# --- Pętla programu -------------------------------------------------------

def main(plik_historii=PLIK_HISTORII):
    historia = wczytaj_historie(plik_historii)
    print("Kalkulator. Przykłady: 2 + 3 * 4, (2 + 3) ** 2, sqrt(16)")
    print("Komendy: historia, wyczysc, q (wyjście)")

    while True:
        try:
            wejscie = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nDo zobaczenia!")
            break

        komenda = wejscie.lower()

        if komenda in ("q", "quit", "exit", "koniec"):
            print("Do zobaczenia!")
            break

        if komenda == "historia":
            if not historia:
                print("Historia jest pusta.")
            for wpis in historia:
                print(wpis)
            continue

        if komenda == "wyczysc":
            historia.clear()
            try:
                wyczysc_historie(plik_historii)
            except OSError as blad:
                print(f"Nie udało się wyczyścić pliku historii: {blad}")
            else:
                print("Historia wyczyszczona.")
            continue

        if not wejscie:
            continue

        try:
            wynik = formatuj(oblicz(wejscie))
        except (ValueError, ZeroDivisionError) as blad:
            print(f"Błąd: {blad}")
            continue

        print(wynik)
        wpis = f"{wejscie} = {wynik}"
        historia.append(wpis)
        try:
            zapisz_wpis(wpis, plik_historii)
        except OSError as blad:
            print(f"Uwaga: nie udało się zapisać historii ({blad}).")


if __name__ == "__main__":
    main()
