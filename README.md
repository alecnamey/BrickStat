Backend
------------------------------------
* To run the backend there are several steps you need to do in order to make sure
the backend server runs properly locally via Docker.


* Make a .env file in project root directory like the following with BrickStat as Root:
  - BrickStat
    - app
    - readme
    - .gitignore
    - .env.example
    - .env            <-----------------  add this file and copy contents from .env.example into .env and change the API key


Backend sever startup via Docker:
1. Download Docker Desktop
  - hit settings,
  - type in 'integration',
  - select the option that says: "Enable integration with additional distros",
  - make sure the ubuntu is selected.

2. Build the dockerfile
  In the terminal in the folder where docker-compose.yml is located (usually in the root)
  * docker compose up --build --detatch

3. Run the dockerfile
  In the terminal in the folder where docker-compose.yml is located (usually in the root)
  * docker compose up

4. If you want to make updates to the code you need to ru nthe following command and redo steps 2 and 3.
  * docker compose down

* Note if a database needs changing, you need to run a different docker compose command
  * docker compose down -v


Frontend
---------------------------------------
TBD
