import numpy as np

'''
标准形的求解，根据作业题的单纯形表硬写出来的，有点儿丑陋
'''
def simplex(c, A, b):
    m, n = A.shape
    tableau = np.hstack((np.zeros(m).reshape(m,1),b.reshape(m, 1),A)) #C_b,b,A_
    tableau = np.vstack((tableau,np.hstack((np.zeros(1),np.zeros(1),c))))#加一行z

    while True:
        # 更新检验数和最优解
        _c = np.hstack((np.zeros(1), c))
        c_b = tableau[:-1, 0]
        for j in range(1, n + 2):
            tableau[-1, j] = _c[j - 1] - np.dot(c_b, tableau[:-1, j])
        print('------')
        print(tableau)
        print('------')
        if np.all(tableau[-1, 2:-1] <= 0): #检验数如果都<=0，找到最优解
            break
        # 选择进基变量
        sigma = tableau[-1, 2:]
        col = np.argmax(sigma)+2

        # 选择出基变量
        arr = tableau[:-1, col]
        b = tableau[:-1, 1]
        row = 0
        ratio = float('inf')
        for i in range(m):
            if arr[i]>0:
                alpha = b[i]/arr[i]
                if alpha<ratio:
                    ratio = alpha
                    row = i
        # 找到主元
        pivot = tableau[row, col]

        #进行归一化
        tableau[row, 1:] /= pivot

        #修改c_b
        tableau[row,0] = c[col-2]
        # 其他行的变化
        for k in range(m):
            if k != row:
                tableau[k, 1:] -= tableau[k, col] * tableau[row, 1:]

    basic_idx = np.where(tableau[-1, 2:] == 0)[0]
    x = np.zeros(n)
    x[basic_idx] = tableau[:-1,1] #有一点儿小问题，没有记录基变量的索引，可以增加一列记录索引，我这里偷懒了
    solution = {'optimal_value': -tableau[-1, 1], 'basic_variables': np.where(tableau[-1,2:] == 0)[0] + 1,'x:':x}
    return solution


if __name__=='__main__':
    A = np.array([[1,4,2,1,0],[1,2,4,0,1]])
    c = np.array([6,14,13,0,0])
    b = np.array([48,60])
    print(np.hstack((np.zeros(1),np.zeros(1),c)))
    solution = simplex(c,A,b)
    print(solution)

    # A = np.array([[4, 5, -2, 1, 0], [1, -2, 1, 0, 1]])
    # c = np.array([-3, 2, 4, 0, 0])
    # b = np.array([22, 30])
    # print(np.hstack((np.zeros(1), np.zeros(1), c)))
    # solution = simplex(c, A, b)
    # print(solution)