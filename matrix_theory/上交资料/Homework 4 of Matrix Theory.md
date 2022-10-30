
## 习题三

### 2.

设 $A$ 为第一章例 1.2.3 中的矩阵，

$$
A = \begin{pmatrix}
-3 & 2 & -2 & 3 \\
-2 & 1 & -1 & 2 \\
-2 & 2 & -2 & 2 \\
-1 & 1 & -1 & 1
\end{pmatrix}
$$

(1) 利用满秩分解和 Sylevester 降幂公式求 $A$ 的特征多项式与 $A^6$;

(2) 求与 $A$ 相似的分块对角矩阵，使得每块恰有唯一的特征值.

(1) 利用 Hermite 标准形可以化得

$$
A = \begin{pmatrix}
3 & 2 \\
2 & 1 \\
2 & 2 \\
1 & 1
\end{pmatrix} \begin{pmatrix}
-1 & 0 & 0 & 1 \\
0 & 1 & -1 & 0
\end{pmatrix} = LR
$$

则特征多项式

$$
\begin{align*}
|\lambda I - A| = |\lambda I -LR| = \lambda^2| \lambda I - RL| = \lambda^2(\lambda+1)(\lambda+2)
\end{align*}
$$

进一步，可以利用 LR 分解对矩阵的幂进行降维操作

$$
\begin{align*}
A^6 &= (LR)^6 = L(RL)^5R \\
&= \begin{pmatrix}
-3 & 2 \\
-2 & 1 \\
-2 & 2 \\
-1 & 1 \end{pmatrix} \begin{pmatrix}
-2 & 1 \\
0 & -1 \end{pmatrix} \begin{pmatrix}
1 & 0 & 0 & -1 \\
0 & 1 & -1 & 0 \end{pmatrix} \\
&= \begin{pmatrix}
96 & -95 & 95 & -96 \\
64 & -63 & 63 & -64 \\
32 & -32 & 32 & -32 \end{pmatrix}
\end{align*}
$$

(2) 由上可知 $A$ 的特征值为：$\lambda_1 = \lambda_2 = 0$, $\lambda_3 = -1$, $\lambda_4 = -2$, 故

$$
A \sim 0 \oplus 0 \oplus -1 \oplus -2
$$

### 3.

设 $\alpha = (\alpha_1, \cdots, \alpha_n)'$, $\beta = (b_1, \cdots, b_n)'$, $x$ 为任意常熟，$A=xI_n + \alpha\beta'$.

(1) 直接计算行列式 $|A|$;

$$
\begin{align*}
A = &\begin{pmatrix}
x+a_1b_1 & a_1b_2 & \cdots & a_1b_n \\
a_2b_1 & x+a_2b_2 & \cdots & a_2b_n \\
\vdots & \vdots & \ddots & \vdots \\
a_nb_1 & a_nb_2 & \cdots & a_nb_n+x
\end{pmatrix} \xrightarrow[加在第i行]{第一行乘(\frac{a_i}{a_1})} \\
& \begin{pmatrix}
x+a_1b_1 & a_1b_2 & a_1b_3 & \cdots & a_1b_n \\
-\frac{a_2}{a_1}x & x & 0 & \cdots & 0 \\
-\frac{a_3}{a_1}x & 0 & x & \cdots & 0 \\
\vdots & \vdots & \vdots & \ddots & \vdots \\
-\frac{a_n}{a_1}x & 0 & 0 & \cdots & x
\end{pmatrix} \xrightarrow[加在第1行]{第i行乘(\frac{a_1b_i}{x})} \\
& \begin{pmatrix}
x+\sum_{i=1}^n a_ib_i & 0 & \cdots & \cdots & 0 \\
-\frac{a_2}{a_1}x & x & 0 & \cdots & 0 \\
-\frac{a_3}{a_1}x & 0 & x & \cdots & 0 \\
\vdots & \vdots & \vdots & \ddots & \vdots \\
-\frac{a_n}{a_1}x & 0 & 0 & \cdots & x
\end{pmatrix}
\end{align*}
$$

于是

$$
|A| = (x+\sum_{i=1}^n a_ib_i) x^{n-1}
$$


(2) 利用 Sylvester 降幂公式计算行列式 $|A|$;

$$
\begin{align*}
|A| &= |xI_n + \alpha\beta'| = x^{n-1}|xI_n + \beta'\alpha| \\
&= x^{n-1}|x+\sum_{i=1}^n a_ib_i| \\
&= x^{n-1}(x+\sum_i^n a_ib_i)
\end{align*}
$$


(3) 利用特征值计算行列式 $|A|$.

只需考察 $\alpha\beta'$ 的特征值，不难发现其为秩1矩阵，且有特征值 $\beta'\alpha$ (对应特征向量 $\alpha$)，从而

$$
|A| = (x-0)^{n-1}(x-\sum_{i=1}^n (-a_ib_i)) = x^{n-1}(x+\sum_{i=1}^n a_ib_i)
$$

### 11.

求下列矩阵的最小多项式并指出其中可以对角化的矩阵:

(1) $\begin{pmatrix} 3&2 \\ 4&5 \end{pmatrix}$  $\qquad$ (3) $\begin{pmatrix} 4&6&0 \\ -3&-5&0 \\ 3&6&1 \end{pmatrix}$

(1)

$$
f_A(x) = \begin{vmatrix}
x-3 & 2 \\
4 & x-5
\end{vmatrix} = (x-3)(x-5)-8 = (x-1)(x-7)
$$

不难发现 $m_A(x) = (x-1)(x-7)$

$$
A \sim \begin{pmatrix}
1 & 0 \\
0 & 7 \end{pmatrix}
$$

(3)

$$
f_A(x) = \begin{vmatrix}
x-4 & 6 & 0 \\
-3 & x+5 & 0 \\
-3 & 6 & x-1
\end{vmatrix} = (x-1)[(x-4)(x+5)+18] = (x-1)^2(x+2)
$$

逐项检查因子可得 $(A-I)(A+2I) = 0$，于是

$$
m_A(x) = (x-1)(x+2)
$$


### 12.

试构造两个同阶矩阵，使得它们

(1) 具有相同的特征多项式与不同的最小多项式；

(2) 具有相同的最小多项式与不同的特征多项式；

(3) 证明矩阵的最小多项式存在且唯一.

解:

(1) 只需构造特征值相同阶数不同的 Jordan 块

$$
A = \begin{pmatrix}
1 & 0 \\
0 & 1
\end{pmatrix} \quad B = \begin{pmatrix}
1 & 1 \\
0 & 1
\end{pmatrix}
$$

容易得到 $m_A(x) = x-1$ 而 $m_B(x) = (x-1)^2$

(2) 只需相同特征值 Jordan 块阶数相同，但特征值重数不同

$$
A = \begin{pmatrix}
1 & 0 & 0 \\
0 & 1 & 0 \\
0 & 0 & 0
\end{pmatrix} \quad B = \begin{pmatrix}
1 & 0 & 0 \\
0 & 0 & 0 \\
0 & 0 & 0
\end{pmatrix}
$$

容易得到 $m_A(x) = m_B(x) = (x-1)x$ 但 $f_A(x) = (x-1)^2x \neq f_B(x) = (x-1)x^2$

(3)

首先，$f_A(x)$ 是 $A$ 的零化多项式，必有其首一的因式是 $A$ 的最小多项式.

齐次，若 $A$ 存在两个最小多项式，记为 $m_A(x), m_A'(x)$ 则有

$$
m_A(x) \mid m_A'(x) \text{ 且 } m_A'(x) \mid m_A(x)
$$

从而 $m_A(x) = m_A'(x)$, 矛盾导致了唯一性。


### 30.

(1) 证明不等于零的幂零矩阵一定不相似于对角阵；

若相似于对角阵，对角阵必幂零。

(2) 设 $A$ 具有唯一特征值但 $A$ 不是对角矩阵. 证明 $A$ 一定不相似于对角矩阵。

$A$ 有唯一特征值但不是对角矩阵, 那么 $A$ 的 Jordan 块阶数必须大于1


### 37.

求矩阵 $A = \begin{pmatrix} 9&1&1 \\ 1&i&1 \\ 1&1&3 \end{pmatrix}$ 的盖尔圆盘并隔离之.

$$
D_1 = \{ |x-9|\leq 2 \} \quad D_2 = \{ |x-i|\leq 2 \} \quad D_3 = \{ |x-3|\leq 2 \}
$$

不妨假设放缩变换为 $P = \mathrm{diag}\{d_1, d_2, d_3 \}, d_i\neq 0$ 则有

$$
PAP^{-1} = \begin{pmatrix}
20 & \frac{3d_1}{d_2} & \frac{d_1}{d_3} \\
\frac{2d_2}{d_1} & 10 & \frac{2d_2}{d_3} \\
\frac{8d_3}{d_1} & \frac{d_3}{d_2} & 0
\end{pmatrix}
$$

取 $d_1 = \frac32, d_2=d_3=1$, 得

$$
D_1 = \{ |x-20|\leq 6 \} \quad D_2 = \{ |x-10|\leq \frac{10}{3} \} \quad D_3 = \{ |x|\leq \frac{19}{3} \}
$$

新的圆盘不再重叠，并确定了特征值范围

$$
[14, 26], \quad [\frac{20}{3}, \frac{40}{3}], \quad [-\frac{19}{3}, \frac{19}{3}]
$$

### 38.

求矩阵 $A = \begin{pmatrix} 20&3&1 \\ 2&10&2 \\ 8&1&0 \end{pmatrix}$ 的盖尔圆盘并讨论 $A$ 的特征值的范围与性质.

$$
D_1 = \{ |x-20|\leq 4 \} \quad D_2 = \{ |x-10|\leq 4 \} \quad D_3 = \{ |x|\leq 9 \}
$$

其中 $D_2$ 与 $D_3$ 连通，可以缩小 $D_3$, 取 $P = \mathrm{diag}\{ 1,1,\frac23 \}$, 计算得

$$
PAP^{-1} = \begin{pmatrix}
20 & 3 & 3/2 \\
2 & 10 & 3 \\
11/3 & 2/3 & 0
\end{pmatrix}
$$

$$
D_1 = \{ |x-20|\leq \frac92 \} \quad D_2 = \{ |x-10|\leq 5 \} \quad D_3 = \{ |x|\leq \frac{13}{3} \}
$$

新的圆盘不再重叠，并确定了特征值范围

$$
[\frac{31}{2}, \frac{49}{2}], \quad [5, 15], \quad [-\frac{13}{3}, \frac{13}{3}]
$$


### 39.

设矩阵

$$
A = \begin{pmatrix}
7 & -16 & 8 \\
-16 & 7 & -8 \\
8 & -8 & -5
\end{pmatrix}
$$

(1) 求 $A$ 的盖尔圆盘并利用对角相似变换改进之;

$$
D_1 = \{ |x-7|\leq 24 \} \quad D_2 = \{ |x-7|\leq 24 \} \quad D_3 = \{ |x+5|\leq 16 \}
$$

不妨假设放缩变换为 $P = \mathrm{diag}\{d_1, d_2, d_3 \}, d_i\neq 0$ 则有

$$
PAP^{-1} = \begin{pmatrix}
7 & -16\frac{d_2}{d_1} & 8\frac{d_3}{d_1} \\
-16\frac{d_1}{d_2} & 7 & -8\frac{d_3}{d_2} \\
8\frac{d_1}{d_3} & -8\frac{d_2}{d_3} & -5
\end{pmatrix}
$$

得到新圆盘

$$
\begin{align*}
&D_1 = \{ |x-7|\leq \frac{16d_2+8d_3}{d_1} \} \\
&D_2 = \{ |x-7|\leq \frac{16d_1+8d_3}{d_2} \} \\
&D_3 = \{ |x+5|\leq \frac{d_1+d_2}{d_3} \}
\end{align*}
$$

(2) 通过特征多项式计算 $A$ 的特征值并与 (1) 比较.

$$
|\lambda I - A| = \begin{vmatrix}
\lambda-7 & 16 & -8 \\
-16 & \lambda-7 & -8 \\
8 & -8 & \lambda+5
\end{vmatrix} = (\lambda-27)(\lambda+9)^2
$$

于是 $A$ 的特征值为 $\lambda_1 = -9$(二重)，$\lambda_2 = 27$

### 40.

证明 Hilbert[^1] 矩阵

[^1]: David Hilbert(1862-1943)，德国著名数学家，对数学与物理的众多分支有杰出贡献.

$$
A = \begin{pmatrix}
2 & \frac12 & \frac{1}{2^2} & \cdots & \frac{1}{2^{n-1}} \\
\frac23 & 4 & \frac{2}{3^2} & \cdots & \frac{2}{3^{n-1}} \\
\frac34 & \frac{3}{4^2} & 6 & \cdots & \frac{3}{4^{n-1}} \\
\vdots & \vdots & \vdots & & \vdots \\
\frac{n}{n+1} & \frac{n}{(n+1)^2} & \frac{n}{(n+1)^3} & \cdots & 2n
\end{pmatrix}
$$

可以对角化，且 $A$ 的特征值都是实数.

根据盖尔圆盘定理，可知第 $i$ 个圆盘为

$$
D_i(A) = \{ x\in\mathbb{C} \mid |x-2i|\leq 1-\frac{1}{(i+1)^{n-1}} \}
$$

因圆盘半径小于1，故 $A$ 的 $n$ 个圆盘彼此分隔，故可对角化且特征值均为实数。

### 41.

分别利用盖尔圆盘定理和 Ostrowski 圆盘定理估计下面矩阵的谱半径：

$$
A = \begin{pmatrix}
1 & 0.1 & 0.2 & 0.3 \\
0.5 & 3 & 0.1 & 0.2 \\
1 & 0.3 & -1 & 0.5 \\
1.2 & -0.6 & -1 & -3.6
\end{pmatrix}
$$

1. (行)盖尔圆盘

$$
\rho(A) \leq \max_{1\leq i\leq 4} \sum_{j=1}^4 |a_{ij}| = \sum_{j=1}^4 |a_{4j}| = 5.6
$$

2. Ostrowski 圆盘

$$
|\lambda - a_{ii}| \leq R_i(A)^{\alpha} C_i(A)^{1-\alpha}
$$

对每一行考虑可以得到

$$
\begin{array}{ccc}
|\lambda-1| &\leq &0.6^{\alpha}\cdot 2.7^{1-\alpha} \\
|\lambda-3| &\leq &0.8^{\alpha}\cdot 1^{1-\alpha} \\
|\lambda+1| &\leq &1.8^{\alpha}\cdot 0.5^{1-\alpha} \\
|\lambda+3.6| &\leq &2^{\alpha}\cdot 1^{1-\alpha}
\end{array}
$$

调整参数 $\alpha$ 例 $\alpha = \frac23$ 可得 $\rho(A) \leq 3.86$