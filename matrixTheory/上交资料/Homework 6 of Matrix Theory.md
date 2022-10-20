
## 习题五

### 1.

设 $\Vert \cdot \Vert$ 是酉空间 $\mathbb{C}^n$ 的向量范数，证明向量范数的下列基本性质：

(1) 零向量的范数为零

由向量范数正定性 $\Vert x \Vert = 0 \iff x = 0$

(2) 当 $x$ 是非零向量时: $\big\lVert \dfrac{x}{\Vert x \Vert} \big\rVert = 1$

由齐次性
$$
\big\lVert \frac{x}{\Vert x \Vert} \big\rVert = \big\vert \frac{1}{\Vert x \Vert} \big\vert \cdot \Vert x \Vert = 1
$$

(3) $\Vert -x \Vert = \Vert x \Vert$

同上，齐次性；

(4) $\big| \Vert x \Vert - \Vert y \Vert \big| \leq \Vert x - y\Vert$

$$
\begin{align*}
&\Vert x \Vert = \Vert x+y-y \Vert y \leq \Vert x-y \Vert + \Vert y \Vert &\implies \Vert x \Vert- \Vert y \Vert\leq\Vert x-y\Vert \\
&\Vert y \Vert = \Vert y+x-x \Vert x \leq \Vert y-x \Vert + \Vert y \Vert &\implies \Vert y \Vert- \Vert x \Vert\leq\Vert x-y\Vert
\end{align*}
$$

综上 $\big\vert \Vert x\Vert - \Vert y\Vert \big\vert \leq \Vert x-y \Vert$

### 2.

证明: 若 $x\in\mathbb{C}^n$, 则

(1) $\Vert x\Vert_2 \leq \Vert x\Vert_1 \leq \sqrt{n}\Vert x\Vert_2$

$$
\begin{align*}
&\Vert x\Vert_2 = \left( \sum_{i=1}^n x_i^2 \right)^{1/2} \leq \sum_{i=1}^n (x_i^2)^{1/2} = \sum_{i=1}^n\vert x_i\vert = \Vert x\Vert_1 \\
&(1+1+\cdots+1)(x_1^2+x_2^2+\cdots+x_n^2) = n\Vert x \Vert \geq (x_1+x_2+\cdots+x_n)^2 = \Vert x\Vert_1^2
\end{align*}
$$

(2) $\Vert x\Vert_{\infty} \leq \Vert x\Vert_1 \leq n\Vert x\Vert_{\infty}$

$$
\max_{1\leq i\leq n}|x_i| \leq \sum_{i=1}^n|x_i| \leq \sum_{i=1}^n\max|x_i| = n\max_{1\leq i\leq n}|x_i|
$$

(3) $\Vert x\Vert_{\infty} \leq \Vert x\Vert_2 \leq \sqrt{n}\Vert x\Vert_{\infty}$

$$
\max_{1\leq i\leq n}|x_i| \leq \left( \sum_{i=1}^n (\max_{1\leq i\leq n} x_i)^2 \right)^{1/2} = \sqrt{n}\max_{1\leq i\leq n}|x_i|
$$

### 12.

设矩阵 $A$ 的F-范数等于 $a$，$U$ 是酉矩阵，问 $AU$ 与 $UA$ 的F-范数各是多少？请总结你的计算

$$
\begin{align*}
&\Vert A\Vert_{F} = \left( \sum_{i=1}^n a_{ij}^2 \right)^2 = \left( \mathrm{tr}(AA^*) \right)^{1/2} \\
&\Vert UA\Vert_{F} = = [\mathrm{tr}(UA\cdot A^*U^*)]^{1/2} = \mathrm{tr}(AA^*)^{1/2} \\
&\Vert AU\Vert_{F} = = [\mathrm{tr}(AU\cdot U^*A^*)]^{1/2} = \mathrm{tr}(A^*A)^{1/2} \\
\end{align*}
$$

由上可知，酉矩阵保持范数不变

### 16.

证明矩阵的1-范数、2-范数和$\infty$-范数分别是向量的1-范数、2-范数和$\infty$-范数的诱导范数

分别依照范数定义证明

$$
\Vert A \Vert_{p} \leq \max_{x\neq 0} \frac{\Vert Ax\Vert_{p}}{\Vert x\Vert_{p}} \quad p = 1,2,\infty
$$

并且说明等号可以取到即可。

(1)
$$
\begin{align*}
\Vert Ax \Vert_1 &= \sum_{i=1}^n|\sum_{j=1}^n a_{ij} x_j| \leq \sum_{i=1}^n\sum_{j=1}^n |a_{ij}|\cdot|x_j| = \sum_{j=1}^n\sum_{i=1}^n|a_{ij}|\cdot|x_j| \\
&\leq \max_{1\leq j\leq n}\sum_{i=1}^n|a_{ij}|\sum_{j=1}^n|x_j| = \Vert A\Vert_1\cdot\Vert x\Vert_1
\end{align*}
$$

从而 $\Vert A\Vert_1 \geq \frac{\Vert Ax\Vert_1}{\Vert x\Vert_1}$

取 $x = e_k$, $\max\limits_{1\leq j\leq n}\sum_{i=1}^n|a_{ij}|=\sum_{i=1}^n|a_{ik}$, $\Vert Ae_k\Vert_1 = \sum_{i=1}^n|a_{ik}|$ 且有 $\Vert e_k\Vert_1 = 1$, 进而

$$
\frac{\Vert Ae_k\Vert_1}{\Vert e_k\Vert_1} = \max_{1\leq j\leq n}\sum_{i=1}^n|a_{ij}| = \Vert A \Vert_1 \implies \Vert A\Vert_1 = \sup_{0\neq x\in\mathbb{F}^n} \frac{\Vert Ax\Vert_1}{\Vert x\Vert_1}
$$

(2)
$$
\Vert Ax\Vert_2^2 = (Ax, Ax) = x^*A^*Ax \geq 0
$$

$A^*A$ 半正定，非负特征值记为 $\lambda_1\geq \lambda_2 \geq \cdots \geq \lambda_n \geq 0$, 对应的特征向量 $\alpha_1, \alpha_2, \cdots, \alpha_n$, 则 $\rho(A^*A)=\lambda_1$.

任取 $\forall x\in\mathbb{F}^n$，$x$ 可写成

$$
x = l_1 \alpha_1 + l_2 \alpha_2 + \cdots + l_n \alpha_n
$$

当取 $||x||_2 = (\sum_{i=1}^n l_i^2)^{1/2}$ 时，$\sum_{i=1}^n l_i^2 = 1$, 可知

$$
\Vert Ax\Vert_2^2 = (Ax, Ax) = (x, A^*Ax) = (\sum_{i=1}^n l_i\alpha_i, \sum_{i=1}^nl_i\lambda_i\alpha_i) = \sum_{i=1}^n \lambda_i l_i^2\alpha_i^*\alpha_i \leq \lambda_i\sum_{i=1}^n l_i^2 = \lambda_i
$$

故 $\dfrac{\Vert Ax\Vert_2}{\Vert x\Vert_2} \leq \sqrt{\lambda_1} = \rho(A^*A)^{1/2} = \Vert A\Vert_2$

取 $x=\alpha_1$ 时，$\Vert x\Vert_2 = 1$,

$$
\Vert Ax\Vert_2^2 = \Vert A\alpha_1\Vert_2^2 = (A\alpha_1, A\alpha_1) = (\alpha_1, A^*A\alpha) = (\alpha_1, \lambda_1\alpha_1) = \lambda_1
$$

进而 $\dfrac{\Vert A\alpha_1\Vert_2}{\Vert \alpha_1 \Vert}_2 = \sqrt{\lambda_1} = [\rho(A^*A)]^{1/2} = \Vert A \Vert_2$, 即 $\Vert A \Vert_2 = \sup\limits_{0\neq x\in\mathbb{F}^n} \frac{\Vert Ax\Vert_2}{\Vert x\Vert_2}$

(3)
$$
\begin{align*}
\Vert Ax\Vert_{\infty} &= \max_{1\leq i\leq n}\lvert \sum_{j=1}^n a_{ij}x_j \rvert \leq \max_{1\leq i\leq n}\sum_{j=1}^n |a_{ij}|\cdot|x_j| \\
&\leq \left( \max_{1\leq i\leq n} \sum_{j=1}^n|a_{ij}| \right)\max_{1\leq j\leq \infty}|x_j|=\Vert A\Vert_{\infty}\cdot\Vert x\Vert_{\infty}
\end{align*}
$$

故 $\Vert A\Vert_{\infty} \geq \dfrac{\Vert Ax\Vert_{\infty}}{\Vert x\Vert_{\infty}}$ 另一方面，若 $\max_{1\leq i\leq n}\sum_{j=1}^n|a_{ij}|=\sum_{j=1}^n|a_{kj}|$

取 $x = (\beta_1, \beta_2, \cdots, \beta_n)$, 其中 $\beta_i = \begin{cases} |a_{kj}|/a_{kj} & a_{kj}\neq 0 \\ 1 & a_{kj} = 0 \end{cases}$，此时 $\Vert x\Vert_{\infty} = 1$, 且有

$$
\Vert Ax \Vert_{\infty} = \sum_{j=1}^n |a_{kj}| = \max_{1\leq i\leq n}\sum_i^n |a_{ij}| \quad \frac{\Vert Ax \Vert_{\infty}}{\Vert x \Vert_{\infty}} = \max_{1\leq i\leq n}\sum_{j=1}^n|a_{ij}| = \Vert A \Vert_{\infty}
$$

### 21.

设 $T$ 为正交矩阵，又 $A\in\mathbb{R}^{n\times n}$. 证明:

(1) $\Vert T \Vert_2 = 1$

$$
T'T=I_n \quad \rho(T^*T)=\rho(I_n)=1 \quad \Vert T \Vert_2 = \sqrt{\rho(T^*T)} = 1
$$

(2) $\Vert A \Vert_2 = \Vert TA \Vert_2$

$$
\Vert TA \Vert_2 = \sqrt{\rho(A^*T^*TA)} = \sqrt{\rho(A^*A)} = \Vert A \Vert_2
$$

(3) 试解释上面的两个结果.

- 正交变换为等距变换
- 正交变换保持矩阵2-范数不变

### 22.

设 $A$, $B$ 为 $n$ 阶矩阵，，其中 $A$ 可逆而 $B$ 不可逆，设 $\Vert \cdot \Vert$ 是任何一种矩阵范数.
定义 $A$ 的条件数 $\mathrm{Cond}(A) = \Vert A\Vert \Vert A^{-1}\Vert$.
证明: $\Vert A-B \Vert \geq 1/\Vert A^{-1}\Vert$. 解释这个结果

因 $B$ 不可逆，故必有0奇异值，从而 $I - A^{-1}B$ 有特征值1

$$
1\leq \Vert I-A^{-1}B \Vert = \Vert A^{-1}(A-B) \Vert \leq \Vert A^{-1}\Vert \cdot\Vert A-B\Vert
$$

则有 $\Vert A-B\Vert \geq \dfrac{1}{\Vert A^{-1}\Vert}$

因 $\Vert A \Vert \neq 0$, $\Vert A^{-1} \Vert = \frac{\mathrm{Cond}(A)}{\Vert A\Vert}$, 于是

$$
\Vert A-B \Vert \leq \frac{\mathrm{Cond}(A)}{\Vert A\Vert} \quad \mathrm{Cond}(A)=\Vert A\Vert\cdot\Vert A^{-1}\Vert=1
$$

以上结果表明存在奇异矩阵 $B$ 与可逆矩阵 $A$ 在范数意义上最接近

### 23.

设 $A\in\mathbb{C}^{m\times n}$, $\sigma_1, \sigma_2, \cdots, \sigma_n$ 是 $A$ 的全部奇异值. 证明

(1) $\mathrm{Cond}(A) = \sigma_1(A)/\sigma_n(A)$, 其中 $\sigma_1(A)$ 与 $\sigma_n(A)$ 分别是 $A$ 的最大和最小奇异值

$\sigma_1, \sigma_2, \cdots, \sigma_n$ 是 $A$ 的全部奇异值, 则 $1/\sigma_1, 1/\sigma_2, \cdots, 1/\sigma_n$ 是 $A^{-1}$ 的全部奇异值, 容易得知

$$
\Vert A\Vert_2 = \sigma_1 \quad \Vert A^{-1} \Vert_2 = \frac{1}{\sigma_n}
$$

从而$\mathrm{Cond}(A) = \sigma_1(A)/\sigma_n(A)$

(2) $\Vert A \Vert_F = \Big( \sum_{i=1}^r \sigma_i^2 \Big)^{1/2} = [\mathrm{tr}(A^*A)]^{1/2}$

$$
\Vert A \Vert_F = \Big( \sum_{i=1}^n \sigma_i^2 \Big)^{1/2} = [\mathrm{tr}(A^*A)]^{1/2} = \Big( \sum_{i=1}^r \sigma_i^2 \Big)^{1/2}
$$

(3) $\Vert A \Vert_2 = \sigma_{\max}(A)$

$$
\Vert A \Vert_2 = \sqrt{\rho(A^*A)} = \sigma_1(A)
$$

### 26.

设 $A_k = \begin{pmatrix} \frac{1}{k^2} & \frac{k^2+k}{k^2+1} \\ 2 & (1-\frac{2}{k})^k \end{pmatrix}$，求 $\lim\limits_{k\to\infty}A_k$

逐项求极限即可 $\lim\limits_{k\to\infty}A_k = \begin{pmatrix} 0&1 \\ 2&e^{-2} \end{pmatrix}$

### 27.

设 $\lim_{k\to\infty} A_k = A$

(1) 如果 $A_k$ 均为正定矩阵，问 $A$ 有何特点

$$
\forall x\in\mathbb{C}^n (A_k x, x) > 0 \iff x'A_k x > 0
$$

若 $A\neq 0$, 则 $(Ax, x) > 0$; 反之 $A=0$, $(Ax, x)=0$. 于是 $(Ax, x) \geq 0$, $A$ 半正定

(2) 如果 $A_k$ 均为正规矩阵，问 $A$ 有何特点

$A$ 为正规矩阵，则 $\forall k, A_kA_k^* = A_k^*A_k$, 两边取极限可以得到 $AA^* = A^*A$

(3) 如果 $A_k$ 均为可逆矩阵，问 $A$ 有何特点

$A$ 不一定可逆，可取 $A_k = \begin{pmatrix} \frac{1}{k}&0 \\ 0&\frac{1}{k} \end{pmatrix}$ 说明问题

### 30.

设 $A = \begin{pmatrix} 2&-\frac{1}{2} \\ 2&0 \end{pmatrix}$, 求 $\sum\limits_{k=0}^{\infty} \dfrac{A^k}{2^k}$

根据求和公式

$$
\sum_{k=0}^{\infty} \frac{A^k}{2^k} = (I-\frac{A}{2})^{-1}
$$

容易解得 $\begin{pmatrix} 4&-1 \\ 4&0 \end{pmatrix}$

### 31.

设 $A = \begin{pmatrix} -0.6&1&0.8 \\ 0&0.2&0 \\ -0.6&1&0.8 \end{pmatrix}$. 试判断 $A$ 是否幂收敛.

$$
\begin{align*}
|\lambda I - A| &= \begin{vmatrix}
\lambda+0.6 & -1 & -0.8 \\
0 & \lambda-0.2 & 0 \\
0.6 & -1 & \lambda-0.8
\end{vmatrix} \\
&= (\lambda-0.2)\times\begin{vmatrix}
\lambda+0.6 & -0.8 \\
0.6 & \lambda-0.8
\end{vmatrix} \\
&= (\lambda-0.2)\lambda(\lambda-0.2)
\end{align*}
$$

不难发现特征值均小于1，从而幂收敛

### 32.

(1) 设 $A = \begin{pmatrix} 0&0 \\ 1&-2 \end{pmatrix}$，求 $e^A, \sin(A), \cos(A)$

此类矩阵函数问题均可按照课本三种方法来解答，根据实际情况采用简洁高效的算法即可。注意：要多利用最小多项式和 Jordan 标准型的信息

下面利用符号计算软件[Mathematica](https://www.wolfram.com/mathematica/) 来给出计算结果，后面相似问题可同样处理。

```mathematica
A = {{0, 0}, {1, -2}};
MatrixExp[A] // MatrixForm // FullSimplify
MatrixFunction[Sin, A] // MatrixForm // FullSimplify
MatrixFunction[Cos, A] // MatrixForm // FullSimplify
```

$$
\left(
\begin{array}{cc}
 1 & 0 \\
 \frac{1}{2}-\frac{1}{2 e^2} & \frac{1}{e^2} \\
\end{array}
\right)
\quad
\left(
\begin{array}{cc}
 0 & 0 \\
 \frac{\sin (2)}{2} & -\sin (2) \\
\end{array}
\right)
\quad
\left(
\begin{array}{cc}
 1 & 0 \\
 \sin ^2(1) & \cos (2) \\
\end{array}
\right)
$$

(2) 设 $J = \begin{pmatrix} -2&&&\\ &1&1& \\ &&1& \\ &&&2 \end{pmatrix}$，求 $e^J, \sin(J), \cos(J)$

```mathematica
J = {{-2, 0, 0, 0}, {0, 1, 1, 0}, {0, 0, 1, 0}, {0, 0, 0, 2}};
MatrixExp[J] // MatrixForm // FullSimplify
MatrixFunction[Sin, J] // MatrixForm // FullSimplify
MatrixFunction[Cos, J] // MatrixForm // FullSimplify
```

$$
\left(
\begin{array}{cccc}
 \frac{1}{e^2} & 0 & 0 & 0 \\
 0 & e & e & 0 \\
 0 & 0 & e & 0 \\
 0 & 0 & 0 & e^2 \\
\end{array}
\right)
\quad
\left(
\begin{array}{cccc}
 -\sin (2) & 0 & 0 & 0 \\
 0 & \sin (1) & \cos (1) & 0 \\
 0 & 0 & \sin (1) & 0 \\
 0 & 0 & 0 & \sin (2) \\
\end{array}
\right)
\quad
\left(
\begin{array}{cccc}
 \cos (2) & 0 & 0 & 0 \\
 0 & \cos (1) & -\sin (1) & 0 \\
 0 & 0 & \cos (1) & 0 \\
 0 & 0 & 0 & \cos (2) \\
\end{array}
\right)
$$

### 35.

对下列方阵 $A$，求矩阵函数 $e^{At}$

(1) $A = \begin{pmatrix} 2&-2&3 \\ 1&1&1 \\ 1&3&-1 \end{pmatrix}$

```mathematica
A = {{2, -2, 3}, {1, 1, 1}, {1, 3, -1}};
JordanDecomposition[A] // MatrixForm
MatrixFunction[Exp, A t] // MatrixForm // ExpandAll
```

$$
\left(
\begin{array}{ccc}
 \{-11,-1,1\} & \{-1,1,1\} & \{14,1,1\} \\
 \{-2,0,0\} & \{0,1,0\} & \{0,0,3\} \\
\end{array}
\right) \\
\left(
\begin{array}{ccc}
 \frac{e^t}{2}+\frac{e^{3 t}}{2} & \frac{11 e^{-2 t}}{15}-\frac{5 e^t}{6}+\frac{e^{3 t}}{10} & -\frac{11 e^{-2 t}}{15} +\frac{e^t}{3}+\frac{2 e^{3 t}}{5} \\
 -\frac{e^t}{2}+\frac{e^{3 t}}{2} & \frac{e^{-2 t}}{15}+\frac{5 e^t}{6}+\frac{e^{3 t}}{10} & -\frac{e^{-2 t}}{15} -\frac{e^t}{3}+\frac{2 e^{3 t}}{5} \\
 -\frac{e^t}{2}+\frac{e^{3 t}}{2} & -\frac{14 e^{-2 t}}{15} +\frac{5 e^t}{6}+\frac{e^{3 t}}{10} & \frac{14 e^{-2 t}}{15}-\frac{e^t}{3}+\frac{2 e^{3 t}}{5} \\
\end{array}
\right)
$$

(3) $A = \begin{pmatrix} -2&1&3 \\ 0&-3&0 \\ 0&2&-2 \end{pmatrix}$

```mathematica
A = {{-2, 1, 3}, {0, -3, 0}, {0, 2, -2}};
MatrixExp[A t] // MatrixForm // ExpandAll
```

$$
\left(
\begin{array}{ccc}
 e^{-2 t} & 6 e^{-2 t} t+5 e^{-3 t}-5 e^{-2 t} & 3 e^{-2 t} t \\
 0 & e^{-3 t} & 0 \\
 0 & -2 e^{-3 t}+2 e^{-2 t} & e^{-2 t} \\
\end{array}
\right)
$$

### 36.

求下列两类矩阵的矩阵函数：$\cos(A), \sin(A), e^A$

(1) $A$ 为幂等矩阵

$A^2 = A$, 可设 $\cos A = aA + bI$

$$
\left\{
\begin{align*}
&\cos0 = b \\
&\cos1 = a+b
\end{align*}
\right. \implies \left\{
\begin{gathered}
&a = \cos1 - 1 \\
&b = 1
\end{gathered}
\right.
$$

于是 $\cos A = (\cos1-1)A + I$. 对 $\sin A, e^A$ 采用同样的方法可以得到 $\sin A = \sin1\cdot A, e^A = I + (e-1)A$

(2) $A$ 为对合矩阵（即 $A^2 = I$)

$A^2 = I$, 可设 $\cos A = aA + bI$

$$
\left\{
\begin{align*}
&\cos1 = a+b \\
&\cos-1 = -a+b
\end{align*}
\right. \implies \left\{
\begin{gathered}
&a = 0 \\
&b = \cos1
\end{gathered}
\right.
$$

于是 $\cos A = \cos1\cdot I$. 对 $\sin A, e^A$ 采用同样的方法可以得到 $\sin A = \sin 1\cdot A, e^A = \dfrac{e-e^{-1}}{2}A + \dfrac{e+e^{-1}}{2}I$


### 37.

设函数矩阵 $A(t) = \begin{pmatrix} \sin t&\cos t& t\\ \frac{\sin t}{t}&e^t&t^2 \\ 1&0&t^3 \end{pmatrix}$，其中 $t\neq 0$. 计算 $\lim\limits_{t\to0}A(t), \dfrac{d}{dt}A(t), \dfrac{d^2}{dt^2}A(t)$

```mathematica
A[t_] := {{Sin[t], Cos[t], t}, {Sin[t]/t, Exp[t], t^2}, {1, 0, t^3}};
Limit[A[t], t -> 0] // MatrixForm // FullSimplify
D[A[t], t] // MatrixForm // ExpandAll
D[A[t], {t, 2}] // MatrixForm // ExpandAll
```

$$
\left(
\begin{array}{ccc}
 0 & 1 & 0 \\
 1 & 1 & 0 \\
 1 & 0 & 0 \\
\end{array}
\right)
\quad
\left(
\begin{array}{ccc}
 \cos (t) & -\sin (t) & 1 \\
 \frac{\cos (t)}{t}-\frac{\sin (t)}{t^2} & e^t & 2 t \\
 0 & 0 & 3 t^2 \\
\end{array}
\right)
\quad
\left(
\begin{array}{ccc}
 -\sin (t) & -\cos (t) & 0 \\
 -\frac{2 \cos (t)}{t^2}+\frac{2 \sin (t)}{t^3}-\frac{\sin (t)}{t} & e^t & 2 \\
 0 & 0 & 6 t \\
\end{array}
\right)
$$

### 38.

设函数矩阵 $A(t)=\begin{pmatrix} e^{2t}&te^t&t^2 \\ e^{-t}&2e^{2t}&0 \\ 3t&0&0 \end{pmatrix}$，计算 $\int_0^1 A(t)dt$ 和 $\dfrac{d}{dt}\int_0^{t^2} A(s)ds$

此题前两问可以由对逐个矩阵元素作用得到，第三问可以采用变上限积分公式求导来简化

$$
\frac{d}{dt}\int_0^{t^2} A(s)ds = (2t)\cdot A(t^2)
$$

```mathematica
A[t_] := {{Exp[2 t], t Exp[t], t}, {Exp[-t], 2 Exp[2 t], 0}, {3 t, 0,
    0}};
Integrate[A[t], {t, 0, 1}] // MatrixForm // FullSimplify
D[Integrate[A[s], {s, 0, t^2}], t] // MatrixForm // FullSimplify
```

$$
\left(
\begin{array}{ccc}
 \frac{-1+e^2}{2}  & 1 & \frac{1}{2} \\
 \frac{-1+e}{e} & -1+e^2 & 0 \\
 \frac{3}{2} & 0 & 0 \\
\end{array}
\right)
\quad
\left(
\begin{array}{ccc}
 2 e^{2 t^2} t & 2 e^{t^2} t^3 & 2 t^3 \\
 2 e^{-t^2} t & 4 e^{2 t^2} t & 0 \\
 6 t^3 & 0 & 0 \\
\end{array}
\right)
$$

### 39.

证明：(1) 若 $A$ 为实反对称矩阵，则 $e^A$ 为正交矩阵

$$
e^A(e^A)' = e^A\cdot e^{A'} = e^{A+A'} = e^0 = I
$$

(2) 若 $A$ 为 Hermite 阵，则 $e^{iA}$ 为酉矩阵

$$
e^{iA}(e^{iA})^* = e^{iA}\cdot e^{-iA^*} = e^{iA}\cdot e^{-iA} = e^0 = I
$$

### 43.

(1) 设 $A = \begin{pmatrix} 1&1&0 \\ 0&2&1 \\ 0&0&3 \end{pmatrix}$，求 $e^{At}, \sin(At), \cos(At)$

首先求解 Jordan 标准形，$|\lambda I - A| = 0 \implies \lambda = 1, 2, 3$，于是 $A \sim \begin{pmatrix}1 & & \\ & 2 & \\ & & 3 \end{pmatrix}$

设 $f(\lambda) = e^{\lambda t}, g(\lambda) = a_0 + a_1\lambda + a_2\lambda^2$

$$
\begin{align*}
& g(1) = f(1) &\quad & a_0 = 3 e^t - 3 e^{2t} + e^{3t} \\
& g(2) = f(2) &\quad & a_1 = -(5e^t+8e^{2t}-3e^{3t})/2 \\
& g(3) = f(3) &\quad & a_2 = (e^t - 2e^{2t} + e^{3t})/2
\end{align*}
$$

从而 $f(A) = g(A) = a_0 I + a_1 A + a_2 A^2 = \ldots$

```mathematica
A = {{1, 1, 0}, {0, 2, 1}, {0, 0, 3}};
Map[MatrixForm, JordanDecomposition[A]]
MatrixFunction[Exp, A t] // MatrixForm // ExpandAll
MatrixFunction[Sin, A t] // MatrixForm // ExpandAll
MatrixFunction[Cos, A t] // MatrixForm // ExpandAll
```

$$
P = \left(
\begin{array}{ccc}
 1 & 1 & 1 \\
 0 & 1 & 2 \\
 0 & 0 & 2 \\
\end{array}
\right), J_A = \left(
\begin{array}{ccc}
 1 & 0 & 0 \\
 0 & 2 & 0 \\
 0 & 0 & 3 \\
\end{array}
\right) \\
e^{At} =
\left(
\begin{array}{ccc}
 e^t & -e^t+e^{2 t} & \frac{e^t}{2}-e^{2 t}+\frac{e^{3 t}}{2} \\
 0 & e^{2 t} & -e^{2 t}+e^{3 t} \\
 0 & 0 & e^{3 t} \\
\end{array}
\right) \\
\sin(At) =
\left(
\begin{array}{ccc}
 \sin (t) & \sin (2 t)-\sin (t) & \frac{\sin (t)}{2}-\sin (2 t)+\frac{1}{2} \sin (3 t) \\
 0 & \sin (2 t) & \sin (3 t)-\sin (2 t) \\
 0 & 0 & \sin (3 t) \\
\end{array}
\right) \\
\cos(At) =
\left(
\begin{array}{ccc}
 \cos (t) & \cos (2 t)-\cos (t) & \frac{\cos (t)}{2}-\cos (2 t)+\frac{1}{2} \cos (3 t) \\
 0 & \cos (2 t) & \cos (3 t)-\cos (2 t) \\
 0 & 0 & \cos (3 t) \\
\end{array}
\right)
$$

### 46.

(1) 设 $A = \begin{pmatrix} 1&0 \\ 1&0 \end{pmatrix}$，计算积分 $\int_0^t e^{As}ds$

```mathematica
A = {{1, 0}, {1, 0}};
Integrate[MatrixExp[A s], {s, 0, t}] // MatrixForm // ExpandAll
```

$$
\left(
\begin{array}{cc}
 -1+e^t & 0 \\
 -t+e^t-1 & t \\
\end{array}
\right)
$$

(2) 设 $A = \begin{pmatrix} 0&1 \\ 1&0 \end{pmatrix}$，计算 $e^A$ 与 $e^{At}$

```mathematica
A = {{0, 1}, {1, 0}};
MatrixExp[A] // MatrixForm // FullSimplify
MatrixExp[A t] // MatrixForm // FullSimplify
```

$$
\left(
\begin{array}{cc}
 \dfrac{1+e^2}{2 e} & \dfrac{-1+e^2}{2 e} \\
 \dfrac{-1+e^2}{2 e} & \dfrac{1+e^2}{2 e} \\
\end{array}
\right)
\quad
\left(
\begin{array}{cc}
 \cosh (t) & \sinh (t) \\
 \sinh (t) & \cosh (t) \\
\end{array}
\right)
$$

### 47.

设 $A^2 - A + I = 0$，计算 $e^{At}$ 与 $\int_0^t e^{As} ds$

由题意，$A$ 的最小多项式至多为2次。设 $f(\lambda) = e^{\lambda t}, g(\lambda) = a_0 + a_1 \lambda$

令 $f(\lambda_i) = g(\lambda_i)$, 可得

$$
\begin{align*}
& a_0 = \frac{\lambda_2 e^{\lambda_1 t} - \lambda_1 e^{\lambda_2 t}}{\lambda_2 - \lambda_1} = e^{t/2}[\cos \frac{\sqrt3 t}{2} - 1/(\sqrt3 \sin\frac{\sqrt3}{2}t)] \\
& a_1 = \frac{e^{\lambda_1 t} - e^{\lambda_2 t}}{\lambda_1 - \lambda_2} = \frac{2}{\sqrt3}e^{\frac{t}{2}}\sin\frac{\sqrt3}{2}t
\end{align*}
$$

代入 $e^{At} = f(A)$ 中，可得

$$
e^{At} = e^{\frac{t}{2}}\left( \cos\frac{\sqrt3 t}{2} - 1/(\sqrt3\sin\frac{\sqrt3}{2}t) \right)I + \frac{2}{\sqrt3}e^{t/2}\sin{\sqrt3 t/2}A
$$

### 56.

求下列微分方程组的通解

(2) $x'(t)=\begin{pmatrix} 0&1&1 \\ 1&1&-1 \\ 0&1&1 \end{pmatrix}x(t)$

```mathematica
X[t_] := {x1[t], x2[t], x3[t]};
A = {{0, 1, 1}, {1, 1, -1}, {0, 1, 1}};
Map[MatrixForm, JordanDecomposition[A]]
MatrixExp[A t] // MatrixForm // ExpandAll
eqs = Thread[D[X[t], t] == A.X[t]];
X[t] /. DSolve[eqs, X[t], t] // ExpandAll
```

$$
P = \left(
\begin{array}{ccc}
 2 & 1 & 0 \\
 -1 & 0 & 1 \\
 1 & 1 & 0 \\
\end{array}
\right), J_A = \left(
\begin{array}{ccc}
 0 & 0 & 0 \\
 0 & 1 & 1 \\
 0 & 0 & 1 \\
\end{array}
\right) \\
\left(
\begin{array}{ccc}
 e^t t-e^t+2 & e^t t & -e^t t+2 e^t-2 \\
 -1+e^t & e^t & 1-e^t \\
 e^t t-e^t+1 & e^t t & -e^t t+2 e^t-1 \\
\end{array}
\right) \\
\begin{split}
&x1(t) = 2 C[1] - E^t C[1] + E^t t C[1] + E^t t C[2] - 2 C[3] + 2 E^t C[3] -
   E^t t C[3] \\
&x2(t) = -C[1] + E^t C[1] + E^t C[2] + C[3] - E^t C[3] \\
&x3(t) = C[1] - E^t C[1] + E^t t C[1] + E^t t C[2] - C[3] + 2 E^t C[3] -
   E^t t C[3]
 \end{split}
$$


### 57.

求下列微分方程组 $x'(t)=Ax(t)$ 满足初始条件 $x(0)$ 的解

(1) $A = \begin{pmatrix} 1&12 \\ 3&1 \end{pmatrix}$, $x(0)=\begin{pmatrix} 0\\ 1\end{pmatrix}$

```mathematica
X[t_] := {x1[t], x2[t]};
A = {{1, 12}, {3, 1}};
eqs = Thread[D[X[t], t] == A.X[t]];
DSolve[eqs && X[0] == {0, 1}, X[t], t] // ExpandAll
```

$$
\left\{\left\{\text{x1}(t)\to e^{7 t}-e^{-5 t},\text{x2}(t)\to \frac{e^{-5 t}}{2}+\frac{e^{7 t}}{2}\right\}\right\}
$$

### 60.

求方程 $y'''+6y''+11y'+6y=e^{-t}$ 满足 $y(0)=y'(0)=y''(0)=0$ 的解

转化为常微分方程组来做，写出等价形式如下

$$
\left\{
    \begin{align*}
    &\frac{dx}{dt} = Ax(t) + B u(t)\\
    &x(t)|_{t=0} = x(0)
    \end{align*}
\right. \quad A = \begin{pmatrix}
0 & 1 & 0 \\
0 & 0 & 1 \\
-6 & -11 & -6
\end{pmatrix} \quad B = \begin{pmatrix}
0 \\
0 \\
1
\end{pmatrix}
$$

```mathematica
DSolve[y'''[t] + 6 y''[t] + 11 y'[t] + 6 y[t] == Exp[-t] &&
   y[0] == y'[0] == y''[0] == 0, y[t], t] // ExpandAll
```

$$
\left\{\left\{y(t)\to \frac{e^{-t} t}{2}-\frac{e^{-3 t}}{4}+e^{-2 t}-\frac{3 e^{-t}}{4}\right\}\right\}
$$


### 61.

(1) 证明微分方程 $x'(t) = Ax(t) + \gamma e^{at}$ 有形如 $x(t) = \beta e^{at}$ 的解 $\iff (aI - A)\beta = \gamma$，其中 $\beta, \gamma$ 都是 $n$ 维向量，$a\in\mathbb{C}$

$\Rightarrow\quad$ 若微分方程 $x'(t) = Ax(t) + \gamma e^{at}$ 有形如 $x(t) = \beta e^{at}$ 的解，则有 $a\beta e^{at} = A\beta e^{at}+\gamma e^{at} \implies a\beta = A\beta + \gamma$, 此即 $(aI-A)\beta = \gamma$

$\Leftarrow\quad$ 若 $(aI - A)\beta = \gamma$, 则 $a\beta = A\beta + \gamma \implies (\beta e^{at})' = A\beta e^{at} + \gamma e^{at}$. 于是 $\beta e^{at}$ 是上述微分方程的解。

(2) 解 $x'(t)=Ax(t)+e^{2t}C$，其中

$$
A = \begin{pmatrix}
3 & 1 \\
2 & 2
\end{pmatrix}, C = \begin{pmatrix}
-1 \\
-1
\end{pmatrix}, x(0) = \begin{pmatrix}
0 \\
1
\end{pmatrix}
$$

```mathematica
X[t_] := {x1[t], x2[t]};
A = {{3, 1}, {2, 2}};
c = {-1, -1};
Map[MatrixForm, JordanDecomposition[A]]
eqs = Thread[D[X[t], t] == A.X[t] + Exp[2 t] c];
DSolve[eqs && X[0] == {0, 1}, X[t], t] // ExpandAll
```

$$
P = \left(
\begin{array}{cc}
 -1 & 1 \\
 2 & 1 \\
\end{array}
\right), J_A = \left(
\begin{array}{cc}
 1 & 0 \\
 0 & 4 \\
\end{array}
\right) \\
\left\{\left\{\text{x1}(t)\to -\frac{e^t}{3}+\frac{e^{2 t}}{2}-\frac{e^{4 t}}{6},\text{x2}(t)\to \frac{2 e^t}{3}+\frac{e^{2 t}}{2}-\frac{e^{4 t}}{6}\right\}\right\}
$$
