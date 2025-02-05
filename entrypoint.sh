#!/bin/sh
pwd

cd ../..

ls -a

echo "config is " $1
echo "multiple crates:" $2
echo "Release_management:" $3
echo "Release_versioning:" $4
echo "Include draft:" $5
echo "draft folder name:" $6
echo "index html:" $7
echo "theme:" $8
echo "space-to-pages-homepage adress:" $9

#echo repo name that called this action
echo "repo name is " $GITHUB_REPOSITORY

#tree -a ./src

#perform a tree on the github workspace
#tree -a ./github/workspace

#make a folder in ./src called data
mkdir ./src/data

#copy all files from ./github/workspace to  ./src/data including hidden files
rsync --recursive --progress -avzh ./github/workspace/* ./src/data
#copy the .git folder from ./github/workspace to ./src/data
rsync --recursive --progress -avzh ./github/workspace/.git ./src/data/

#install all requirements
pip install -r requirements.txt

#echo "files in ./src/data"
#tree -a ./src/data

#run the python script
cd src/
python main.py $GITHUB_REPOSITORY $2 $3 $4 $5 $6 $7 $8 $9
cd ..

# Fetch the navigation.html file
curl -o ./src/templates/navigation.html "${9}/navigation.html"

# Extract the necessary parts from navigation.html and insert them into index.html
awk '/<head>/,/<\/head>/' ./src/templates/navigation.html | sed '1d;$d' > /tmp/nav_head.tmp
awk '/<body>/,/<\/body>/' ./src/templates/navigation.html | sed '1d;$d' > /tmp/nav_body.tmp

# Insert the extracted parts into index.html
sed -i "/<!-- Navigation styles and scripts will be inserted here -->/r /tmp/nav_head.tmp" ./src/templates/index.html
sed -i "/<!-- Navigation script will be inserted here -->/r /tmp/nav_body.tmp" ./src/templates/index.html

# Clean up temporary files
rm /tmp/nav_head.tmp /tmp/nav_body.tmp

#make a folder in ./github/workspace called unicornpages
mkdir ./github/workspace/unicornpages

pwd

#echo all files from ./src/build
#echo "files in ./src/build"
#tree -a ./src/build

#copy over all files from ./src/data to ./github/workspace/unicornpages with rsync except for the .git folder
rsync --recursive --progress --exclude '.git' ./src/build/* ./github/workspace/unicornpages

#list everything that is in unicornpages
ls -a ./github/workspace/unicornpages
