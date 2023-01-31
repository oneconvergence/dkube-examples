#!/bin/bash
set -e

if [ "$EVENT" = "schemagen" ]; then
    python schemagen.py

elif [ "$EVENT" = "fit" ]; then
    python fit.py

elif [ "$EVENT" = "data-drift" ]; then
    python data_drift.py

else
    echo "$0:${LINENO} error: Event not recognized " | tee -a ${MM_HOME}/out.log
    exit 1
fi
