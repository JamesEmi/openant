#!/bin/bash

chronyc sources
lsusb
cd /triage/james/openant/ant
sudo udevadm control --reload-rules && sudo udevadm trigger
openant scan

