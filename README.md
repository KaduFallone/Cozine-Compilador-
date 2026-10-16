# Compilador Cozine

Compilador da linguagem **Cozine**, uma linguagem didática com tema de cozinha. O compilador é escrito em Python e traduz programas `.cz` para **C++**.

- Especificação da linguagem e gramática: [docs/README.md](docs/README.md)
- Relatório do trabalho: [docs/relatorio.md](docs/relatorio.md)
- Resultados dos testes: [docs/testes.md](docs/testes.md)

## Requisitos

| Ferramenta | Para quê              | Versão usada 
|------------|-----------------------|------------------------
| Python     | rodar o compilador    | 3.14 (versão testada) 
| g++        | compilar o C++ gerado | MinGW-w64 (MSYS2) 

Nenhuma biblioteca externa é necessária: o compilador usa só a biblioteca padrão do Python.

No Windows, o g++ pode ser instalado pelo [MSYS2](https://www.msys2.org/) com `pacman -S mingw-w64-x86_64-gcc`. Depois, a pasta `C:\msys64\mingw64\bin` precisa estar no `PATH`. Para conferir:

```
python --version
g++ --version
```

## Como usar

Na pasta do projeto:

```
python main.py tests/example.cz
```

O compilador passa pelas 4 etapas e grava o C++ em `output/example.cpp`:

```
[1/4] Lexical analysis      OK (111 tokens)
[2/4] Syntactic analysis    OK
[3/4] Semantic analysis     OK
[4/4] Code generation       OK -> output\example.cpp
```

### Opções

| Opção            | O que faz |
|------------------|----------------------------------------------------------------
| `--tokens`       | mostra a lista de tokens (análise léxica) 
| `--ast`          | mostra a árvore sintática 
| `--table`        | mostra a tabela de símbolos (também quando há erro semântico)
| `--run`          | compila o `.cpp` gerado com g++ e executa 
| `-o arquivo.cpp` | escolhe o arquivo de saída 

Exemplo mostrando tudo:

```
python main.py tests/example.cz --tokens --ast --table --run
```

Para compilar o C++ manualmente:

```
g++ -std=c++17 -o output/example.exe output/example.cpp
output\example.exe
```

### Quando há erro

A mensagem mostra a etapa, a linha e o motivo. Nenhum `.cpp` é gerado:

```
[1/4] Lexical analysis      OK (19 tokens)
[2/4] Syntactic analysis    OK
[3/4] Semantic analysis     FAILED
Semantic error at line 3: variable 'total' was not declared
Compilation failed: no output file was generated.
```

## Testes

```
python run_tests.py
```

Roda todos os programas de `tests/`. Para cada `nome.cz` existe um `nome.expected` com o resultado esperado:

- programas válidos: a saída do programa depois de compilado com g++;
- programas com erro: a mensagem de erro.

O script compara o esperado com o obtido e grava o relatório em [docs/testes.md](docs/testes.md).

## Estrutura do projeto

```
main.py                 ponto de entrada (linha de comando)
run_tests.py            roda os testes e gera docs/testes.md
compiler/
  token.py              tipos de token e tabelas de palavras e símbolos
  lexic.py              análise léxica (texto -> tokens)
  ast_nodes.py          classes da árvore sintática
  parser.py             análise sintática (tokens -> árvore)
  symbol_table.py       tabela de símbolos
  semantic.py           análise semântica (confere a árvore)
  generator.py          geração de código (árvore -> C++)
  pipeline.py           as 4 etapas em sequência
  errors.py             erros de cada etapa
tests/                  programas de teste (.cz) e resultados esperados (.expected)
output/                 código C++ gerado
docs/                   especificação, relatório e resultados dos testes
```
