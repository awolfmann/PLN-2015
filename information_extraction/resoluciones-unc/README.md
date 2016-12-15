python bin/manage.py flush
python bin/manage.py createsuperuser
python bin/manage.py loaddata fixtures/entitykind.json
python bin/manage.py loaddata fixtures/relations.json
python bin/csv_to_iepy.py resoluciones-unc.csv
python bin/preprocess.py 
python bin/manage.py runserver