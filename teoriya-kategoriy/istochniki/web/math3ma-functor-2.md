<!-- SOURCE: https://www.math3ma.com/blog/what-is-a-functor-part-2 | captured 2026-07-19 | math3ma (Tai-Danae Bradley), free blog | curl+stdlib extract -->

# math3ma — What Is A Functor Part 2 (captured)

What is a Functor? Definitions and Examples, Part 2 

 -

math3ma 

 Home About categories Subscribe Institute shop 

    

© 2015 - 2023 Math3ma 
Ps. 148 

    

© 2015 – 2025 Math3ma 
Ps. 148 

Archives 

July 2025 
 
February 2025 
 
March 2023 
 
February 2023 
 
January 2023 
 
February 2022 
 
November 2021 
 
September 2021 
 
July 2021 
 
June 2021 
 
December 2020 
 
September 2020 
 
August 2020 
 
July 2020 
 
April 2020 
 
March 2020 
 
February 2020 
 
October 2019 
 
September 2019 
 
July 2019 
 
May 2019 
 
March 2019 
 
January 2019 
 
November 2018 
 
October 2018 
 
September 2018 
 
May 2018 
 
February 2018 
 
January 2018 
 
December 2017 
 
November 2017 
 
October 2017 
 
September 2017 
 
August 2017 
 
July 2017 
 
June 2017 
 
May 2017 
 
April 2017 
 
March 2017 
 
February 2017 
 
January 2017 
 
December 2016 
 
November 2016 
 
October 2016 
 
September 2016 
 
August 2016 
 
July 2016 
 
June 2016 
 
May 2016 
 
April 2016 
 
March 2016 
 
February 2016 
 
January 2016 
 
December 2015 
 
November 2015 
 
October 2015 
 
September 2015 
 
August 2015 
 
July 2015 
 
June 2015 
 
May 2015 
 
April 2015 
 
March 2015 
 
February 2015 

February 2, 2017 

• 
Category Theory 

#### What is a Functor? Definitions and Examples, Part 2

 Continuing yesterday's list of examples of functors, here is... 

#### Example #3: the chain rule

Let $\mathsf{E}$ be the category whose objects are the Euclidean spaces $\mathbb{R},\mathbb{R}^2,\mathbb{R}^3,\ldots,\mathbb{R}^n,\ldots$ and let's suppose each has a special point in it. That is, an object will not just be the space $\mathbb{R}^n$ but $\mathbb{R}^n$ together with a basepoint $x_0$. (Just let $x_0$ be your favorite $n$-dimensional vector. Pick the zero-vector if you like). In this category the morphisms $\mathbb{R^n}\overset{f}{\longrightarrow}\mathbb{R}^m$ are the differentiable functions that preserve basepoints: if $y_0$ is the basepoint in $\mathbb{R}^m$ and $x_0$ is the basepoint in $\mathbb{R}^n$, then $f(x_0)=y_0$.

Let $\mathsf{M}$ be the category whose objects are positive integers and where a morphism $n\to m$ is an $m\times n$ matrix with real entries. In other words, there is an arrow  from $n$ to $m$ for each such matrix. So here, composition of morphisms corresponds to matrix multiplication. 

Define $D:\mathsf{E}\to\mathsf{M}$ as follows,
   
on objects in $\mathsf{E}$: let $D$ send $\mathbb{R}^n$ to its dimension, $n$ 
on morphisms in $\mathsf{E}$: let $D$ send a differentiable function $f:\mathbb{R}^n\to\mathbb{R}^m$ to its $m\times n$ Jacobian matrix, evaluated at $x_0\in\mathbb{R}^n.$ 

The $ij^{\text{th}}$ entry of the matrix $Df\big\vert_{x_0}$ is $\dfrac{\partial f_i}{\partial x_j}(x_0)$ where $f_i$ is the $i^{\text{th}}$ component function of $f=(f_1,f_2,\ldots,f_m)$ and where $x_j$ is the $j^{\text{th}}$ standard basis of $\mathbb{R}^n$. 

Now, is $D$ a functor? If so, then it must respect composition. Let's check this. Suppose $\mathbb{R}^m\overset{g}{\longrightarrow}\mathbb{R}^k$ is another basepoint-preserving differentiable function. Does the following equality hold?

Of course it does! It's the chain rule from multivariable calculus! To find the Jacobian of $g\circ f$ at $x_0$, we simply multiply the Jacobian of $f$ at $x_0$ on the left by the Jacobian of $g$ at $f(x_0)$. And in the special case when $n=m=1$, we recover the familiar single-variable equation:

And a quick check will show that if $\mathbb{R}^n\overset{f}{\longrightarrow}\mathbb{R}^n$ is the identity function, then $Df\big\vert_{x_0}$ is indeed the $n\times n$ identity matrix. 
Thanks to calculus, our $D$ is indeed a functor.  
‍ 

#### Example #4: contravariant functors

There is a functor $F:\mathsf{Vect}_{\mathbb{k}}\to \mathsf{Vect}_{\mathbb{k}}$ where $\mathsf{Vect}_{\mathbb{k}}$ consists of all vector spaces over a field $\mathbb{k}$ with linear transformations as morphisms. This $F$ sends a vector space $V$ to $\text{hom}(V,\mathbb{k})$, the  space of linear functions $V\to\mathbb{k}$. This space of maps is called the dual space of $V$ and is sometimes denoted $V^*$. What do you think this functor does to morphisms? That is, given a linear map $V\overset{f}{\longrightarrow} W$, how can we get a map $F(f)$ between $\text{hom}(V,\mathbb{k})$ and $\text{hom}(W,\mathbb{k})$? 

Well, a map $F(f):\text{hom}(V,\mathbb{k})\to \text{hom}(W,\mathbb{k})$ would have to take a linear transformation $\varphi$ with domain $V$ and send it to one with domain $W$, and it would have to do it using $f:V\to W$ somehow. I'm not sure if there's a way to do this---the arrows simply don't line up.  

BUT, if we instead started with a linear transformation on $W$, say $\varphi:W\to\mathbb{k}$, we could obtain a linear transformation on $V$ by precomposing with $f$!

So let's define $F(f):=f^*$, typically called a pullback , to be the function $f^*$ that takes a linear transformation $\varphi:W\to\mathbb{k}$ and sends it to $\varphi\circ f:V\to\mathbb{k}$, in other words, $f^*(\varphi)=\varphi\circ f$.

See how this assignment of $F$ reverses arrows? 

We give functors with this arrow-flipping property a special name-- contravariant. The "normal" functors (as defined yesterday ) are then called covariant . Formally, a contravariant functor $F:\mathsf{C}^{op}\to\mathsf{D}$ (sometimes you'll see the "op" placed on the $\mathsf{C}$ to remind you, "Hey! this functor's contravariant!") has the same data and properties as a covariant functor, except that the composition property is now $F(f\circ g)=F(g)\circ F(f)$ whenever $f$ and $g$ are composable morphisms in $\mathsf{C}$.

‍ 
For practice, you could try checking that the functor $F:\mathsf{Vect}_{\mathbb{k}}\to\mathsf{Vect}_{\mathbb{k}}$ we defined above is indeed a contravariant functor. (We only discussed its action on morphisms and objects but didn't check that it satisfies the functorial properties.)

#### Example #5: representable functors

If you're familiar with some basic topology, then you might like our last example: 

  There is a contravariant functor $\mathscr{O}$ from $\mathsf{Top}^{op}$ to $\mathsf{Set}$ that associates to each topological space $X$ its set $\mathscr{O}(X)$ of open subsets. On morphisms, $\mathscr{O}$ takes a continuous function $f:X\to Y$ to $f^{-1}:\mathscr{O}(Y)\to\mathscr{O}(X)$ where $f^{-1}$ is a function sending an open set $U$ in $Y$ to the open set $f^{-1}(U)$ in $X$. (We know $f^{-1}(U)$ is open since $f$ is continuous!) 

Now here's what's cool: it turns out that $\mathscr{O}$ is a very, very special kind of functor---it is representable. I won't go into the details here, but in short, for any category $\mathsf{C}$, a (covariant or contravariant) functor $F:\mathsf{C}\to\mathsf{Set}$ is said to be representable if there is an object $c$ in $\mathsf{C}$ so that for all objects $x$ in $C$, the elements of $F(x)$ are really maps $x\to c$ (or maps $c\to x$, depending on the "variance" of $F$). In this case we say $F$ is represented by the object $c$. 

I know this may sound like a head-scratcher, but we've seen this before! Remember our discussion on that measly space with two points, a.k.a. the Sierpinski space , $S$? In that post, we discovered that for any topological space $X$, continuous functions $X\to S$ are in one-to-one correspondence with the open subsets of $X$.

Friends, that's precisely the statement that $\mathscr{O}$ is a representable functor, represented by the one and only Sierpinski space!   Who knew two little dots could be so special?

 Pretty cool, huh?
 
I'd love to chat more about representability on the blog, but to do so, we first need to understand natural transformations . And that's what we'll do next week !

 References: 
 Category Theory in Context  by Emily Riehl 

Share 

 Tweet 

 Share 

Related Posts 

#### Announcing Applied Category Theory 2019

January 5, 2019 

in 
Category Theory 

#### Language, Statistics, & Category Theory, Part 3

July 28, 2021 

in 
Category Theory 

#### Topology: A Categorical Approach

April 3, 2020 

in 
Topology 

#### Language, Statistics, & Category Theory, Part 2

July 7, 2021 

in 
Category Theory 
 
Leave a comment!
