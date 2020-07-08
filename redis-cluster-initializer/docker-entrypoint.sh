#!/bin/bash
set -e

# starting redis server so that we can run redis create cluster command from python script.
redis-server --daemonize yes

if [ $# -eq 0 ]; then
    exec python3 main.py
else
	exec python3 "$@"
fi

exec "$@"