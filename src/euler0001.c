#include <stdio.h>

int range_sum (int);
const int FACTOR1 = 3;
const int FACTOR2 = 5;
const int PRODUCT = FACTOR1 * FACTOR2;

int main () {
    int limit;
    int real_limit;
    printf ("Please enter the upper limit: ");
    scanf ("%d", &limit);
    real_limit = limit - 1;
    int limit1 = real_limit / FACTOR1;
    int limit2 = real_limit / FACTOR2;
    int limit3 = real_limit / PRODUCT;
    int sum    = FACTOR1 * range_sum (limit1) + FACTOR2 * range_sum (limit2) -
    PRODUCT * range_sum (limit3);
    printf ("The sum of all the multiples of %d or %d below %d is %d", FACTOR1,
    FACTOR2, limit, sum);
    return 0;
}

int range_sum (int upper) {
    return upper * (upper + 1) / 2;
}
