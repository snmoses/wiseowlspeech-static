#!/bin/bash
#echo "$(date +'%Y-%m-%d %H:%M:%S'): Starting script in directory $1" >> /Users/fred/localdev/bootstrap-studio-export/log.log

#cd $1

#echo "$(date +'%Y-%m-%d %H:%M:%S'): Adding changes to git" >> /Users/fred/localdev/bootstrap-studio-export/log.log

# track on git
#git add .
#git commit -m "Auto commit on $(date +'%Y-%m-%d %H:%M:%S')" >> /Users/fred/localdev/bootstrap-studio-export/log.log 2>&1
#git push >> /Users/fred/localdev/bootstrap-studio-export/log.log 2>&1

#echo "$(date +'%Y-%m-%d %H:%M:%S'): Git push done" >> /Users/fred/localdev/bootstrap-studio-export/log.log

#echo "$(date +'%Y-%m-%d %H:%M:%S'): Starting rsync" >> /Users/fred/localdev/bootstrap-studio-export/log.log

# rsync to remote server
#rsync -avz -e "ssh -i ~/.ssh/fredpret.net" ./ fred@valustox:/var/www/html/wiseowlspeech.com/
#echo "$(date +'%Y-%m-%d %H:%M:%S'): Rsync done" >> /Users/fred/localdev/bootstrap-studio-export/log.log

# put this script in your Bootstrap Studio export folder; make it executable and give it to Bootstrap Studio to run after exporting your page

#!/bin/bash
django_template_directory="/Users/fred/localdev/wiseowlspeech.com/cms/templates/cms"
static_file_directory="/Users/fred/localdev/wiseowlspeech.com/cms/static/cms/assets"
chart_json_path=""
log_path="/Users/fred/localdev/bootstrap-studio-export/log.log"
appname="cms"
python_script_path="/Users/fred/localdev/django-template-builder/create-django-template.py"

# clear logs
rm $log_path
touch $log_path
echo "$(date +'%Y-%m-%d %H:%M:%S'): Starting script in directory $1" >> $log_path

# move assets
cd $1
rsync -av assets/* "$static_file_directory"
echo "$(date +'%Y-%m-%d %H:%M:%S'): rsync from $1/assets/* to $static_file_directory done" >> $log_path

# move HTML files
cd $1
rsync -av *.html "$django_template_directory"
echo "$(date +'%Y-%m-%d %H:%M:%S'): rsync from $1/*.html to $django_template_directory done" >> $log_path

# run processing script
cd $django_template_directory

# set up command 
command="/usr/local/bin/python $python_script_path "

# add app-name
if [ $appname=="" ]; then
    echo "$(date +'%Y-%m-%d %H:%M:%S'): no app name" >> "$log_path"
else
    echo "$(date +'%Y-%m-%d %H:%M:%S'): app name: $appname" >> "$log_path"
    command+=" -n $appname "
fi

# add directories
command+=" -n cms -hd $django_template_directory -a "

# check if a chart json path was specified
if [ -z "$chart_json_path" ]; then
    # chart_json_path is empty; leave command as is
    echo "$(date +'%Y-%m-%d %H:%M:%S'): no chart json path" >> $log_path
else
    # chart json path specified
    echo "$(date +'%Y-%m-%d %H:%M:%S'): chart json path: $chart_json_path" >> $log_path
    command+=" -c $chart_json_path"
fi

# check if static file path = template_path + '/assets' (the default config) or if it's hosted elsewhere (like through Nginx)
if [ "$static_file_directory"=="$django_template_directory/assets" ]; then
    echo "$(date +'%Y-%m-%d %H:%M:%S'): static files in root directory" >> $log_path
else
    echo "$(date +'%Y-%m-%d %H:%M:%S'): static file dir: $static_file_directory " >> $log_path
    command+=" -a"
fi

echo "command: $command" >> "$log_path"

# run command to process HTML files
python_output=$(eval $command)
echo "$python_output" >> "$log_path"

# run command to minify CSS and JS files
#command="/usr/local/bin/python $python_script_path -sd $static_file_directory"
#python_output=$(eval $command)
#echo "$python_output" >> "$log_path"

echo "$(date +'%Y-%m-%d %H:%M:%S'): python template update complete" >> $log_path
