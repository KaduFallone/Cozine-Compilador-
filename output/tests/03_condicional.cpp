#include <iostream>
#include <string>

int main() {
    int nota = 7;
    if (nota >= 6) {
        std::cout << "1 verdadeira: aprovado" << std::endl;
    }
    if (nota > 9) {
        std::cout << "2 nunca aparece" << std::endl;
    }
    std::cout << "2 falsa: bloco ignorado" << std::endl;
    if (nota != 7) {
        std::cout << "3 nunca aparece" << std::endl;
    } else {
        std::cout << "3 falsa: caiu no faca" << std::endl;
    }
    if (nota < 5) {
        std::cout << "4 nunca aparece" << std::endl;
    } else if (nota < 8) {
        std::cout << "4 colher verdadeira: recuperacao" << std::endl;
    } else {
        std::cout << "4 nunca aparece" << std::endl;
    }
    if (nota * 2 == 14) {
        std::cout << "5 verdadeira: dobro e 14" << std::endl;
    }
    return 0;
}
