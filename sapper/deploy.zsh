#!/bin/zsh
npx sapper export
rsync -r __sapper__/export/* ..

