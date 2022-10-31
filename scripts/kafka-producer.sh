#!/bin/bash

#
# Helper script to run producer CLI
#
# Examples:
#   ./kafka-producer.sh             # Run the producer CLI
#

# Find project home folder
f () { [[ -d ".git" ]] && echo "`pwd`" && exit 0; cd .. && f; }
project_home=$(f)

# Set command variables
OPT_REMAINDER="${@:-}"

if [ -z "$OPT_REMAINDER" ]; then
  OPT_REMAINDER=(--help)
fi

# Compose the command
CMD=( python3 -m producer)
CMD+=(${OPT_REMAINDER[@]})

# Execute the command
pushd $project_home
eval "${CMD[@]}"
popd
