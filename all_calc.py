#this is a python calculator

"""A safe, friendly command-line calculator.

Type full expressions like `2 + 3 * (4 - 1)`, reuse the last result with `ans`,
and use functions like sqrt(16) or constants like pi.

Commands: history, clear, help, exit
"""

import ast
import math
import operator

BINARY_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
UNARY_OPS = {ast.UAdd: operator.pos, ast.USub: operator.neg}

FUNCTIONS = {
    "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos, "tan": math.tan,
    "log": math.log, "log10": math.log10, "abs": abs, "round": round,
    "floor": math.floor, "ceil": math.ceil, "factorial": math.factorial,
}
CONSTANTS = {"pi": math.pi, "e": math.e}

MAX_EXPONENT = 10_000  # stops things like 9**9**9 from freezing the program

HELP = """\
Examples:   2 + 3 * 4      (10 + 5) / 3      2 ** 10      17 % 5
            sqrt(144)      sin(pi / 2)       ans * 2
Operators:  +  -  *  /  //  %  **   and parentheses
Commands:   history | clear | help | exit"""


class CalcError(Exception):
    """Raised for any problem the user should see as a friendly message."""


def evaluate(node, variables):
    """Recursively evaluate a parsed expression, allowing only safe nodes."""
    if isinstance(node, ast.Expression):
        return evaluate(node.body, variables)

    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            return node.value
        raise CalcError("Only numbers are allowed.")

    if isinstance(node, ast.Name):
        if node.id in variables:
            return variables[node.id]
        raise CalcError(f"Unknown name '{node.id}'.")

    if isinstance(node, ast.UnaryOp) and type(node.op) in UNARY_OPS:
        return UNARY_OPS[type(node.op)](evaluate(node.operand, variables))

    if isinstance(node, ast.BinOp) and type(node.op) in BINARY_OPS:
        left = evaluate(node.left, variables)
        right = evaluate(node.right, variables)
        if isinstance(node.op, ast.Pow) and abs(right) > MAX_EXPONENT:
            raise CalcError("Exponent is too large.")
        return BINARY_OPS[type(node.op)](left, right)

    if (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id in FUNCTIONS
        and not node.keywords
    ):
        args = [evaluate(arg, variables) for arg in node.args]
        return FUNCTIONS[node.func.id](*args)

    raise CalcError("That expression isn't supported.")


def calculate(text, last_result=0):
    """Parse and evaluate `text`, converting all failures into CalcError."""
    variables = {**CONSTANTS, "ans": last_result}
    try:
        tree = ast.parse(text.replace("^", "**"), mode="eval")
        return evaluate(tree, variables)
    except ZeroDivisionError:
        raise CalcError("Cannot divide by zero.")
    except SyntaxError:
        raise CalcError("That doesn't look like a valid expression.")
    except (ValueError, TypeError, OverflowError) as err:
        raise CalcError(f"Math error: {err}")


def format_number(value):
    """Show 5.0 as 5, and trim floating point noise like 0.30000000000000004."""
    if isinstance(value, float):
        if value.is_integer() and abs(value) < 1e15:
            return str(int(value))
        return f"{value:.10g}"
    return str(value)


def main():
    print("--- Python Calculator ---")
    print("Type an expression, or 'help' for examples.")

    history = []
    last_result = 0

    while True:
        try:
            text = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        command = text.lower()
        if not text:
            continue
        if command in ("exit", "quit", "q"):
            print("Goodbye!")
            break
        if command == "help":
            print(HELP)
            continue
        if command == "clear":
            history.clear()
            last_result = 0
            print("History cleared.")
            continue
        if command == "history":
            if not history:
                print("No calculations yet.")
            for i, (expr, result) in enumerate(history, 1):
                print(f"{i:>3}. {expr} = {result}")
            continue

        try:
            result = calculate(text, last_result)
        except CalcError as err:
            print(f"Error: {err}")
            continue

        last_result = result
        shown = format_number(result)
        history.append((text, shown))
        print(f"= {shown}")


if __name__ == "__main__":
    main()
