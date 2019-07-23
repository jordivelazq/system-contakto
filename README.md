Contakco System
==============

Installation Steps
------

BE

* [Create a virtual environment](https://docs.python-guide.org/dev/virtualenvs/) and activate:
`source ./contakto/bin/activate`
* Clone project
* Create your branch (**topics/feature**)
* Install python packages (`$ pip install -r requirements.txt`)
* Run server
`./project/manage.py runserver`

### NOTES:
* To improve speed when generating sprites, install oily (gem install oily_png) (http://compass-style.org/help/tutorials/spriting/)


### Migrate DB
`./project/manage.py syncdb`
`./project/manage.py migrate`
./project/manage.py migrate persona
./project/manage.py migrate


docker build -t garciadiazjaime/admin-contakto .
docker run -d -p 49164:8000 garciadiazjaime/admin-contakto
docker push garciadiazjaime/admin-contakto
docker pull garciadiazjaime/admin-contakto

### Setup

- Create `contactos` Group.
This group will be assigned to Company contacts with restricted access to the system:
  

### Deploy

`fab deploy`

### Debug

- Import pdb

`import pdb`

- Add tracer

`pdb.set_trace()`

The application will stop righ where the tracer has been added.


### Reset DB

- Copy Password (copy it)
`echo $MYSQL_PASSWORD`

- Dump DB
`mysqldump -u $MYSQL_USER -h $HOSTNAME -p db_contakto > db_contakto.sql`

- Copy DB Out of container
`docker cp mysql-contakto:/db_contakto.sql ./`

- Copy DB from server to local folder
`scp [user:ip]:/root/container-nginx/db_contakto.sql docs`

- Create DB locally
`create database db_contakto;`

- Load DB from sql file
`mysql -uroot db_contakto < docs/db_contakto.sql`


### Migrations

Follow steps found on this [tutorial](https://south.readthedocs.io/en/latest/tutorial/part1.html) to create/run migrations.

ie.
- Create migration
`./project/manage.py schemamigration persona --auto`

- Run migration
`./project/manage.py migrate persona`

### Compass

- Watch sass files
`compass watch project`

- Compile sass files
`compass compile project`
