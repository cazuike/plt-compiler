import sys
from scanner import IncurvusScanner
from ast_nodes import *

TK_KEY = "KEYWORD"
TK_ID = "IDENTIFIER"
TK_STR = "STRINGLITERAL"
TK_INT = "INTLITERAL"
TK_OP = "OPERATOR"
TK_PUNC = "PUNCTUATION"

class Parser:
    def __init__(self, toks):
        self.tokens = toks
        self.idx = 0
        self.curr = self.tokens[self.idx] if self.tokens else None

    def error_handlr(self, msg):
        print("Syntax Error: " 
        + msg + 
        "  at token " + str(self.idx))
        sys.exit(1)

    def next_tok(self):
        self.idx += 1
        if self.idx < len(self.tokens):
            self.curr = self.tokens[self.idx]
        else:
            self.curr = None

    def expect(self, ttype=None, tval=None):
        if self.curr is None:
            self.error_handlr("Unexpected end")
        type_c, val_c = self.curr
        if ttype and type_c != ttype:
            self.error_handlr("Expected",ttype,"got",type_c)
        if tval and val_c != tval:
            self.error_handlr("Expected",tval,"got ",val_c)
        self.next_tok()
        return (type_c, val_c)

    def look_type(self):
        if self.curr:
            return self.curr[0]
        return None

    def look_val(self):
        if self.curr:
            return self.curr[1]
        return None

    def parse(self):
        prog = self.Prog()
        if self.curr:
            self.error_handlr("...")
        return prog

    def Prog(self):
        stmts = []
        while self.curr:
            stmts.append(self.Stat())
        return ProgramNode(stmts)

    def Stat(self):
        if self.look_type() == TK_KEY:
            kw = self.look_val()
            if kw == "input!":
                return self.InputS()
            elif kw == "filter!":
                return self.FilterS()
            elif kw == "groupby!":
                return self.GroupbyS()
            elif kw == "aggregate!":
                return self.AggregateS()
            elif kw == "sort!":
                return self.SortS()
            elif kw == "combine!":
                return self.CombineS()
            elif kw == "multiply!":
                return self.MultiplyS()
            elif kw == "delete!":
                return self.DeleteS()
            elif kw == "rename!":
                return self.RenameS()
            elif kw == "output!":
                return self.OutputS()
            elif kw == "shout!":
                return self.ShoutS()
        self.error_handlr("missing statement")

    def CombineS(self):
        self.expect(TK_KEY, "combine!")
        _, fname = self.expect(TK_STR)
        _, mk = self.expect(TK_ID)
        if mk != "mode":
            self.error_handlr("missing 'mode' param")
        self.expect(TK_OP, "=")
        _, mv = self.expect(TK_ID)
        if mv not in ["vertical", "horizontal"]:
            self.error_handlr("inc: Mode must be vertical or horizontal")
        return CombineNode(fname.strip('"'), mv)

    def MultiplyS(self):
        self.expect(TK_KEY, "multiply!")
        _, fk = self.expect(TK_ID)
        if fk != "factor":
            self.error_handlr("missing factor param")
        self.expect(TK_OP, "=")
        t = self.look_type()
        if t == TK_INT:
            _, fv = self.expect(TK_INT)
            factor = int(fv)
        elif t == "FLOATLIT":
            _, fv = self.expect("FLOATLIT")
            factor = float(fv)
        else:
            self.error_handlr("Missing a number for factor")
        return MultiplyNode(factor)

    def DeleteS(self):
        self.expect(TK_KEY, "delete!")
        _, ck = self.expect(TK_ID)
        if ck != "condition":
            self.error_handlr("Missing  param")
        self.expect(TK_OP, "=")
        cond = self.Cond()
        return DeleteNode(cond)

    def RenameS(self):
        self.expect(TK_KEY, "rename!")
        _, oldn = self.expect(TK_ID)
        self.expect(TK_OP, "=")
        _, newn = self.expect(TK_ID)
        return RenameNode(oldn, newn)

    def InputS(self):
        self.expect(TK_KEY, "input!")
        _, f = self.expect(TK_STR)
        return InputNode(f.strip('"'))

    def FilterS(self):
        self.expect(TK_KEY, "filter!")
        cond = self.Cond()
        return FilterNode(cond)

    def GroupbyS(self):
        self.expect(TK_KEY, "groupby!")
        _, idn = self.expect(TK_ID)
        return GroupByNode(idn)

    def AggregateS(self):
        self.expect(TK_KEY, "aggregate!")
        aggs = self.AggList()
        return AggregateNode(aggs)

    def SortS(self):
        self.expect(TK_KEY, "sort!")
        cols = []
        while True:
            _, col = self.expect(TK_ID)
            order = 'asc'
            if self.curr and self.look_type() == TK_ID:
                ord_val = self.look_val().lower()
                if ord_val in ['asc', 'desc']:
                    self.expect(TK_ID)
                    order = ord_val
                else:
                    self.error_handlr("Valid parms are only asc/desc")
            cols.append((col, order))
            if self.curr and self.look_val() == ",":
                self.expect(TK_PUNC, ",")
            else:
                break
        return SortNode(cols)

    def OutputS(self):
        self.expect(TK_KEY, "output!")
        _, f = self.expect(TK_STR)
        return OutputNode(f.strip('"'))

    def ShoutS(self):
        self.expect(TK_KEY, "shout!")
        _, msg = self.expect(TK_STR)
        return ShoutNode(msg.strip('"'))

    def Cond(self):
        _, left = self.expect(TK_ID)
        _, op = self.expect(TK_OP)
        t = self.look_type()
        if t == TK_ID:
            _, right = self.expect(TK_ID)
            return ConditionNode(left, op, right, "IDENTIFIER")
        elif t == TK_INT:
            _, right = self.expect(TK_INT)
            return ConditionNode(left, op, right, "INT")
        elif t == TK_STR:
            _, right = self.expect(TK_STR)
            return ConditionNode(left, op, right.strip('"'), "STRING")
        else:
            self.error_handlr("Valids are only ID, INT, or STRING in condition")

    def AggList(self):
        aggs = []
        aggs.append(self.FuncC())
        while self.curr and self.look_val() == ",":
            self.expect(TK_PUNC, ",")
            aggs.append(self.FuncC())
        return aggs

    def FuncC(self):
        _, fn = self.expect(TK_ID)
        self.expect(TK_PUNC, "(")
        _, col = self.expect(TK_ID)
        self.expect(TK_PUNC, ")")
        return (fn.lower(), col)

if __name__ == "__main__":
    x = sys.argv[1]
    with open(x, "r") as file:
        txt = file.read()
    scanner = IncurvusScanner(txt)
    scanner.exec()
    tokens = scanner.get_tokens()
    for i, tok in enumerate(tokens):
        print(i, tok)
    prs = Parser(tokens)
    ast = prs.parse()

    def ast_print(node, indent=0):
        space = " " * indent
        if isinstance(node, ProgramNode):
            print(space + "Program")
            for s in node.statements:
                ast_print(s, indent + 2)
        elif isinstance(node, InputNode):
            print(space + "Input: " + node.filename)
        elif isinstance(node, FilterNode):
            print(space + "Filter:")
            ast_print(node.condition, indent + 2)
        elif isinstance(node, GroupByNode):
            print(space + "GroupBy: " + node.identifier)
        elif isinstance(node, AggregateNode):
            print(space + "Aggregate:")
            for f, c in node.aggregations:
                print(space + "  " + f + "(" + c + ")")
        elif isinstance(node, SortNode):
            details = ", ".join(["('" + c + "', '" + o + "')" for c, o in node.columns_orders])
            print(space + "Sort: [" + details + "]")
        elif isinstance(node, CombineNode):
            print(space + "Combine: " + node.filename + " (mode=" + node.mode + ")")
        elif isinstance(node, MultiplyNode):
            print(space + "Multiply: factor=" + str(node.factor))
        elif isinstance(node, DeleteNode):
            print(space + "Delete:")
            ast_print(node.condition, indent + 2)
        elif isinstance(node, RenameNode):
            print(space + "Rename: " + node.old_name + " to " + node.new_name)
        elif isinstance(node, OutputNode):
            print(space + "Output: " + node.filename)
        elif isinstance(node, ShoutNode):
            print(space + "Shout: " + node.message)
        elif isinstance(node, ConditionNode):
            print(space + "Condition: " + node.left_id + " " + node.operator + " " + str(node.right_val) + " (type=" + node.right_type + ")")
        else:
            print(space + "bug")

    print("\nAST:")
    ast_print(ast)

