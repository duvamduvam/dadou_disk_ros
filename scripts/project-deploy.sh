#!/bin/bash

####################### PROJECT PARAMS #############################

export PROJECT_NAME="hardrive"
export PROJECT_PATH=~/Nextcloud/Didier/python/dadou_disk/

export USER_HOST="d"
export ROOT_HOST="dr"
export RPI_HOST_NAME="disk.local"

export INSTALL_LIB="yes"
#export SET_USB_AUDIO="yes"
#export ACTIVATE_I2C="yes"
export SET_BASHRC="yes"
export SET_VIMRC="yes"
export INSTALL_SERVICE="yes"
#export INSTALL_AUTOSTART="yes"
export SERVICE_NAME="disk"
export LOG_FILE="disk.log"

export PROJECT_SYSTEM_LIB=
export PROJECT_PYTHON_LIB="adafruit_ssd1306"

####################################################################

export RPI_HOME=/home/didier
export LOCAL_HOME=~

export UTILS_PROJECT=$LOCAL_HOME/Nextcloud/Didier/python/dadou_utils
export UTILS_SCRIPTS=$UTILS_PROJECT/scripts/deploy

declare -A PROJECT_DEPENDENCIES
PROJECT_DEPENDENCIES[0]=$LOCAL_HOME/Nextcloud/Didier/python/dadou_robot/dadourobot
PROJECT_DEPENDENCIES[1]=$UTILS_PROJECT
export PROJECT_DEPENDENCIES
#printf "$PROJECT_DEPENDENCIES[@]"

if [ "$1" = "read_param" ]; then
  printf "${CYAN}Only read param${CYAN}\n"
  if [ -d "$RPI_SCRIPTS" ]; then
    printf "$RPI_SCRIPTS/params.sh\n"
  fi
  if [ -d "$UTILS_SCRIPTS" ]; then
    printf "$UTILS_SCRIPTS/params.sh\n"
  fi
else
  source $UTILS_SCRIPTS/deploy-utils.sh $1
fi
