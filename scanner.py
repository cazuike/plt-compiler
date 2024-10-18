import sys

class IncurvusScanner:
    def __init__(self, input_string):
        self.input = input_string
        self.position = self.start_pos = 0
        self.tokens = []
        self.current_state = "START"  

        self.keywords = {
"input!",
            "filter!",
    "groupby!",
            "aggregate!",
            "output!",
            "shout!",
        }

        self.operators = {">", "<", ">=", "<=", "="}

    def next_char(self):
        if self.position < len(self.input):
            return self.input[self.position]
        return None

    def exec(self):
        while self.position < len(self.input):
            char = self.next_char()

            if self.current_state == "START" :
                if char.isspace():
                    self.position += 1
                elif char.isalpha() or char == "_":
                    self.current_state = "identifier"
                    self.start_pos = self.position
                elif char.isdigit():
                    self.current_state = "number"
                    self.start_pos = self.position
                elif char == '"':
                    self.current_state = "string_literal"
                    self.start_pos = self.position
                    self.position += 1
                elif char in [">", "<", "=", "!"]:
                    self.current_state = "operator"
                    self.start_pos = self.position
                else:
                    exit(1)

            elif self.current_state == "identifier":
                if not (char.isalnum() or char == "_"):
                    token_value = self.input[self.start_pos : self.position]
                    self.add_token(
                        self.identify_token(token_value), token_value
                    )
                    self.current_state = "START" 
                else:
                    self.position += 1

            elif self.current_state == "number":
                if not char.isdigit():
                    token_value = self.input[self.start_pos : self.position]
                    self.add_token("INTLITERAL", token_value)
                    self.current_state = "START" 
                else:
                    self.position += 1

            elif self.current_state == "string_literal":
                if char == '"':
                    token_value = self.input[self.start_pos : self.position + 1]
                    self.add_token("STRINGLITERAL", token_value)
                    self.position += 1
                    self.current_state = "START" 
                else:
                    self.position += 1

            elif self.current_state == "operator":
                token_value = self.input[self.start_pos : self.position + 1]
                if token_value in self.operators:
                    self.add_token("OPERATOR", token_value)
                    self.position += 1
                else:
                    exit(1)
                self.current_state = "START"  

    def add_token(self, token_type, token_value):
        self.tokens.append((token_type, token_value))
        self.position += 1

    def identify_token(self, token_value):
        if token_value in self.keywords:
            return "KEYWORD"
        return "IDENTIFIER"

    def get_tokens(self):
        return self.tokens


if __name__ == "__main__":
    x = sys.argv[1]
    with open(x, 'r') as f:
        y = f.read()

    scanner = IncurvusScanner(y)
    scanner.exec()

    for token in scanner.get_tokens():
        print(token)