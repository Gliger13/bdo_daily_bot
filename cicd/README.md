# Daily Discord Bot BDO
## Bot deployment
This repository contains docker configuration, scripts and information for deploy Daily Discord Bot on a linux instance.

### How to deploy bot in Docker
1. Using bot_deployer script
2. Using docker-compose commands
3. Using https://hub.docker.com/
4. Using whatever you want


### Using bot_deployer script
- Download script from git repository via wget or curl:
    ```bash
    wget https://raw.githubusercontent.com/Gliger13/bdo_daily_bot/master/bot_deployment/bot_deployer.sh
    ```
- Install bot_deployer script
    ```bash
    bash bot_deployer.sh install
    ```
- Create single file with name **secrets.py**.
  PRODUCTION_TOKEN is discord access token for connect to your bot.
  PRODUCTION_BOT_ID is discord id of your bot.
  DB_STRING - string for connect to mongo database, can be localhost.
  Example of content of **secrets.py**:
    ```text
    PRODUCTION_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cf.df.dfa.das.d"
    PRODUCTION_BOT_ID = 324528465682366468
    DB_STRING = "mongodb://localhost:27017"
    ```
- Run build command and bot will be deployed
    ```bash
    bot_deployer build
    ```

#### Available command to manage container with bot in it:
- To start bot in the container run:
    ```bash
    bot_deployer start
    ```
- To stop bot in the container run:
    ```bash
    bot_deployer stop
    ```
- To down bot in the container run:
    ```bash
    bot_deployer down
    ```
- To update bot in the container run:
    ```bash
    bot_deployer build
    ```

### Using docker-compose
- Download git repository
    ```bash
    git clone git@github.com:Gliger13/bdo_daily_bot.git
    ```
- Fill file **bdo_daily_bot/bot/settings/secrets.py** with your secrets.
  PRODUCTION_TOKEN is discord access token for connect to your bot.
  PRODUCTION_BOT_ID is discord id of your bot.
  DB_STRING - string for connect to mongo database, can be localhost.
  Example of content of **secrets.py**:
    ```text
    PRODUCTION_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cf.df.dfa.das.d"
    PRODUCTION_BOT_ID = 324528465682366468
    DB_STRING = "mongodb://localhost:27017"
    ```
- Copy docker configurations to working directory:
    ```bash
    cp bdo_daily_bot/bot_deployment/{Dockerfile,docker-compose.yml} ./
    ```
- Run docker-compose build to end deployment
    ```bash
    docker-compose build
    ```
#### Basic docker-compose commands to managing container
- To start bot run command
    ```bash
    docker-compose start
    ```
- To stop bot run command
    ```bash
    docker-compose stop
    ```
- To down bot container run
    ```bash
    docker-compose down
    ```
- To update bot run all previous steps
