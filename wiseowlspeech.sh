#!/bin/bash
cd $1

# track on git
git add .
git commit -m "Auto commit on $(date +'%Y-%m-%d %H:%M:%S')"
git push

# rsync to remote server
rsync -avz -e "ssh -i ~/.ssh/fredpret.net" ./ fred@valustox:/var/www/html/wiseowlspeech.com/