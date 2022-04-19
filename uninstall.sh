#!/bin/bash

# Exit if something fails
set -e

rm  ~/.local/share/kservices5/plasma-runner-libvirt.desktop
rm  ~/.local/share/dbus-1/services/plasma-runner-libvirt.service
rm  ~/.local/bin/plasma-runner-libvirt.py

kquitapp5 krunner
