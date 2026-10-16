#include <iostream>
#include <string>

int main() {
    double preco = 12.5;
    int qtd = 3;
    std::string prato = "risoto";
    char tamanho = 'G';
    std::cout << prato + std::string(" de cogumelos") << std::endl;
    std::cout << "Tamanho:" << " " << tamanho << std::endl;
    std::cout << "Total:" << " " << preco * qtd << std::endl;
    std::cout << "Por pessoa:" << " " << static_cast<double>(qtd) / 4 << std::endl;
    if (prato == std::string("risoto")) {
        std::cout << "prato do dia" << std::endl;
    }
    if (tamanho != 'P') {
        std::cout << "nao e pequeno" << std::endl;
    }
    return 0;
}
