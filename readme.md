# Movie Searcher Backend
## Installation

### Pre requisites
python 3.8+
pip

### Clone repo

``` bash
# clone the repo
$ git clone https://github.com/0rdep/movie-searcher-backend.git

# go into app's directory
$ cd movie-searcher-backend

# install app's dependencies
$ pip install -r requirements.txt

# create database 
$ python manage.py migrate

# create admin user
$ python manage.py createsuperuser

# dev server at http://localhost:8000
$ python manage.py runserver
```