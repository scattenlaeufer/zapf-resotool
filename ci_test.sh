#!/usr/bin/sh

celery multi start zapf_resotool_test -A reso_mail --loglevel=info
py.test -v
celery multi stopwait zapf_resotool_test
