# Extracción de Información en Resoluciones Universitarias

### Descripción del proyecto
La UNC ofrece acceso público a todas las resoluciones.
En este proyecto se propone detectar y procesar aquellas resoluciones de la UNC que se refieren a cambios en la planta docente, encontrando y etiquetando las entidades como: 
- Nombres de personas 
- Cargos
- Dedicaciones 
- Fechas
La información obtenida podrá ser consultada a través de una interfaz web.

### Herramientas Utilizadas
##### IEPY:
Proyecto de código abierto para Extracción de Información enfocado en extracción de relaciones. Referencias:
- http://iepy.readthedocs.io/en/latest/ 
- https://github.com/machinalis/iepy 

##### Resoluciones-UNC:
Proyecto de código abierto relacionado, sobre el cual se continuó el desarrollo existente. Referencia: 
- https://github.com/HackatONG-ProgramAR/resoluciones-unc 

##### Django:
Framework para desarrollo web, utilizado para la interfaz web. Referencia: 
- https://www.djangoproject.com/ 

### Tareas Realizadas

###### Preprocesamiento de los datos:
- Segmentar texto por articulos (basado en palabras clave)
- Detección de Entidades, basado en palabras claves y expresiones regulares.
- Definir fixtures para cargar entidades y relaciones en la base de datos.
- Se deshabilitaron las partes de Parser, y POS Tagger provistas por IEPY(Stanford). 
###### Procesamiento de los datos generados:
- Binarización de relacion: Designación(Persona, Fecha, Cargo, Dedicación,Tipo_Designacion) a Desig_Persona(Designacion, Persona), etc.
- Extraccion de relaciones basada en reglas: se definieron reglas a mano.
- Adaptar IEPY para poder detectar multiples relaciones.

### Ejemplo de Uso
###### Para correr el proyecto
- python bin/manage.py createsuperuser 
- python bin/manage.py loaddata fixtures/entitykind.json 
- python bin/manage.py loaddata fixtures/relations.json 
- python bin/csv_to_iepy.py resoluciones-unc.csv 
- python bin/preprocess.py (Corroborar que haya creado segmentos)
- python bin/iepy_rules_runner.py 
- python bin/manage.py runserver

### Ejemplo de Salida obtenida
###### Archivo csv (Extracto): Designacion, Persona, Posición, Fecha, Dedicación, Tipo_Designación
- "designacion 14 (104, 105)","Daniel MOISSET DE ESPANES (153, 157)","Prof . Asistente (179, 182)",,"DS (182, 183)","concurso (16, 17)"
- "designacion 8 (534, 535)","VILELA , Demetrio (642, 645)","Profesor Ayudante A (540, 543)","a partir del 1 de marzo aI 30 de junio de 2014 (521, 533)","dedicaci6n simple (544, 546)","interinas (536, 537)"
- "designacion 16 (278, 279)","BEDERIAN , Carlos (376, 379)","Profesores Asistentes (302, 304)","1 de mayo de 2014 (284, 289)","dedicaci6n simple (305, 307)","concurso (280, 281)" 


### Conclusiones
- Utilizando el proyecto se puede realizar una extracción básica de designaciones mencionadas en Resoluciones de la UNC.
- Al aplicar la técnica basada en reglas, se obtiene una precisión muy alta pero es necesario definir reglas para cada uno de los posibles casos que pueden aparecer, es decir es poco generalizable, este problema se puede observar cuando se manejan grandes cantidades de datos.
- Una posible mejora sería aplicar utilizar la técnica de Active Learning provista por IEPY.

### Trabajo Futuro
- Adaptar para extraer múltiples relaciones de una misma designación, por ejemplo varias personas.
- Incrementar el número de resoluciones procesadas, mayor cantidad de datos.
- Utilizar el core de Active Learning para aumentar el número de relaciones detectadas, de una forma mas generalizada.