#!/bin/bash

file="test2.sh"
if [ -f "$file" ]
then
	echo "$file found."
  source test2.sh
else
	echo "$file not found."
fi
