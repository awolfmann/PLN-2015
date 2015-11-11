# Procesamiento de Lenguaje Natural #

## Practico 3: Análisis Sintáctico  ##
## Wolfmann, Ariel, FaMAF, UNC  ##

### Ejercicio 1: Evaluación de Parsers ###
Resultados obtenidos de los distintos baselines:

#### Baseline Flat  
100.0% (1444/1444) (P=99.93%, R=14.57%, F1=25.43%)  
Parsed 1444 sentences  
- Labeled  
  * Precision: 99.93% 
  * Recall: 14.57% 
  * F1: 25.43% 
- Unlabeled  
  * Precision: 100.00% 
  * Recall: 14.58% 
  * F1: 25.45%  
  
real  0m12.330s  
user  0m11.137s  
sys 0m0.260s  

#### Baseline Rbranch

100.0% (1444/1444) (P=8.81%, R=14.57%, F1=10.98%)  
- Labeled
  * Precision: 8.81% 
  * Recall: 14.57% 
  * F1: 10.98% 
- Unlabeled
  * Precision: 8.87% 
  * Recall: 14.68% 
  * F1: 11.06% 

real  0m12.037s
user  0m11.813s
sys 0m0.192s


#### Baseline Lbranch
100.0% (1444/1444) (P=8.81%, R=14.57%, F1=10.98%)  
- Labeled
  * Precision: 8.81% 
  * Recall: 14.57% 
  * F1: 10.98% 
- Unlabeled
  * Precision: 14.71% 
  * Recall: 24.33% 
  * F1: 18.33% 

real  0m11.753s  
user  0m11.509s  
sys 0m0.196s  

### Ejercicio 2: Algoritmo CKY ###
Al inicializar el parser, a partir de la gramática, armo 2 diccionarios, uno para producciones binarias y otro para unarias, ambos con la parte derecha de la produccion como clave.
Luego en el metodo parse creo 2 diccionarios, pi y bp. En pi se almacenan las probabilidades de los distintos splits de la oracion y en bp se va construyendo el arbol de parseo para la oración. Cada entrada de ambos contiene solo la opción de mayor probabilidad para ese split.

Para el test de ambiguedad:  
Gramatica ambigua  
- S -> NP NP           [1.0]
- NP -> NP NN          [0.3]
- NP -> NN NP          [0.4]
- NP -> 'Natural'      [0.15]
- NP -> 'processing'   [0.15]
- NN -> 'language'     [1.0]

Para la oracion Natural language processing, existen 2 posibles arboles de parseo:  
(S  
    (NP (NP Natural) (NN language))  
    (NP processing)  
)  

(S  
    (NP Natural)  
    (NP (NN language) (NP processing))  
)  
Como el algoritmo elige la opcion con mayor probabilidad, selecciona el segundo como árbol de parseo para esta oración.

### Ejercicio 3: PCFGs No Lexicalizadas ###
Al inicializar la UPCFG, se deslexicaliza, se transforma a Forma Normal de Chomsky y finalmente de colapsan las producciones unarias de cada oración parseada. Ademas para definir cual va a ser el No terminal inicial de la PCFG, se realiza un conteo de los no terminales iniciales de cada oración y se elige el de mayor ocurrencia.
Con el No terminal inicial calculado y las producciones obtenidas de las oraciones parseada, se induce una PCFG.
El metodo parse basicamente llama al metodo parse de CKY, y luego lexicaliza el arbol de parseo obtenido.

#### Resultados Obtenidos
#### Upcfg  
100.0% (1444/1444) (P=73.26%, R=72.96%, F1=73.11%)  
- Labeled
  * Precision: 73.26% 
  * Recall: 72.96% 
  * F1: 73.11% 
- Unlabeled
  * Precision: 75.37% 
  * Recall: 75.06% 
  * F1: 75.22% 

real  2m58.922s  
user  2m58.167s  
sys 0m0.300s  

##### EXTRA
Como prueba extra a las solicitadas en el enunciado, se agregó un paralelismo simple al script eval.py, que se llama agregando el parametro -p cuando se corre el script. El paralelismo consiste en que en lugar de realizar el parseo de un conjunto de oraciones, secuencialmente, se hace en paralelo entre todos los cpus de la maquina en la que se corra.
Para esto se tuvo que ignorar el metodo progress, ya que en paralelo es mas complejo de implementar.

Tiempos utilizando multiprocessing en 4 cpus:  
real  1m39.913s  
user  6m4.347s  
sys 0m1.872s  
Si bien la relacion no es lineal, es decir no es 4 veces mas rapido que la secuencial, probablemente corriendo el script con un volumen de datos mayor, la diferencia se notaría aun mas.

### Ejercicio 4: Markovización Horizontal ###
Para este ejercicio, la única modificación al anterior fue agregarle un parámetro adicional, que determine el orden de la Markovización Horizontal, pasandole este parámetro al metodo chomsky_normal_form provisto por NLTK.
 
##### Resultados obtenidos:
##### N=0
100.0% (1444/1444) (P=70.25%, R=70.02%, F1=70.14%)
- Labeled
  * Precision: 70.25% 
  * Recall: 70.02% 
  * F1: 70.14% 
- Unlabeled
  * Precision: 72.11% 
  * Recall: 71.88% 
  * F1: 72.00% 

real  1m17.395s  
user  1m16.981s  
sys 0m0.212s

##### N=1
100.0% (1444/1444) (P=74.64%, R=74.55%, F1=74.59%)  
- Labeled
  * Precision: 74.64% 
  * Recall: 74.55% 
  * F1: 74.59% 
- Unlabeled
  * Precision: 76.51% 
  * Recall: 76.41% 
  * F1: 76.46% 

real  1m37.693s  
user  1m37.202s  
sys 0m0.224s  

##### N=2
100.0% (1444/1444) (P=74.86%, R=74.34%, F1=74.60%)  
- Labeled
  * Precision: 74.86% 
  * Recall: 74.34% 
  * F1: 74.60% 
- Unlabeled
  * Precision: 76.78% 
  * Recall: 76.25% 
  * F1: 76.51% 

real  2m37.967s  
user  2m37.082s  
sys 0m0.264s  

##### N=3
100.0% (1444/1444) (P=74.08%, R=73.45%, F1=73.76%)
- Labeled
  * Precision: 74.08% 
  * Recall: 73.45% 
  * F1: 73.76% 
- Unlabeled
  * Precision: 76.23% 
  * Recall: 75.58% 
  * F1: 75.90% 

real  3m3.224s  
user  3m1.903s  
sys 0m0.516s  
