#!/bin/bash
rm -rf build/html/*
mkdir -p build/html
cp -R img build/html/
cp -R src build/html/

for fullfile in ./*.md; do
  filename=$(basename -- "$fullfile")
  extension="${filename##*.}"
  filename="${filename%.*}"
  pandoc -s --toc --template=build/.pandoc/templates/uikit.html --metadata title="Python Backtesting & Trading Bot" "$filename".md -o build/html/"$filename".html
done

