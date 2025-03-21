# AIContentCreator
AI-Powered Content Curation for Small Businesses 

## Pain Point:
- Small businesses lack time, resources, and expertise to consistently create engaging social media content.

## Solution:
- An AI tool that generates post ideas, curates content, and schedules posts for selected platforms.

## How To Use:
- First install docker using the offical [install script](https://github.com/docker/docker-install/?tab=readme-ov-file)
- OPTIONAL: To add permissions to run docker without needing `sudo`, you'll need to add permissions. Refer to this [link](https://docs.docker.com/engine/install/linux-postinstall/). This is necessary for getting VSCode to connect to docker containers.
    - For me I actually had to restart my laptop to get changes to reflect for VSCode, even though they say you have to just log out and log in.
- Then clone this repo and `cd` into the directory
- Then run `docker compose build`
- Then run `docker compose up -d`
    - This will get the dockers running without any output from them
    - To see the output from the dockers in realtime you can run the command `docker compose logs -f`
    - To shutdown the dockers use `docker compose down`
- Now follow these steps for getting the database schema updated
    - run `docker compose exec flask flask db migrate`
    - run `docker compose exec flask flask db stamp head`
    - run `docker compose exec flask flask db upgrade`
    - the database schema should be up to date now
- To get the website running, run `docker compose exec flask python backend.py` and then you can access the website at [http://localhost:5017/](http://localhost:5017/).
- To turn off the website, run `docker compose down` in the project root directory.
## Backend technical description:
- Framework: Flask
- Dependencies: This project will use `Flask`, `Flask-SQLAlchemy`, and `Flask-Migrate`
- Database: PostgresSQL