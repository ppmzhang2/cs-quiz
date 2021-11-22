#include <math.h>
#include <stdio.h>
#include <string.h>
#include <vector>

#define N_MAX 2000
#define NUM 600851475143
#define FACTOR 775146

// boolean vecter in cpp uses **bitmap**
// memory efficiency is high!
std::vector<bool> primes (FACTOR, true);

void eratosthenes_sieve (std::vector<bool>& array, unsigned long);

int main () {
    eratosthenes_sieve (primes, FACTOR);
    for (unsigned long i = 0; i <= FACTOR; i++) {
        if (primes[i] && NUM % i == 0) {
            printf ("%ld\n", i);
        }
    }
    return 0;
}

void eratosthenes_sieve (std::vector<bool>& array, unsigned long limit) {
    array[0] = array[1] = false;
    for (int i = 2; i <= sqrt (limit); i++) {
        if (array[i] == 1) {
            for (int j = i; j * i <= limit; j++) {
                array[j * i] = false;
            }
        }
    }
}
