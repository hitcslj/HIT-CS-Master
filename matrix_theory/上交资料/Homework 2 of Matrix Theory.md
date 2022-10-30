
## 习题一

### 30.

> 对 $x=(x_1, x_2)^{\mathrm{T}}$, $y=(y_1, y_2)^{\mathrm{T}}$, 规定
> $$
(x,y)=ax_1y_1+bx_1y_2+bx_2y_1+cx_2y_2
$$
> 证明: $(x,y)$ 是 $\mathbb{R}^2$ 的内积 $\iff a>0$， $ac>b^2$

由定义 $(x,y) = ax_1y_1+bx_1y_2+bx_2y_1+cx_2y_2$ ，双线性性和共轭对称性易证。

只需证明此內积满足正定性

因

$$
(x,y) = (y_1, y_2)\begin{pmatrix}
a & b \\
b & c \\
\end{pmatrix} \begin{pmatrix}
x_1 \\
x_2 \\
\end{pmatrix} = y'Ax
$$

故 $(x,y)$ 是 $\mathbb{R}^2$ 的內积 $\iff\quad$ $A$ 正定 $\iff\quad ac>b^2, a>0$

### 31.

> 设$V=\{ a\cos t+ b\sin t: \text{其中}a,b为\text{任意实数} \}$ 是实二维线性空间. 对任意 $f, g\in V$, 定义
> $$
(f,g)=f(0)g(0)+f(\frac{\pi}{2})g(\frac{\pi}{2})
$$
> 证明 $(x,y)$ 是 $V$ 上的内积，并求 $h(t)=3\cos(t+7)+4\sin(t+9)$ 的长度

不妨假设 $f=a_1\cos t + b_1\sin t \quad g=a_2\cos t + b_2\sin t$ 根据內积定义

$$
(f,g)=f(0)g(0)+f(\frac{\pi}{2})g(\frac{\pi}{2})=a_1a_2+b_1b_2
$$

于是

1. $(f,g) = a_1a_2+b_1b_2 = g(0)f(0)+g(\frac{\pi}{2})f(\frac{\pi}{2})=(g,f)$

2. $(f,f) = f^(0)+f^2(\frac{\pi}{2}) = a_1^2 +b_1^2 \geq 0$ 且等号成立 $\iff f=0$

3. $$
\begin{split}
(mf+ng, h) &= [mf(0)+ng(0)]h(0) + [mf(\frac{\pi}{2})+ng(\frac{\pi}{2})]h(\frac{\pi}{2}) \\
&= m[f(0)h(0)+f(\frac{\pi}{2}g(\frac{\pi}{2})] + n [g(0)h(0) + g(\frac{\pi}{2})h(\frac{\pi}{2})] \\
&= m(f,h) + n(g,h) \\
\end{split}
$$

所以，$(f,g)$ 是 $V$ 上的一个內积

$$
\begin{split}
\Vert h \Vert &= \sqrt{(h,h)} = \sqrt{h^2(0)+h^2(\frac{\pi}{2})} \\
&= \sqrt{(2\cos 7 + 4\sin 9)^2 + [3\cos (\frac{\pi}{2}+7) + 4\sin(\frac{\pi}{2}+9)]^2} \\
&= \sqrt{ 25 + 24 (\cos 7 \sin 9 - \sin 7 \cos 9)} \\
&= \sqrt{25+24\sin 2} \neq 5 \\
\end{split}
$$

## 习题二

### 4.

> 证明定理 2.4.1(多子空间直和的判定)

（多子空间直和的判定）设 $W_1, W_2, \cdots, W_s$ 是线性空间 $V$ 的子空间，则下列命题等价：
(1) $W_1+W_2+\cdots+W_s$ 是直和，即

$$
\dim(W_1+W_2+\cdots+W_s) = \dim W_1 +\dim W_2 + \cdots + \dim W_s
$$

(2) $W_j\cap \Sigma_{k\neq j}W_k = 0$, $1\leq j\leq s$, $1\leq k\leq s$

(3) 任意向量 $\alpha\in W_1+W_2+\cdots+W_s$ 的分解式唯一；

(4) 零向量的分解式唯一

(1)$\implies$(2):

因 $W_1+W_2+\cdots+W_s$ 是直和，故 $(W_1+W_2+\cdots+W_{s-1})\oplus W_s$ 为直和。每个子空间与其余子空间交集均为 $0$，即

$$
W_j\cap \Sigma_{k\neq j}W_k = 0, 1\leq j\leq s, 1\leq k\leq s
$$

(2)$\implies$(3):

反证法，若分解式不唯一，即

$$
\alpha = w_1 + w_2 + \cdots + w_s = w_1' + w_2' + \cdots + w_s'
$$

其中 $w_i-w_i'\in W_i$。则可得

$$
w_1'-w_1 = (w_2-w_2')+\cdots+(w_s-w_s')\in W_2+\cdots+W_s
$$

故 $w_1'-w_1\in W_1$ 且 $w_1'-w_1\in W_2+\cdots+W_s$

因 $W_1\cap (W_2+\cdots+W_s) = 0$，故 $w_1'-w_1=0$ 与假设矛盾！

(3)$\implies$(4):

取任意向量 $\alpha=0$ 即可

(4)$\implies$(1):

因零向量分解式唯一，故 $W_1+(W_2+\cdots+W_s)$ 是直和，即

$$
\dim(W_1+W_2+\cdots+W_s) = \dim W_1 + \dim(W_2+\cdots+W_s)
$$

对 $W_2+\cdots+W_s$ 同样有如上，依此归纳可得

$$
\dim(W_1+W_2+\cdots+W_s) = \dim W_1 +\dim W_2 + \cdots + \dim W_s
$$

### 5.

> 设
$$
\begin{pmatrix}
1 & 1 & 2 \\
0 & 1 & 1 \\
1 & 3 & 4 \\
\end{pmatrix}
$$
> 求 $A$ 的四个相关子空间.

$$
\begin{split}
A = \begin{pmatrix}
1 & 1 & 2 \\
1 & 1 & 1 \\
1 & 3 & 4 \\
\end{pmatrix} &\rightarrow \left(\begin{array}{@{}ccc:ccc@{}}
1 & 1 & 2 & 1 & 0 & 0 \\
0 & 1 & 1 & 0 & 1 & 0 \\
1 & 3 & 4 & 0 & 0 & 1 \\
\end{array}\right) \\
&\rightarrow \left( \begin{array}{@{}ccc:ccc@{}}
1 & 0 & 1 & 1 & -1 & 0 \\
0 & 1 & 1 & 0 & 1 & 0 \\
0 & 0 & 0 & -1 & -2 & 1 \\
\end{array} \right) = \begin{pmatrix}
H_A & P \\
\end{pmatrix}
\end{split}
$$

于是

$$
\begin{split}
&R(A) = \mathrm{span}\{ (1,0,1)', (1,1,3)' \} \\
&R(A') = \mathrm{span}\{ (1,0,1)', (0,1,1)' \} \\
&N(A) = \mathrm{span}\{ (-1,-1, 1)' \} \\
&N(A') = \mathrm{span}\{ (-1,-2,1)' \} \\
\end{split}
$$

### 9.

> 设 $U = [(1,2,3,6)^{\mathrm{T}}, (4,-1,3,6)^{\mathrm{T}}, (5,1,6,12)^{\mathrm{T}}]$，$W=[(1,-1,1,1)^{\mathrm{T}}, (2,-1,4,5)^{\mathrm{T}}]$ 是 $\mathbb{R}^4$ 的两个子空间
>
> (1) 求 $U\cap W$ 的基；
> (2) 扩充 $U\cap W$ 的基，使其成为 $U$ 的基；
> (3) 扩充 $U\cap W$ 的基，使其成为 $W$ 的基；
> (4) 求 $U+W$ 的基

不妨设 $U = (u_1, u_2, u_3), W = (w_1, w_2)$ 不难发现 $u_1+u_2=u_3$ 则有 $\dim U = \dim W =2$

考虑方程组

$$
\underbrace{\left(\begin{array}{@{}cc:cc@{}}
u_1 & u_2 & w_1 & w_2 \\
\end{array}\right)}_{A}  X = 0
$$

的解，可得 $x = (\frac79, -\frac49, 3, -1)'$ 由此 $\dim (U+W) = 3$

于是 $U\cap W$ 的基是

$$
\begin{pmatrix}
1 & 4 \\
2 & -1 \\
3 & 3 \\
6 & 6 \\
\end{pmatrix}\begin{pmatrix}
\frac79 \\
-\frac49 \\
\end{pmatrix} = \begin{pmatrix}
-1 \\
2 \\
1 \\
2 \\
\end{pmatrix}
$$

由基的扩充定理，可得 $U$ 的基为 $(-1, 2, 1, 2)', (1,2, 3, 6)'$ $W$ 的基为 $(-1, 2, 1, 2)' (1, -1, 1, 1)'$

$U+W$ 的基为 $(-1, 2, 1, 2 )'$， $(1, 2, 3, 6)'$，$(1, -1, 1, 1)'$

### 10.

> 设 $U=\{ (x,y,z,w): x+y+z+w=0 \}$，$W=\{ (x,y,z,w): x-y+z-w=0 \}$.
>
> 求 $U\cap W$，$U+W$ 的维数与基

将 $U$, $W$ 视为齐次线性方程的解空间，可知 $\dim U = \dim W = 4-1 = 3$

记 $U\cap W$ 为 $AX=0$ 的解空间，其中

$$
A = \begin{pmatrix}
1 & 1 & 1 & 1 \\
1 & -1 & 1 & -1 \\
0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 \\
\end{pmatrix}
$$

可以解得 $U\cap W$ 的一组基为 $(1,0,-1,0)$，$(0,1,0,-1)$

由维数定理 $\dim(U+W) = \dim(U) + \dim(W) - \dim(U\cap W) = 4$

故可取标准基 $e_1, e_2, e_3, e_4$



### 25.

> 分别求导数运算 $\partial : f(x)\mapsto f'(x)$ 在标准基 $1,x,x^2,\cdots,x^{n-1}$ 与基 $1,(x-a),(x-a)^2,\cdots,(x-a)^{n-1}$ 下的矩阵.
>
> 问 $\partial$ 的行列式与迹是多少？解释之

$$
\begin{split}
\partial(1, x, x^2, \cdots, x^{n-1}) &= (0, 1, 2x, \cdots, (n-1)x^{n-2}) \\
&= (1, x, x^2, \cdots, x^{n-1}) \underbrace{\begin{pmatrix}
0 & 1 & & & & \\
& 0 & 2 & & & \\
& & 0 & \ddots & & \\
& & & \ddots & \ddots & \\
& & & & \ddots & n-1 \\
& & & & & 0 \\
\end{pmatrix}}_{A}
\end{split}
$$

$$
\mathrm{tr}(A) = 0 \quad r(A) = n-1<n \implies \vert A \vert = 0
$$

利用变量替换 $x=x-a$ 可以知道另一组基下结果是一样的。

### 26.

> 设 $V$ 是数域 $\mathbb{F}$ 上的 $n$ 阶矩阵全体，$\sigma$ 是将 $V$ 中任意元素的严格下三角部分变为 $0$ 的映射.
>
> 判断 $\sigma$ 是否为 $V$ 的线性变换. 若是，求其核与像；并任选 $V$ 的一组基，求 $\sigma$ 在该组基下的矩阵.

1. 首先证明若 $\sigma$ 保持其余部分不变为线性变换，这是因为

$$
\forall A, B \in V\, k_1, k_2\in\mathbb{F} \quad k_1A+k_2B \in V
$$

且

$$
\sigma(k_1A + k_2B)=k_1\sigma(A)+k_2\sigma(B)\in V
$$

2. 根据定义

$$
\begin{split}
&\mathrm{Ker} \sigma = \lbrace A \mid \sigma(A)= 0 \rbrace = \lbrace A \text{为严格下三角矩阵} \rbrace \\
&\mathrm{Im} \sigma = \lbrace A \mid \sigma(B) = A ,\forall B\in V \rbrace = \lbrace A \text{为上三角矩阵} \rbrace
\end{split}
$$

取 $V$ 的一组标准基 $E_{ij} \quad (i,j = 1,2,\cdots, n)$，然后按照先 $E_{ij}\in\mathrm{Ker}\sigma$ 再 $E_{ij}\in\mathrm{Im}\sigma$ 顺序进行排序，即

$$
(E_{21}, E_{31}，E_{32}, \cdots, E_{n,n-1}, E_{11}, E_{12}, \cdots, E_{1n}, E_{22}, \cdots, E_{2n}, \cdots\cdots, E_{nn})
$$

易知，$\sigma$ 在此基下的矩阵为

$$
\begin{pmatrix}
\mathbf{0}_{\frac{n(n-1)}{2}} & 0 \\
0 & I_{\frac{n(n+1)}{2}} \\
\end{pmatrix}
$$

### 29.

> 设 $V=\mathbb{R}^3$，$\sigma(x,y,z)=(x+2y-z,y+z,x+y-2z)$. 求
>
> (1) $\sigma$ 的核与像空间的基和维数；
>
> (2) $\sigma$ 的行列式与迹.

(1)

$$
\begin{split}
\sigma(x,y,z) &= (x+2y-z, y-z, x+y-2z) \\
&= (x, y, z)\underbrace{\begin{pmatrix}
1 & 0 & 1 \\
2 & 1 & 1 \\
-1 & 1 & -2 \\
\end{pmatrix}}_{A}
\end{split}
$$

于是

$$
\mathrm{Ker}\sigma = \{ X \mid XA = 0 \} = \{ X \mid A'X' = 0 \} = \mathrm{span} \{ (3, -1, 1)' \}
$$

从而 $\dim\mathrm{Ker}\sigma = 1$ 因 $\mathrm{Im}\sigma\cong R(A')$ 有

$$
\mathrm{Im}\sigma = \mathrm{span}\{ (1,0,1)', (2,1,1)' \} \quad \dim(\mathrm{Im}\sigma) = 2
$$

(2)

$$
\begin{split}
&\mathrm{tr}(A) = 1 + 1 - 2 = 0 \\
&r(A) = 2 < 3 \implies |A| = 0 \\
\end{split}
$$

### 30.

> 设 $V$ 是 $n$ 维內积空间，$U$ 是 $V$ 的子空间.
>
> 令 $W=\{ \alpha\in V : (\alpha, \beta)=0, \forall \beta\in U \}$. 证明 $W$ 是 $V$ 的子空间且 $V=U\oplus W$

1. 先证 $W$ 是线性子空间。显然 $W\subset V$ 又

$$
\forall \alpha, \gamma\in W, (a\alpha + b\gamma, \beta) = a(\alpha, \beta) + b(\gamma , \beta) = 0\quad \forall \beta\in U
$$

则 $a\alpha + b\gamma \in W$

2. 下证直和。因

$$
U\cap W = \{ \alpha\in U: (\alpha, \beta) = 0,\, \forall \beta\in U \} = \{ 0 \}
$$

对任意 $\alpha \in V$, 将其往 $\beta$ 上作正交投影分解，即 $\alpha = \mathrm{Proj}_{\beta} \alpha + (\alpha - \mathrm{Proj}_{\beta}\alpha)$

其中 $\mathrm{Proj}_{\beta}\alpha\in U$, 且有 $(\mathrm{Proj}_{\beta}\alpha, \alpha - \mathrm{Proj}_{\beta}\alpha) = 0$

故有 $\alpha \in U + W$ 即 $V \subset U + W$

又有 $U+W\subset V$，所以 $V=U+W$，从而 $V = U\oplus W$

### 32.

> 设 $V=\mathbb{R}[x]_n$, 其上的内积为
> $$
(f(x),g(x))=\int_0^1 f(x)g(x)\,dx
$$
> 设 $U=\{ f(x)\in V: f(0)=0 \}$.
> (1) 证明 $U$ 是 $V$ 的一个 $n-1$ 维子空间，并求 $U$ 的一组基；
> (2) 当 $n=3$ 时，求 $U$ 的正交补 $U^{\perp}$

(1)

设 $f, g\in U$，对任意实数 $a, b$，我们有 $af+bg\in U$ 所以 $U$ 是 $V$ 的一个子空间。

取 $U$ 的一组基 $\{x, x^2, \cdots, x^n\}$ 可以知道 $\dim U = n - 1$

(2)

当 $n=3$ 时，我们有 $V = \mathrm{span}\{1, x, x^2\}$ 以及 $U = \mathrm{span}\{ x, x^2\}$

不妨假设 $U^{\perp} = \mathrm{span}\{ ax^2+bx+c \}$ 因 $U\oplus U^{\perp} = V$ 则由

$$
\begin{split}
&(ax^2+bx+c,\, x) &= 0 \\
&(ax^2+bx+c,\, x^2) &= 0 \\
\end{split}
$$

可以推出

$$
a=-10 \quad b=12 \quad c=-3
$$

从而给出正交补空间的一种表达 $U^{\perp} = \mathrm{span}\{ -3 + 12x -10 x^2 \}$
