# Procesamiento de Lenguaje Natural #

## Practico 2: Etiquetado de Secuencias  ##
## Wolfmann, Ariel, FaMAF, UNC  ##

### Ejercicio 1:  Corpus Ancora: Estadísticas de etiquetas POS ###
top words ('nc', 92002) [('años', 849), ('presidente', 682), ('millones', 616), ('equipo', 457), ('partido', 438)]
top words ('sp', 79904) [('de', 28475), ('en', 12114), ('a', 8192), ('del', 6518), ('con', 4150)]
top words ('da', 54552) [('la', 17897), ('el', 14524), ('los', 7758), ('las', 4882), ('El', 2817)]
top words ('vm', 50609) [('está', 564), ('tiene', 511), ('dijo', 499), ('puede', 381), ('hace', 350)]
top words ('aq', 33904) [('pasado', 393), ('gran', 275), ('mayor', 248), ('nuevo', 234), ('próximo', 213)]
top words ('fc', 30148) [(',', 30148)]
top words ('np', 29113) [('Gobierno', 554), ('España', 380), ('PP', 234), ('Barcelona', 232), ('Madrid', 196)]
top words ('fp', 21157) [('.', 17513), ('(', 1823), (')', 1821)]
top words ('rg', 15333) [('más', 1707), ('hoy', 772), ('también', 683), ('ayer', 593), ('ya', 544)]
top words ('cc', 15023) [('y', 11211), ('pero', 938), ('o', 895), ('Pero', 323), ('e', 310)]
sents: 17379
tokens: 517300
words: 46483
taggs: 48
taggs most common: [('nc', 92002), ('sp', 79904), ('da', 54552), ('vm', 50609), ('aq', 33904), ('fc', 30148), ('np', 29113), ('fp', 21157), ('rg', 15333), ('cc', 15023)]

### Ejercicio 2: Baseline Tagger ###
Accuracy: 88.07%


### Ejercicio 3: Entrenamiento y Evaluación de Taggers ###
hmm2
100.0% (92.72%)
Accuracy: 92.72%
Accuracy Unknown: 48.42%
Accuracy known: 97.61%
Confusion Matrix
    nc  sp  vm  da  aq  fc  fp  rg  np  cc
nc  0   69  176 168 344 41  1   44  471 2
sp  3   0   5   13  1   1   0   16  4   4
vm  198 339 0   86  195 31  1   57  120 2
da  69  4   8   0   1   0   0   0   40  0
aq  418 146 300 98  0   86  4   53  149 1
fc  0   0   0   0   0   0   0   0   0   0
fp  0   0   0   0   0   0   0   0   0   0
rg  32  65  43  25  51  1   0   0   68  22
np  470 51  90  37  148 35  2   23  0   1
cc  0   1   1   0   0   0   0   51  10  0


hmm3
100.0% (93.17%)
Accuracy: 93.17%
Accuracy Unknown: 52.31%
Accuracy known: 97.67%
Confusion Matrix
    nc  sp  vm  da  aq  fc  fp  rg  np  cc
nc  0   41  146 159 339 23  3   40  298 7
sp  2   0   6   14  2   1   0   14  5   3
vm  243 309 0   73  197 59  1   62  74  12
da  82  0   7   0   4   0   0   0   29  0
aq  439 94  238 70  0   74  5   54  77  4
fc  0   0   0   0   0   0   0   0   0   0
fp  0   0   0   0   0   0   0   0   0   0
rg  43  58  23  25  45  10  0   0   31  21
np  567 47  77  36  132 24  3   52  0   4
cc  0   0   1   1   0   0   0   60  8   0

hmm4
100.0% (93.14%)
Accuracy: 93.14%
Accuracy Unknown: 54.14%
Accuracy known: 97.44%
Confusion Matrix
nc  sp  vm  da  aq  fc  fp  rg  np  cc
nc  0   42  119 138 348 28  6   39  280 6
sp  1   0   5   13  1   1   0   16  5   3
vm  241 309 0   72  184 47  1   64  71  12
da  74  3   8   0   4   1   1   0   37  0
aq  456 93  257 66  0   93  2   61  65  13
fc  0   0   0   0   0   0   0   0   0   0
fp  0   0   0   0   0   0   0   0   0   0
rg  43  60  26  27  51  7   0   0   30  29
np  514 42  85  40  126 21  1   42  0   11
cc  0   1   1   1   3   0   0   58  6   0

1540 segs

memm1LR
100.0% (92.70%)
Accuracy: 92.70%
Accuracy Unknown: 69.32%
Accuracy known: 95.28%
Confusion Matrix
    nc  sp  vm  da  aq  fc  fp  rg  np  cc
nc  0   9   497 6   535 0   0   16  115 1
sp  11  0   31  0   41  0   0   4   0   0
vm  393 1   0   0   494 0   0   0   167 0
da  118 0   4   0   0   0   0   0   4   0
aq  672 5   546 0   0   0   0   2   44  0
fc  0   0   0   0   0   0   0   0   0   0
fp  0   0   0   0   0   0   0   0   0   0
rg  48  16  204 1   292 0   0   0   32  21
np  238 2   87  0   23  0   0   0   0   1
cc  1   1   13  0   2   0   0   44  1   0

memm2LR
100.0% (91.99%)
Accuracy: 91.99%
Accuracy Unknown: 68.75%
Accuracy known: 94.55%
Confusion Matrix
nc  sp  vm  da  aq  fc  fp  rg  np  cc
nc  0   8   543 6   713 0   0   11  116 0
sp  25  0   34  0   33  0   0   4   0   0
vm  534 1   0   0   567 0   0   0   170 0
da  118 0   3   0   0   0   0   0   4   0
aq  913 5   539 0   0   0   0   3   44  0
fc  0   0   0   0   0   0   0   0   0   0
fp  0   0   0   0   0   0   0   0   0   0
rg  165 16  208 1   176 0   0   0   32  21
np  244 2   88  0   16  0   0   0   0   1
cc  3   1   13  0   1   0   0   45  1   0


memm3LR
100.0% (92.18%)
Accuracy: 92.18%
Accuracy Unknown: 69.20%
Accuracy known: 94.72%
Confusion Matrix
nc  sp  vm  da  aq  fc  fp  rg  np  cc
nc  0   10  509 6   696 0   0   11  113 0
sp  20  0   37  0   36  0   0   4   0   0
vm  524 1   0   0   534 0   0   0   168 0
da  119 0   3   0   0   0   0   0   4   0
aq  874 5   523 0   0   0   0   3   44  0
fc  0   0   0   0   0   0   0   0   0   0
fp  0   0   0   0   0   0   0   0   0   0
rg  116 16  258 1   181 0   0   0   32  21
np  254 3   80  0   19  0   0   0   0   1
cc  5   1   12  0   3   0   0   45  1   0

memm4LR
100.0% (92.23%)
Accuracy: 92.23%
Accuracy Unknown: 69.63%
Accuracy known: 94.72%
Confusion Matrix
nc  sp  vm  da  aq  fc  fp  rg  np  cc
nc  0   10  444 4   704 0   0   11  113 0
sp  18  0   38  0   35  0   0   4   0   0
vm  554 1   0   0   538 0   0   0   171 0
da  118 0   3   0   0   0   0   0   4   0
aq  883 5   495 0   0   0   0   4   44  0
fc  0   0   0   0   0   0   0   0   0   0
fp  0   0   0   0   0   0   0   0   0   0
rg  124 16  247 1   192 0   0   0   32  21
np  258 3   77  0   21  0   0   0   0   1
cc  4   1   12  0   3   0   0   44  1   0

memm1LRextra con word_len
100.0% (92.97%)
Accuracy: 92.97%
Accuracy Unknown: 71.51%
Accuracy known: 95.34%
Confusion Matrix
nc  sp  vm  da  aq  fc  fp  rg  np  cc
nc  0   8   506 4   516 0   0   13  134 0
sp  15  0   25  0   39  0   0   4   1   0
vm  406 1   0   0   488 0   0   0   144 0
da  101 0   3   0   1   0   0   0   23  0
aq  672 5   557 0   0   0   0   3   51  0
fc  0   0   0   0   0   0   0   0   0   0
fp  0   0   0   0   0   0   0   0   0   0
rg  64  16  171 0   291 0   0   0   40  21
np  74  2   33  0   15  0   0   2   0   1
cc  2   1   12  0   2   0   0   44  1   0

 memm2LRextra 
100.0% (92.30%)
Accuracy: 92.30%
Accuracy Unknown: 71.14%
Accuracy known: 94.64%
Confusion Matrix
nc  sp  vm  da  aq  fc  fp  rg  np  cc
nc  0   8   557 4   715 0   0   13  135 0
sp  28  0   26  0   35  0   0   4   1   0
vm  520 1   0   0   553 0   0   2   144 0
da  101 0   2   0   0   0   0   0   23  0
aq  880 5   577 0   0   0   0   5   50  0
fc  0   0   0   0   0   0   0   0   0   0
fp  0   0   0   0   0   0   0   0   0   0
rg  136 16  186 1   180 0   0   0   45  21
np  76  2   30  0   17  0   0   2   0   1
cc  3   1   12  0   1   0   0   45  2   0

memm1LRextra2
100.0% (95.64%)
Accuracy: 95.64%
Accuracy Unknown: 84.57%
Accuracy known: 96.86%
Confusion Matrix
nc  sp  vm  da  aq  fc  fp  rg  np  cc
nc  0   9   158 5   406 0   0   24  113 1
sp  4   0   5   0   1   0   0   6   0   0
vm  151 3   0   0   135 0   0   5   61  0
da  19  0   0   0   7   0   0   0   21  0
aq  647 5   122 0   0   0   0   50  30  0
fc  0   0   0   0   0   0   0   0   0   0
fp  0   0   0   0   0   0   0   0   0   0
rg  45  37  15  0   89  0   0   0   4   21
np  41  2   17  0   10  0   0   6   0   1
cc  0   1   8   0   0   0   0   49  1   0


memm1NB
100.0% (82.18%)
Accuracy: 82.18%
Accuracy Unknown: 48.89%
Accuracy known: 85.85%
Confusion Matrix
nc  sp  vm  da  aq  fc  fp  rg  np  cc
nc  0   406 98  251 77  10  0   2   111 0
sp  10  0   0   59  1   1   1   2   43  0
vm  479 625 0   371 69  60  5   0   26  0
da  107 0   0   0   0   0   0   0   5   0
aq  1324    1234    302 126 0   46  4   0   18  0
fc  0   0   0   1   0   0   0   0   0   0
fp  2   1   1   8   0   0   0   0   0   0
rg  268 405 154 285 107 32  3   0   7   14
np  350 140 21  468 1   1   0   0   0   1
cc  12  17  1   129 1   0   0   46  104 0

memm2NB 100.0% (76.46%)
Accuracy: 76.46%
Accuracy Unknown: 40.68%
Accuracy known: 80.41%
Confusion Matrix
nc  sp  vm  da  aq  fc  fp  rg  np  cc
nc  0   1087    287 724 200 51  1   2   123 0
sp  39  0   9   211 1   3   1   1   49  0
vm  525 944 0   758 173 153 6   0   37  0
da  127 7   0   0   0   0   0   0   4   0
aq  1113    1396    378 394 0   87  4   1   17  0
fc  4   0   1   5   0   0   0   0   0   0
fp  22  0   12  76  0   0   0   0   2   0
rg  263 413 215 449 133 66  2   0   13  12
np  332 288 41  536 2   12  0   0   0   1
cc  57  20  11  407 3   3   0   49  110 0


### Ejercicio 4: Hidden Markov Models ###
tests modificados para python 3.2
### Ejercicio 5: HMM POS Tagger ###

### Ejercicio 6: Ejercicio 6: Maximum Entropy Markov Models ###
