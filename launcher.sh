#!/bin/bash

cd /home/rotor/rotor/

python3 all_on.py
python3 rotor.py >/home/rotor/rotor/logs/cronlog 2>&1
