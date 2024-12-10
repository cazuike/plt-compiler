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
    lex "lexer_examples/example1.inc"
    lex "lexer_examples/example2.inc"
    lex "lexer_examples/example3.inc"
    lex "lexer_examples/example4.inc"
    lex "lexer_examples/example5.inc"
else
    lex "$1"
fi
