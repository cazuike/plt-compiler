Name: Chidi Azuike ca2970


# Incurvus Compiler

## Introduction

The goal of this project is to tackle an existing problem in data by creating a domain-specific language (DSL) that simplifies the process of managing large datasets. Incurvus, the eponymous language named after the Latin word for distort, will manipulate data sets with ease while providing intuitive commands for normal data operations such as filtering, sorting, aggregating, transformation, and other ways of manipulating data sets. 

Incurvus is a domain-specific language (DSL) designed to simplify data manipulation tasks, especially when working with large datasets. The primary goal is to allow users—even those without extensive programming experience—to quickly gain mastery of the language and perform data operations with ease.

### Example Program

```incurvus
input! "data.csv"
groupby! department
aggregate! avg(salary)
output!  "output.csv"
```

This program loads data.csv, groups data by department, aggregates by average salary, and returns the manipulated csv in output.csv. Very easy to use to perform data manipulations and you don't even have to open the csv file to manually make changes! 

## Lexer/Scanner

The lexer/scanner tokenizes the input code into a sequence of tokens which will be used by the parser. 

Keywords:
input!
filter!
groupby!
aggregate!
sort!
combine!
multiply!
output!
shout!
delete!
rename!

```./lexer.sh test```
To run test results, and the results were saved here: https://github.com/cazuike/plt-compiler/blob/main/lexer_examples/lexer_test_results.txt

```
lexing
('KEYWORD', 'input!')
('STRINGLITERAL', '"sales-data.csv"')
('KEYWORD', 'filter!')
('IDENTIFIER', 'quantity')
('OPERATOR', '>')
('INTLITERAL', '100')
('KEYWORD', 'output!')
('STRINGLITERAL', '"filtered_sales.csv"')
```

## Parser

After lexing, the parser uses the tokens to construct Abstract Syntax Tree (AST) with our defined grammar. 

```
AST:
Program
  Input: data.csv
  Filter:
    Condition: quantity > 100 (type=INT)
  Output: output.csv
```

### Grammar for the language:

```
[Start]    - -- >  [Func]*;

[Func]      - - - > [Input]
  - - - >  [Filter]
- - - >  [GroupBy]
- - - >  [Aggregate]
- - - > [Sort]
  - - - >  [Combine]
  - - - >  [Multiply]
    - - - > [Delete]
     - - - >  [Rename]
           - - - > [Output]
       - - - >  [Shout];

[Input]   - - - >  "input!" STRINGLITERAL;

[Filter]  - - - >  "filter!" [Cond];

[Cond]        - - - >  IDENTIFIER [Operator] ([RightHandSide]);

[RightHandSide]    - - - >  IDENTIFIER
                    | INTLITERAL
                    | STRINGLITERAL;

[Operator]        - - - >  ">" | "<" | "=" | ">=" | "<=" | "==" | "!=";

[GroupBy]  - - - >  "groupby!" IDENTIFIER;

[Aggregate]  - - - >  "aggregate!" [AggList];

[AggList]          - - - >  [FuncCall] ("," [FuncCall])*;

[FuncCall]         - - - >  IDENTIFIER "(" IDENTIFIER ")";

[Sort]    - - - >  "sort!" [SortColumn] ("," [SortColumn])*;

[SortColumn]       - - - >  IDENTIFIER ( "asc" | "desc" )?;

[Combine]  - - - >  "combine!" STRINGLITERAL "mode" "=" ("vertical" | "horizontal");

[Multiply] - - - >  "multiply!" "factor" "=" (INTLITERAL );

[Delete]  - - - >  "delete!" "condition" "=" [Condition];

[Rename]  - - - >  "rename!" IDENTIFIER "=" IDENTIFIER;

[Output]  - - - >  "output!" STRINGLITERAL;

[Shout]   - - - >  "shout!" STRINGLITERAL;
```

Run ```./parser.sh test``` to test, outputs saved : https://github.com/cazuike/plt-compiler/blob/main/parser_examples/parser_test_results.txt

## Code Generation & Compiler Backend

Lastly, we have the code generation phase. To generate code, use ```./compiler.sh A B``` where A is the incurvus file you'd like to run and B is the python file you'd like to save the compiled code too. The command also executes the code which is generated, so users can perform transformations to various data files without even opening them! 

I have examples in code gen examples: https://github.com/cazuike/plt-compiler/tree/main/codegen_examples and you can run these examples through ```./compiler.sh test```. 


Demo videos 

https://github.com/user-attachments/assets/783812b5-0284-4279-8429-87f9be83fc23

I ran the test script and the test outputs are generated, which are manipulated csvs without ever needing to open one.

https://github.com/user-attachments/assets/2cbdb840-a39f-4ba5-8c58-aadd48c94f97



