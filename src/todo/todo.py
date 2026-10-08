"""Lista zadań w terminalu z zapisem do pliku JSON.

Użycie:
    python3 todo.py add "kupić mleko"
    python3 todo.py list
    python3 todo.py done 1
    python3 todo.py delete 1
"""

import argparse
import json
import sys
from pathlib import Path

DOMYSLNY_PLIK = Path("zadania.json")


def wczytaj(sciezka=DOMYSLNY_PLIK):
    """Wczytuje zadania z pliku JSON. Brak pliku oznacza pustą listę."""
    sciezka = Path(sciezka)
    if not sciezka.exists():
        return []
    try:
        with sciezka.open(encoding="utf-8") as plik:
            return json.load(plik)
    except json.JSONDecodeError:
        raise ValueError(f"Plik {sciezka} jest uszkodzony (zły format JSON).") from None


def zapisz(zadania, sciezka=DOMYSLNY_PLIK):
    """Zapisuje listę zadań do pliku JSON."""
    with Path(sciezka).open("w", encoding="utf-8") as plik:
        json.dump(zadania, plik, ensure_ascii=False, indent=2)


def dodaj(zadania, tresc):
    """Dodaje zadanie na koniec listy i zwraca je."""
    tresc = tresc.strip()
    if not tresc:
        raise ValueError("Treść zadania nie może być pusta.")
    zadanie = {"tresc": tresc, "wykonane": False}
    zadania.append(zadanie)
    return zadanie


def _znajdz(zadania, numer):
    """Zamienia numer widoczny dla użytkownika (od 1) na zadanie z listy."""
    if not 1 <= numer <= len(zadania):
        raise IndexError(f"Nie ma zadania o numerze {numer}.")
    return zadania[numer - 1]


def oznacz_wykonane(zadania, numer):
    zadanie = _znajdz(zadania, numer)
    zadanie["wykonane"] = True
    return zadanie


def usun(zadania, numer):
    zadanie = _znajdz(zadania, numer)
    zadania.remove(zadanie)
    return zadanie


def formatuj(zadania):
    """Zwraca listę zadań jako tekst do wyświetlenia."""
    if not zadania:
        return "Brak zadań."
    linie = []
    for numer, zadanie in enumerate(zadania, start=1):
        znacznik = "x" if zadanie["wykonane"] else " "
        linie.append(f"{numer}. [{znacznik}] {zadanie['tresc']}")
    return "\n".join(linie)


def stworz_parser():
    parser = argparse.ArgumentParser(description="Lista zadań w terminalu.")
    parser.add_argument(
        "--plik", default=DOMYSLNY_PLIK, help="plik JSON z zadaniami (domyślnie zadania.json)"
    )
    podkomendy = parser.add_subparsers(dest="komenda", required=True)

    p_add = podkomendy.add_parser("add", help="dodaj zadanie")
    p_add.add_argument("tresc", help="treść zadania")

    podkomendy.add_parser("list", help="pokaż zadania")

    p_done = podkomendy.add_parser("done", help="oznacz zadanie jako wykonane")
    p_done.add_argument("numer", type=int)

    p_delete = podkomendy.add_parser("delete", help="usuń zadanie")
    p_delete.add_argument("numer", type=int)

    return parser


def main(argv=None):
    args = stworz_parser().parse_args(argv)

    try:
        zadania = wczytaj(args.plik)

        if args.komenda == "add":
            dodaj(zadania, args.tresc)
            print(f"Dodano: {args.tresc.strip()}")
        elif args.komenda == "list":
            print(formatuj(zadania))
            return 0
        elif args.komenda == "done":
            zadanie = oznacz_wykonane(zadania, args.numer)
            print(f"Wykonane: {zadanie['tresc']}")
        elif args.komenda == "delete":
            zadanie = usun(zadania, args.numer)
            print(f"Usunięto: {zadanie['tresc']}")

        zapisz(zadania, args.plik)
    except (ValueError, IndexError) as blad:
        print(f"Błąd: {blad}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
