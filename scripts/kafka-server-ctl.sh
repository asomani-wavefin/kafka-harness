#!/bin/bash

#
# Script to launch kafka-server deployment.
#
# Examples:
#   ./kafka-server-ctl.sh             # Start the kafka-server stack
#   ./kafka-server-ctl.sh up -d       # Run kafka-server stack in the background (detached)
#   ./kafka-server-ctl.sh down        # Stop the kafka-server stack
#

# Find project home folder
f () { [[ -d ".git" ]] && echo "`pwd`" && exit 0; cd .. && f; }
project_home=$(f)

# Directory locations
ks_deploy="$project_home/deploy/kafka-server"
ks_tmp="$project_home/tmp/kafka-server"

# Set command variables
SUBCMD="${1:-up}"
shift 1
OPT_REMAINDER="${@:-}"

# Create tmp folders if they don't already exist
# ks_tmp_folders=(.)
# for f in "${ks_tmp_folders[@]}"
# do
#   if [ ! -d "$ks_tmp/$f" ]
#   then
#     mkdir -p "$ks_tmp/$f"
#   fi
# done

# Compose the command
CMD=( docker compose )
CMD+=(--file "$ks_deploy/docker-compose.yml")
CMD+=(--project-name kafka_server)
CMD+=(--project-directory "$ks_deploy")
CMD+=("$SUBCMD") 
CMD+=(${OPT_REMAINDER[@]})

# Execute the command
eval "${CMD[@]}"
