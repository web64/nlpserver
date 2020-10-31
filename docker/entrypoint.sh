#!/bin/bash
/usr/bin/supervisord -n -c /etc/supervisor/supervisord.conf
supervisorctl reread
supervisorctl update
supervisorctl start nlpserver 