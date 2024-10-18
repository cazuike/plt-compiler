#!/bin/bash

lex() {
    local input=$1
    if [ ! -f "$input" ]; then
        echo "file not found"
        exit 1
    fi
    echo "lexing"
    python3 scanner.py "$input"
    echo ""
}

if [ "$1" == "test" ]; then
    lex "example1.inc"
    lex "example2.inc"
    lex "example3.inc"
    lex "example4.inc"
    lex "example5.inc"
else
    lex "$1"
fi
