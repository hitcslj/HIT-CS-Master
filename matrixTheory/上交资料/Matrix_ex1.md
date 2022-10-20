
## 矩阵理论试题精选(一)

### 1.

设 $V = \mathbb{R}[x]_{2016}$ 是次数小于 $2016$ 的实多项式构成的实线性空间。设 $n\geq 0, f^{(n)}(x)$ 表示 $f(x)\in V$ 的 $n$ 阶导数，$f^{(0)}(x) = f(x)$. 给定 $V$ 的两个子空间 $U, W$ 如下：

$$
U=\{ f(x)\in V \mid f^{(n)}(0) = 0, n\leq 1949 \} \quad W=\{ g(x)\in V\mid g(x)=x^{1896}(x-1)^{60}h(x), \forall h(x)\in V \}
$$

则 $V$ 的子空间 $U+W$ 的维数 $\dim(U+W)$ 是多少？

<div STYLE="page-break-after: always;"></div>

### 2.

设 $\sigma$ 是 $\mathbb{R}^2$ 上线性变换，$e_1 = (1,0)'$，$e_2=(0,1)'$，$\sigma(e_1)=e_1$，$\sigma(e_1+e_2)=2e_1$，则 $\sigma$ 关于基 $e_1+e_2$，$e_1-e_2$ 的矩阵是？

<div STYLE="page-break-after: always;"></div>

### 3.

设

$$
U=\{ (x,y,z,w)'\in\mathbb{R}^4\mid x+y+z+w=0 \}\quad W=\{ (x,y,z,w)'\in\mathbb{R}^4\mid x-y+z-w=0 \}
$$

是通常欧式空间 $\mathbb{R}^4$ 的两个子空间，设 $I$ 是 $\mathbb{R}^4$ 上的恒等变换。

(1) 求 $U$ 与 $U\cap W$ 的正交补 $(U\cap W)^{\perp}$ 的各一组标准正交基；

(2) 试求出 $\mathbb{R}^4$ 上的所有正交变换 $\sigma$ 使得线性变换 $I-\sigma$ 的核 $\mathrm{Ker}(I-\sigma) = U$.

<div STYLE="page-break-after: always;"></div>

### 4.

设给定矩阵 $A=\left( \begin{smallmatrix} 2 & 0\\ 1 & 2 \\ \end{smallmatrix}\right)$, $B=\left( \begin{smallmatrix} -1 & 0 \\ 2 & -1 \\ \end{smallmatrix} \right)$, 矩阵空间 $\mathbb{R}^{2\times 2}$ 上线性变换 $T$ 为：$T(X) = kX + AXB$, $\forall X\in\mathbb{R}^{2\times2}$。$T$ 是可逆变换当且仅当参数 $k$ 满足何条件？

<div STYLE="page-break-after: always;"></div>

### 5.

设

$$
A = \begin{pmatrix}
0 & 0 & 1 & 0 & -1 \\
1 & -1 & 0 & 1 & 1 \\
-1 & 1 & 1 & -1 & -2 \\
1 & -1 & 1 & 1 & 0 \\
\end{pmatrix}
$$

(1) 求矩阵 $A$ 的一个满秩分解 $LR$, 使得 $L$ 的第一列为矩阵 $A$ 的最后一列，并求出 $A$ 的列空间 $R(A)$ 的一组基；

(2) 求 $A$ 的左零化空间 $N(A')$ 的一组基；

(3) 设 $b = (1,1,1,1)'$，求向量 $b$ 在线性空间 $R(A)$ 上的最佳近似

(4) 设 $\sigma$ 是线性空间 $\mathbb{R}^4$ 上的正交投影变换，且满足 $\sigma$ 的像空间 $\mathrm{Im}(\sigma) = R(A)$，求 $\sigma$ 在标准基 $e_1,e_2,e_3,e_4$ 下的矩阵。

<div STYLE="page-break-after: always;"></div>

### 6.

证明变换 $\mathrm{tr}: X\to \mathrm{tr}(X)$ 是线性空间 $M_n(R)$ 到 $R$ 的满足性质：$\sigma(XY) = \sigma(YX)$ 及 $\sigma(1)=n$ 的唯一线性变换.

<div STYLE="page-break-after: always;"></div>

### 7.

设 $V$ 是全体$3$阶实矩阵构成的实线性空间。设

$$
U=\{ A=(a_{ij})\in V \mid a_{12} + a_{23} + a_{31} + a_{32} = 0 \} \quad W=\{ A\in V \mid A' - A = 0 \}
$$

则 $\dim(U\cap W)$ 为多少？

<div STYLE="page-break-after: always;"></div>

### 8.

设 $U=\{ (x,y,z,w)\mid x+y+z+w=0 \}$, $W=\{ (x,y,z,w)\mid x-y+z-w=0 \}$ 是通常欧式空间 $\mathbb{R}^4$ 的两个子空间

(1) 求 $U\cap W$, $U+W$ 的维数和各自的一组标准正交基；

(2) 求 $U$ 的一个2维子空间 $U_0$ 使得其正交补空间 $U_0^{\perp}\subset W$;

(3) 设 $\sigma$ 是 $\mathbb{R}^4$ 上的正交投影变换使得 $\mathrm{Ker}(\sigma) = U$, 求 $\sigma$ 在标准基下的矩阵

<div STYLE="page-break-after: always;"></div>

### 9.

设有 $n(n\geq 2)$ 阶实对称矩阵

$$
A=\begin{pmatrix}
1+a_n^2 & a_1 & 0 & \cdots & 0 & 0 & a_n \\
a_1 & 1+a_n^2 & a_2 & \cdots & 0 & 0 & 0 \\
0 & a_2 & 1+a_2^2 & \cdots & 0 & 0 & 0 \\
\vdots & \vdots & \vdots & & \ddots & \vdots & \vdots \\
0 & 0 & 0 & \cdots & a_{n-2} & 1+a_{n-2}^2 & a_{n-1} \\
a_n & 0 & 0 & \cdots & 0 & a_{n-1} & 1+a_{n-1}^2 \\
\end{pmatrix}
$$

其中 $a_i (1\leq i\leq n)$ 为实数。记 $x=(x_1, x_2, \cdots, x_n)'$, $f(x) = f(x_1, x_2, \cdots, x_n)=x'Ax$.

(1) 判断集合 $U = \{ x\in\mathbb{R}^n \mid f(x)=0 \}$ 是否为 $\mathbb{R}^n$ 的子空间；如果是，求其维数；如果否，求其生成的子空间的维数；

(2) 设存在 $\mathbb{R}^n$ 的内积 $(\cdot, \cdot)$ 使得对任意 $x\in\mathbb{R}^n$ 有 $(x,x)= f(x)$，求 $a_i (1\leq i \leq n)$ 的值；并求向量 $\alpha = (1,0,\cdots, 0)'$ 与 $\beta = (1,1,\cdots,1)’$ 在该內积下的长度与夹角

<div STYLE="page-break-after: always;"></div>


### 10.

设 $V=M_n({\mathbb{C}})$ 是全体$n$阶复矩阵构成的线性空间，$A, B\in V$，对任意 $X\in V$，定义 $\sigma(X) = AX - XB$。证明：$A$ 与 $B$ 没有公共特征值的充分必要条件是对任意$n$阶矩阵 $C\in V$，存在唯一的$n$阶矩阵 $X\in V$ 使得 $\sigma(X) = C$
