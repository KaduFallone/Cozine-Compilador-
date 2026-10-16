# Relatório — Compilador Cozine

## 1. Visão geral

O compilador lê um arquivo `.cz`, passa o código por quatro etapas e, se nenhuma encontrar erro, grava um arquivo `.cpp` equivalente. Cada etapa fica num módulo da pasta `compiler/` e entrega uma estrutura de dados para a seguinte:

```
código .cz ──► léxico ──► tokens ──► sintático ──► árvore ──► semântico ──► árvore aprovada
                                                                + tabela de símbolos ──► gerador ──► código .cpp
```

Qualquer erro interrompe a compilação. A mensagem informa a etapa, a linha e o motivo, e nenhum `.cpp` é gerado.

## 2. As etapas

### 2.1 Análise léxica (`lexic.py`)

O `Lexer` percorre o texto caractere por caractere, guardando a posição e a linha atuais. O primeiro caractere de cada elemento decide o que ler:

| Começa com   | O que é lido                                                                                     |
|--------------|--------------------------------------------------------------------------------------------------|
| letra ou `_` | palavra: se estiver no dicionário `RESERVED_WORDS`, é palavra reservada; se não, é identificador |
| dígito       | número inteiro ou decimal (`3.14`)                                                               |
| `"` / `'`    | texto / caractere                                                                                |
| `#`          | comentário (ignorado até o fim da linha)                                                         |
| outro        | símbolo: primeiro tenta os de 2 caracteres (`==`, `->`...), depois os de 1                       |

Espaços e quebras de linha só separam os elementos. A quebra de linha também soma 1 no contador de linhas. Um caractere que não pertence à linguagem gera erro léxico.

### 2.2 Análise sintática (`parser.py`)

É um **parser descendente recursivo**: cada regra da gramática EBNF (seção 12 da especificação) virou uma função. A precedência dos operadores vem da própria gramática, com uma função por nível: `parse_expression` (`+ -`) chama `parse_term` (`* /`), que chama `parse_unary` (`-`), que chama `parse_factor` (valores e parênteses).

O resultado é uma **árvore sintática** (classes em `ast_nodes.py`), que guarda a estrutura do programa sem os detalhes de escrita (`;`, `{`, `}`).

Para decidir o que fazer quando um comando começa com um nome, o parser olha um token à frente: se vier `=`, é atribuição; se vier `(`, é chamada de receita.

### 2.3 Análise semântica (`semantic.py` e `symbol_table.py`)

O `SemanticAnalyzer` percorre a árvore e usa a **tabela de símbolos** para guardar, de cada nome, o tipo, o tipo de símbolo (variável, parâmetro ou receita), o escopo, se já recebeu valor e a linha da declaração.

Cada expressão devolve o seu tipo, e as regras da seção 7 da especificação conferem se a operação é permitida. A análise também verifica variáveis não declaradas, declarações repetidas, uso antes de receber valor, declaração dentro de bloco, argumentos de receita e uso de `comer`.

Para a regra de "uso antes de receber valor", o analisador guarda quais variáveis tinham valor antes de cada bloco e restaura essa situação no `}`. Assim, um valor recebido só dentro de um `garfo` não conta depois dele.

### 2.4 Geração de código (`generator.py`)

O `CodeGenerator` percorre a árvore aprovada e escreve o C++ linha a linha, controlando a indentação. As receitas viram funções antes do `main`, e os outros comandos vão dentro do `main`.

| Cozine                      | C++ 
|-----------------------------|-------------------------------------------|
| `panela x: int = 3;`        | `int x = 3;`                              |
| `float` / `str` / `char`    | `double` / `std::string` / `char`         |
| `acenderfogao(a, b);`       | `std::cout << a << " " << b << std::endl;`| 
| `garfo` / `colher` / `faca` | `if` / `else if` / `else`                 |
| `liquidificar (c) { }`      | `while (c) { }`                           |
| `flambar (i em range(a, b))`| `for (i = a; i < b; i++)`                 |
| `receita f(x: int) -> int`  | `int f(int x)`                            |
| `comer x;`                  | `return x;`                               |
| `a / b`                     | `static_cast<double>(a) / b`              | 

## 3. Exemplo: o caminho de um trecho

Trecho: `total = quantidade * preco;` (do programa `tests/01_declaracao.cz`)

**1. Léxico**: o texto vira 6 tokens:

```
IDENTIFIER total | ASSIGN = | IDENTIFIER quantidade | MULTIPLY * | IDENTIFIER preco | SEMICOLON ;
```

**2. Sintático**: o comando começa com um nome seguido de `=`, então é uma atribuição. A expressão depois do `=` vira uma operação `*`:

```
Assign name='total'
  value:
    BinaryOp operator='*'
      left:
        Variable name='quantidade'
      right:
        Variable name='preco'
```

**3. Semântico**: consulta a tabela de símbolos e confere:
- `quantidade` e `preco` foram declaradas e já têm valor;
- as duas são `int`, então `int * int` dá `int`;
- `total` foi declarada como `int` e aceita um valor `int`.

Depois disso, `total` é marcada na tabela como "recebeu valor".

**4. Gerador**: escreve a linha de C++:

```cpp
total = quantidade * preco;
```

## 4. Decisões adotadas

- **C++ como destino.** A Cozine tem tipos nas declarações, e o C++ também, então cada declaração vira diretamente uma declaração C++.
- **Blocos com `{ }` e `;` no fim de todo comando.** A indentação é livre, o que deixa o léxico mais simples do que numa linguagem que depende de indentação, como o Python.
- **Um único `;` no fim da sequência `garfo`/`colher`/`faca`.** Assim, a sequência inteira é um comando só.
- **`/` sempre devolve `float`, como no Python.** No C++, `7 / 2` daria `3`, então o gerador converte o lado esquerdo para `double`.
- **Variáveis só podem ser declaradas fora de blocos.** No C++, uma variável declarada dentro de `{ }` deixa de existir no `}`.
- **Uma receita não enxerga as variáveis do programa principal.** No C++ gerado, essas variáveis ficam dentro do `main`.
- **A compilação para no primeiro erro**, em qualquer etapa.

## 5. Dificuldades encontradas

- **Letras e dígitos fora do ASCII.** As funções `isalpha()` e `isdigit()` do Python aceitam `ç`, `é` e `²`. O léxico passou a usar conjuntos explícitos com `string.ascii_letters` e `string.digits`.
- **Laço infinito no fim do arquivo.** No fim do texto, o léxico devolve `''` como caractere atual, e `'' in "abc"` é `True` no Python. Usar `set` em vez de `str` para as letras e os dígitos resolveu.
- **Arquivo `token.py`.** O Python tem um módulo interno chamado `token`. Executar um arquivo de dentro da pasta `compiler/` faz o módulo do projeto tomar o lugar do interno e causa erro de importação circular. Pelo `main.py` da raiz, o problema não acontece.
- **BOM nos arquivos.** Alguns editores do Windows gravam um caractere invisível no início dos arquivos UTF-8, e o léxico acusava esse caractere como inválido. A leitura com `encoding="utf-8-sig"` descarta o BOM.
- **Texto no C++.** No C++, `"a" + "b"` não junta textos: soma ponteiros e não compila. Dentro de operações, o gerador escreve os textos como `std::string("a")`.
- **Variáveis sem valor no C++.** Uma variável C++ sem valor inicial contém lixo de memória. A regra semântica de "uso antes de receber valor" garante que o programa gerado nunca leia esse lixo.
- **Fim do `range`.** O `for` do C++ recalcula o limite a cada volta, mas o `range` do Python calcula uma vez só. Quando o fim não é um número fixo, o gerador guarda o valor numa constante antes do `for`.
- **Nomes reservados do C++.** `class`, `new` e `main` são nomes válidos na Cozine, mas não no C++. O gerador renomeia essas variáveis (por exemplo, `class` vira `class_cz`).

## 6. Limitações

- O compilador mostra só o **primeiro** erro encontrado.
- Números `float` são impressos no formato padrão do C++: `25.0` aparece como `25`, e são mostrados até 6 algarismos significativos (`1/3` aparece como `0.333333`).
- Não há verificação de estouro de `int` (o `int` do C++ tem 32 bits) nem de divisão por zero.
- Textos não aceitam `"` nem sequências de escape, e um `char` precisa ser um caractere ASCII. Texto com acento pode aparecer com caracteres trocados se o terminal não estiver em UTF-8 (no Windows, `chcp 65001`).
- A regra de valor recebido dentro de bloco é conservadora: uma variável que recebe valor tanto no `garfo` quanto no `faca` ainda conta como "sem valor" depois deles.
- Alterar o contador dentro do `flambar` muda a repetição, como num `for` do C.
- Não há operadores lógicos (`e`, `ou`): cada condição tem exatamente uma comparação.
