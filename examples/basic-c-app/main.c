#include <stdio.h>

#include "module1.h"

int main(int argc, char **argv)
{
	printf("Example app has started..\n");
    function1(51);
    function2("abcd1234", 87);
    printf("Example app ending..\n");
	return 0;
}
