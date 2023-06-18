#!/bin/bash

source no-webp_env/bin/activate

if [ ! -d no-webp_env/lib/python3.10/site-packages/watchdog ]; then
	pip install watchdog
fi

if [ ! -d no-webp_env/lib/python3.10/site-packages/yaml ]; then
	pip install pyyaml
fi

python3 src/main.py
