#!/bin/bash
# Shell script to run python job

PID = `pgrep -f 'schedule_job.py'`  # To check if the same script is already running

if [[-n $PID]]; then
  echo "schedule_job.py is running" >> schedule_job.log >&1

else
  echo "Starting schedule_job.py" >> schedule_job.log
  source .application-vars/local && python schedule_job.py >> schedule_job.log 2>&1