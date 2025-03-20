# AIContentCreator
AI-Powered Content Curation for Small Businesses 

## Pain Point:
- Small businesses lack time, resources, and expertise to consistently create engaging social media content.

## Solution:
- An AI tool that generates post ideas, curates content, and schedules posts for selected platforms.

## Backend:
### Developing:
- If you need to add dependencies, you must create a local python virtual environment, make sure it has everything installed from `requirements.txt`
    - Then, after installing your new dependancy with the virtual environment, run `pip freeze > requirements.txt` to output the python dependancies for the docker to read off of
- To run the backend, run `docker compose up -d` and then `docker compose exec flask python backend.py` to run the local development server
### Backend technical description:
- Framework: Flask
- Dependencies: This project will use `Flask`, `Flask-SQLAlchemy`, and `Flask-Migrate`
- Database: PostgresSQL