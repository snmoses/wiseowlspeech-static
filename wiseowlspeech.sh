#!/bin/bash
echo "$(date +'%Y-%m-%d %H:%M:%S'): Starting script in directory $1" >> /Users/fred/localdev/bootstrap-studio-export/log.log

cd $1

echo "$(date +'%Y-%m-%d %H:%M:%S'): Adding changes to git" >> /Users/fred/localdev/bootstrap-studio-export/log.log

# track on git
git add .
git commit -m "Auto commit on $(date +'%Y-%m-%d %H:%M:%S')" >> /Users/fred/localdev/bootstrap-studio-export/log.log 2>&1
git push >> /Users/fred/localdev/bootstrap-studio-export/log.log 2>&1

echo "$(date +'%Y-%m-%d %H:%M:%S'): Git push done" >> /Users/fred/localdev/bootstrap-studio-export/log.log

echo "$(date +'%Y-%m-%d %H:%M:%S'): Starting rsync" >> /Users/fred/localdev/bootstrap-studio-export/log.log

# rsync to remote server
rsync -avz -e "ssh -i ~/.ssh/fredpret.net" ./ fred@valustox:/var/www/html/wiseowlspeech.com/
echo "$(date +'%Y-%m-%d %H:%M:%S'): Rsync done" >> /Users/fred/localdev/bootstrap-studio-export/log.log
