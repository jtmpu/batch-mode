#!/bin/bash 

echo "Setting up bin links"
sudo ln -f -s $(pwd)/batch-mode.py /usr/bin/batch-mode
echo "done."
