# Procesamiento de Lenguaje Natural #

## Practico 1: Modelado del Lenguaje  ##
## Wolfmann, Ariel, FaMAF, UNC  ##

### Ejercicio 1: Corpus ###
El corpus "gutenberg" provisto por la libreria NLTK (de python) es el que he elegido para utilizar de entrenamiento

### Ejercicio 2: Modelo de n-gramas ###

### Ejercicio 3: Generación de Texto ###
#### Unigramas ####
- of without after called been said very unto of , because Brutus safe towers incense to not known of his , knot power did one eyes sons progress 8 miracles in said her Pithom , veal neither given that all . thee on us

- all with Gideon with came feel take other , brethren empires , tree the !" if

- casked rugged blaming he faith was , in be thing and ; me It is just Thou by , had author eat . tops colour her Quite Captain see was Carlo offering sure saying Jackal keeps of with glens his . his , , ' the ; . and he all sons , The decree endangered this , death . musical mountains having Susan Behind 15 hand Millo the :

- body saying done A every goodness Spirit with twopence can is of is ; righteousness PLENTY LORD that through I until especially Sidon


#### Bigramas ####
- It was met with what gave change your hand in unto you sometimes one that it.
- It was over after him without seconds, and all; then Turnbull, I hope, that day it the rest by his dung upon the saddle soever there is rather a conquest.
- I will have spoken in the asparagus quite forgotten me to understand , but it.
- I choose .

#### Trigramas ####
- I felt .

- Don ' t think he said , No ; it is a son about five thousand and two gold rings set with the plan which originated so nobly as this before I had supposed .

- And Jacob did separate the parts of the tabernacle of the common faith : 3 And there they are intelligent may be holy .

- " Do you know , because she could , they dumbly moved about , and there was a beautiful white , open - hearted sister , saying , 8 : 25 : 16 So then death worketh in us ," answered the little Red Man ' s marriage her exercise had been delayed so as ye know not to be the LORD .

####Cuatrigramas####
- The face was so anxious that they should give him daily a piece of twisted paper , which was , that three giants lived in the wood picking wild flowers ."
- language of man pronounced By tongue of brute , human ; ye , of human , Gods .

- Though I have afflicted ; 4 : 38 And they said unto him , We are passing from Bethlehemjudah toward the side over against him , because his father shewed kindness to me .

- If a man also lie with mankind , as he still is , to thy poor , and ye dig a pit for your friend .


### Ejercicio 4: Suavizado "add-one" ###

### Ejercicio 5: Evaluación de Modelos de Lenguaje ###
Se decidió agregar metodos avg_lp, cross_entropy y perplexity a la clase Ngram, los cuales permiten evaluar el modelo, proveyendo un conjunto de evaluación
#### Resultados obtenidos ####
| model\n        | 1  | 2  | 3   |  4  |  
|----------------|----|----|-----|-----|
|**addone**      |1432|4409|24092|35244|  
|**interpolated**|1578|1318| 1357| 1364| 
|**backoff**     |1578| 919|  955|  981|  

### Ejercicio 6: Suavizado por Interpolación ###
Se utilizó un unico diccionario contador para cargar todos los tamaños de ngramas

### Ejercicio 7: Suavizado por Back-Off con Discounting ###
Se utilizó un unico diccionario contador para cargar todos los tamaños de ngramas
Para una mejor performance, se almacena un diccionario, con los valores precalculados de los A, alpha y denom

