#include <iostream>
#include <string>

int main() {
    int contador = 0;
    int soma = 0;
    int i;
    while (contador < 3) {
        std::cout << "volta" << " " << contador << std::endl;
        contador = contador + 1;
    }
    for (i = 1; i < 5; i++) {
        soma = soma + i;
    }
    std::cout << "soma de 1 a 4:" << " " << soma << std::endl;
    std::cout << "i depois do flambar:" << " " << i << std::endl;
    return 0;
}
