#!/bin/sh
pwd

cd ../..

ls -a

echo "config is " $1

#echo repo name that called this action
echo "repo name is " $GITHUB_REPOSITORY

#echo all files in tree 
tree -a

#perform a tree on the github workspace
tree -a ./github/workspace

#check if config file exists
if [ -f ./github/workspace/config.yml]
then
    echo "config file exists"
else
    echo "config file does not exist"
    #exit 1
    exit 1
fi

#make a folder in ./src called data
mkdir ./src/data

#copy all files from ./github/workspace to  ./src/data
cp -r ./github/workspace/* ./src/data

#install all requirements
pip install -r requirements.txt

#run the python script
python ./src/main.py

#make a folder in ./github/workspace called unicornpages
mkdir ./github/workspace/unicornpages

#copy over all files from ./src/data to ./github/workspace/unicornpages with rsync
rsync --recursive --progress ./src/data/* ./github/workspace/unicornpages

#list everything that is in unicornpages
ls -a ./github/workspace/unicornpages
