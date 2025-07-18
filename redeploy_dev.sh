#!/bin/bash

sudo docker compose down -v
source build_and_push.sh
sudo docker compose up -d
