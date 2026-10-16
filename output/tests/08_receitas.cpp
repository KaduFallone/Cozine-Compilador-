#include <iostream>
#include <string>

int dobro(int x) {
    return x * 2;
}

double media(double a, double b) {
    return static_cast<double>((a + b)) / 2;
}

int maior(int a, int b) {
    if (a > b) {
        return a;
    } else {
        return b;
    }
}

int fatorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * fatorial(n - 1);
}

void anunciar(std::string prato) {
    std::cout << "Saindo:" << " " << prato << std::endl;
}

int main() {
    std::cout << dobro(21) << std::endl;
    std::cout << media(7, 8) << std::endl;
    std::cout << maior(3, 9) << std::endl;
    std::cout << fatorial(5) << std::endl;
    anunciar("lasanha");
    return 0;
}
