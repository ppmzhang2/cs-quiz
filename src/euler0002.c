#include <stdio.h>
#include <stdlib.h>

unsigned long fib_even_sum (unsigned long);

int main () {
    const unsigned long MAX_LIMIT = 4000000;
    unsigned long sum             = fib_even_sum (MAX_LIMIT);
    printf ("The sum of the even fibonacci numbers (under %ld) is %ld",
            MAX_LIMIT, sum);
    return 0;
}

unsigned long fib_even_sum (unsigned long limit) {
    unsigned long a     = 2;
    unsigned long b     = 3;
    unsigned long total = 0;
    unsigned long tmp;
    int n = 0;
    while (1) {
        if (a > limit) {
            break;
        }
        tmp = a + b;
        a   = b;
        b   = tmp;
        if (n % 3 == 0) {
            total += a;
        }
        n++;
    }
    return total;
}
