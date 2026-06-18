import numpy as np
import matplotlib.pyplot as plt


def gen_matrix(arr, p1, p2): 
    alpha1, alpha2 = np.random.uniform(0, 2 * np.pi), np.random.uniform(0, 2 * np.pi)
    
    t1, t2 = np.cos(alpha1) + 1j * np.sin(alpha1), np.cos(alpha2) + 1j * np.sin(alpha2)

    arr[*p1] = t1
    arr[*p2] = t2

    return arr


def gen_base_matrix(n, values):
    arr = np.zeros((n, n), dtype=complex)
    for x in range(n):
        for y in range(n): 
            arr[x, y] = np.random.choice(values)

    return arr


iter = 0

while True:
    X, Y = [], []

    N = np.random.randint(3, 10)
    values=[0, -1, 1, -1j, 1j]

    arr = gen_base_matrix(N, values)

    p1 = np.random.randint(0, N, size=2)
    p2 = np.random.randint(0, N, size=2)

    np.savez(f'tests/matrix/data_{iter}.npz', p1=p1, p2=p2, N=N, arr=arr)

    print(N)
    print(p1, p2)
    print(arr)
    print(100 * '=' + '\n')

    for i in range(200_000):
        matrix = gen_matrix(arr, p1, p2)

        lambdas = np.linalg.eigvals(matrix)
        
        # lambdas = [lambd for lambd in lambdas if lambd.imag != 0]
        
        for lambd in lambdas:
            X.append(lambd.real)
            Y.append(lambd.imag)
        
    plt.figure(figsize=(16, 9))

    color = 'black'

    alpha = 0.03
    s = 0.1

    plt.scatter(np.array(X), np.array(Y), color=color, alpha=alpha, s=s)
        

    # plt.xlim(-3, 3)
    # plt.ylim(-3, 3)

    # plt.axis('off')

    plt.tight_layout()
    plt.savefig(f'tests/img/eigenvalues_{iter}.png', dpi=200)

    plt.close()
    plt.clf()

    iter += 1
