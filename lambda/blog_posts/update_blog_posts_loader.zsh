#!/bin/zsh

# cleanup
rm function.zip
cd requirements
rm -r __pycache__

# make new zip
zip -r ../function.zip .
cd ..
raco exe -o parser --orig-exe gdoc_body_parser/main.rkt
zip -g function.zip parser blog_posts.py gkey.py gdrive.py
aws lambda update-function-code --function-name load_blog_posts --zip-file fileb://function.zip
