# Time Capsule WebApp

A fun app to send a message, forget about it, and then hear from yourself or others in 5 years (or any user chosen time frame)!  

---


## Features

- Write messages and schedule email delivery to yourself within a future time frame  
- Simple but effective user interface for composing, viewing scheduled messages  
- Social media like user interface where users can search and add friends
- Group messages allow groups to receive future messages from the whole group

---

## Tech Stack

- **Backend / Web Framework**: Django
- **Database**: SQLite
- **Frontend / Static files**: HTML, CSS 

---

## Youtube Demonstration

- https://youtu.be/twkvc0JzkjY

---

## Setup

If you wish, below are the typical steps to get this project running locally:

```bash
# clone the repo
git clone https://github.com/milozg/time-capsule-webapp.git
cd time-capsule-webapp

# create & activate virtual environment
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# install dependencies
pip install -r requirements.txt   # or use `pipenv install` if using pipfile

# apply migrations
python manage.py migrate

# (Optional) create a superuser if needed
python manage.py createsuperuser

# run the development server
python manage.py runserver
