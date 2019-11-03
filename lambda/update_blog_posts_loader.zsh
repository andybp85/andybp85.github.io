#!/bin/zsh

cd blog_posts
raco exe -o parser --orig-exe gdoc_body_parser/main.rkt
rm function.zip
cd requirements
rm -r *.dist-info __pycache__
zip -r ../function.zip .
cd ..
zip -g function.zip application blog_posts.py gkey.py gdrive.py
aws lambda update-function-code --function-name load_blog_posts --zip-file fileb://function.zip
