# Resultados dos testes

Gerado automaticamente por `python run_tests.py`.
Nos programas válidos, o resultado obtido é a saída do executável compilado a partir do C++ gerado.

**21 de 21 testes passaram.**

| Teste | Situação |
|---|---|
| `01_declaracao.cz` | passou |
| `02_expressoes.cz` | passou |
| `03_condicional.cz` | passou |
| `04_erro_lexico.cz` | passou |
| `05_erro_sintatico.cz` | passou |
| `06_erro_semantico.cz` | passou |
| `07_repeticao.cz` | passou |
| `08_receitas.cz` | passou |
| `09_tipos.cz` | passou |
| `10_erro_lexico_texto.cz` | passou |
| `11_erro_sintatico_parenteses.cz` | passou |
| `12_erro_sintatico_operando.cz` | passou |
| `13_erro_sintatico_bloco.cz` | passou |
| `14_erro_sintatico_colher.cz` | passou |
| `15_erro_sintatico_ordem.cz` | passou |
| `16_erro_semantico_sem_valor.cz` | passou |
| `17_erro_semantico_repetida.cz` | passou |
| `18_erro_semantico_tipos.cz` | passou |
| `19_erro_semantico_bloco.cz` | passou |
| `20_erro_semantico_receita.cz` | passou |
| `example.cz` | passou |

## 01_declaracao.cz

**Entrada**

```
# Teste 1: declaração, atribuição e saída
panela quantidade: int;
panela preco: int = 8;
panela total: int;

quantidade = 3;
total = quantidade * preco;

acenderfogao(quantidade);
acenderfogao(preco);
acenderfogao("Total:", total);
```

**Resultado esperado**

```
3
8
Total: 24
```

**Resultado obtido**

```
3
8
Total: 24
```

## 02_expressoes.cz

**Entrada**

```
# Teste 2: expressões, precedência e parênteses
panela a: int = 2;
panela b: int = 3;
panela c: int = 4;

acenderfogao(a + b * c);                 # 14  (* antes de +)
acenderfogao((a + b) * c);               # 20  (parênteses primeiro)
acenderfogao(10 - 3 - 2);                # 5   (esquerda para a direita)
acenderfogao(a * (b + c) - 1);           # 13
acenderfogao(-a * (b - c * 2));          # 10  (menos unário)
acenderfogao(a * b + c / 8);             # 6.5 (/ sempre dá float)
acenderfogao(((a + b) * (c - 1)) * 2);   # 30  (parênteses aninhados)
```

**Resultado esperado**

```
14
20
5
13
10
6.5
30
```

**Resultado obtido**

```
14
20
5
13
10
6.5
30
```

## 03_condicional.cz

**Entrada**

```
# Teste 3: condicional com condições verdadeiras e falsas
panela nota: int = 7;

garfo (nota >= 6) {
    acenderfogao("1 verdadeira: aprovado");
};

garfo (nota > 9) {
    acenderfogao("2 nunca aparece");
};
acenderfogao("2 falsa: bloco ignorado");

garfo (nota != 7) {
    acenderfogao("3 nunca aparece");
} faca {
    acenderfogao("3 falsa: caiu no faca");
};

garfo (nota < 5) {
    acenderfogao("4 nunca aparece");
} colher (nota < 8) {
    acenderfogao("4 colher verdadeira: recuperacao");
} faca {
    acenderfogao("4 nunca aparece");
};

garfo (nota * 2 == 14) {
    acenderfogao("5 verdadeira: dobro e 14");
};
```

**Resultado esperado**

```
1 verdadeira: aprovado
2 falsa: bloco ignorado
3 falsa: caiu no faca
4 colher verdadeira: recuperacao
5 verdadeira: dobro e 14
```

**Resultado obtido**

```
1 verdadeira: aprovado
2 falsa: bloco ignorado
3 falsa: caiu no faca
4 colher verdadeira: recuperacao
5 verdadeira: dobro e 14
```

## 04_erro_lexico.cz

**Entrada**

```
# Teste 4: erro léxico (símbolo que não existe na Cozine)
panela total: int = 10;
total = total @ 2;
acenderfogao(total);
```

**Resultado esperado**

```
Lexical error at line 3: invalid character '@'
```

**Resultado obtido**

```
Lexical error at line 3: invalid character '@'
```

## 05_erro_sintatico.cz

**Entrada**

```
# Teste 5: erro sintático (declaração sem o ';')
panela total: int = 10
acenderfogao(total);
```

**Resultado esperado**

```
Syntactic error at line 2: expected ';' after '10', found 'acenderfogao'
```

**Resultado obtido**

```
Syntactic error at line 2: expected ';' after '10', found 'acenderfogao'
```

## 06_erro_semantico.cz

**Entrada**

```
# Teste 6: erro semântico (variável não declarada)
panela preco: int = 8;
total = preco * 2;
acenderfogao(total);
```

**Resultado esperado**

```
Semantic error at line 3: variable 'total' was not declared
```

**Resultado obtido**

```
Semantic error at line 3: variable 'total' was not declared
```

## 07_repeticao.cz

**Entrada**

```
# Teste 7: repetições com liquidificar e flambar
panela contador: int = 0;
panela soma: int = 0;
panela i: int;

liquidificar (contador < 3) {
    acenderfogao("volta", contador);
    contador = contador + 1;
};

flambar (i em range(1, 5)) {
    soma = soma + i;
};

acenderfogao("soma de 1 a 4:", soma);
acenderfogao("i depois do flambar:", i);
```

**Resultado esperado**

```
volta 0
volta 1
volta 2
soma de 1 a 4: 10
i depois do flambar: 5
```

**Resultado obtido**

```
volta 0
volta 1
volta 2
soma de 1 a 4: 10
i depois do flambar: 5
```

## 08_receitas.cz

**Entrada**

```
# Teste 8: receitas (funções), com retorno, sem retorno e recursão
receita dobro(x: int) -> int {
    comer x * 2;
};

receita media(a: float, b: float) -> float {
    comer (a + b) / 2;
};

receita maior(a: int, b: int) -> int {
    garfo (a > b) {
        comer a;
    } faca {
        comer b;
    };
};

receita fatorial(n: int) -> int {
    garfo (n <= 1) {
        comer 1;
    };
    comer n * fatorial(n - 1);
};

receita anunciar(prato: str) {
    acenderfogao("Saindo:", prato);
};

acenderfogao(dobro(21));
acenderfogao(media(7, 8));
acenderfogao(maior(3, 9));
acenderfogao(fatorial(5));
anunciar("lasanha");
```

**Resultado esperado**

```
42
7.5
9
120
Saindo: lasanha
```

**Resultado obtido**

```
42
7.5
9
120
Saindo: lasanha
```

## 09_tipos.cz

**Entrada**

```
# Teste 9: tipos float, str e char
panela preco: float = 12.5;
panela qtd: int = 3;
panela prato: str = "risoto";
panela tamanho: char = 'G';

acenderfogao(prato + " de cogumelos");
acenderfogao("Tamanho:", tamanho);
acenderfogao("Total:", preco * qtd);
acenderfogao("Por pessoa:", qtd / 4);

garfo (prato == "risoto") {
    acenderfogao("prato do dia");
};

garfo (tamanho != 'P') {
    acenderfogao("nao e pequeno");
};
```

**Resultado esperado**

```
risoto de cogumelos
Tamanho: G
Total: 37.5
Por pessoa: 0.75
prato do dia
nao e pequeno
```

**Resultado obtido**

```
risoto de cogumelos
Tamanho: G
Total: 37.5
Por pessoa: 0.75
prato do dia
nao e pequeno
```

## 10_erro_lexico_texto.cz

**Entrada**

```
# Teste 10: erro léxico (texto sem aspas de fechamento)
panela nome: str = "Ana";
acenderfogao("Ola, nome);
```

**Resultado esperado**

```
Lexical error at line 3: unterminated string literal
```

**Resultado obtido**

```
Lexical error at line 3: unterminated string literal
```

## 11_erro_sintatico_parenteses.cz

**Entrada**

```
# Teste 11: erro sintático (parêntese sem fechamento)
panela x: int = (2 + 3 * 4;
acenderfogao(x);
```

**Resultado esperado**

```
Syntactic error at line 2: expected ')' after '4', found ';'
```

**Resultado obtido**

```
Syntactic error at line 2: expected ')' after '4', found ';'
```

## 12_erro_sintatico_operando.cz

**Entrada**

```
# Teste 12: erro sintático (expressão sem um dos operandos)
panela x: int = 5;
x = x * ;
```

**Resultado esperado**

```
Syntactic error at line 3: expected a value (number, text, character, name or '(') after '*', found ';'
```

**Resultado obtido**

```
Syntactic error at line 3: expected a value (number, text, character, name or '(') after '*', found ';'
```

## 13_erro_sintatico_bloco.cz

**Entrada**

```
# Teste 13: erro sintático (estrutura condicional incompleta: bloco sem '}')
panela x: int = 5;
garfo (x > 1) {
    acenderfogao(x);
```

**Resultado esperado**

```
Syntactic error at line 3: '{' was not closed with '}'
```

**Resultado obtido**

```
Syntactic error at line 3: '{' was not closed with '}'
```

## 14_erro_sintatico_colher.cz

**Entrada**

```
# Teste 14: erro sintático (';' no meio da sequência garfo/colher)
panela x: int = 5;
garfo (x > 10) {
    acenderfogao("grande");
};
colher (x > 1) {
    acenderfogao("medio");
};
```

**Resultado esperado**

```
Syntactic error at line 6: 'colher' without a 'garfo' before it
```

**Resultado obtido**

```
Syntactic error at line 6: 'colher' without a 'garfo' before it
```

## 15_erro_sintatico_ordem.cz

**Entrada**

```
# Teste 15: erro sintático (comando com elementos fora de ordem)
panela int: total;
```

**Resultado esperado**

```
Syntactic error at line 2: expected a variable name after 'panela', found 'int'
```

**Resultado obtido**

```
Syntactic error at line 2: expected a variable name after 'panela', found 'int'
```

## 16_erro_semantico_sem_valor.cz

**Entrada**

```
# Teste 16: erro semântico (variável usada antes de receber valor)
panela total: int;
acenderfogao(total + 1);
```

**Resultado esperado**

```
Semantic error at line 3: variable 'total' is used before receiving a value
```

**Resultado obtido**

```
Semantic error at line 3: variable 'total' is used before receiving a value
```

## 17_erro_semantico_repetida.cz

**Entrada**

```
# Teste 17: erro semântico (declaração repetida)
panela preco: int = 5;
panela preco: float = 2.5;
```

**Resultado esperado**

```
Semantic error at line 3: 'preco' was already declared at line 2
```

**Resultado obtido**

```
Semantic error at line 3: 'preco' was already declared at line 2
```

## 18_erro_semantico_tipos.cz

**Entrada**

```
# Teste 18: erro semântico (operação com tipos incompatíveis)
panela nome: str = "bolo";
panela x: int = 3;
acenderfogao(nome * x);
```

**Resultado esperado**

```
Semantic error at line 4: operator '*' cannot be applied to str and int
```

**Resultado obtido**

```
Semantic error at line 4: operator '*' cannot be applied to str and int
```

## 19_erro_semantico_bloco.cz

**Entrada**

```
# Teste 19: erro semântico (valor recebido só dentro do bloco)
panela x: int;
garfo (1 > 0) {
    x = 5;
    acenderfogao(x);
};
acenderfogao(x);
```

**Resultado esperado**

```
Semantic error at line 7: variable 'x' is used before receiving a value
```

**Resultado obtido**

```
Semantic error at line 7: variable 'x' is used before receiving a value
```

## 20_erro_semantico_receita.cz

**Entrada**

```
# Teste 20: erro semântico (receita chamada com argumentos errados)
receita soma(a: int, b: int) -> int {
    comer a + b;
};

acenderfogao(soma(1));
```

**Resultado esperado**

```
Semantic error at line 6: receita 'soma' expects 2 argument(s), but received 1
```

**Resultado obtido**

```
Semantic error at line 6: receita 'soma' expects 2 argument(s), but received 1
```

## example.cz

**Entrada**

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

**Resultado esperado**

```
Total: 25.5
41.5
Desconto: 5.5
Prato 0
Prato 1
Prato 2
```

**Resultado obtido**

```
Total: 25.5
41.5
Desconto: 5.5
Prato 0
Prato 1
Prato 2
```
