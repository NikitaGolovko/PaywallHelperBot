#!/bin/sh
cd "$(dirname "$0")";
CWD="$(pwd)"

#Log/output current directory
echo $CWD

#Execute main script
python main.py