#!/bin/bash

if [[ $1 = "--uninstall" ]]; then
    echo "Uninstall NEOM";
    chmod 644 NEOM.py Protocol.py Select_Server.py Select_Client.py;
    if find tmp >/dev/null 2>/dev/null; then
        echo "  Removing tmp folder"
        rm -rf tmp;
    fi;
    if find keys/neom_users.pic.tz >/dev/null 2>/dev/null; then
        echo "  Removing users file"
        rm keys/neom_users.pic.tz
    fi;
    exit 0
fi;


echo "Install NEOM";

if [[ $1 = "--server" ]]; then
    echo "Server installation";
    chmod 544 Select_Server.py;
    chmod 444 Protocol.py Select_Client.py NEOM.py;

    echo "  Setting up enviroment"
    python -c 'from Protocol import createUserFile; createUserFile("neom_users", "neom", path="./keys")'
else
    echo "Client installation";
    chmod 544 NEOM.py;
    chmod 444 Protocol.py Select_Client.py Select_Server.py;

    echo "  Setting up enviroment"
    if ! find tmp >/dev/null 2>/dev/null; then
        mkdir tmp;
    fi;
    for arg in "$@"; do
        echo
        if [[ $arg = "--no-pkg" ]]; then
            echo "  Won't install any modules";
        else
            echo "  Installing python modules";
            #sudo apt-get PyQt4;
            #pip install emoji --upgrade;
        fi;
    done;
fi;

