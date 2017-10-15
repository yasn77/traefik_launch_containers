#!/bin/bash

set -e

case "$1" in
  "app-status")
    exec /usr/local/bin/gunicorn -w 8 -b 0.0.0.0:80 --log-file - --error-log - --access-logfile - app:app
    ;;
  *)
    exec "$@"
    ;;
esac
