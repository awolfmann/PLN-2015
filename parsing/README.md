# Procesamiento de Lenguaje Natural #

## Practico 3: Análisis Sintáctico  ##
## Wolfmann, Ariel, FaMAF, UNC  ##

Ejercicio 1
Baseline Flat
100.0% (1336/1336) (P=99.93%, R=15.49%, F1=26.83%)
Parsed 1336 sentences
Labeled
  Precision: 99.93% 
  Recall: 15.49% 
  F1: 26.83% 
Unlabeled
  Precision: 100.00% 
  Recall: 15.51% 
  F1: 26.85%

Baseline Rbranch

100.0% (1336/1336) (P=9.31%, R=15.49%, F1=11.63%)
Parsed 1336 sentences
Labeled
  Precision: 9.31% 
  Recall: 15.49% 
  F1: 11.63% 
Unlabeled
  Precision: 9.39% 
  Recall: 15.62% 
  F1: 11.73% 

Baseline Lbranch
100.0% (1336/1336) (P=9.31%, R=15.49%, F1=11.63%)
Parsed 1336 sentences
Labeled
  Precision: 9.31% 
  Recall: 15.49% 
  F1: 11.63% 
Unlabeled
  Precision: 15.43% 
  Recall: 25.67% 
  F1: 19.28% 

Upcfg
time python parsing/scripts/eval.py -i upcfg -m 20
Loading model...
Loading corpus...
Parsing...
100.0% (1336/1336) (P=72.15%, R=72.31%, F1=72.23%)
Parsed 1336 sentences
Labeled
  Precision: 72.15% 
  Recall: 72.31% 
  F1: 72.23% 
Unlabeled
  Precision: 75.53% 
  Recall: 75.70% 
  F1: 75.61% 

real  9m30.741s
user  9m27.771s
sys 0m1.404s
