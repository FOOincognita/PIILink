/* ----- main.cpp | TestThree Student3 | UIN686375998 | Tester3@tamu.edu | csce-12x-709 | Submission ID: 132000448 ----- */

#include <iostream>
#include "tester.h"


int main(int argc, char const *argv[]) {
    std::cout << "Howdy World!" << std::endl
              << "Add: " << add(10, 2) << std::endl
              << "Subtract: " << subtract(10, 2) << std::endl;
}
/* ----- tester.cpp | TestThree Student3 | UIN686375998 | Tester3@tamu.edu | csce-12x-709 | Submission ID: 132000448 ----- */

#include "tester.h"

int add(int a, int b) {
    return a + b;
}

int subtract(int a, int b) {
    return a - b;
}/* ----- tester.h | TestThree Student3 | UIN686375998 | Tester3@tamu.edu | csce-12x-709 | Submission ID: 132000448 ----- */

#ifndef TESTER_H__
#define TESTER_H__

int add(int a, int b);
int subtract(int a, int b);

#endif