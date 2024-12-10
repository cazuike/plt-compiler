#!/bin/bash

compile() {
    local input=$1
    local output=$2
    if [ ! -f "$input" ]; then
        echo "file not found"
        exit 1
    fi
    echo "Stage 1: Lexing..."
    python3 scanner.py "$input"
    if [ $? -ne 0 ]; then
        echo "unable to lex. "
        exit 1
    fi
    echo "Stage 2: Parsing..."
    python3 my_parser.py "$input"
    if [ $? -ne 0 ]; then
        echo "unable to parse :9"
        exit 1
    fi
    echo "Stage 3: Code Gen..."
    python3 code_gen.py "$input" "$output"
    if [ $? -ne 0 ]; then
        echo "code gen stage failed"
        exit 1
    fi
    echo "Executing Generated code..."
    python3 "$output"
    if [ $? -ne 0 ]; then
        echo "failed to execute code :("
        exit 1
    fi
    echo "Everything is a success!"
}

if [ "$1" == "test" ]; then
    compile "codegen_examples/example1.inc" "generated_program1.py"
    compile "codegen_examples/example2.inc" "generated_program2.py"
    compile "codegen_examples/example3.inc" "generated_program3.py"
    compile "codegen_examples/example4.inc" "generated_program4.py"
    compile "codegen_examples/example5.inc" "generated_program5.py"
else
    compile "$1" "$2"
fi
