"""Prosty kalkulator w terminalu."""


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


OPERACJE = {
    "+": dodaj,
    "-": odejmij,
    "*": pomnoz,
    "/": podziel,
}


def oblicz(wyrazenie):
    """Liczy wyrażenie w formacie 'liczba operator liczba', np. '2 + 3'."""
    czesci = wyrazenie.split()
    if len(czesci) != 3:
        raise ValueError("Użyj formatu: liczba operator liczba, np. 2 + 3")

    a_tekst, operator, b_tekst = czesci

    if operator not in OPERACJE:
        raise ValueError(f"Nieznany operator: {operator}")

    try:
        a = float(a_tekst.replace(",", "."))
        b = float(b_tekst.replace(",", "."))
    except ValueError:
        raise ValueError("Argumenty muszą być liczbami.") from None

    return OPERACJE[operator](a, b)


def formatuj(wynik):
    """Zamienia 5.0 na '5', a 2.5 zostawia jako '2.5'."""
    if wynik.is_integer():
        return str(int(wynik))
    return str(round(wynik, 10))


def main():
    historia = []
    print("Kalkulator. Wpisz np. 2 + 3. Komendy: historia, q (wyjście).")

    while True:
        wejscie = input("> ").strip()

        if wejscie.lower() in ("q", "quit", "exit", "koniec"):
            print("Do zobaczenia!")
            break

        if wejscie.lower() == "historia":
            if not historia:
                print("Historia jest pusta.")
            for wpis in historia:
                print(wpis)
            continue

        if not wejscie:
            continue

        try:
            wynik = formatuj(oblicz(wejscie))
        except (ValueError, ZeroDivisionError) as blad:
            print(f"Błąd: {blad}")
            continue

        print(wynik)
        historia.append(f"{wejscie} = {wynik}")


if __name__ == "__main__":
    main()
