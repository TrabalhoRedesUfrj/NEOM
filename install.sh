#!/bin/bash

if [[ $1 = "--uninstall" ]]; then
    echo "Uninstall NEOM";
    chmod 644 NEOM.py Protocol.py Select_Server.py Select_Client.py;
    if find tmp >/dev/null 2>/dev/null; then
        echo "  Removed tmp folder"
        rm -rf tmp;
    fi;
    exit 0
fi;


echo "Install NEOM";

if [[ $1 = "--server" ]]; then
    echo "Server installation";
    chmod 544 Select_Server.py;
    chmod 444 Protocol.py Select_Client.py NEOM.py;
else
    echo "Client installation";
    chmod 544 NEOM.py;
    chmod 444 Protocol.py Select_Client.py Select_Server.py;

    echo "Setting up enviroment"
    mkdir tmp
fi;

echo "Installing python modules";
#sudo apt-get PyQt4;
#pip install emoji --upgrade;
