from ast_nodes import *
import sys
from scanner import IncurvusScanner
from my_parser import Parser
import time
from code_opt import optimize

class CodeGenerator:
    def __init__(self, ast_tree):
        self.ast = ast_tree
        self.code_lines = []
        self.indent = 0
        self.data = "data"

    def add_indent(self):
        return "    " * self.indent

    def generate(self):
        self.code_lines.append("import pandas as pd")
        self.code_lines.append("")
        self.code_lines.append("def main():")
        self.indent += 1

        for stmt in self.ast.statements:
            self.create_stmt(stmt)

        self.code_lines.append(self.add_indent() + "return")
        self.indent -= 1
        self.code_lines.append("")
        self.code_lines.append("if __name__ == '__main__':")
        self.code_lines.append("    main()")

        return "\n".join(self.code_lines)

    def create_stmt(self, stmt):
        if isinstance(stmt, InputNode):
            self.input_data(stmt)
        elif isinstance(stmt, FilterNode):
            self.filter_data(stmt)
        elif isinstance(stmt, GroupByNode):
            self.group_by(stmt)
        elif isinstance(stmt, AggregateNode):
            self.aggregate_data(stmt)
        elif isinstance(stmt, SortNode):
            self.sort_data(stmt)
        elif isinstance(stmt, CombineNode):
            self.combine_data(stmt)
        elif isinstance(stmt, MultiplyNode):
            self.multiply_data(stmt)
        elif isinstance(stmt, DeleteNode):
            self.delete_rows(stmt)
        elif isinstance(stmt, RenameNode):
            self.rename_column(stmt)
        elif isinstance(stmt, OutputNode):
            self.output_data(stmt)
        elif isinstance(stmt, ShoutNode):
            self.shout_message(stmt)
        else:
            self.error("Unknown statement type: " + str(type(stmt)))

    def input_data(self, stmt):
        self.code_lines.append(self.add_indent() + self.data + " = pd.read_csv('" + stmt.filename + "')")

    def filter_data(self, stmt):
        cond = self.build_condition(stmt.condition)
        self.code_lines.append(self.add_indent() + self.data + " = " + self.data + "[" + cond + "]")

    def group_by(self, stmt):
        self.code_lines.append(self.add_indent() + self.data + " = " + self.data + ".groupby('" + stmt.identifier + "')")

    def aggregate_data(self, stmt):
        agg_dict = {}
        func_map = {
            'sum': 'sum',
            'avg': 'mean',
            'count': 'count',
            'max': 'max',
            'min': 'min'
        }
        rename = {}

        for func, col in stmt.aggregations:
            if func not in func_map:
                self.error("Unsupported function: " + func)
            agg_func = func_map[func]
            agg_dict[col] = agg_func

            if func == 'avg':
                new_col = "avg_" + col
            elif func == 'sum':
                new_col = "total_" + col
            else:
                new_col = func + "_" + col
            rename[col] = new_col

        self.code_lines.append(self.add_indent() + self.data + " = " + self.data + ".agg(" + str(agg_dict) + ").reset_index()")
        if rename:
            self.code_lines.append(self.add_indent() + self.data + " = " + self.data + ".rename(columns=" + str(rename) + ")")

    def sort_data(self, stmt):
        cols = []
        asc = []
        for col, order in stmt.columns_orders:
            cols.append("'" + col + "'")
            if order == 'asc':
                asc.append("True")
            else:
                asc.append("False")
        cols_str = "[" + ", ".join(cols) + "]"
        asc_str = "[" + ", ".join(asc) + "]"
        self.code_lines.append(self.add_indent() + self.data + " = " + self.data + ".sort_values(by=" + cols_str + ", ascending=" + asc_str + ")")

    def combine_data(self, stmt):
        self.code_lines.append(self.add_indent() + "extra = pd.read_csv('" + stmt.filename + "')")
        if stmt.mode == "vertical":
            self.code_lines.append(self.add_indent() + self.data + " = pd.concat([" + self.data + ", extra], ignore_index=True)")
        elif stmt.mode == "horizontal":
            self.code_lines.append(self.add_indent() + self.data + " = pd.concat([" + self.data + ", extra], axis=1)")

    def multiply_data(self, stmt):
        self.code_lines.append(self.add_indent() + "numeric = " + self.data + ".select_dtypes(include=['number']).columns")
        self.code_lines.append(self.add_indent() + self.data + "[numeric] = " + self.data + "[numeric] * " + str(stmt.factor))

    def delete_rows(self, stmt):
        cond = self.build_condition(stmt.condition)
        self.code_lines.append(self.add_indent() + self.data + " = " + self.data + "[~(" + cond + ")]")

    def rename_column(self, stmt):
        self.code_lines.append(self.add_indent() + self.data + " = " + self.data + ".rename(columns={'" + stmt.old_name + "': '" + stmt.new_name + "'})")

    def output_data(self, stmt):
        self.code_lines.append(self.add_indent() + self.data + ".to_csv('" + stmt.filename + "', index=False)")

    def shout_message(self, stmt):
        self.code_lines.append(self.add_indent() + "print('" + stmt.message + "')")

    def build_condition(self, condition):
        left = condition.left_id
        op = condition.operator
        right = condition.right_val

        op_map = {
            "==": "==",
            "!=": "!=",
            ">": ">",
            "<": "<",
            ">=": ">=",
            "<=": "<=",
        }

        if op not in op_map:
            self.error("Unsupported operator: " + op)

        py_op = op_map[op]

        if condition.right_type == "STRING":
            right = "'" + right + "'"
        elif condition.right_type == "INT":
            right = right
        elif condition.right_type == "IDENTIFIER":
            right = self.data + "['" + right + "']"
        else:
            self.error("Unsupported condition type: " + condition.right_type)

        return self.data + "['" + left + "'] " + py_op + " " + right

    def error(self, msg):
        print("Code Generation Error: " + msg)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Incorrect args provided.")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]


    with open(input_file, "r") as f:
        content = f.read()


    scanner = IncurvusScanner(content)
    scanner.exec()
    tokens = scanner.get_tokens()

    parser = Parser(tokens)
    ast_tree = parser.parse()
    optimizer = optimize(ast_tree)
    optimized_ast = optimizer.optimize()

    generator = CodeGenerator(ast_tree)
    code = generator.generate()

    with open(output_file, "w") as f:
        f.write(code)
    
    generator = CodeGenerator(optimized_ast)
    code = generator.generate()

    with open("opt-"+output_file, "w") as f:
        f.write(code)

    print("intermediate python code generated")
