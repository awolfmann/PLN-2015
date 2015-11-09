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
100.0% (1444/1444) (P=73.26%, R=72.96%, F1=73.11%)
Parsed 1444 sentences
Labeled
  Precision: 73.26% 
  Recall: 72.96% 
  F1: 73.11% 
Unlabeled
  Precision: 75.37% 
  Recall: 75.06% 
  F1: 75.22% 

real  2m58.922s
user  2m58.167s
sys 0m0.300s

upcfg0
100.0% (1444/1444) (P=70.25%, R=70.02%, F1=70.14%)
Parsed 1444 sentences
Labeled
  Precision: 70.25% 
  Recall: 70.02% 
  F1: 70.14% 
Unlabeled
  Precision: 72.11% 
  Recall: 71.88% 
  F1: 72.00% 

real  1m17.395s
user  1m16.981s
sys 0m0.212s


upcfg1
100.0% (1444/1444) (P=74.64%, R=74.55%, F1=74.59%)
Parsed 1444 sentences
Labeled
  Precision: 74.64% 
  Recall: 74.55% 
  F1: 74.59% 
Unlabeled
  Precision: 76.51% 
  Recall: 76.41% 
  F1: 76.46% 

real  1m37.693s
user  1m37.202s
sys 0m0.224s


upcfg2
100.0% (1444/1444) (P=74.86%, R=74.34%, F1=74.60%)
Parsed 1444 sentences
Labeled
  Precision: 74.86% 
  Recall: 74.34% 
  F1: 74.60% 
Unlabeled
  Precision: 76.78% 
  Recall: 76.25% 
  F1: 76.51% 

real  2m37.967s
user  2m37.082s
sys 0m0.264s


upcfg3
Loading model...
Loading corpus...
Parsing...
100.0% (1444/1444) (P=74.08%, R=73.45%, F1=73.76%)
Parsed 1444 sentences
Labeled
  Precision: 74.08% 
  Recall: 73.45% 
  F1: 73.76% 
Unlabeled
  Precision: 76.23% 
  Recall: 75.58% 
  F1: 75.90% 

real  3m3.224s
user  3m1.903s
sys 0m0.516s
