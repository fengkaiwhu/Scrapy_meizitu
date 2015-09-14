#!/bin/bash 
if [ $# != 1 ] ; then 
    echo "USAGE: $0 message"
    echo ""
    echo " e.g.: $0 'changed something'" 
    exit 1; 
fi 
git add --all
git commit -m $1
git push -u origin master
