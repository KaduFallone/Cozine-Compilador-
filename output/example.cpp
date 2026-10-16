#include <iostream>
#include <string>

int main() {
    int quantidade = 3;
    double preco = 8.5;
    double total;
    int i;
    total = quantidade * preco;
    std::cout << "Total:" << " " << total << std::endl;
    std::cout << (quantidade + 2) * preco - 1 << std::endl;
    if (total > 20) {
        std::cout << "Desconto:" << " " << total - 20 << std::endl;
    } else if (total == 20) {
        std::cout << "Sem desconto" << std::endl;
    } else {
        std::cout << "Pedido pequeno" << std::endl;
    }
    for (i = 0; i < 3; i++) {
        std::cout << "Prato" << " " << i << std::endl;
    }
    return 0;
}
