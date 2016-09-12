set flp=\\v^\\s*[[(]?(\\d+\|\\a\|[IiVvXxLlCcDdMm]+)[]:.)]\\s+
set com^=s1:#\|,mb:\|,ex:\|#,b:--,b:#:,n:# com+=b:!,b:\",b:;,b:\\
set ai bs=2 nocp cpo+=M enc=utf-8 fcl=all fo+=n ic lcs+=tab:‣‧,trail:‧ ml mls=1
set mps+=<:> ru ruf=%l:%c sc scs sw=1 ww=h,l,[,]

au BufNewFile,BufRead *.{json,md,pl,pm,py,sh,yml} setl et sts=4
au BufNewFile,BufRead .{bashrc,profile} setl et sts=4

" This is for files whose filetypes are determined via #! lines (only enabled
" when syntax hilighting is on):
au FileType python,perl,sh setl et sts=4

dig uh 601 y- 563 Y- 562 zh 658 sh 643 dh 240 DH 208 !? 8253 :: 776
dig ^1 185 ^2 178 ^3 179 ^4 8308 ^5 8309 ^6 8310 ^7 8311 ^8 8312 ^9 8313 ^0 8304
dig ^n 8319 ^+ 8314 ^- 8315
dig _1 8321 _2 8322 _3 8323 _4 8324 _5 8325 _6 8326 _7 8327 _8 8328 _9 8329
dig _0 8320 _+ 8330 _- 8331
dig NN 8469 ZZ 8484 QQ 8474 RR 8477 CC 8450 HH 8461 PP 8473
dig && 8743 \|\| 8744 !! 172 ^^ 8853 (< 10216 >) 10217 (/ 8713 x\| 8906
dig NE 8708 ~= 8773 ~~ 8776 T^ 8868 \|- 8866 v\| 8595 ^\| 8593 \\ 8726 dx 10799
dig _. 8228 .. 8230 )< 8828

map s 24j|map S 24k
"map s <C-F>zz|map S <C-B>zz
map W <C-W>w
map \- :exe "normal " . (81-col("$")) . "A-\e"<CR>
map \= :exe "normal " . (81-col("$")) . "A=\e"<CR>
cmap <C-A> <C-B>

let loaded_matchparen=1
"syntax off

hi String ctermfg=DarkBlue
hi! link Character String
hi Number ctermfg=DarkRed
hi! link Float Number
hi Special ctermfg=DarkRed
hi Operator ctermfg=DarkRed
hi Function ctermfg=DarkRed
hi Boolean ctermfg=DarkGreen
hi Constant ctermfg=DarkGreen
hi! link Structure Label
