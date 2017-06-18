#!/bin/bash

if [[ $1 = "--uninstall" ]]; then
    echo "Uninstall NEOM";
    chmod 644 NEOM.py Protocol.py Protocol.pyc;
    rm -rfi tmp
    exit 0
fi;


echo "Install NEOM";

if [[ $1 = "--server" ]]; then
    echo "Server installation";
    # chmod 544 Server.py;
    chmod 444 Protocol.py Protocol.pyc;
else
    echo "Client installation";
    # chmod 544 Client.py;
    chmod 444 Protocol.py Protocol.pyc;
fi;

echo "Installing python modules";
#sudo apt-get PyQt4;
#pip install emoji --upgrade;

echo "Setting up enviroment"
mkdir tmp
