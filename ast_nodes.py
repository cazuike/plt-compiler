class ProgramNode:
    def __init__(self, statements):
        self.statements = statements

class InputNode:
    def __init__(self, filename):
        self.filename = filename

class FilterNode:
    def __init__(self, condition):
        self.condition = condition


class CombineNode:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode 

class MultiplyNode:
    def __init__(self, factor):
        self.factor = factor

class DeleteNode:
    def __init__(self, condition):
        self.condition = condition

class RenameNode:
    def __init__(self, old_name, new_name):
        self.old_name = old_name
        self.new_name = new_name


class GroupByNode:
    def __init__(self, identifier):
        self.identifier = identifier

class AggregateNode:
    def __init__(self, aggregations):
        self.aggregations = aggregations

class SortNode:
    def __init__(self, columns_orders):
        self.columns_orders = columns_orders

class OutputNode:
    def __init__(self, filename):
        self.filename = filename

class ShoutNode:
    def __init__(self, message):
        self.message = message

class ConditionNode:
    def __init__(self, left_id, operator, right_val, right_type):
        self.left_id = left_id
        self.operator = operator
        self.right_val = right_val
        self.right_type = right_type

class FuncCallNode:
    def __init__(self, func_name, args):
        self.func_name = func_name
        self.args = args
