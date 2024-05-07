#!/bin/bash
echo "Starting script in directory $1" >> /Users/fred/localdev/bootstrap-studio-export/log.log

cd $1

echo "Adding changes to git" >> /Users/fred/localdev/bootstrap-studio-export/log.log

# track on git
git add .
git commit -m "Auto commit on $(date +'%Y-%m-%d %H:%M:%S')" >> /Users/fred/localdev/bootstrap-studio-export/log.log 2>&1
git push >> /Users/fred/localdev/bootstrap-studio-export/log.log 2>&1

echo "Git push done" >> /Users/fred/localdev/bootstrap-studio-export/log.log

echo "Starting rsync" >> /Users/fred/localdev/bootstrap-studio-export/log.log

# rsync to remote server
rsync -avz -e "ssh -i ~/.ssh/fredpret.net" ./ fred@valustox:/var/www/html/wiseowlspeech.com/
echo "Rsync done" >> /Users/fred/localdev/bootstrap-studio-export/log.log
