augroup filetypedetect
au BufNewFile,BufRead *.json        setf javascript
au BufNewFile,BufRead *.json-schema setf javascript
au BufNewFile,BufRead *.md          setf markdown
augroup END
