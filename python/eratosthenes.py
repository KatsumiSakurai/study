import numpy as np

def simple_primes(N=100):
    primes = []
    for i in range(2, N):
        isPrime = True
        for p in primes:
            if i % p == 0:
                isPrime = False
                break
        if isPrime:
            primes.append(i)
    return primes

def eratosthenes(N=100):
    isPrime = np.ones(N+1)
    isPrime[0] = 0
    isPrime[1] = 0

    for i in range(2, len(isPrime)):
        if isPrime[i] == 0:
            continue
        for j in range(i * 2, len(isPrime), i):
            isPrime[j] = 0
    return np.where(isPrime == 1)[0]
    

if __name__ == '__main__':
    # ret = eratosthenes(100)
    ret = simple_primes(100)
    print(list(ret))
