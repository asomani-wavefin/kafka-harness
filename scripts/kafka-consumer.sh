#!/bin/bash

#
# Helper script to run consumer CLI
#
# Examples:
#   ./kafka-consumer.sh             # Run the consumer CLI to display help information
#   ./kafka-consumer.sh             # Run the consumer CLI to display help information
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
CMD=( python3 -m consumer)
CMD+=(${OPT_REMAINDER[@]})

# Execute the command
pushd $project_home
eval "${CMD[@]}"
popd
