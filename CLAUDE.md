# Instrukcje dla Claude — repo z rozwiązaniami „Analizy algorytmów”

Repo służy przez cały semestr: co jakiś czas dochodzi nowy zestaw zadań (PDF).
Zadanie: rozwiązać go w LaTeX-u w tym samym stylu co poprzednie zestawy.

## Przy nowym zestawie
1. `./nowy-zestaw.sh NN ścieżka/do/zestawu.pdf` (treść ląduje w `zestawy/aaNN/tresc.pdf`).
2. Przeczytaj PDF (obraz, nie tylko pdftotext — wzory się psują).
3. Napisz `zestawy/aaNN/aaNN.tex` wg wzoru `zestawy/aa00`, `zestawy/aa01`:
   - każde zadanie to `\section{Zadanie N. krótki opis}` + pudełko `tresc`
     z wiernie przepisaną treścią;
   - nieoczywiste definicje/twierdzenia w `teoria` (z `definicja`, `twierdzenie`,
     `lemat`), wytłumaczone, nie tylko przytoczone; jeśli coś było już
     wyjaśnione we wcześniejszym zestawie, można się odwołać;
   - `intuicja` (po ludzku, jak do studenta), potem `\formalnie` (pełny dowód),
     na końcu `odpowiedz`;
   - matematyka w tytułach sekcji przez `\texorpdfstring`;
   - zestaw trafia też automatycznie do pliku zbiorczego `wszystko.pdf`
     (`build.sh` → `\wlaczzestaw`); etykiety `\label` są tam prefiksowane
     nazwą zestawu, więc mogą się powtarzać między zestawami.
4. Wszystkie wzory zwarte / liczby sprawdź skryptem `weryfikacja/aaNN.py`
   (ułamki `fractions`, porównanie z rekurencją / brute force).
5. `./build.sh --check aaNN` musi przejść — w tym `marginesy.py` dla wersji
   telefonowej (strona ma tylko ~10 cm szerokości: długie wzory łam przez
   `align*`/`gather*`, nie dawaj szerokich tabel).
6. Commit + push na `main` → GitHub Actions buduje i publikuje na Pages.

## Konwencje
- Język: polski. `\lg = \log_2`. Makra w `common/aa.sty` (`\O`, `\floor`, `\ceil`, `\lgs`, `\ff`).
- Nie zmieniaj wyglądu `common/aa.sty` bez potrzeby — wpływa na wszystkie zestawy.
