# Cozine

Trabalho final de Compiladores: criação de uma linguagem de programação e de um compilador do zero.

## Visão geral

| | |
|---|---|
| **Linguagem** | Cozine |
| **Finalidade** | Linguagem didática com tema de cozinha e escrita inspirada em Python, para fazer cálculos, comparações e exibir resultados. |
| **Compilador escrito em** | Python |
| **Linguagem de destino** | C++ |
| **Extensão dos arquivos** | `.cz` |

**Fluxo:** `programa.cz` → compilador Cozine (Python) → `programa.cpp` → g++ → executável

---

## 1. Palavras reservadas

| Palavra                    | Significado                      | Equivalente em Python                       |
|----------------------------|----------------------------------|---------------------------------------------|
| `panela`                   | declara uma variável             | `x: int = 0`                                |
| `acenderfogao`             | exibe valores na tela            | `print`                                     |
| `garfo`                    | se                               | `if`                                        |
| `colher`                   | senão se                         | `elif`                                      |
| `faca`                     | senão                            | `else`                                      |
| `liquidificar`             | enquanto                         | `while`                                     |
| `flambar`                  | repetição com contador           | `for`                                       |
| `em`                       | usado no `flambar`               | `in`                                        |
| `range`                    | intervalo do `flambar`           | `range`                                     | 
| `receita`                  | declara uma função               | `def`                                       |
| `comer`                    | devolve o valor de uma `receita` | `return`                                    |
| `int` `float` `str` `char` | nomes dos tipos                  | `int` `float` `str` (Python não tem `char`) |

---

## 2. Tipos de dados

| Tipo    | O que guarda             | Como escrever um valor |
|---------|--------------------------|------------------------|
| `int`   | número inteiro           | `42`, `0`              |
| `float` | número com casas decimais| `3.14`, `0.5`          |
| `str`   | texto                    | `"bolo de cenoura"`    |
| `char`  | um único caractere       | `'a'`                  |

Regras dos valores:

- Números negativos são escritos com o menos unário: `-7`, `-2.5`.
- `float` precisa de dígito dos dois lados do ponto: `0.5` é válido, `.5` e `5.` não são.
- Zeros à esquerda são ignorados: `007` vale `7`.
- `str` usa aspas duplas e não pode conter quebra de linha nem `"`. Não existem sequências de escape (`\n`).
- `char` usa aspas simples e tem exatamente um caractere: `''` e `'ab'` são inválidos.
- Texto ou caractere sem a aspa de fechamento é **erro léxico**.

---

## 3. Nomes de variáveis e receitas

- Começam com uma letra (`a-z`, `A-Z`) ou `_`.
- Depois podem ter letras, dígitos ou `_`.
- Não aceitam acento nem `ç`. Qualquer outro caractere é **erro léxico**.
- Diferenciam maiúsculas de minúsculas: `Total` e `total` são nomes diferentes.
- Não podem ser palavras reservadas.

| Válidos                                 | Inválidos                           |
|-----------------------------------------|-------------------------------------|
| `total`, `preco_final`, `_aux`, `Bolo2` | `2bolo`, `preço`, `total$`, `garfo` |

---

## 4. Operadores e símbolos

| Símbolo           | Significado                                            |
|-------------------|--------------------------------------------------------|
| `+`               | soma; entre dois `str`, junta os textos                |
| `-`               | subtração; antes de um valor, menos unário             |
| `*`               | multiplicação                                          |
| `/`               | divisão (o resultado é sempre `float`, como no Python) |
| `==` `!=`         | igual, diferente                                       |
| `<` `>` `<=` `>=` | menor, maior, menor ou igual, maior ou igual           |
| `=`               | atribuição                                             |
| `:`               | separa o nome do tipo na declaração                    |
| `->`              | indica o tipo de retorno de uma `receita`              |
| `,`               | separa valores, parâmetros e argumentos                |
| `( )`             | agrupam expressões; envolvem condições e argumentos    |
| `{ }`             | delimitam blocos                                       |
| `;`               | terminam comandos                                      |
| `#`               | comentário até o fim da linha                          |

### Precedência (da maior para a menor)

1. `( )` e chamada de `receita`
2. `-` unário
3. `*` `/`
4. `+` `-`
5. comparações (`==` `!=` `<` `>` `<=` `>=`), usadas só dentro de condições

Operadores do mesmo nível são resolvidos da esquerda para a direita: `10 - 3 - 2` vale `5`.

---

## 5. Estrutura do programa

- O programa é uma sequência de comandos, executados de cima para baixo. Não existe marcador de início ou fim.
- Espaços, tabulações e quebras de linha servem apenas para separar os elementos. A indentação é livre.
- **Todo comando termina com `;`.** Nos comandos com bloco, o `;` vem depois do `}`. Na sequência `garfo` / `colher` / `faca`, o `;` aparece **uma única vez, depois do último `}`**.

---

## 6. Comandos

### Declaração — `panela`

```
panela idade: int;
panela preco: float = 9.5;
panela nome: str = "Ana";
panela letra: char = 'a';
```

Forma: `panela nome: tipo;` ou `panela nome: tipo = expressão;`

### Atribuição

```
idade = 20;
preco = preco * 2;
```

Forma: `nome = expressão;`

### Exibição — `acenderfogao`

```
acenderfogao(total);
acenderfogao("Total:", total * 2);
```

Forma: `acenderfogao(expressão, expressão, ...);`. Recebe um ou mais valores, mostra todos separados por espaço e pula uma linha no final.

### Condicional — `garfo` / `colher` / `faca`

```
garfo (total > 20) {
    acenderfogao("caro");
} colher (total == 20) {
    acenderfogao("justo");
} faca {
    acenderfogao("barato");
};
```

- A condição fica entre parênteses e tem **exatamente uma** comparação entre duas expressões.
- `colher` pode aparecer zero ou mais vezes. `faca` aparece no máximo uma vez e sempre por último.
- `colher` e `faca` não existem sozinhos: são partes do comando `garfo`.

### Repetição — `liquidificar`

```
liquidificar (contador < 10) {
    contador = contador + 1;
};
```

Repete o bloco enquanto a condição for verdadeira.

### Repetição com contador — `flambar`

```
panela i: int;
flambar (i em range(0, 5)) {
    acenderfogao(i);
};
```

- A variável do contador precisa ter sido declarada antes, com tipo `int`.
- `range(inicio, fim)` vai de `inicio` até `fim - 1`, de 1 em 1, como no Python. `inicio` e `fim` são expressões `int`.
- `fim` é calculado uma única vez, antes da primeira repetição, como no Python.
- Depois do `flambar`, o contador vale o valor em que a repetição parou: `fim`, ou `inicio` se o intervalo for vazio.

### Funções — `receita` / `comer`

```
receita soma(a: int, b: int) -> int {
    comer a + b;
};

receita saudar(nome: str) {
    acenderfogao("Ola,", nome);
};

panela resultado: int = soma(2, 3);
saudar("Ana");
```

- Forma: `receita nome(param: tipo, ...) -> tipo { ... };`. O `-> tipo` é opcional. Sem ele, a `receita` não devolve valor.
- `comer expressão;` devolve um valor e encerra a receita. Numa receita sem tipo de retorno, usa-se `comer;`.
- Uma `receita` só pode ser declarada no nível principal do programa, antes de ser chamada.
- Dentro de uma `receita` só são visíveis os seus parâmetros e as `panela` declaradas nela. As variáveis do programa principal não são visíveis.
- A chamada precisa ter a mesma quantidade de argumentos que a receita, com os tipos compatíveis.
- Uma `receita` sem tipo de retorno só pode ser chamada como comando (`saudar("Ana");`), nunca dentro de uma expressão.

---

## 7. Regras de tipos

### Operações aritméticas (`+ - * /`)

| Operandos                                           | Resultado          |
|-----------------------------------------------------|--------------------|
| `int` com `int` (`+ - *`)                           | `int`              |
| `int` com `float`, ou `float` com `float` (`+ - *`) | `float`            |
| quaisquer números com `/`                           | `float`            |
| `str` + `str`                                       | `str`              |
| qualquer outra combinação                           | **erro semântico** |

O menos unário só aceita `int` e `float`.

### Comparações (`== != < > <= >=`)

| Operandos                                             | Permitido?             |
|-------------------------------------------------------|------------------------|
| número com número (`int` e `float` podem se misturar) | sim                    |
| `str` com `str`                                       | sim (ordem alfabética) |
| `char` com `char`                                     | sim                    | 
| qualquer outra combinação                             | **erro semântico**     |

### Atribuição, declaração, argumentos e retorno

| Variável do tipo | Aceita valor do tipo |
|------------------|----------------------|
| `int`            | `int`                |
| `float`          | `float` ou `int`     |
| `str`            | `str`                |
| `char`           | `char`               |

---

## 8. Regras semânticas

O compilador acusa erro semântico quando:

1. uma variável ou `receita` é usada sem ter sido declarada;
2. um nome é declarado duas vezes no mesmo escopo;
3. uma variável é usada antes de receber um valor;
4. uma operação, atribuição, argumento ou retorno mistura tipos incompatíveis (seção 7);
5. uma `panela` é declarada dentro de um bloco (`garfo`, `colher`, `faca`, `liquidificar`, `flambar`);
6. uma `receita` é declarada fora do nível principal;
7. `comer` aparece fora de uma `receita`, ou não combina com o tipo de retorno dela;
8. uma `receita` é chamada com a quantidade ou o tipo de argumentos errado;
9. a variável do `flambar` não é do tipo `int`, ou o `inicio`/`fim` do `range` não é `int`;
10. uma `receita` com tipo de retorno pode terminar sem passar por um `comer`.

### Valor recebido dentro de um bloco

Se uma variável recebe o **primeiro** valor dentro de um bloco, ela pode ser usada dentro desse bloco, mas depois do `}` volta a contar como "sem valor". O bloco pode não ter sido executado.

```
panela x: int;
garfo (1 > 0) {
    x = 5;
    acenderfogao(x);   # ok
};
acenderfogao(x);       # erro: x pode não ter recebido valor
```

O contador do `flambar` é exceção: ele sempre recebe valor, então pode ser usado depois da repetição.

---

## 9. Mensagens de erro

Toda mensagem informa a etapa, a linha e o motivo:

```
Lexical error at line 3: invalid character '@'
Syntactic error at line 2: expected ';' after '10', found 'acenderfogao'
Semantic error at line 3: variable 'total' was not declared
```

Se houver qualquer erro, a compilação é interrompida e nenhum arquivo `.cpp` é gerado.

---

## 10. Recursos obrigatórios e adicionais

| Recurso                                           | Situação    |
|---------------------------------------------------|-------------|
| Declaração de variável numérica (`panela`, `int`) | obrigatório |
| Atribuição                                        | obrigatório |
| `+ - *`, parênteses e precedência                 | obrigatório |
| Exibição (`acenderfogao`)                         | obrigatório |
| Condicional com comparação numérica (`garfo`)     | obrigatório |
| `/`, `colher`, `faca`                             | adicional   |
| `float`, `str`, `char`                            | adicional   |
| `liquidificar`, `flambar`                         | adicional   |
| `receita`, `comer`                                | adicional   |

---

## 11. Exemplo de programa

```
# Cozine: calcula o preço de um pedido
panela quantidade: int = 3;
panela preco: float = 8.5;
panela total: float;
panela i: int;

total = quantidade * preco;
acenderfogao("Total:", total);
acenderfogao((quantidade + 2) * preco - 1);

garfo (total > 20) {
    acenderfogao("Desconto:", total - 20);
} colher (total == 20) {
    acenderfogao("Sem desconto");
} faca {
    acenderfogao("Pedido pequeno");
};

flambar (i em range(0, 3)) {
    acenderfogao("Prato", i);
};
```

Saída esperada:

```
Total: 25.5
41.5
Desconto: 5.5
Prato 0
Prato 1
Prato 2
```

---

## 12. Gramática (EBNF)

Notação usada:

| Notação                                | Significado                                                     |
|----------------------------------------|-----------------------------------------------------------------|
| `"texto"`                              | símbolo ou palavra escrita exatamente assim                     |
| `a b`                                  | `a` seguido de `b`                                              |
| `a \| b`                               | `a` ou `b`                                                      |
| `[ a ]`                                | `a` é opcional (zero ou uma vez)                                |
| `{ a }`                                | `a` se repete zero ou mais vezes                                |
| `IDENT`, `INT`, `FLOAT`, `STR`, `CHAR` | nome, inteiro, número decimal, texto e caractere (seções 2 e 3) |

```
programa     = { comando } ;

comando      = declaracao | atribuicao | chamada_cmd | exibicao
             | condicional | enquanto | para | receita | retorno ;

declaracao   = "panela" IDENT ":" tipo [ "=" expressao ] ";" ;
tipo         = "int" | "float" | "str" | "char" ;
atribuicao   = IDENT "=" expressao ";" ;
chamada_cmd  = chamada ";" ;
exibicao     = "acenderfogao" "(" argumentos ")" ";" ;

condicional  = "garfo" condicao bloco
               { "colher" condicao bloco }
               [ "faca" bloco ] ";" ;
enquanto     = "liquidificar" condicao bloco ";" ;
para         = "flambar" "(" IDENT "em" "range" "(" expressao "," expressao ")" ")" bloco ";" ;

receita      = "receita" IDENT "(" [ parametro { "," parametro } ] ")" [ "->" tipo ] bloco ";" ;
parametro    = IDENT ":" tipo ;
retorno      = "comer" [ expressao ] ";" ;

bloco        = "{" { comando } "}" ;
condicao     = "(" expressao comparador expressao ")" ;
comparador   = "==" | "!=" | "<" | ">" | "<=" | ">=" ;

expressao    = termo { ( "+" | "-" ) termo } ;
termo        = unario { ( "*" | "/" ) unario } ;
unario       = "-" unario | fator ;
fator        = INT | FLOAT | STR | CHAR | chamada | IDENT | "(" expressao ")" ;
chamada      = IDENT "(" [ argumentos ] ")" ;
argumentos   = expressao { "," expressao } ;
```

Observações:

- **Precedência:** cada nível da expressão é uma regra (`expressao` → `termo` → `unario` → `fator`). Quanto mais embaixo, mais forte. Por isso `*` e `/` são resolvidos antes de `+` e `-`, e os parênteses antes de tudo.
- **Esquerda para a direita:** as repetições `{ ... }` em `expressao` e `termo` montam a árvore da esquerda para a direita, então `10 - 3 - 2` vira `(10 - 3) - 2`.
- **Um token à frente:** quando um comando ou um `fator` começa com `IDENT`, o parser olha o token seguinte para decidir. Se vier `=`, é atribuição. Se vier `(`, é chamada de `receita`. Nos outros casos, é uma variável.
- Cada regra da gramática virou uma função no arquivo `compiler/parser.py` (`parse_declaration`, `parse_if`, `parse_expression`...).
