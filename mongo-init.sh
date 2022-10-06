#!/bin/bash
set -e;


if [ -n "${MONGO_INITDB_USERNAME:-}" ] && [ -n "${MONGO_INITDB_PASSWORD:-}" ]; then
	mongosh "$MONGO_INITDB_DATABASE" <<-EOJS
		db.createUser({
			user: $(_js_escape "$MONGO_INITDB_USERNAME"),
			pwd: $(_js_escape "$MONGO_INITDB_PASSWORD"),
			roles: [ { role: 'readWrite', db: $(_js_escape "$MONGO_INITDB_DATABASE") } ]
			})
	EOJS
else
  true
	# print warning or kill temporary mongo and exit non-zero
fi