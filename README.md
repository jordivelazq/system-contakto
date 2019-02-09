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
`./wsgi/project/manage.py runserver`

### NOTES:
* To improve speed when generating sprites, install oily (gem install oily_png) (http://compass-style.org/help/tutorials/spriting/)


### Migrate DB
`./wsgi/project/manage.py syncdb`
`./wsgi/project/manage.py migrate`
./wsgi/project/manage.py migrate persona
./wsgi/project/manage.py migrate


docker build -t garciadiazjaime/admin-contakto .
docker run -d -p 49164:8000 garciadiazjaime/admin-contakto
docker push garciadiazjaime/admin-contakto
docker pull garciadiazjaime/admin-contakto

### Deploy

`fab deploy`
