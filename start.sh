#!/bin/bash

projectDir=$(cd $(dirname $0); pwd)
cd $projectDir/confessions-client
#ng build --prod --output-path $projectDir/confessions-rest/rest/static/ang --output-hashing none

cd $projectDir/confessions-rest
gunicorn confessions_rest.wsgi