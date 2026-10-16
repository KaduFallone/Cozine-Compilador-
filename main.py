import argparse
import os
import subprocess
import sys
from pathlib import Path

from compiler.ast_nodes import format_tree
from compiler.errors import CompilationError
from compiler.generator import CodeGenerator
from compiler.lexic import Lexer
from compiler.parser import Parser
from compiler.semantic import SemanticAnalyzer

OUTPUT_DIR = Path("output")


def read_arguments():
    parser = argparse.ArgumentParser(description="Compilador da linguagem Cozine (Cozine -> C++)")
    parser.add_argument("file", help="arquivo .cz de entrada")
    parser.add_argument("-o", "--output", help="arquivo .cpp de saída (padrão: output/<nome>.cpp)")
    parser.add_argument("--tokens", action="store_true", help="mostra os tokens (análise léxica)")
    parser.add_argument("--ast", action="store_true", help="mostra a árvore sintática")
    parser.add_argument("--table", action="store_true", help="mostra a tabela de símbolos")
    parser.add_argument("--run", action="store_true", help="compila o .cpp com g++ e executa")
    return parser.parse_args()


def print_tokens(tokens):
    print(f'{"LINE":<6} {"TYPE":<15} LEXEME')

    for token in tokens:
        print(f'{token.line:<6} {token.type.name:<15} {token.lexeme}')


def stage(number, name):
    print(f"[{number}/4] {name:<22}", end="", flush=True)


def compile_file(args, output_path):
    with open(args.file, "r", encoding="utf-8-sig") as file:
        code = file.read()

    stage(1, "Lexical analysis")
    tokens = Lexer(code).tokenize()
    print(f"OK ({len(tokens)} tokens)")

    if args.tokens:
        print_tokens(tokens)

    stage(2, "Syntactic analysis")
    program = Parser(tokens).parse_program()
    print("OK")

    if args.ast:
        print(format_tree(program), end="")

    stage(3, "Semantic analysis")
    analyzer = SemanticAnalyzer()

    try:
        table = analyzer.analyze(program)
    except CompilationError as error:
        error.table = analyzer.table
        raise

    print("OK")

    if args.table:
        print(table.format())

    stage(4, "Code generation")
    cpp = CodeGenerator(table).generate(program)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(cpp, encoding="utf-8")
    print(f"OK -> {output_path}")


def run_cpp(cpp_path):
    executable = cpp_path.with_suffix(".exe" if os.name == "nt" else "")
    sys.stdout.flush()
    build = subprocess.run(["g++", "-std=c++17", "-o", str(executable), str(cpp_path)])

    if build.returncode != 0:
        print("g++ failed to compile the generated code")
        sys.exit(1)

    print(f"--- running {executable} ---", flush=True)
    subprocess.run([str(executable)])


def main():
    args = read_arguments()
    output_path = Path(args.output) if args.output else OUTPUT_DIR / f"{Path(args.file).stem}.cpp"

    try:
        compile_file(args, output_path)

    except FileNotFoundError:
        print(f"File not found: {args.file}")
        sys.exit(1)

    except CompilationError as e:
        print("FAILED")
        print(e)

        if args.table and hasattr(e, "table"):
            print("\nSymbol table up to the error:")
            print(e.table.format())

        if output_path.exists():
            output_path.unlink()

        print("Compilation failed: no output file was generated.")
        sys.exit(1)

    if args.run:
        run_cpp(output_path)


if __name__ == "__main__":
    main()
