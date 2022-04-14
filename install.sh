#!/bin/bash

# Exit if something fails
set -e

mkdir -p ~/.local/share/kservices5/
mkdir -p ~/.local/share/dbus-1/services/
mkdir -p ~/.local/bin/

cp "plasma-runner-libvirt.desktop"  ~/.local/share/kservices5/
cp "plasma-runner-libvirt.service" ~/.local/share/dbus-1/services/
cp "plasma-runner-libvirt.py" ~/.local/bin/

kquitapp5 krunner
