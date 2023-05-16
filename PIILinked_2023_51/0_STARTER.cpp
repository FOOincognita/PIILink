/* ----- main.cpp | STARTER CODE ----- */

#include <iostream>
#include "tester.h"


int main(int argc, char const *argv[]) {
    std::cout << "Howdy World!" << std::endl
              << "Add: " << add(10, 2) << std::endl
              << "Subtract: " << subtract(10, 2) << std::endl;
}
/* ----- tester.cpp | STARTER CODE ----- */

#include "tester.h"

int add(int a, int b) {
    return a + b;
}

int subtract(int a, int b) {
    return a - b;
}/* ----- tester.h | STARTER CODE ----- */

#ifndef TESTER_H__
#define TESTER_H__

int add(int a, int b);
int subtract(int a, int b);

#endif