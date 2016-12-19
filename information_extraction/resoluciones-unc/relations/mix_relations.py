import csv
from pprint import pprint

ENTITIES = ['Designation', 'Person', 'Position', 'Date', 'Dedication', 
    'Designation_Type']


dates_file = open('DesignationDate.csv', 'r')
relations_Date = csv.DictReader(dates_file)

persons_file = open('DesignationPerson.csv', 'r')
relations_Person = csv.DictReader(persons_file)

positions_file = open('DesignationPosition.csv', 'r')
relations_Position = csv.DictReader(positions_file)

types_file = open('DesignationHasType.csv', 'r')
relations_Designation_Type = csv.DictReader(types_file)

dedications_file = open('DesignationDedication.csv', 'r')
relations_Dedication = csv.DictReader(dedications_file)

entity_kind_dict = {
    'Person': relations_Person,
    'Position': relations_Position,
    'Date': relations_Date,
    'Designation_Type': relations_Designation_Type,
    'Dedication': relations_Dedication
}


full_relations_dict = {}

for entity_kind in entity_kind_dict:
    for relation in entity_kind_dict[entity_kind]:
        if relation['Relation present']:
            designation = relation['Candidate evidence left entity']
            
            if designation not in full_relations_dict:
                full_relations_dict[designation] = {}

            designation_dict = full_relations_dict[designation]
            designation_dict[entity_kind] = relation['Candidate evidence right entity']

# pprint(full_relations_dict)

full_relations_file =  open('full_relations.csv', 'w')
full_relations = csv.DictWriter(full_relations_file, fieldnames=ENTITIES)
full_relations.writeheader()
for desig, values in full_relations_dict.items():
    desig_dict = {'Designation': desig}
    desig_dict.update(values)
    full_relations.writerow(desig_dict)



    # writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
    # writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
    # writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})
