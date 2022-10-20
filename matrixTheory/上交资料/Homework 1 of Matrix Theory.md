## 习题一

### 1.

计算：

(1)

> $$
\begin{pmatrix}
\cos x & \sin x \\
-\sin x & \cos x \\
\end{pmatrix}^n
$$

令 $R = $$
\begin{pmatrix}
\cos x & \sin x \\
-\sin x & \cos x \\
\end{pmatrix}
$，则 $\vert R \vert = 1$ 且 $R$ 是一个单位旋转变换，转角为 $x$.

于是

$$
R^n = \begin{pmatrix}
\cos nx & \sin nx \\
-\sin nx & \cos nx \\
\end{pmatrix}
$$

(3)

> $$
\begin{pmatrix}
a & 1 & \, & \, & \, \\
\, & a & 1 & \, & \, \\
\, & \, & a & 1 & \, \\
\, & \, & \, & a & 1 \\
\, & \, & \, & \, & a \\
\end{pmatrix}^n
$$

令 $A=aI+J$，其中 $J$ 为幂零阵 i.e. $J^n=0，\forall n\geq 5$

$$
J = \begin{pmatrix}
0 & 1 & \, & \, & \, \\
\, & 0 & 1 & \, & \, \\
\, & \, & 0 & 1 & \, \\
\, & \, & \, & 0 & 1 \\
\, & \, & \, & \, & 0 \\
\end{pmatrix}
$$

于是对 $n\geq 4$, 我们有

$$
\begin{align*}
A^n &= (aI+J)^n = (aI)^n+C_n^1(aI)^{n-1}J+\cdots+C_n^{n-1}(aI)J^{n-1}+J^n \\
&= a^nI+C_n^1a^{n-1}J+C_n^2a^{n-2}J^2+C_n^3a^{n-3}J^3+C_n^4a^{n-4}J^4 \\
&= \begin{pmatrix}
a^n & C_n^1a^{n-1} & C_n^2a^{n-2} & C_n^3a^{n-3} & C_n^4a^{n-4} \\
\, & a^n & C_n^1a^{n-1} & C_n^2a^{n-2} & C_n^3a^{n-3} \\
\, & \, & a^n & C_n^1a^{n-1} & C_n^2a^{n-2} \\
\, & \, & \, & a^n & C_n^1a^{n-1} \\
\, & \, & \, & \, & a^n \\
\end{pmatrix}
\end{align*}
$$

其中，定义 $C_n^i=0$ 如果 $n<i$.

### 2.

> 证明：与任意 $n$ 阶方阵可交换的矩阵必是纯量矩阵 $\lambda I$.

记 $A=(a_{ij})=\sum\limits_{i=1}^n\sum\limits_{j=1}^n a_{ij}E_{ij}$

由题意 $AE_{ij}=E_{ij}A$，比较两边矩阵元素可得 $a_{ii}=a_{jj}, a_{ij}=0, \forall i\neq j$

### 3.

> 利用初等变换求 $A^{-1}B$ 及 $CA^{-1}$, 其中
>
> $$
A=\begin{pmatrix}
4 & 5 & 0 \\
2 & 3 & 1 \\
2 & 7 & -3 \\
\end{pmatrix} , B=\begin{pmatrix}
4 & 5 & 0 & 10 \\
2 & 3 & 1 & -1 \\
2 & 7 & 9 & -3 \\
\end{pmatrix} , C=\begin{pmatrix}
4 & 5 & 0 \\
2 & 3 & 1 \\
2 & 7 & 9 \\
-2 & 3 & 7 \\
\end{pmatrix}
$$

利用矩阵的行列变换可以简化求解

$$
(\begin{array}{@{}c:c@{}}
A & B \\
\end{array}) \xrightarrow[左乘A^{-1}]{初等行变换} (\begin{array}{@{}c:c@{}}
I & A^{-1}B \\
\end{array})
$$

$$
\begin{pmatrix}
A \\  \hdashline\,
C \\
\end{pmatrix} \xrightarrow[右乘A^{-1}]{初等列变换}
\begin{pmatrix}
I \\  \hdashline\,
CA^{-1} \\
\end{pmatrix}
$$

结果为

$$
\begin{split}
A^{-1}B &= \begin{pmatrix}
1 & 0 & -\frac52 & \frac{95}{12} \\
0 & 1 & 2 & -\frac{13}{3} \\
0 & 0 & 0 & -\frac{23}{6} \\
\end{pmatrix} \\
CA^{-1} &= \begin{pmatrix}
1 & 0 & 0 \\
0 & 1 & 0 \\
-4 & 9 & 0 \\
-\frac{14}{3} & 8 & \frac13 \\
\end{pmatrix}
\end{split}
$$

### 5.

> 证明：对任意矩阵 $A$, 有 $r(A^*A) = r(AA^*) = r(A)$.

记 $N(A)$ 为 $AX=0$ 的解空间。欲证 $r(A'A)=r(A)$ 只需证[^1] $\dim N(A'A)=\dim N(A)$

显然 $\dim N(A'A) \geq \dim N(A)$，这是因为 $AX=0$ 的解均为 $A'AX=0$ 的解.

又当 $A'AX=0$ 时，$X'A'AX=(AX)'(AX)=0$ 则 $AX=0$

从而 $\dim N(A'A)\leq\dim N(A)$

[^1]: 这是因为 $\dim N(A)= n - r(A)$

### 7.

> 设 $\omega$ 是 $n$ 次本原单位根 (可设 $\omega=\mathrm{e}^{2\pi i/n}=\cos\frac{2\pi}{n}+i\sin\frac{2\pi}{n}$ )，试求Fourier[^2]矩阵
>
> $$
\begin{pmatrix}
1 & 1 & 1 & \cdots & 1 \\
1 & \omega & \omega^2 & \cdots & \omega^{n-1} \\
1 & \omega^2 & \omega^4 & \cdots & \omega^{2(n-1)} \\
1 & \vdots & \vdots & \, & \vdots \\
1 & \omega^{n-1} & \omega^{2(n-1)} & \cdots & \omega^{(n-1)\times(n-1)} \\
\end{pmatrix}
$$
的逆矩阵.

由本原单位根的性质[^4]，知 $\forall j = 0, 1, 2, \cdots, n-1$

$$
(\omega^j)^0 + (\omega^j)^1 + \cdots + (\omega^j)^{n-1} = 0 \quad \omega^j \cdot \bar{\omega}^j = 1
$$

现记 $F$ 中第 $i$ 行为 $\alpha_{i+1}=(1, \omega^i, \omega^{2i}, \cdot, \omega^{(n-1)i})$, 其中 $i=0,1,\cdots, n-1$ 则有

$$
\alpha_{i+1}\bar{\alpha_{j+1}}' = 1 + \omega^i\bar{\omega}^j + \cdot + \omega^{(n-1)i}\cdot\bar{\omega}^{(n-1)j} = \begin{cases}
n & i=j \\
0 & i\neq j \\
\end{cases}
$$

故 $F\cdot \bar{F}' = nI$

即

$$
F^{-1} = \frac1n \bar{F}' = \frac1n \begin{pmatrix}
1 & 1 & 1 & \cdots & \cdots & 1 \\
1 & \bar{\omega} & \bar{\omega}^2 & \cdots & \cdots & 1 \\
1 & \bar{\omega}^2 & \bar{\omega}^4 & \cdots & \cdots & \bar{\omega}^{2(n-1)} \\
\vdots & \vdots & \vdots & & & \vdots \\
\vdots & \vdots & \vdots & & & \vdots \\
1 & \bar{\omega}^{n-1} & \bar{\omega}^{2(n-1)} & \cdots & \cdots & \bar{\omega}^{(n-1)\times (n-1)} \\
\end{pmatrix}
$$

[^4]: 本原单位根共轭分布于单位圆上

[^2]: Joseph Fourier (1768-1830), 法国著名数学家与物理学家，发现了三角级数、Fourier变换、热传导方程、热传导定律和温室效应.

### 13.

> 设 $n$ 阶矩阵 $A$ 可逆，$B,C,D$ 分别是 $n\times m, m\times n, m\times m$ 矩阵. 证明
>
> $$
\begin{vmatrix}
A & B \\
C & D \\
\end{vmatrix} = \begin{vmatrix}
A
\end{vmatrix} \cdot \begin{vmatrix}
D - C A^{-1} B
\end{vmatrix}
$$

在增广矩阵上作初等变换

$$
\left( \begin{array}{@{}cc:cc@{}}
A & B & I & 0 \\
C & D & 0 & I \\
\end{array} \right) \xrightarrow{-CA^{-1}\times r(1)+r(2)} \left( \begin{array}{@{}cc:cc@{}}
A & B & I & 0 \\
0 & D-CA^{-1}B & -CA^{-1} & I \\
\end{array} \right)
$$

等价于

$$
\begin{pmatrix}
I & 0 \\
-CA^{-1} & I \\
\end{pmatrix} \begin{pmatrix}
A & B \\
C & D \\
\end{pmatrix} = \begin{pmatrix}
A & B \\
0 & D-CA^{-1}B \\
\end{pmatrix}
$$

两边取行列式即得.


### 14.

(1)
> 设矩阵 $A,C$ 均可逆，求分块矩阵 $\left(\begin{smallmatrix} A & B \\ C & D \\ \end{smallmatrix}\right)$ 的逆矩阵.

$$
\left(\begin{array}{@{}cc:cc@{}}
A & B & I & 0 \\
0 & C & 0 & I \\
\end{array}\right) \xrightarrow[C^{-1}\times r(2)]{A^{-1}\times r(1)} \left(\begin{array}{@{}cc:cc@{}}
I & A^{-1}B & A^{-1} & 0 \\
0 & I & 0 & C^{-1} \\
\end{array}\right) \xrightarrow{-A^{-1}B\times r(2)+r(1)} \left(\begin{array}{@{}cc:cc@{}}
I & 0 & A^{-1} & -A^{-1}BC^{-1} \\
0 & I & 0 & C^{-1} \\
\end{array}\right)
$$

于是

$$
\begin{pmatrix}
A & B \\
0 & C \\
\end{pmatrix}^{-1} = \begin{pmatrix}
A^{-1} & -A^{-1}BC^{-1} \\
0 & C^{-1} \\
\end{pmatrix}
$$

(2)
> 设矩阵 $A$ 可逆，$D-CA^{-1}B$ 也可逆，证明矩阵 $\left( \begin{smallmatrix} A & B \\ C & D \\ \end{smallmatrix} \right)$ 也可逆并求其逆.

结合[13](###13.) 和 (1) 中结论，可设 $F=D-CA^{-1}B$

$$
\begin{split}
\begin{pmatrix}
A & B \\
C & D \\
\end{pmatrix}^{-1} &= \begin{pmatrix}
A & B \\
0 & F \\
\end{pmatrix}^{-1} \begin{pmatrix}
I & 0 \\
-CA^{-1} & I \\
\end{pmatrix} \\
&= \begin{pmatrix}
A^{-1} & -A^{-1}BF^{-1} \\
0 & F^{-1} \\
\end{pmatrix} \begin{pmatrix}
I & 0 \\
-CA^{-1} & I \\
\end{pmatrix} \\
&= \begin{pmatrix}
A^{-1}+A^{-1}BF^{-1}CA^{-1} & -A^{-1}BF^{-1} \\
-F^{-1}CA^{-1} & F^{-1} \\
\end{pmatrix} \\
\end{split}
$$

### 17.

> 求下列各矩阵的满秩分解：
> $$
A=\begin{pmatrix}
1 & 2 & 3 & 0 \\
0 & 2 & 1 & -1 \\
1 & 0 & 2 & 1 \\
\end{pmatrix}
$$

$$
\begin{pmatrix}
1 & 2 & 3 & 0 \\
0 & 2 & 1 & -1 \\
1 & 0 & 2 & 1 \\
\end{pmatrix} \xrightarrow{初等行变换} \begin{pmatrix}
1 & 2 & 3 & 0 \\
0 & 2 & 1 & -1 \\
0 & 0 & 0 & 0 \\
\end{pmatrix} \xrightarrow{标准化}
\begin{pmatrix}
1 & 0 & 2 & 1 \\
0 & 1 & \frac12 & -\frac12 \\ \hdashline
0 & 0 & 0 & 0 \\
\end{pmatrix} := H
$$

从而

$$
A = (a_1, a_2)\begin{pmatrix}
H_1 \\
H_2 \\
\end{pmatrix} = \begin{pmatrix}
1 & 2 \\
0 & 2 \\
1 & 0 \\
\end{pmatrix} \begin{pmatrix}
1 & 0 & 2 & 1 \\
0 & 1 & \frac12 & -\frac12 \\
\end{pmatrix}
$$

### 21.

> 证明例1.4.2[^3]中的 $(V,\oplus,\cdot)$ 是 $\mathbb{R}$ 上的线性空间.

- (C) **封闭性**： $\forall x,y\in V$，$x\oplus y\in V$
- (A1) **结合律**： $\forall x,y,z \in V$，$(x\oplus y)\oplus z=xyz=x\oplus (y\oplus z)$
- (A2) **交换律**： $\forall x,y\in V$，$x\oplus y=xy=y\oplus x$
- (A3) 存在**零向量**：存在 $ 1\in V$，使得 $\forall x\in V$，$x\oplus 1=x\cdot 1=x$
- (A4) 存在**负向量**：$\forall x\in V$，存在 $x^{-1}\in V$ 使得 $x\oplus x^{-1}=x\cdot x^{-1}=1$
- (B1) 数乘的结合律：设 $x\in V$，$a, b\in F$ 有
$$
a\cdot(b\cdot x)=a\cdot x^b=x^{ab}=(ab)\cdot x
$$
- (B2) 数乘关于向量加法的分配律： 设 $x,y\in V$，$k\in F$ 有
$$
k\cdot(x\oplus y)=(xy)^k=x^k y^k=x^k\oplus y^k=k\cdot x\oplus k\cdot y
$$
- (B3) 数乘关于数的加法分配律：设 $x\in V$，$a,b\in F$ 有
$$
(a+b)\cdot x = x^{a+b} = x^a\cdot x^b = x^a \oplus x^b = a\cdot x \oplus b\cdot x
$$
- (B4) 数乘初始条件：存在单位元"1"，使得 $1\cdot x = x^1 = x$，其中 $1\in F$

[^3]: $V=\lbrace\text{所有正实数}\rbrace$, $F=\mathbb{R}$, $x\oplus y = xy$, $k\cdot x = x^k \quad \forall k \in F, x,y \in V$

### 28.

> 证明 $1, x-1, (x-1)^2, \cdots, (x-1)^n$ 是 $\mathbb{R}[x]_{n+1}$ 上的一组基，并求多项式 $f(x)=a_0 + a_1 x + a_2 x^2 + \cdots + a_n x^n$在该组基下的坐标.

先证 $1, x-1, (x-1)^2, \cdots, (x-1)^n$ 线性无关.

若存在不全为0的 $k_0, k_1, \cdots, k_n$ 使得

$$
f(x)=k_0 \cdot 1+k_1\cdot (x-1)+\cdots+k_n\cdot(x-1)^n
$$

令 $x\to\infty$，可知最高项系数 $k_n=0$，依次下去得到 $k_{n-1}=\cdots=k_1=k_0=0$ 矛盾！

由泰勒展式

$$
f(x)=a_0+a_1 x+\cdots+a_n x^n = \sum\limits_{k=0}^n \frac{f^{(n)}(1)}{k!} (x-1)^k
$$

得到基坐标为

$$
\left( f(1), f'(1), \frac{f''(1)}{2!}, \cdots, \frac{f^{(n)}(1)}{n!} \right)
$$
