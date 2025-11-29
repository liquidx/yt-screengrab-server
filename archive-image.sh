#!/bin/bash
# Making tar file for portainer.

tar cvf ../yt-screengrab-server.tar --no-xattrs --exclude .venv --exclude .git --exclude __pycache__
