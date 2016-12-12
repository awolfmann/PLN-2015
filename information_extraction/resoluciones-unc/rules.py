from refo import Question, Star, Any, Plus
from iepy.extraction.rules import rule, Token, Pos

# Write here your rules
# RELATION = 'your relation here'

# Designation(Person, Date, Position, DesignationType, Dedication)
# Binarize the relation to: 
# DesignationPerson(Designation, Person)
# DesignationDate(Designation, Date)
# DesignationPosition(Designation, Position)
# DesignationHasType(Designation, DesignationType)
# DesignationDedication(Designation, Dedication)

# Relation: DesignationPerson(Designation, Person)
@rule(True)
def designation_person_with_date_before(Subject, Object):
    """ Example: 
        Prorrogar, a partir del 1 aI 31 de marzo de 2014 la designaci6n 
        docente interina del:
        Profesor Ayudante A - dedicaci6n simple (c6digo 119) FERVARI,Raul  
        legajo 46638 - c6d. cargo 119/08 en suplencia del Lic. Daniel Moisset. """
    anything = Star(Any())
    return (anything + Kind(Date) + anything + Subject + anything + 
        DesignationType + anything + Kind(Position) + anything + Object +  anything)


# Relation: DesignationPerson(Designation, Person)
@rule(True)
def designation_person_with_date_after(Subject, Object):
    """ Example: 
        Designar interinamente como Profesor Adjunto con dedicaci6n
        simple (c6digo intemo 111/19) en el area Ciencias de la 
        Computaci6n aI Dr. Matfas D. LEE (legajo 41972), 
        por el lapso 01 de abril al 31 de Julio de 2014.    
    """
    anything = Star(Any())
    return (anything + Subject + anything + Kind(Position) + 
        anything + Object +  anything + Kind(Date) + anything)

# Relation: DesignationPerson(Designation, Person)
@rule(True)
def designation_person_upperscore_enumerated(Subject, Object):
    """ Example: 
        Prorrogar, a partir del 1 de marzo al 30 de junio de 2014 
        las designaciones docentes interinas de los:
        Profesores Asistentes - dedicaci6n simple (c6d. 115)
        -GARCIA IGLESIAS, Agustin  legajo 43099 -  c6d. cargo 115/29 
    """
    anything = Star(Any())
    return (anything + Subject + anything + Token("-") + Object + anything)


# Relation: DesignationDate(Designation, Date)
@rule(True)
def designation_date(Subject, Object):
    """ Example: 
        Prorrogar, a partir del 1 aI 31 de marzo de 2014 la designaci6n 
        docente interina del:
        Profesor Ayudante A - dedicaci6n simple (c6digo 119) FERVARI,Raul  
        legajo 46638 - c6d. cargo 119/08 en suplencia del Lic. Daniel Moisset. """
    anything = Star(Any())
    return (anything + Object + anything + Subject + anything + 
        Kind(DesignationType) + anything + Kind(Position) + anything +  Kind(Dedication) + 
        anything + Kind(Person) +  anything)

# Relation: DesignationDate(Designation, Date)
@rule(True)
def designation_date_before(Subject, Object):
    """ Example: 
        Prorrogar, a partir del 1 aI 31 de marzo de 2014 la designaci6n 
        docente interina """
    anything = Star(Any())
    return (anything + Object + anything + Subject + anything)

# Relation: DesignationDate(Designation, Date)
@rule(True)
def designation_date_after(Subject, Object):
    """ Example: Designar interinamente, a partir del 10 de marzo de 2014 
        y hasta el 28 de febrero de 2015
    """
    anything = Star(Any())
    return (anything + Subject + anything + Object + anything)


# Relation: DesignationPosition(Designation, Position)
@rule(True)
def designation_position(Subject, Object):
    """ Example: 
        Prorrogar, a partir del 1 aI 31 de marzo de 2014 la designaci6n 
        docente interina del: Profesor Ayudante A - dedicaci6n 
        simple (c6digo 119) FERVARI,Raul legajo 46638 - c6d. cargo 
        119/08 en suplencia del Lic. Daniel Moisset. 
    """
    anything = Star(Any())
    return (anything + Kind(Date) + anything + Subject + anything + 
        DesignationType + anything + Object + anything +  Dedication + 
        anything + Person + anything)

# Relation: DesignationPosition(Designation, Position)
@rule(True)
def designation_position_1(Subject, Object):
    """ Example: 
        Deslgnar por concurso a partir del 1 de mayo de 2014 y por el lapso
        estatutario de 3 (tres) aRos, como Profesores Asistentes 
    """
    anything = Star(Any())
    return (anything + Subject + anything + Object + anything)


# Relation: DesignationPosition(Designation, Position)
@rule(True)
def designation_position_2(Subject, Object):
    """ Example: 
    Los Lics. Diego DUBOIS, Demetrio VILELA y Carlos BEDERIAN
    cesan en Sus designaciones interinas como Prof. Ayudante A DS, c6digos intemos
    119/48, 119/60, 119/50 respectivamente, a partir del 1 de mayo de 2014.
    """
    anything = Star(Any())
    return (anything + Kind(Person) + anything + Subject + anything + Object + anything)

# Relation: DesignationHasType(Designation, DesignationType)
@rule(True)
def designation_with_type(Subject, Object):
    """ Example: 
        Prorrogar, a partir del 1 aI 31 de marzo de 2014 la designaci6n 
        docente interina del:
        Profesor Ayudante A - dedicaci6n simple (c6digo 119) FERVARI,Raul  
        legajo 46638 - c6d. cargo 119/08 en suplencia del Lic. Daniel Moisset. """
    anything = Star(Any())
    return (anything + Date + anything + Subject + anything + 
        Object + anything + Position + anything +  Dedication + 
        anything + Person +  anything)


# Relation: DesignationDedication(Designation, Dedication)
@rule(True)
def designation_dedication(Subject, Object):
    """ Example: 
        Prorrogar, a partir del 1 aI 31 de marzo de 2014 la designaci6n 
        docente interina del:
        Profesor Ayudante A - dedicaci6n simple (c6digo 119) FERVARI,Raul  
        legajo 46638 - c6d. cargo 119/08 en suplencia del Lic. Daniel Moisset. """
    anything = Star(Any())
    return (anything + Date + anything + Subject + anything + 
        DesignationType + anything + Position + anything + Object + 
        anything + Person +  anything)


