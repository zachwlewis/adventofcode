#!/bin/zsh

set -e
echo "Starting build of $( pwd; )/$1.cpp"
/usr/bin/clang++ -std=c++2a -stdlib=libc++ -fcolor-diagnostics -fansi-escape-codes -g $( pwd; )/$1.cpp -o $( pwd; )/out/$1
echo
echo Running $1
$( pwd; )/out/$1
