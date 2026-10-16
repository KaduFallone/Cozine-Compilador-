import os
import subprocess
import sys
from pathlib import Path

from compiler.errors import CompilationError
from compiler.pipeline import compile_source

ROOT = Path(__file__).parent
TESTS_DIR = ROOT / "tests"
BUILD_DIR = ROOT / "output" / "tests"
REPORT = ROOT / "docs" / "testes.md"


def run_generated(name, cpp):
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    cpp_path = BUILD_DIR / f"{name}.cpp"
    executable = cpp_path.with_suffix(".exe" if os.name == "nt" else "")
    cpp_path.write_text(cpp, encoding="utf-8")

    build = subprocess.run(["g++", "-std=c++17", "-o", str(executable), str(cpp_path)], capture_output=True, text=True)

    if build.returncode != 0:
        return f"g++ error:\n{build.stderr}"

    return subprocess.run([str(executable)], capture_output=True, text=True).stdout


def run_test(source):
    try:
        cpp = compile_source(source.read_text(encoding="utf-8-sig"))
    except CompilationError as error:
        return str(error)

    return run_generated(source.stem, cpp)


def write_report(results):
    passed = sum(1 for result in results if result["passed"])
    lines = [
        "# Resultados dos testes",
        "",
        "Gerado automaticamente por `python run_tests.py`.",
        "Nos programas válidos, o resultado obtido é a saída do executável compilado a partir do C++ gerado.",
        "",
        f"**{passed} de {len(results)} testes passaram.**",
        "",
        "| Teste | Situação |",
        "|---|---|",
    ]

    for result in results:
        lines.append(f"| `{result['name']}` | {'passou' if result['passed'] else '**FALHOU**'} |")

    for result in results:
        lines += [
            "",
            f"## {result['name']}",
            "",
            "**Entrada**",
            "",
            "```",
            result["source"].rstrip(),
            "```",
            "",
            "**Resultado esperado**",
            "",
            "```",
            result["expected"],
            "```",
            "",
            "**Resultado obtido**",
            "",
            "```",
            result["obtained"],
            "```",
        ]

    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    results = []

    for source in sorted(TESTS_DIR.glob("*.cz")):
        expected_path = source.with_suffix(".expected")
        expected = expected_path.read_text(encoding="utf-8").strip() if expected_path.exists() else "(sem arquivo .expected)"
        obtained = run_test(source).strip()
        passed = obtained == expected

        print(f"{'PASS' if passed else 'FAIL'}  {source.name}")

        if not passed:
            print(f"      expected: {expected}")
            print(f"      obtained: {obtained}")

        results.append({
            "name": source.name,
            "source": source.read_text(encoding="utf-8-sig"),
            "expected": expected,
            "obtained": obtained,
            "passed": passed,
        })

    write_report(results)
    failures = sum(1 for result in results if not result["passed"])
    print(f"\n{len(results) - failures}/{len(results)} tests passed. Report: {REPORT.relative_to(ROOT)}")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
