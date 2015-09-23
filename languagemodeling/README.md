# Procesamiento de Lenguaje Natural #

## Practico 1: Modelado del Lenguaje  ##
## Wolfmann, Ariel, FaMAF, UNC  ##

### Ejercicio 1: Corpus ###
El corpus "gutenberg" provisto por la libreria NLTK (de python) es el que he elegido para utilizar de entrenamiento

### Ejercicio 2: Modelo de n-gramas ###

### Ejercicio 3: Generación de Texto ###

### Ejercicio 4: Suavizado "add-one" ###

### Ejercicio 5: Evaluación de Modelos de Lenguaje ###
Se decidió agregar metodos avg_lp, cross_entropy y perplexity a la clase Ngram, los cuales permiten evaluar el modelo, proveyendo un conjunto de evaluación
#### Resultados obtenidos ####
 n            1   | 2   | 3      |  4
addone       1432|4409 |24092    |35244
interpolated 1578|49313|106633789|6267861583
backoff      inf |inf  |inf        |inf

### Ejercicio 6: Suavizado por Interpolación ###
Se utilizó un unico diccionario contador para cargar todos los tamaños de ngramas

### Ejercicio 7: Suavizado por Back-Off con Discounting ###
Se utilizó un unico diccionario contador para cargar todos los tamaños de ngramas
Para una mejor performance, se almacena un diccionario, con los valores precalculados de los A, alpha y denom

