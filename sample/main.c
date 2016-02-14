
#include <mcs51/8051.h>

#include <stdio.h>
#include <ctype.h>
#include <stdint.h>

void putchar(char c)
{
    while(!TI);
    TI = 0;
    SBUF = c;
}

void main()
{
    int i = 0;
    char *input = "this is a test.";

    RI = 0;
    for(; input[i]; ++i) {
        input[i] = toupper(input[i]);
    }

    printf("%s", input);
}
