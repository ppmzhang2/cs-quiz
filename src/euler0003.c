#include <math.h>
#include <stdio.h>
#include <string.h>

#define N_MAX 2000
#define NUM 600851475143
#define FACTOR 775146

char primes[FACTOR];

void eratosthenes_sieve (char[], unsigned long);

int main () {
    eratosthenes_sieve (primes, FACTOR);
    for (unsigned long i = 0; i <= FACTOR; i++) {
        if (primes[i] == 1 && NUM % i == 0) {
            printf ("%ld ", i);
        }
    }
    return 0;
}

void eratosthenes_sieve (char array[], unsigned long limit) {
    memset (array, 1, limit);
    array[0] = array[1] = 0;
    for (int i = 2; i <= sqrt (limit); i++) {
        if (array[i] == 1) {
            for (int j = i; j * i <= limit; j++) {
                array[j * i] = 0;
            }
        }
    }
}
