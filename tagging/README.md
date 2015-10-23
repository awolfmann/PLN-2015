# Procesamiento de Lenguaje Natural #

## Practico 2: Etiquetado de Secuencias  ##
## Wolfmann, Ariel, FaMAF, UNC  ##

### Ejercicio 1:  Corpus Ancora: Estadísticas de etiquetas POS ###
#### Estadísticas básicas: ####
Cantidad de oraciones: 17379  
Cantidad de ocurrencias de palabras: 517300  
Cantidad de palabras (vocabulario): 46483  
Cantidad de etiquetas (vocabulario de tags): 48  
Etiquetas más frecuentes: Una tabla con las 10 etiquetas más frecuentes y la siguiente información para cada una:  
Cantidad de veces que aparece (frecuencia), y porcentaje del total.  
Top 10 tags statistics
|Tag| Frecuency|Percentage|
|---|---|---|
|nc  |92002|   17.79%|
|sp  |79904|   15.45%|
|da  |54552|   10.55%|
|vm  |50609|   9.78%|
|aq  |33904|   6.55%|
|fc  |30148|   5.83%|
|np  |29113|   5.63%|
|fp  |21157|   4.09%|
|rg  |15333|   2.96%|
|cc  |15023|   2.90%|

Cinco palabras más frecuentes con esa etiqueta:
* nc(nombre común) :años, presidente, millones, equipo, partido
* sp(Preposición): de, en, a, del, con
* da(determinante artículo): la, el, los, las, El
* vm(verbo principal): está, tiene, dijo, puede, hace
* aq(adjetivo calificativo): pasado, gran, mayor, nuevo, próximo
* fc(puntuación coma):','
* np: Gobierno, España, PP, Barcelona, Madrid
* fp(puntuación punto/paréntesis): '.', '(', ')'
* rg(adverbio general): más, hoy, también, ayer, ya
* cc(conjunción coordinada): y, pero, o, Pero, e

Niveles de ambigüedad de las palabras: 
|Nivel   |Frecuencia  |Porcentaje|
|---|---|---|
|1       |289397|      55.95%|
|2       |122816|      23.74%|
|3       |50530|       9.77%|
|4       |32635|       6.31%|
|5       |15967|       3.09%|
|6       |5923|        1.15%|

### Ejercicio 6: Features para Etiquetado de Secuencias ###
Features extra implementados:
* word_len: devuelve el largo de una palabra
* word_prefix: devuelve el prefijo de una palabra, con un parametro se puede determinar el largo del prefijo, valor por defecto: 3.   
* word_sufix: devuelve el sufijo de una palabra, con un parametro se puede determinar el largo del sufijo, valor por defecto: 3.  
* Agregando estos 3 features, se logro mejorar la prediccion sobre todo para las palabras desconocidas, logrando acercase a los valores del "estado del arte". Los valores son mostrados en el reporte del ejercicio 7.

### REPORTE DE VALORES OBTENIDOS ###
* El titulo de cada reporte muestra el metodo utilizado, el orden del model y el tipo de clasificador, en caso de que tenga la palabra 'extra' como sufijo, significa que son modelos entrenados con los features adicionales implementados como bonus.

Por ejemplo 'memm4SVCextra' significa el reporte para un modelo de maxima entropia, de orden 4, con un clasificador SVC, entrenado con los features extra.
* La matriz de confusion se muestra solo para los 10 tags mas frecuentes, y esta reportada solo para el modelo baseline y hmm1 

#### Baseline ####
100.0% (88.07%)
* Accuracy: 88.07%
* Accuracy Unknown: 31.80%
* Accuracy known: 94.28%
* Confusion Matrix
|    |nc  |sp |vm  |da  |aq  |fc  |fp  |rg  |np  |cc  |
|--- |--- |---|--- |--- |--- |--- |--- |--- |--- |--- | 
|nc  | 0  | 11|  84|  63| 450|  0 |   0| 23 |   3|   1|
|sp  |45  |  0|   0|   0|   0|   0|   0|  10|   0|   3|
|vm  |2131|  1|   0|   0| 200| 0  |   0|   0|   0|   0|
|da  |143 |  0|   0|0   |   0|   0|   0|   0|   0|   0|
|aq  |2194|  5| 183| 0  |   0|   0|   0|  68|   0|   0|
|fc  |0   |0  |0   | 0  |   0|   0|   0|   0|   0|   0|
|fp  |0   |0  |0   |0   |   0|   0|   0|   0|   0|   0|
|rg  |304 |18 |0   |0   |  12|  0 |   0|   0|   0|  21|
|np  |1936|  3|   0|   0|   1|   0|   0|   0|   0|   1|
|cc  |12  |1  |0   |0   |   0|   0|   0|  52|   0|   0|

* * real    0m7.765s
* * user    0m7.532s
* * sys 0m0.180s

#### hmm1 ####
100.0% (89.01%)
* Accuracy: 89.01%
* Accuracy Unknown: 31.80%
* Accuracy known: 95.32%
* Confusion Matrix
|    |nc  |sp |vm |da |aq |fc |fp |rg |np |cc  |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
|nc  |0   |11 | 88| 1 |471| 0 | 0 | 32|  4|   1|
|sp  | 45 |0  |  0|  0|  0|  0|  0|  5|  0|   0|
|vm  |2105|  1|  0|  0|167| 0 |  0|  0|  0|   0|
|da  |143 |0  |  0|  0|  0|  0|  0|  0|  0|   0|
|aq  |2041|  5|183| 0 |  0|  0| 0 |3  | 0 |   0|
|fc  |0   |0  |0  | 0 | 0 | 0 |  0| 0 | 0 |   0|
|fp  |0   |0  |0  | 0 | 0 | 0 |  0| 0 |  0|   0|
|rg  |297 |17 |0  | 0 |29 | 0 |  0| 0 |  0|  21|
|np  |1935| 3 |0  |0  | 1 |  0| 0 | 0 |  0|   1|
|cc  |12  |1  |0  |0  | 0 |  0| 0 |46 | 1 |   0|

* real    0m13.038s
* user    0m12.629s
* sys 0m0.332s

#### hmm2 ####
100.0% (92.72%)
* Accuracy: 92.72%
* Accuracy Unknown: 48.42%
* Accuracy known: 97.61%
* real    0m23.455s
* user    0m23.157s
* sys 0m0.220s


#### hmm3 ####
100.0% (93.17%)
* Accuracy: 93.17%
* Accuracy Unknown: 52.31%
* Accuracy known: 97.67%
* real    1m23.501s
* user    1m23.005s
* sys 0m0.288s


#### hmm4 ####
100.0% (93.14%)
* Accuracy: 93.14%
* Accuracy Unknown: 54.14%
* Accuracy known: 97.44%
* real    7m15.788s
* user    7m13.507s
* sys 0m1.132s

#### memm1LR ####
100.0% (92.70%)
* Accuracy: 92.70%
* Accuracy Unknown: 69.32%
* Accuracy known: 95.28%
* real    0m45.357s
* user    0m44.155s
* sys 0m0.292s

#### memm2LR ####
100.0% (91.99%)
* Accuracy: 91.99%
* Accuracy Unknown: 68.75%
* Accuracy known: 94.55%
* real    1m0.335s
* user    0m59.328s
* sys 0m0.276s

#### memm3LR ####
100.0% (92.18%)
* Accuracy: 92.18%
* Accuracy Unknown: 69.20%
* Accuracy known: 94.72%
* real    1m6.963s
* user    1m5.312s
* sys 0m0.304s


#### memm4LR ####
100.0% (92.23%)
* Accuracy: 92.23%
* Accuracy Unknown: 69.63%
* Accuracy known: 94.72%
* real    1m8.398s
* user    1m7.148s
* sys 0m0.316s

#### memm1LRextra ####
100.0% (95.64%)
* Accuracy: 95.64%
* Accuracy Unknown: 84.57%
* Accuracy known: 96.86%


#### memm1NB ####
100.0% (82.18%)
* Accuracy: 82.18%
* Accuracy Unknown: 48.89%
* Accuracy known: 85.85%
* real    36m43.456s
* user    36m34.557s
* sys 0m0.936s

#### memm2NB #### 
100.0% (76.46%)
* Accuracy: 76.46%
* Accuracy Unknown: 40.68%
* Accuracy known: 80.41%
* real    36m57.908s
* user    36m48.618s
* sys 0m1.436s


#### memm3NB ####
100.0% (71.47%)
* Accuracy: 71.47%
* Accuracy Unknown: 38.59%
* Accuracy known: 75.09%
* real    36m38.706s
* user    36m28.821s
* sys 0m1.092s

#### memm4NB ####
100.0% (68.20%)
* Accuracy: 68.20%
* Accuracy Unknown: 40.01%
* Accuracy known: 71.31%
* real    33m35.043s
* user    33m27.229s
* sys 0m1.132s

#### memm1SVC ####
100.0% (94.43%)
* Accuracy: 94.43%
* Accuracy Unknown: 70.82%
* Accuracy known: 97.04%
* real    0m44.292s
* user    0m43.887s
* sys 0m0.208s

#### memm2SVC ####
100.0% (94.29%)
* Accuracy: 94.29%
* Accuracy Unknown: 70.57%
* Accuracy known: 96.91%
* real    1m8.090s
* user    1m6.972s
* sys 0m0.368s

#### memm3SVC ####
100.0% (94.40%)
* Accuracy: 94.40%
* Accuracy Unknown: 71.38%
* Accuracy known: 96.94%
* real    0m49.160s
* user    0m48.023s
* sys 0m0.272s

#### memm4SVC ####
100.0% (94.46%)
* Accuracy: 94.46%
* Accuracy Unknown: 71.81%
* Accuracy known: 96.96%
* real    0m49.558s
* user    0m49.135s
* sys 0m0.332s

#### memm1SVCextra ####
100.0% (96.19%)
* Accuracy: 96.19%
* Accuracy Unknown: 86.11%
* Accuracy known: 97.30%
* real    1m8.122s
* user    1m7.640s
* sys 0m0.276s

#### memm3SVCextra ####
100.0% (96.23%)
* Accuracy: 96.23%
* Accuracy Unknown: 86.56%
* Accuracy known: 97.29%
* real    1m17.474s
* user    1m16.989s
* sys 0m0.220s

#### memm4SVCextra ####
100.0% (96.26%)
* Accuracy: 96.26%
* Accuracy Unknown: 86.70%
* Accuracy known: 97.31%
* real    1m9.464s
* user    1m9.000s
* sys 0m0.220s