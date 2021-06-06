#!/bin/bash
# Script that response for installing, building, starting and stopping docker
# container with bdo daily bot in it.

# ======================================================================
# Constants and settings

GIT_REMOTE_REPO_URL="https://github.com/Gliger13/bdo_daily_bot.git"
GIT_BRANCH="update"
GIT_CLONE_DST_FOLDER="bdo_daily_bot_src"

# ======================================================================
# Help function

function help() {
  echo "
Command management to deploy daily bdo bot using docker and stop/start created
container with bot.


Available commands:

bot_deployer install
Set script in user scripts directory and if not installed docker and
docker-compose then install them.

bot_deployer build
Download source code of the bdo daily bot and create docker container for him.

bot_deployer start
Start docker container with bot in it.

bot_deployer stop
Stop docker container with bot in it.

bot_deployer down
Remove docker container with bot in it.
"
}


# ======================================================================
# Common functions

function log() {
  echo "[Bot Deployer] $1"
}

# ======================================================================
# Installation functions

function check_and_install_docker() {
  # Check that docker is installed
  if [ ! -x "$(command -v docker)" ]
  then

    log "WARNING Docker not installed"
    read -p "$(log "Docker will be automatically installed, are you sure?")" \
         -n 1 -r; echo

    if [[ ! $REPLY =~ ^[Yy]$ ]]
    then
        exit 1
    else
      sudo apt-get install apt-transport-https ca-certificates curl gnupg lsb-releasedocker-ce
      curl -fsSL https://download.docker.com/linux/ubuntu/gpg |
           sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
      echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
           $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
      if sudo apt-get update && docker-ce docker-ce-cli containerd.io
      then
        log "Docker installed"
      else
        log "Docker not installed"
        exit 1
      fi
    fi

  fi
}


function check_and_install_docker_compose() {
  # Check that docker-compose is installed
  if [ ! -x "$(command -v docker-compose)" ]
  then
    log "WARNING docker-compose not installed"
    read -p "$(log "docker-compose will be automatically installed, are you sure?")" \
         -n 1 -r; echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]
    then
        exit 1
    else
      sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" \
           -o /usr/local/bin/docker-compose
      sudo chmod +x /usr/local/bin/docker-compose
      log "docker-compose installed"
    fi
  fi
}


function install() {
  log "Starting bot deployer script installation"

  user_scripts_directory_path="$HOME/.local/bin"
  if [[ ! -d $user_scripts_directory_path ]]
  then
    log "Creation user scripts directory in user home directory"
    mkdir -p "$user_scripts_directory_path"
    log "Adding new user scripts directory to PATH variable using .bashrc"
    echo "PATH=$PATH:$user_scripts_directory_path" >> "$HOME/.bashrc"
    source "$HOME/.bashrc"
  fi

  log "Copying bot deployer script in $user_scripts_directory_path"
  cp "$(realpath "$0")" "$user_scripts_directory_path/bot_deployer"
  chmod +x "$user_scripts_directory_path/bot_deployer"

  check_and_install_docker && check_and_install_docker_compose
  log "Bot deployer installation ended"
}


# ======================================================================
# Build functions


function build() {
  log "Starting bot building and updating"

  if [[ -d $GIT_CLONE_DST_FOLDER ]]
  then
    rm -rf $GIT_CLONE_DST_FOLDER
    log "Removed old directory with source code from git"
  fi

  if git clone --branch $GIT_BRANCH $GIT_REMOTE_REPO_URL $GIT_CLONE_DST_FOLDER
  then
    log "Source code of bdo daily bot downloaded from github"
  else
    log "ERROR Problem with downloading code from git"
    exit 1
  fi

  if cp -r $GIT_CLONE_DST_FOLDER/{bot,requirements.txt} ./ &&
     cp $GIT_CLONE_DST_FOLDER/bot_deployment/{Dockerfile,docker-compose.yml} ./
  then
    log "Bot source code is moved"
  else
    log "ERROR Problem with moving files"
    exit 1
  fi

  log "Creation directory for docker volume"
  mkdir bot_data 2>&1

  if [[ -f secrets.py ]]
  then
    log "Moving secrets.py to $GIT_CLONE_DST_FOLDER/bot/settings/secrets.py"
    cp secrets.py bot/settings/secrets.py
  else
    log "ERROR secrets.py not found in current directory"
    exit 1
  fi

  log "Starting building docker images and container"
  if docker-compose build
  then
    log "Bot build is successful"
  else
    log "ERROR Bot build is unsuccessful"
  fi
}

# ======================================================================
# Start functions

function start() {
  if docker-compose up -d
  then
    log "Bot is running"
  else
    log "ERROR Bot run failed"
  fi
}

# ======================================================================
# Stop functions

function stop() {
  if docker-compose stop
  then
    log "Bot stopped"
  else
    log "ERROR Failed to stop the bot"
  fi
}

# ======================================================================
# Down functions

function down() {
  if docker-compose down
  then
    log "Bot is down"
  else
    log "ERROR Failed to down the bot"
  fi
}

# ======================================================================
# Script choices

case "$1" in
  "install")
    install
  ;;
  "build")
    build
  ;;
  "start")
    start
  ;;
  "down")
    down
  ;;
  "stop")
    stop
  ;;
  "help" | "--help" | "-h" | *)
    help
  ;;
esac
