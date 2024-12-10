#!/bin/bash

parse() {
    local input=$1
    if [ ! -f "$input" ]; then
        echo "file not found"
        exit 1
    fi
    echo "parsing"
    python3 my_parser.py "$input"
    echo ""
}

if [ "$1" == "test" ]; then
    parse "parser_examples/example1.inc"
    parse "parser_examples/example2.inc"
    parse "parser_examples/example3.inc"
    parse "parser_examples/example4.inc"
    parse "parser_examples/example5.inc"
else
    parse "$1"
fi
