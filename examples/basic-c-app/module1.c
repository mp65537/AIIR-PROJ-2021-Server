#include "module1.h"

#include <stdio.h>

void function1(int number)
{
    printf("Called function1() with number = %d\n", number);
}

void function2(const char* text, int number)
{
    printf("Called function2() with text = '%s',"
        " number = %d\n", text, number);
}
