#include <iostream>
#include <string>

int main() {
    int a = 2;
    int b = 3;
    int c = 4;
    std::cout << a + b * c << std::endl;
    std::cout << (a + b) * c << std::endl;
    std::cout << 10 - 3 - 2 << std::endl;
    std::cout << a * (b + c) - 1 << std::endl;
    std::cout << -a * (b - c * 2) << std::endl;
    std::cout << a * b + static_cast<double>(c) / 8 << std::endl;
    std::cout << ((a + b) * (c - 1)) * 2 << std::endl;
    return 0;
}
