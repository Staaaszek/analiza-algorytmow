# Analiza algorytmów — rozwiązania zestawów

📱 **PDF-y online:** https://staaaszek.github.io/analiza-algorytmow/

Każdy zestaw jest w dwóch wersjach:
- **telefon** — wąska strona (11 × 19,5 cm), czyta się bez przybliżania,
- **A4** — do druku / na komputer, ze spisem treści.

W każdym zadaniu: przepisana treść, potrzebne definicje i twierdzenia,
intuicja, rozwiązanie formalne i odpowiedź.

## Struktura

```
zestawy/aaNN/aaNN.tex    rozwiązania zestawu NN
zestawy/aaNN/tresc.pdf   oryginalna treść zestawu
common/aa.sty            wspólny styl (pudełka, notacja, tryb telefonu)
weryfikacja/aaNN.py      numeryczne sprawdzenie wyników z zestawu
weryfikacja/marginesy.py sprawdza, czy nic nie wystaje poza stronę
szablon/zestaw.tex       szablon nowego zestawu
```

## Budowanie lokalne

Wymaga TeX Live (`latexmk`, `pdflatex`, pakiety polskie) i `python3`.

```bash
./build.sh            # wszystkie zestawy -> build/
./build.sh aa01       # jeden zestaw
./build.sh --check    # + weryfikacja numeryczna i test marginesów
./build.sh --clean
```

## Nowy zestaw

```bash
./nowy-zestaw.sh 02 ~/Pobrane/aa02.pdf   # tworzy zestawy/aa02/ z szablonu
# uzupełnij zestawy/aa02/aa02.tex (+ opcjonalnie weryfikacja/aa02.py)
./build.sh --check aa02
git add . && git commit -m "Zestaw 2" && git push
```

Po `git push` GitHub Actions buduje PDF-y i publikuje je na stronie
(GitHub Pages) — zwykle w ~3 minuty.
