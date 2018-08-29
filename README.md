Contakco System
==============

Installation Steps
------

BE

* [Create a virtual environment](http://desarrolloweblibre.com/por-que-usar-virtualenv/) and activate it (`$ . bin/activate` or `$ source bin/activate`)
* Clone project
* Checkout to **dev** branch
* Create your branch (**topics/feature**)
* Install python packages (`$ pip install -r requirements.txt`)
* Run server (`$ python manage.py runserver `)

### NOTES:
* In case of using Osx you might need to install Xcode
* To improve speed when generating sprites, install oily (gem install oily_png) (http://compass-style.org/help/tutorials/spriting/)


./wsgi/project/manage.py syncdb
./wsgi/project/manage.py migrate
./wsgi/project/manage.py migrate persona
./wsgi/project/manage.py migrate


docker build -t garciadiazjaime/admin-contakto .
docker run -d -p 49164:8000 garciadiazjaime/admin-contakto
docker push garciadiazjaime/admin-contakto
docker pull garciadiazjaime/admin-contakto