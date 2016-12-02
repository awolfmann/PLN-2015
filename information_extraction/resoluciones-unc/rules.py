# Write here your rules
# RELATION = 'your relation here'

# Designacion_interina(f:fecha, p:persona, c:position) 
# Designacion_concurso(f:fecha, p:persona, c:position)
# Licencia(f:fecha, p:persona, c:position)
# Renuncia(f:fecha, p:persona, c:position)
# Cese_desigancion(f:fecha, p:persona, c:position)

# Se podria agregar dedicacion, para esto habria que definir un NER de dedicaciones
# Para las designaciones interinas no se establece un lapso y para las por concurso si?, pero si se establecen prorrogas
# Todas las relaciones toman los mismos parametros, por lo que se podria definir una relacion Designacion(f:fecha, p:persona, c:position, t:tipo) donde tipo sea concurso o interina, renuncia, licencia o cese?
# Como seria el tema de "binarizar", cuando defino la relacion Designacion_fecha(f:fecha, d:designacion), no me queda claro como definir la entidad designacion?

# Con el tema de las reglas:
# El ejemplo que hay en la documentacion de iepy es: 
# def born_date_and_death_in_parenthesis(Subject, Object):
#     """ Example: Carl Bridgewater (January 2, 1965 - September 19, 1978) was shot dead """
#     anything = Star(Any())
#     return Subject + Pos("-LRB-") + Object + Token("-") + anything + Pos("-RRB-") + anything 

# como seria para definir este mismo ejemplo con entidades? vi que hay un bloque Kind, equivalente a Subject y Object, pero no se como usarlo,
# pense algo asi, pero es solo una aproximacion, no hay ejemplos con entidades en la documentacion..
# def born_date_and_death_in_parenthesis(Kind=Persona, Kind=Fecha):
#     """ Example: Carl Bridgewater (January 2, 1965 - September 19, 1978) was shot dead """
#     anything = Star(Any())
#     return Persona + Token("(") + Fecha + Token("-") + anything + Token(")") + anything 
