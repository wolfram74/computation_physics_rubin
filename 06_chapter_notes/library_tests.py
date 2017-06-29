
import numpy
import random
'''
6.6
    1:
mat_A = [
    [4.0,-2.0,1.0],
    [3.0,6.0, -4.0],
    [2.0, 1.0, 8.0]
    ]
mat_A_inv_exact = [
    [52.0, 17.0, 2.0],
    [-32.0, 30.0, 19.0],
    [-9.0, -8.0, 30.0]
    ]/263.0
use packages to numerically find inverse A, compare with exact solution, compare error there with error of A*A^-1 = 1
2: using A as the matrix, take 3 given b vectors and find their matching x vectors for Ax=b
3: given matrix of a particular form, convince yourself it has a particular set of eigenvalues and eigenvectors
4: take a specific 3x3 matrix and
    a: find it's eigenvalues, note degeneracy
    b: find the eigenvector for the unique value
    c: find a valid pair of eigenvectors for the degenerate value
5: giant 100x100 matrix solver that turns into very simple results
6: dirac gamma matrices, build gamma matrices, verify their properties

'''

def p66_1_2():
    mat_a = numpy.array([
    [4.0,-2.0,1.0],
    [3.0,6.0, -4.0],
    [2.0, 1.0, 8.0]
    ])
    num_inv = numpy.linalg.inv(mat_a)
    analytic = numpy.array([
    [52.0, 17.0, 2.0],
    [-32.0, 30.0, 19.0],
    [-9.0, -8.0, 30.0]
    ])/263.0
    print(mat_a)
    print(numpy.dot(mat_a, num_inv)-numpy.eye(3))
    print(num_inv-analytic)
    b_vecs = []
    b_vecs.append(numpy.array([12.0, -25.0, 32.0]))
    b_vecs.append(numpy.array([4.0, -10.0, 22.0]))
    b_vecs.append(numpy.array([20.0, -30.0, 40.0]))
    analytic_x_sol = []
    analytic_x_sol.append(numpy.array([1.0 , -2.0, 4.0]))
    analytic_x_sol.append(numpy.array([0.312 , -0.038, 2.677]))
    analytic_x_sol.append(numpy.array([ 2.319, -2.965, 4.790]))
    for index in range(len(b_vecs)):
        x_sol = numpy.linalg.solve(mat_a, b_vecs[index])
        print(x_sol, x_sol-analytic_x_sol[index])
    return

def p66_3():
    a = random.random()
    b = random.random()
    print(a, b)
    mat = numpy.array([[a, b],[-b, a]])
    vals, vecs = numpy.linalg.eig(mat)
    print(vecs[:,0])
    print(vecs[:,1])
    print(vals)

    return

def p66_4():
    mat_A = numpy.array([
        [-2.0,2.0,-3.0],
        [2.0,1.0,-6.0],
        [-1.0,-2.0,0.0]
        ])
    vals, vecs = numpy.linalg.eig(mat_A)
    print(vals, 'vs', [5,-3,-3])
    print(vecs)
    an_uni= -numpy.array([-1.0,-2.0,1.0])/6**.5
    deg_1 = numpy.array([-2.0,1.0,0.0])/5**.5
    deg_2 = numpy.array([3.0,0.0,1.0])/10**.5
    print('difference', vecs[:,1]+numpy.array([-1.0,-2.0,1.0])/6**.5)
    cross_num = numpy.cross(vecs[:,0], vecs[:,2])
    cross_an = numpy.cross(deg_1, deg_2)
    print('(x1 cross x2) cross (nx1 cross nx2)')
    print(numpy.cross(cross_num, cross_an))
    return

def p66_5():
    mat_a = numpy.array(
        [
        [1.0/(j+i-1) for i in range(1,101)]
        for j in range(1,101)]
        )
    # print(mat_a.shape, mat_a[:,0])
    x_vec = numpy.linalg.solve(mat_a, mat_a[:, 0])
    print(sum(x_vec)-1.0, x_vec)
    return

def p66_6():
    diracs = []
    diracs.append(numpy.array([[0.0,1.0],[1.0,0.0]]))
    diracs.append(numpy.array([[0.0,-1.0j],[1.0j,0.0]]))
    diracs.append(numpy.array([[1.0,0.0],[0.0,-1.0]]))
    print(numpy.matmul(diracs[0], diracs[0]))
    print(numpy.matmul(diracs[0], diracs[1]))
    gamma1 = numpy.array([
        [0,0,0,1],[0,0,1,0],
        [0,-1,0,0],[-1,0,0,0]
        ])
    gamma2 = numpy.array([
        [0,0,0,-1j],[0,0,1j,0],
        [0,1j,0,0],[-1j,0,0,0]
        ])
    gamma3 = numpy.array([
        [0,0,1,0],[0,0,0,-1],
        [-1,0,0,0],[0,1,0,0]
        ])
    print(numpy.linalg.inv(gamma2)+gamma2)
    print(numpy.matmul(gamma1, gamma2))
    return
# p66_1_2()
# p66_3()
# p66_4()
# p66_5()
p66_6()
