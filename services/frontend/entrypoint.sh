#!/bin/sh

cd /usr/src/app
ls
echo "Before serve"
ng serve --host 0.0.0.0
echo "After serve"
