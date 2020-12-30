#!/usr/bin/env bash


if [ "$1" == "" ]
then
    echo "Where is the argument"
else
    echo "Move along nothing to see here"
fi


Dupa=$1

echo $Dupa

echo ${Dupa/mała/duża}

case "$Variable" in
    #List patterns for the conditions you want to meet
    0) echo "There is a zero.";;
    1) echo "There is a one.";;
    *) echo "It is not null.";;
esac
