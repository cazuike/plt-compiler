from ast_nodes import (
    ProgramNode, InputNode, FilterNode, CombineNode, MultiplyNode, 
    DeleteNode, RenameNode, GroupByNode, AggregateNode, SortNode,
    OutputNode, ShoutNode, ConditionNode
)

class optimize:
    def __init__(self, ast):
        self.ast = ast

    def optimize(self):
        self.ast = self.dead_code_elim(self.ast)
        self.ast = self.multiply_compress(self.ast)
        self.ast = self.keep_last_sort(self.ast)
        return self.ast

    def dead_code_elim(self, ast):
        if not isinstance(ast, ProgramNode):
            return ast

        res = []
        for curr in ast.statements:
            if isinstance(curr, ShoutNode) and curr.message.strip() == "":
                continue
            res.append(curr)

        ast.statements = res
        return ast

    def multiply_compress(self, ast):
        if not isinstance(ast, ProgramNode):
            return ast

        res = []
        skip_next = False

        for i in range(len(ast.statements)):
            if skip_next:
                skip_next = False
                continue

            curr = ast.statements[i]
            if i < len(ast.statements) - 1 and isinstance(curr, MultiplyNode):
                nxt = ast.statements[i + 1]
                if isinstance(nxt, MultiplyNode):
                    combined = curr.factor * nxt.factor
                    res.append(MultiplyNode(combined))
                    skip_next = True
                else:
                    res.append(curr)
            else:
                res.append(curr)

        ast.statements = res
        return ast

    def keep_last_sort(self, ast):
        if not isinstance(ast, ProgramNode):
            return ast

        res = []
        i = 0
        while i < len(ast.statements):
            curr = ast.statements[i]
            if isinstance(curr, SortNode):
                j = i + 1
                last_sort = curr
                while j < len(ast.statements) and isinstance(ast.statements[j], SortNode):
                    last_sort = ast.statements[j]
                    j += 1
                res.append(last_sort)
                i = j
            else:
                res.append(curr)
                i += 1

        ast.statements = res
        return ast
