
## 习题三

### 18.

求 $A$ 的 Jordan 标准形，其中

$$
A = \begin{pmatrix}
0 & 2 & 0 & 1 & 0 \\
0 & 0 & 1 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 1 \\
0 & 0 & 0 & 0 & 0
\end{pmatrix}
$$

不难发现 $A$ 为严格上三角矩阵，$A^3 = 0, \mathrm{rank}(A) = 3$ 且 $A$ 的零度 $\eta = n - \mathrm{rank}(A) = 2$，故

$$
J_A = J_3(0) \oplus J_2(0)
$$

### 25.

详细证明如下定理，并研究矩阵 $A$ 的特征向量与变换矩阵 $P$ 的特征向量之间的关系.

> 设 $n$ 阶矩阵 $A$ 的 Jordan 标准形 $J = J_{n_1}(\lambda_1) \oplus J_{n_2}(\lambda_2) \oplus \cdots \oplus J_{n_m}(\lambda_m)$, 设 $\mu$ 为 $A$ 的一个特征值，记 $(A-\mu I)^k$ 的零度为 $\eta_k$, $J$ 中对角线元素为 $\mu$ 的 $k$ 阶 Jordan 块的个数为 $\ell_k$, 则
> 1. $\eta_1$ 等于 $J$ 中对角线元素为 $\mu$ 的 Jordan 块的个数
> 2. $\ell_1 = 2\eta_1 - \eta_2, \ell_k = 2\eta_k - \eta_{k-1} - \eta_{k+1}, k\geq 2$



### 27.

求下列矩阵的 Jordan 标准形

(1) $A = \begin{pmatrix} 0&1&0 \\ -4&4&0 \\ -2&1&2 \end{pmatrix}$

$$
|\lambda I - A| = (\lambda - 2)(\lambda^2 - 4\lambda + 4) = (\lambda - 2)^3
$$

$A$ 的特征值全为 $2$，检验可知 $(A-2I)^2 = 0$，最大 Jordan 块的阶数为 $2$

$$
J_A = J_2(2) \oplus J_1(2)
$$

(3) $A = \begin{pmatrix} 9&-6&-2 \\ 18&-12&-3 \\ 18&-9&-6 \end{pmatrix}$

$$
|\lambda I - A| = (\lambda + 3)(\lambda^2 + 6\lambda + 9) = (\lambda + 3)^3
$$

$A$ 的特征值全为 $3$，检验可知 $(A+3I)^2 = 0$，最大 Jordan 块的阶数为 $2$

$$
J_A = J_2(-3) \oplus J_1(-3)
$$

(5) $A = \begin{pmatrix} 0&-4&0 \\ 1&-4&0 \\ 1&-2&-2 \end{pmatrix}$

$$
|\lambda I - A| = (\lambda + 2)(\lambda^2 + 4\lambda + 4) = (\lambda + 2)^3
$$

$A$ 的特征值全为 $-2$，检验可知 $(A+2I)^2 = 0$，最大 Jordan 块的阶数为 $2$

$$
J_A = J_2(-2) \oplus J_1(-2)
$$

### 28.

求下列矩阵的 Jordan 标准形，并求变换矩阵 $P$, 使 $P^{-1}AP = J$

(1) $A = \begin{pmatrix} -4&2&10 \\ -4&3&7 \\ -3&1&7 \end{pmatrix}$

$$
|\lambda I - A| = \lambda^3 - 6\lambda^2 + 12\lambda - 8 = (\lambda - 2)^3
$$

$A$ 的特征值全为 $2$，检验可知 $(A+2I)^3 = 0$，最大 Jordan 块的阶数为 $3$

$$
J_A = J_3(2) = \begin{pmatrix}
2 & 1 & \\
  & 2 & 1 \\
  &   & 2
\end{pmatrix} = P^{-1} A P
$$

从而 $P^{-1}(A-2I)P = J_A - 2I$，即 $(A-2I)P = P(J_A-2I)$，容易解得

$$
P = \begin{pmatrix}
2 & 2 & -1 \\
1 & 2 & -2 \\
1 & 1 & 0
\end{pmatrix}
$$


(3) $A = \begin{pmatrix} 2&2&2&1 \\ -1&-1&-3&-2 \\ 1&2&5&3 \\ -1&-2&-4&-2 \end{pmatrix}$

$$
|\lambda I - A| = \lambda(\lambda - 2)(\lambda - 1)^2 + (\lambda - 1)^2 = (\lambda - 1)^4
$$

$A$ 的特征值全为 $1$，检验可知 $(A-I)^2 = 0$，最大 Jordan 块的阶数为 $2$

$$
A - I = \begin{pmatrix}
1 & 2 & 2 & 1 \\
-1 & -2 & -3 & -2 \\
1 & 2 & 4 & 3 \\
-1 & -2 & -4 & -3
\end{pmatrix} \rightarrow \begin{pmatrix}
1 & 2 & 2 & 1 \\
0 & 0 & -1 & -1 \\
0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0
\end{pmatrix}
$$

故 $(A-I)$ 的零度 $\eta_1 = 2$, $\eta_2 = 4$，且有 $\ell_1 = 2\eta_1 - \eta_2 = 0$，故不含一阶 Jordan 块

$$
J_A = J_2(1) \oplus J_2(1) = \begin{pmatrix}
1 & 1 & & \\
& 1 & & \\
& & 1 & 1 \\
& & & 1
\end{pmatrix} = P^{-1} A P
$$

从而 $P^{-1}(A-I)P = J_A - I$，即 $(A-I)P = P(J_A-I)$，容易解得

$$
P = \begin{pmatrix}
-1 & -2 & -2 & -3 \\
0 & 0 & 1 & 0 \\
1 & 0 & 0 & 0 \\
-1 & 1 & 0 & 0
\end{pmatrix}
$$


### 32.

设 $A=\begin{pmatrix} 0&0&1 \\ 1&0&-1 \\ 0&1&1 \end{pmatrix}$

(1) 求 $A$ 的特征值及 $A^{100}$

因 $|\lambda I - A| = (\lambda^2 + 1)(\lambda - 1)$，故 $\lambda_1 = i, \lambda_2 = -i, \lambda_3 = 1$

验证可知 $A^4 = I$，故 $A^{100} = (A^4)^{25} = I$

(2) $A$ 的 Jordan-Chevalley 分解是什么？

$A$ 有三个互不相同的特征值，故可对角化。令 $D = A, N = 0$ 显然有 $DN = ND = 0$，$A = A + 0$ 即为 $A$ 的 Jordan-Chevalley 分解

### 34.

设 $V$ 是由函数 $e^x, xe^x, x^2e^x, e^{2x}$ 的线性组合生成的线性空间. 定义 $V$ 的一个线性算子如下：$T(f)=f'$. 求 $T$ 的 Jordan 标准形及 Jordan 基

利用 $e^x$ 的导函数性质可以证明得到 $e^x, xe^x, x^2e^x, e^{2x}$ 线性无关。由题意

$$
\begin{align*}
T(e^x, xe^x, x^2e^x, e^{2x}) &= (e^x, xe^x+xe^x, 2xe^x+x^2e^x, 2e^{2x}) \\
&= (e^x, xe^x, x^2e^x, e^{2x}) \underbrace{\begin{pmatrix}
1 & 1 & 0 & 0 \\
0 & 1 & 2 & 0 \\
0 & 0 & 1 & 0 \\
0 & 0 & 0 & 2
\end{pmatrix}}_{A}
\end{align*}
$$

计算 $|\lambda I - A| = (\lambda-1)^3(\lambda-2) = 0$ 得 $\lambda_1 = \lambda_2 = \lambda_3 = 1, \lambda_4 = 2$

又 $\ell_1 = 2\eta_1 - \eta_2 = 0, \ell_2 = 0$ 故最大 Jordan 块的阶数为 $3$，$J_A = J_3(1) \oplus J_1(2)$

欲求 Jordan 基只需求得相似矩阵 $P$，使得 $P^{-1}AP = J_A$. 可解得

$$
P = \mathrm{diag} \{ 1, 1, \frac12, \frac12 \} \quad (\beta_1, \cdots, \beta_n) = (\alpha_1, \cdots, \alpha_n)P = (e^x, xe^x, \frac12 x^2e^x, \frac12 e^{2x})
$$

### 35.

如果矩阵 $A$ 的特征多项式和最小多项式相同，问 $A$ 的 Joran 标准形有何特点

即 $f_A(\lambda) = m(\lambda)$，且 $n$ 次多项式 $f_A(x)$ 有 $n$ 个不同的根。则 $A$ 的 Joran 标准形有 $n$ 个 Jordan 块.

### 36.

设 $\sigma$ 是 $\mathbb{C^n}$ 的循环位移变换，即 $\sigma \Big( (x_1, x_2, \cdots, x_n)' \Big) = (x_2, x_3, \cdots, x_n, x_1)'$. 证明：

(1) $\sigma$ 的特征值恰好为方程 $\lambda^n = 1$ 的所有根 $\lambda_j = e^{\frac{2\pi i}{n}j}, 1\leq j \leq n$

$$
\sigma\Big( (x_1, \cdots, x_n)' \Big) = A(x_1, \cdots, x_n)' = (x_2, x_3, \cdots, x_n, x_1)'
$$

故 $A = \begin{pmatrix} 0&1&& \\ &\ddots&& \\ &&\ddots&1 \\ 1&&&0 \end{pmatrix}$，令 $|\lambda I - A| = 0$ 得到

$$
\begin{vmatrix}
\lambda & 1 & & \\
& \ddots & & \\
& & \ddots & 1 \\
1 & & & \lambda
\end{vmatrix} = \lambda^n - 1 = 0
$$

(2) $\sigma$ 的属于特征值 $\lambda_j$ 的特征向量为 $\alpha_j = (\lambda_j, \lambda_j^2, \cdots, \lambda_j^n)'$, 且 $\Vert \alpha_j \Vert = \sqrt{n}$

假设特征值为 $\lambda_j$, 代入验证特征向量 $\alpha_j$

$$
A\alpha_j = (\lambda_j^2, \cdots, \lambda_j^n, \lambda_j)' = (\lambda_j^2, \cdots, \lambda_j^n, \lambda_j^{n+1})' = \lambda_j (\lambda_j, \lambda_j^2, \cdots, \lambda_j^n)' = \lambda_j \alpha_j
$$

(3) $\alpha_1, \cdots, \alpha_n$ 是 $\mathbb{C}^n$ 的一组正交基

由定义

$$
(\alpha_i, \alpha_j) = \lambda_i\bar\lambda_j + (\lambda_i\bar\lambda_j)^2 + \cdots + (\lambda_i\bar\lambda_j)^n = \lambda_i\bar\lambda_j \cdot \frac{1-(\lambda_i\bar\lambda_j)^n}{1-\lambda_i\bar\lambda_j} = 0
$$

最后一个等号是因为 $(\lambda_i\bar\lambda_j)^n = \lambda_i^n\bar\lambda_j^n = 1$

而当 $i=j$ 时，$\lambda_i\bar\lambda_i = |\lambda_i|^2 = 1$,

$$
(\alpha_i, \alpha_i) = \lambda_i\bar\lambda_i + (\lambda_i\bar\lambda_i)^2 + \cdots + (\lambda_i\bar\lambda_i)^n = n
$$

(4) 任何向量 $x = (x_1, x_2, \cdots, x_n)'$ 均是 $\sigma$ 的特征向量 $\alpha_j$ 的线性组合 $x=\sum_{j=1}^n a_j\alpha_j$，即 $x_k = \sum_{j=1}^n a_j e^{\frac{2\pi i}{n}j}$

因 $\alpha_1, \cdots, \alpha_n$ 是 $\mathbb{C}^n$ 的一组正交基，故任何向量可以被其线性表示。

(5) 上面的系数 $a_j = (x, \alpha_j)/n = \frac{1}{n}\sum_{k=1}^n x_k e^{-\frac{-2\pi i}{n} jk}$

由正交基的性质可知

$$
a_j = \frac{(x, \alpha_j)}{(\alpha_j, \alpha_j)} = (x, \alpha_j)/n
$$

(6) 研究 $\sigma$ 与第一章习题7中 Fourier 矩阵的关系，并由此再求该矩阵的逆

Fourier 矩阵可以写成 $(\alpha_0, \alpha_1, \cdots, \alpha_{n-1}$ 的形式。

由 (3) 所求

$$
(\alpha_i, \alpha_j) = \alpha_j^* \alpha_i = \begin{cases}
0 & i\neq j \\
n & i=j
\end{cases}
$$

可以得到 $F^{-1} = \dfrac{1}{n}F^*$, 其中 $F^*$ 为 $F$ 的共轭转置。

## 习题四

### 3.

证明两个正规矩阵相似的充要条件是特征多项式相同

1. 必要性

$$
\text{相似} \iff A = P^{-1}BP \iff |\lambda I - A| = |\lambda I - P^{-1}BP| = |P^{-1}||\lambda I - B||P| = |\lambda I - B|
$$

2. 充分性

$A$ 和 $B$ 的特征多项式相同，故 $A$ 和 $B$ 有相同的特征值。又 $A$ 和 $B$ 是正规阵，可以酉对角化，故两者相似于相同的对角阵，从而相似。

### 5.

设 $A$ 是 $n$ 阶正规矩阵，$x$ 是任意复数. 证明

(1) $A-xI$ 也是正规矩阵

$A$ 正规阵，故存在酉阵 $U$ 使得 $U^* A U = D$ 为对角阵， 从而

$$
U^* (A - xI) U = U^*AU - U^* xI U = D - xI
$$

也是一个对角阵，故 $A-xI$ 也是正规阵

(2) 对于任何向量 $x$，向量 $Ax$ 与 $A^*x$ 的长度相同

$$
\Vert Ax \Vert^2 = (Ax)^*(Ax) = x^*A^*Ax = x^*AA^*x = (A^*x)^*(A^*x) = \Vert A^*x \Vert^2
$$

(3) $A$ 的任一特征向量都是 $A^*$ 的特征向量

$A$ 为正规阵，设 $A$ 的酉对角化为 $U^*AU = D$, 两边同时乘 $U$ 得特征向量 $AU = DU$ 为 $U$ 的列向量；两边同时取共轭转置有 $U^*A^*U = D^*$，同样有 $A^*U = D^*U$ 特征向量仍为 $U$ 的列向量.

(4) $A$ 的属于不同特征值的特征向量正交

由(3)，不同特征值对应的特征向量为 $U$ 中不同的列，因 $U$ 为酉阵，故正交。

### 7.

设 $A$ 是正规矩，证明

(1) 若 $A$ 是幂等阵，则 $A$ 是 Hermite 矩阵

幂等阵的特征值非零即1，故必有 $A^* = A$

(2) 若 $A^3 = A^2$，则 $A^2 = A$

不妨假设 $A = U^*DU$ 为 $A$ 的酉对角化. 因 $A^3 = A^2$, 容易推出 $D^3 = D^2$, 进而 $D^2(D-I) = 0$. $A$ 的特征值均为 $0$ 或 $1$, 故 $A$ 幂等（也可直接从特征值考虑）

(3) 若 $A$ 又是 Hermite 阵，而且也是一个幂幺阵 (即 $A^k=I$)，则 $A$ 是对合阵 (即 $A^2 = I$)

不妨假设 $\lambda$ 为 $A$ 的特征值，则 $\lambda^k = 1$. 因 $A$ 为 Hermite 阵，故 $\lambda$ 为实数 $\lambda = \pm 1$, 进而 $\lambda^2 = I$, 容易推出 $A^2 = I$

### 8.

证明特征值的极大极小定理：设 $A$ 是 Hermite 矩阵，其全部特征值为 $\lambda_1 \leq \lambda_2 \leq \cdots \lambda_n$ 则：

$$
\lambda_k = \min_{w_i\in\mathbb{C}^n\atop 1\leq i\leq n-k} \max_{0\neq x\perp w_i\atop 1\leq i\leq n-k} \frac{x^* Ax}{x^*x} = \max_{w_i\in\mathbb{C}^n\atop 1\leq i\leq n-k} \min_{0\neq x\perp w_i\atop 1\leq i\leq n-k} \frac{x^* Ax}{x^*x}
$$

特别地,

$$
\lambda_{\max} = \lambda_n = \max_{x\neq 0, x\in\mathbb{C}} \frac{x^*Ax}{x^*} = \max_{x^*x=1} x^*Ax \\
\lambda_{\min} = \lambda_1 = \min_{x\neq 0, x\in\mathbb{C}} \frac{x^*Ax}{x^*} = \min_{x^*x=1} x^*Ax
$$

参考[wikipedia](https://en.wikipedia.org/wiki/Min-max_theorem)上的证明即可

### 10.

直接证明实对称矩阵与（实）正交矩阵可以酉对角化，从而均为正规矩阵.

1. 实对称矩阵 $A$ 可以对角化

$$
Q'AQ = (\alpha_1, \cdots, \alpha_n)' A (\alpha_1, \cdots, \alpha_n) = \mathrm{diag}\{ \lambda_1, \cdots, \lambda_n \}
$$

2. 实正交矩阵 $A$ 可做 Schur 三角变换

$$
U^* A U = T
$$

其中 $U$ 为酉阵，$A'A = I$ 得 $T^* = T^{-1}$ 进而 $T$ 为对角阵(上三角+下三角)。

### 21.

设 $A=LU$ 可逆，其中 $L$ 与 $U$ 分别为下三角矩阵与上三角矩阵，证明存在单位下三角矩阵 $L'$ 与上三角矩阵 $U'$, 使得 $A=L'U'$

利用高斯消元的思想进行分解，设 $A = (a_{ij})$，对其做行变换得上三角阵

$$
LA^{(0)} = A^{(1)} = \begin{pmatrix}
a_{11}^{(1)} & a_{12}^{(1)} & \cdots & a_{1n}^{(1)} \\
& a_{22}^{(1)} & \cdots & a_{2n}^{(1)} \\
& & \ddots & \vdots \\
& & & a_{nn}^{(1)}
\end{pmatrix} \quad L = \begin{pmatrix}
1 & & & \\
-m_{21} & \ddots & & \\
\vdots & & \ddots & \\
-m_{n1} & & & 1 \\
\end{pmatrix} \quad m_{i1} = -\frac{a_{i1}^{(1)}}{a_{11}^{(1)}}
$$

从而 $A^{(0)} = L^{-1}A^{(1)} = L'U'$ 即为所求

### 22.

证明矩阵 $A=\begin{pmatrix} 0&1 \\ 1&0 \end{pmatrix}$ 不存在三角分解

设 $A = \begin{pmatrix} 0&1 \\ 1&0 \end{pmatrix} = \begin{pmatrix} a&b \\ 0&c \end{pmatrix}\begin{pmatrix} 1&0 \\ d&1 \end{pmatrix} = \begin{pmatrix} a+bd & b \\ cd & c \end{pmatrix}$

找不到符合要求的 $a, b, c, d $. 故 $A$ 不存在三角分解

### 27.

设 $A = \begin{pmatrix} 2&1 \\ 1&1 \\ 2&1 \end{pmatrix}$, $b = \begin{pmatrix} 12\\ 6\\ 8\end{pmatrix}$

(1) 求 $R(A)$ 的标准正交基

容易知道 $R(A) = \mathrm{span}\{ (2,1,2)', (1,1,1)' \} = \mathrm{span}\{ \alpha_1, \alpha_2 \}$

对 $\alpha_1$, $\alpha_2$ 做 Schmidt 正交化可得标准正交基

$$
\begin{split}
&\beta_1 = \frac{\alpha_1}{\Vert \alpha_1 \Vert} = (\frac23, \frac13, \frac23)' \\
&\beta_2 = \frac{\alpha_2 - (\alpha_2, \beta_1)\beta_1}{\Vert \alpha_2 - (\alpha_2, \beta_1)\beta_1 \Vert} = (-\frac{1}{\sqrt{18}}, \frac{4}{\sqrt{18}}, -\frac{1}{\sqrt{18}})'
\end{split}
$$

(2) 写出 $A$ 的 $QR$ 分解

令 $Q = (\beta_1, \beta_2)$, 可得

$$
R = \begin{pmatrix}
\Vert \alpha_1 \Vert & (\alpha_2, \beta_1) \\
0 & \Vert \alpha_2 - (\alpha_2, \beta_1)\beta_1 \Vert
\end{pmatrix} = \begin{pmatrix}
3 & 5/3 \\
0 & \sqrt{2}/3
\end{pmatrix}
$$

(3) 求 $Ax=b$ 的最小二乘解

最小二乘解为 $x = (A'A)^{-1}A'b = R^{-1}Q'b$ 代入可得 $x = (4, 2)'$

(4) 证明 $u_1 = (0,1,0)'$, $u_2=(\frac{1}{\sqrt{2}}, 0, \frac{1}{\sqrt{2}})'$ 也是 $R(A)$ 的标准正交基，其中 $R(A)$ 为 $A$ 的列空间

不难发现 $u_1, u_2$ 线性无关且 $(u_1, u_2)=0$, $\Vert u_1 \Vert = \Vert u_2 \Vert = 1$. 故 $u_1, u_2$ 为 $R(A)$ 的标准正交基。

### 28.

求下列矩阵的 QR 分解

(1) $A= \begin{pmatrix} 0&1&1 \\ 1&1&0 \\ 1&0&0 \end{pmatrix}$

不难发现 $\mathrm{rank}(A) = 3$ 列满秩, 记 $A = (\alpha_1, \alpha_2, \alpha_3)$

$$
\begin{align*}
&\eta_1 = \alpha_1 = \begin{pmatrix} 0\\ 1\\ 1 \end{pmatrix} \\
&\eta_2 = \alpha_2 - \frac{(\alpha_2, \eta_1)}{(\eta_1, \eta_1)}\eta_1 = \begin{pmatrix} 1\\ \frac12\\ -\frac12 \end{pmatrix} \\
&\eta_3 = \alpha_3 - \frac{(\alpha_3, \eta_1)}{(\eta_1, \eta_1)}\eta_1 - \frac{(\alpha_3, \eta_2)}{(\eta_2, \eta_2)}\eta_2 = \begin{pmatrix} \frac13\\ -\frac13\\ \frac13 \end{pmatrix}
\end{align*}
$$

进一步标准化

$$
\beta_1 = \frac{\eta_1}{\Vert \eta_1 \Vert} = \frac{1}{\sqrt{2}}\eta_1 \quad
\beta_2 = \frac{\eta_2}{\Vert \eta_2 \Vert} = \frac{2}{\sqrt{6}}\eta_2 \quad
\beta_3 = \frac{\eta_3}{\Vert \eta_3 \Vert} = \sqrt{3}\eta_3
$$

从而

$$
\begin{align*}
A &= QR \\
&= (\beta_1, \beta_2, \beta_3)\begin{pmatrix}
\sqrt{(\eta_1, \eta_1)} & (\alpha_2, \beta_1) & (\alpha_3, \beta_1) \\
& \sqrt{(\eta_2, \eta_2)} & (\alpha_3, \beta_2) \\
& & \sqrt{(\eta_3, \eta_3)}
\end{pmatrix} \\
&= (\beta_1, \beta_2, \beta_3)\begin{pmatrix}
\sqrt{2} & \frac{1}{\sqrt{2}} & \frac{1}{\sqrt{2}} \\
& \frac{3}{\sqrt{6}} & \frac{1}{\sqrt{6}} \\
& & \frac{2}{\sqrt{3}}
\end{pmatrix}
\end{align*}
$$

(3) $A= \begin{pmatrix} 1&0 \\ 0&1 \\ 1&1 \end{pmatrix}$

不难发现 $\mathrm{rank}(A) = 2$ 列满秩，记 $A = \begin{pmatrix} \alpha_1 & \alpha_2 \end{pmatrix}$

$$
\begin{align*}
&\eta_1 = \alpha_1 = \begin{pmatrix} 1\\ 0\\ 1 \end{pmatrix} \\
&\eta_2 = \alpha_2 - \frac{(\alpha_2, \eta_1)}{(\eta_1, \eta_1)}\eta_1 = \begin{pmatrix} -\frac12\\ 1\\ \frac12 \end{pmatrix}
\end{align*}
$$

进一步标准化

$$
\beta_1 = \frac{\eta_1}{\Vert \eta_1 \Vert} = \frac{1}{\sqrt{2}}\eta_1 \quad
\beta_2 = \frac{\eta_2}{\Vert \eta_2 \Vert} = \frac{2}{\sqrt{6}}\eta_2
$$

从而

$$
\begin{align*}
A &= QR \\
&= (\beta_1, \beta_2)\begin{pmatrix}
\sqrt{(\eta_1, \eta_1)} & (\alpha_2, \beta_1) \\
& \sqrt{(\eta_2, \eta_2)}
\end{pmatrix} \\
&= (\beta_1, \beta_2)\begin{pmatrix}
\sqrt{2} & \frac{1}{\sqrt{2}} \\
& \frac{\sqrt{6}}{2}
\end{pmatrix}
\end{align*}
$$


### 30.

计算 28 题中各矩阵的奇异值分解和相应的四个子空间

(1) $A= \begin{pmatrix} 0&1&1 \\ 1&1&0 \\ 1&0&0 \end{pmatrix}$

本题特征值手算较为复杂，可以采用 [julia](http://onlookerliu.leanote.com/post/bc7bf6a21b9d) 做分解计算

```julia
A = [0 1 1; 1 1 0; 1 0 0];
U, D, V = svd(A);
U # 依次输入U, D, V 即可SVD分解
```

```julia
3×3 Array{Float64,2}:
 -0.591009  -0.736976   0.327985
 -0.736976   0.327985  -0.591009
 -0.327985   0.591009   0.736976
```

可以得到

$$
\begin{align*}
A &= \begin{pmatrix}
0 & 1 & 1 \\
1 & 1 & 0 \\
1 & 0 & 0
\end{pmatrix} = UDV'\\
&= \begin{pmatrix}
-0.591009 & -0.736976 &  0.327985 \\
-0.736976 &  0.327985 & -0.591009 \\
-0.327985 &  0.591009 &  0.736976
\end{pmatrix} \begin{pmatrix}
1.80194 & & \\
& 1.24698 & \\
& & 0.445042 \\
\end{pmatrix} \begin{pmatrix}
-0.591009  & -0.736976 &  0.327985 \\
-0.736976  &  0.327985 & -0.591009 \\
-0.327985  &  0.591009 &  0.736976
\end{pmatrix}'
\end{align*}
$$

从而四个相关子空间

$$
\begin{align*}
&R(A) = \mathrm{span}\{ u_1, u_2, u_3 \} \quad &R(A^*) = \mathrm{span}\{ v_1, v_2, v_3 \} \\
&N(A) = \emptyset \quad &N(A^*) = \emptyset
\end{align*}
$$

(3) $A= \begin{pmatrix} 1&0 \\ 0&1 \\ 1&1 \end{pmatrix}$

$$
A^*A = \begin{pmatrix}
1 & 0 & 1 \\
0 & 1 & 1
\end{pmatrix} \begin{pmatrix}
1 & 0 \\
0 & 1 \\
1 & 1
\end{pmatrix} = \begin{pmatrix}
2 & 1 \\
1 & 2
\end{pmatrix}
$$

令 $|\lambda I - A^*A | = (\lambda - 2)^2 - 1 = 0$ 可得特征值 $\lambda_1 = 1, \lambda_2 = 3$, 故 $D = \begin{pmatrix} 1&0 \\ 0&\sqrt{3} \\ 0&0 \end{pmatrix}$

对 $(\lambda_i I - A^*A )\beta = 0$ 可以求得单位特征向量

$$
\beta_1 = \begin{pmatrix}
\frac{1}{\sqrt{2}} \\
-\frac{1}{\sqrt{2}}
\end{pmatrix} \quad \beta_2 = \begin{pmatrix}
\frac{1}{\sqrt{2}} \\
\frac{1}{\sqrt{2}}
\end{pmatrix}
$$

则 $A^*A$ 的三个特征值为 $\lambda_1 = 1, \lambda_2 = 3, \lambda_3 = 0$ 对应的特征向量

$$
\alpha_1 = \begin{pmatrix}
\frac{1}{\sqrt{2}} \\
-\frac{1}{\sqrt{2}} \\
0
\end{pmatrix} \quad \alpha_2 = \begin{pmatrix}
\frac{1}{\sqrt{6}} \\
\frac{1}{\sqrt{6}} \\
\frac{2}{\sqrt{6}}
\end{pmatrix} \quad \alpha_3 = \begin{pmatrix}
-\frac{\sqrt{3}}{3} \\
-\frac{\sqrt{3}}{3} \\
\frac{\sqrt{3}}{3}
\end{pmatrix}
$$

令 $U = \begin{pmatrix} \alpha_1 & \alpha_2 & \alpha_3 \end{pmatrix}, V = \begin{pmatrix} \beta_1 & \beta_2 \end{pmatrix}$, 则 $A = UDV^*$ 为 $A$ 的 SVD 分解

$$
\begin{align*}
&R(A) = \mathrm{span}\{ \alpha_1, \alpha_2 \}, \quad &R(A^*) = \mathrm{span}\{ \beta_1, \beta_2 \} \\
&N(A) = \emptyset, \quad &N(A^*) = \mathrm{span}\{ \alpha_3 \}
\end{align*}
$$

### 31.

设 $A\in\mathbb{C}^{m\times n}$, 证明

$$
\sigma_{\min}(A) = \min\{ (x^*A^*Ax)^{1/2}: x^*x = 1 \} \qquad \sigma_{\max}(A) = \max\{ (x^*A^*Ax)^{1/2}: x^*x = 1 \}
$$

$(A^*A)^* = A^*A$，$A$ 是 Hermite 阵，故 $A^*A$ 是正规阵

存在酉阵 $U$，使得 $U^*A^*AU = \mathrm{diag}\{ \lambda_1, \cdots, \lambda_n \}$, 其中 $\lambda_i$ 是 $A^*A$ 的特征值 $\lambda_i\geq 0$

不妨设 $\lambda_1 \geq \lambda_2 \geq \cdots \geq \lambda_n \geq 0$ 取 $X = u_i$, 则

$$
(AX,AX) = X^*A^*AX = \lambda_i X^*X = \lambda_i \implies (X^*A^*AX)^{1/2} = \sqrt{\lambda_i}
$$ 

为 $A$ 的奇异值，故 $\sigma_{\min}(A) = \sqrt{\lambda_n}, \sigma_{\max}(A) = \sqrt{\lambda_1}$

### 33.

设 $A\in\mathbb{C}^{m\times n}$ 的秩为 $r>0$, $A$ 的奇异值分解为 $A = U\mathrm{diag}(s_1, \cdots, s_r, 0, \cdots, 0)V^*$，求矩阵 $B = \begin{pmatrix} A\\ A\end{pmatrix}$ 的奇异值分解.

由题意 $B^*B = (A^* A^*)\begin{pmatrix} A\\ A\end{pmatrix} = 2A^*A$, $A^*A$, $B^*B$ 为正规阵。于是存在 $Q$ 酉阵，使得
$$
Q^*A^*AQ = \begin{pmatrix}
s_1^2 & & & & & \\
& \ddots & & & & \\
& & s_r^2 & & & \\
& & & 0 & & \\
& & & & \ddots & \\
& & & & & 0 \\
\end{pmatrix} \quad Q^*B^*BQ = \begin{pmatrix}
2s_1^2 & & & & & \\
& \ddots & & & & \\
& & 2s_r^2 & & & \\
& & & 0 & & \\
& & & & \ddots & \\
& & & & & 0 \\
\end{pmatrix}
$$
设 $\Sigma = \mathrm{diag}\{ s_1, \cdots, s_r, 0, \cdots, 0 \}$, 则 $B$ 的非零奇异值为 $\sqrt{2}s_1, \cdots, \sqrt{2}s_r$

因 $B^*B$ 特征向量与 $A^*A$ 一致，故
$$
B = \begin{pmatrix}
\frac{u}{\sqrt{2}} & \frac{u}{\sqrt{2}} \\
\frac{u}{\sqrt{2}} & -\frac{u}{\sqrt{2}}
\end{pmatrix} \begin{pmatrix}
\sqrt{2} D \\
0
\end{pmatrix}\cdot V^* \qquad A = U\Sigma V^*
$$
