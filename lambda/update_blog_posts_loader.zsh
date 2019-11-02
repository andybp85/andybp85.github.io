#!/bin/zsh

cd blog_posts
raco exe --orig-exe application.rkt
rm function.zip
zip function.zip application blog_posts.py gkey.py
aws lambda update-function-code --function-name load_blog_posts --zip-file fileb://function.zip
