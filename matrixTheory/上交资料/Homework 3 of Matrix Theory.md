
## 习题一

### 32.

> 设欧式空间 $\mathbb{R}[x]_2$ 中的內积为
>
> $$
(f,g) = \int_{-1}^{1} f(x)g(x)dx
$$
> (1) 求基 $1,t,t^2$ 的度量矩阵
> (2) 用矩阵乘法形式计算 $f(x) = 1-x+x^2$ 与 $g(x)=1-4x-5x^2$ 的內积.

(1)

由 $(f, g) = \int_{-1}^{1} f(x)g(x) dx$ 定义计算得

$$
G = \begin{pmatrix}
2 & 0 & \frac23 \\
0 & \frac23 & 0 \\
\frac23 & 0 & \frac25 \\
\end{pmatrix}
$$

(2)

$$
(f(x), g(x)) = ((1, t, t^2)\begin{pmatrix} 1 \\ -1 \\ 1 \\ \end{pmatrix}, (1, t, t^2)\begin{pmatrix} 1 \\ -4 \\ -5 \\ \end{pmatrix}) = (1, -4, -5)G\begin{pmatrix} 1\\ -1\\ 1\\ \end{pmatrix}
$$

### 34.

> (1) 复数域 $\mathbb{C}$ 是实数域 $\mathbb{R}$ 上的二维线性空间. 是否存在 $\mathbb{C}$ 上的一个內积，使得 $i$ 与 $1+i$ 成为 $\mathbb{C}$ 的一组标准正交基，为什么？
>
> (2) 试构造实线性空间 $\mathbb{R}^3$ 上的一个內积，使得向量组 $e_1, e_1+e_2, e_1+e_2+e_3$ 是一组标准正交基. 问此时 $e_2$ 与 $e_3$ 的长度是多少？它们的夹角又是多少？

(1) 存在。因为 $\mathrm{i}$ 和 $\mathrm{i} + 1$ 线性无关，可以作为二维线性空间的一组基。然后用 Gram_Schmidt 正交化方法将其变为一组标准正交基。

(2) 若 $e_1, e_1+e_2, e_1+e_2+e_3$ 是一组标准正交基，利用內积性质可计算得度量矩阵

$$
A = \begin{pmatrix}
1 & -1 & 0 \\
-1 & 2 & -1 \\
0 & -1 & 2 \\
\end{pmatrix}
$$

i.e. 若 $\alpha, \beta$ 在 $e_1, e_2, e_3$ 这组基下坐标为 $(x_1, x_2, x_3)'$ 和 $(y_1, y_2, y_3)'$，则有

$$
(\alpha, \beta) = (y_1, y_2, y_3)A(x_1, x_2, x_3)' = x_1y_1 + 2x_2y_2 + 2x_3y_3 - (x_1y_2 + x_2y_1 + x_2y_3 + x_3y_2)
$$

且 $\Vert e_2 \Vert = \sqrt2, \Vert e_3 \Vert = \sqrt2$，得 $\cos (e_2, e_3) = \frac{(e_2, e_3)}{\Vert e_2 \Vert \cdot \Vert e_3 \Vert} = -\frac12$ 即 $\langle e_2, e_3 \rangle = \frac23 \pi$

### 37.

> 在欧式空间 $\mathbb{R}^4$ 中，求三个向量 $\alpha_1 =(1, 0, 1, 1)', \alpha_2 =(2, 1, 0, -3)'$ 和 $\alpha_3 =(1, -1, 1, -1)'$ 所生成的子空间的一个标准正交基.

直接用 Gram-Schmidt 方法求解

$$
\begin{split}
&\beta_1 = \alpha_1 = (1, 0, 1, 1)' &\qquad r_1 = \beta_1/\Vert \beta_1 \Vert = \frac{1}{\sqrt3}(1, 0, 1, 1)' \\
&\beta_2 = \alpha_2 - (\alpha_2, r_1)r_1 = \frac13(7, 3, 1, -8)' &\qquad r_2 = \beta_2/\Vert \beta_2 \Vert = \frac{1}{\sqrt{123}}(7, 3, 1, -8)' \\
&\beta_3 = \alpha_3 - (\alpha_3, r_2)r_2 - (\alpha_3, r_1)r_1 = \frac14(-3, -54, 23, -20)' &\qquad r_3 = \beta_3/\Vert \beta_3 \Vert = \frac{1}{\sqrt{3854}}(-3, -54, 23, -20)' \\
\end{split}
$$

### 39.

> 设二维欧式空间 $V$ 的一组基为 $\alpha_1, \alpha_2$，其度量矩阵为
> $$
A = \begin{pmatrix}
5 & 4 \\
4 & 5 \\
\end{pmatrix}
$$
> 试求 $V$ 的一个标准正交基到 $\alpha_1, \alpha_2$ 的过渡矩阵.

由度量矩阵可知 $(\alpha_1, \alpha_1) = (\alpha_2, \alpha_2) = 5$ 故 $\alpha_1, \alpha_2$ 长度相等，则 $\beta_1 = \alpha_1 + \alpha_2, \beta_2 = \alpha_1 - \alpha_2$ 必正交。令

$$
r_1 = \frac{\beta_1}{\Vert \beta_1 \Vert} = \frac{1}{\sqrt{18}}(\alpha_1 + \alpha_2) \quad r_2 = \frac{\beta_2}{\Vert \beta_2 \Vert} = \frac{1}{\sqrt{2}}(\alpha_1 - \alpha_2)
$$

则 $r_1, r_2$ 是一个标准正交基，且有

$$
(r_1, r_2) = (\alpha_1, \alpha_2)\begin{pmatrix}
\frac{1}{\sqrt{18}} & \frac{1}{\sqrt{2}} \\
\frac{1}{\sqrt{18}} & -\frac{1}{\sqrt{2}} \\
\end{pmatrix} := (\alpha_1, \alpha_2)\cdot P
$$

则 $r_1, r_2$ 到 $\alpha_1, \alpha_2$ 的过渡矩阵为

$$
P^{-1} = \begin{pmatrix}
\frac{3}{\sqrt2} & \frac{3}{\sqrt2} \\
\frac{1}{\sqrt2} & -\frac{1}{\sqrt2} \\
\end{pmatrix}
$$

### 42.

> 设线性空间 $V = \mathbb{R}^2$ 是欧式空间 (未必是通常的欧式空间). 设 $\alpha_1 = (1, 1)', \alpha_2 = (1, -1)'$ 与 $\beta_1 = (0, 2)', \beta_2 = (6, 12)'$ 是 $V$ 的两组基. 设 $\alpha_j$ 与 $\beta_k$ 的內积分别为
> $$
(\alpha_1, \beta_1) = 1, (\alpha_1, \beta_2) = 15, (\alpha_2, \beta_1) = -1, (\alpha_2, \beta_2) = 3
$$
> (1) 求两组基的度量矩阵
> (2) 求 $V$ 的一个标准正交基.

(1)

易知 $\beta_1 = \alpha_1 - \alpha_2, \beta_2 = 9\alpha_1 - 3\alpha_2$

$$
\begin{split}
(\alpha_1, \beta_1) &= (\alpha_1, \alpha_1-\alpha_2) = (\alpha_1, \alpha_1) - (\alpha_1, \alpha_2) = 1 \\
(\alpha_1, \beta_2) &= (\alpha_1, 9\alpha_1-3\alpha_2) = 9(\alpha_1, \alpha_1) - 3(\alpha_1 - \alpha_2) = 15 \\
(\alpha_2, \beta_1) &= (\alpha_2, \alpha_1-\alpha_2) = (\alpha_2, \alpha_1) - (\alpha_2, \alpha_2) = -1 \\
(\beta_1, \beta_1) &= (\alpha_1-\alpha_2, \alpha_1-\alpha_2) = 2 \\
(\beta_1, \beta_2) &= (\alpha_1-\alpha_2, 9\alpha_1-3\alpha_2) = 12 \\
(\beta_2, \beta_2) &= (9\alpha_1 - 3\alpha_2, 9\alpha_1 - 3\alpha_2) = 126 \\
\end{split}
$$

可以推出

$$
\begin{split}
&(\alpha_1, \alpha_1) = 2 \quad (\alpha_1, \alpha_2) = 1 \\
&(\alpha_2, \alpha_2) = (\alpha_2, \alpha_1) + 1 = 2 \\
\end{split}
$$

从而度量矩阵

$$
A = \begin{pmatrix}
2 & 1 \\
1 & 2 \\
\end{pmatrix} \quad B = \begin{pmatrix}
2 & 12 \\
12 & 126 \\
\end{pmatrix}
$$

(2)

$$
\begin{split}
&r_1 = \frac{\alpha_1}{\Vert \alpha_1 \Vert} = \frac{1}{\sqrt2}\alpha_1 &\quad r_2 = \frac{1}{\Vert \beta_2 \Vert}\cdot\beta_2 = \frac{2}{\sqrt6}\alpha_2 - \frac{1}{\sqrt6}\alpha_1 \\
&\beta_2 = \alpha_2 - (\alpha_2, r_1)r_1 = \alpha_2 - \frac12 \alpha_1 &\quad \Vert \beta_2 \Vert = \sqrt{(\alpha_2-\frac12\alpha_1, \alpha_2-\frac12\alpha_1)} = \sqrt{\frac32} \\
\end{split}
$$

### 44.

> 设 $A$ 是**反对称**实矩阵（即 $A' = -A$），证明：
> (1) $A$ 的特征值为 $0$ 或纯虚数
> (2) 设 $\alpha + \beta\mathrm{i}$ 是 $A$ 的属于一个非零特征值的特征向量，其中 $\alpha, \beta$ 均为实向量，则 $\alpha$ 与 $\beta$ 正交。

(1)

不妨假设 $\lambda$ 为 $A$ 的特征值，$x$ 为对应的特征向量。即 $Ax=\lambda x$，两边同时乘 $x^*$，有

$$
x^* A x = \lambda x^*x
$$

对上式取共轭转置得

$$
x^* A^* x = \lambda^* x^*x
$$

因 $A^* = -A$，则有 $\lambda + \lambda^* = 0$。故 $\lambda$ 为 $0$ 或纯虚数

(2)

假设非零特征值为 $\lambda\mathrm{i}$，根据定义有 $A(\alpha + \beta\mathrm{i}) = \lambda\mathrm{i}(\alpha + \beta\mathrm{i})$，即

$$
\begin{split}
A\alpha &= -\lambda\beta \\
A\beta &= \lambda\alpha \\
\end{split}
$$

从而 $-\alpha'A = -\lambda\beta'$, 进一步地 $ \alpha'A\alpha = \lambda\beta'\alpha $，两边同时取转置得 $ -\alpha'A\alpha = \lambda\beta'\alpha $

故 $\beta'\alpha = 0$，即 $\alpha$ 与 $\beta$ 正交。

### 45.

> 设 $A$ 是 Hermite 矩阵。如果对任意向量 $x$ 均有 $x^*Ax = 0$，则 $A = 0$.

由题设，当 $x$ 取 $A$ 的特征向量时，可以发现 $A$ 的特征值均为 $0$。又因 $A$ 为 Hermite 矩阵，则 $A$ 可以对角化，且对角线元素全为0。故 $A=0$

事实上，$n$ 阶 Hermite 矩阵 $A$ 正定（半正定）的充要条件是 $A$ 的特征值大于（大于等于）$0$.

## 习题二

### 33.

> 在欧式空间 $\mathbb{R}^n$ 中求一个超平面 $W$，使得向量 $e_1 + e_2$ 在 $W$ 中的最佳近似向量为 $e_2$.

利用最佳近似的几何意义，$e_1 + e_2$ 在 $W$ 中的最佳近似就是 $e_1 + e_2$ 在超平面 $W$ 上的投影 i.e.

$$
\mathrm{Proj}_{W}(e_1 + e_2) = e_2 \implies e_1\in W^{\perp}
$$

则当 $n=2$ 时，$W = \mathrm{span}\{ e_2 \}$；当 $n>2$ 时， $W=\mathrm{span}\{ e_2, e_3, \cdots, e_n \}$

### 37.

> 设 $\alpha_0$ 是欧式空间中 $V$ 的单位向量，$\sigma(\alpha) = \alpha - 2(\alpha, \alpha_0)\alpha_0, \alpha\in V$. 证明
> (1) $\sigma$ 是线性变换；
> (2) $\sigma$ 是正交变换.

(1)

$$
\begin{split}
\sigma(m\alpha + n\beta) &= m\alpha + n\beta - 2(m\alpha+n\beta, \alpha_0)\alpha_0 \\
&= m\alpha + n\beta - 2m(\alpha, \alpha_0)\cdot\alpha_0 - 2n(\beta, \alpha_0)\alpha_0 \\
&= m(\alpha - 2(\alpha - \alpha_0)\alpha_0) + n(\beta - 2(\beta, \alpha_0)\alpha_0) \\
\end{split}
$$

可见 $\sigma$ 满足可加性和齐次性，故 $\sigma$ 为线性变换

(2)

只需证明 $\sigma$ 为等距变换

$$
\begin{split}
(\sigma(\alpha), \sigma(\alpha)) &= (\alpha - 2(\alpha, \alpha_0)\alpha_0, \alpha-2(\alpha-\alpha_0)\alpha_0) \\
&= (\alpha, \alpha) - 4((\alpha, \alpha_0)\alpha_0, \alpha) + 4(\alpha, \alpha_0)^2(\alpha_0, \alpha_0) \\
&= (\alpha, \alpha) - 4(\alpha, \alpha_0)(\alpha, \alpha_0) + 4(\alpha_0, \alpha)^2 \\
&= (\alpha, \alpha) \\
\end{split}
$$

故 $\Vert \sigma(\alpha) \Vert = \Vert \alpha \Vert$

### 38.

> 证明：欧式空间 $V$ 的线性变换 $\sigma$ 是反对称变换 $\iff \sigma$ 在 $V$ 的标准正交基下的矩阵是反对称矩阵.

设 $\sigma$ 在 $V$ 的标准正交基 $\alpha_1, \alpha_2, \cdots, \alpha_n$ 下的矩阵为 $A = (\alpha_{ij})$, 则 $\sigma(\alpha_i) = \sum_{k=1}^n a_{ki}\alpha_k \quad (1\leq i\leq n)$

$$
\begin{split}
&(\sigma(\alpha_i), \alpha_j) = \sum_{k=1}^n a_{ki}(\alpha_k, \alpha_j) = a_{ji} \\
&(\alpha_i, \sigma(\alpha_j)) = \sum_{k=1}^n a_{kj}(\alpha_i, \alpha_k) = a_{ij} \\
\end{split}
$$

故 $\sigma$ 是反对称矩阵 $\iff a_{ji}=-a_{ij} \iff A$ 反对称

<!-- ### 44.

> 证明 Givens 旋转矩阵 $G$ 是正交矩阵，对任意向量 $x=(x_1, x_2, \cdots, x_n)'$，计算 $Gx$ 的各个分量. 设 $x$ 是单位向量，讨论如何重复使用若干 Givens 旋转矩阵将 $x$ 变为标准向量 $e_1$.

-->

## 习题三

### 10.

> 设 $A$ 的特征值为 $0,1$，对应的特征向量为 $(1,2)', (2,-1)'$. 判断 $A$ 是否为对称矩阵并求 $A$.

两个特征向量正交，故 $A$ 可以正交对角化，从而 $A$ 对称

事实上，不妨假设
$$
A = \begin{pmatrix}
a & b \\
c & d \\
\end{pmatrix} \quad P = \begin{pmatrix}
1 & 2 \\
2 & -1 \\
\end{pmatrix}
$$

则 $P^{-1}AP = \mathrm{diag}\{ 0, 1 \} \iff AP = PD$

$$
\begin{pmatrix}
a & b \\
c & d \\
\end{pmatrix} \begin{pmatrix}
1 & 2 \\
2 & -1 \\
\end{pmatrix} = \begin{pmatrix}
0 & 2 \\
0 & -1 \\
\end{pmatrix} \implies a=\frac45 \quad b=c=-\frac25 \quad d=\frac15
$$

从而

$$
A = \begin{pmatrix}
4/5 & -2/5 \\
-2/5 & 1/5 \\
\end{pmatrix}
$$

## Bonus Questions

> 求 $\alpha = (7, -4, -1, 2)'$ 在 $\omega$ 上的正交投影，其中 $\omega$ 为 $Ax = 0$ 的解空间
> $$
A = \begin{pmatrix}
2 & 1 & 1 & 3 \\
3 & 2 & 2 & 1 \\
1 & 2 & 2 & -9 \\
\end{pmatrix}
$$

首先为求 $\omega$，将 $A$ 化为 Hermite 标准形

$$
A \rightarrow H_A = \begin{pmatrix}
1 & 0 & 0 & 5 \\
0 & 1 & 1 & -7 \\
0 & 0 & 0 & 0 
\end{pmatrix}
$$

可得 $\omega = N_A = \mathrm{span}\{ (0, -1, 1, 0)', (-5, 7, 0, 1)' \}$

下面进行 Schmidt 正交化

$$
\begin{split}
&\beta_1 = \alpha_1 = (0, -1, 1, 0)' &\quad \gamma_1 = \frac{\beta_1}{\Vert \beta_1 \Vert} = \frac{1}{\sqrt2}(0, -1, 1, 0)' \\
&\beta_2 = \alpha_2 - (\alpha_2, \gamma_1)\gamma_1 = (-5, \frac72, \frac72, 1)' &\quad \gamma_2 = \frac{\beta_2}{\Vert \beta_2 \Vert} = \frac{1}{\sqrt{202}}(-10, 7, 7, 2)' \\
\end{split}
$$

故

$$
\begin{split}
\mathrm{Proj}_{\omega}\alpha &= (\alpha, \gamma_1)\gamma_1 + (\alpha, \gamma_2)\gamma_2 \\
&= \frac32(0, -1, 1, 0)' - \frac12(-10, 7, 7, 2)' \\
&= (5, -5, -2, -1)'
\end{split}
$$
