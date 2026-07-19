<!-- SOURCE: https://www.math3ma.com/blog/what-is-a-natural-transformation-2 | captured 2026-07-19 | math3ma (Tai-Danae Bradley), free blog | curl+stdlib extract -->

# math3ma — What Is A Natural Transformation 2 (captured)

What is a Natural Transformation? Definition and Examples, Part 2 

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

February 13, 2017 

• 
Category Theory 

#### What is a Natural Transformation? Definition and Examples, Part 2

Continuing our list of examples of natural transformations , here is... 

#### Example #2: double dual space

This is really the archetypical example of a natural transformation. You'll recall (or let's observe) that every finite dimensional vector space $V$ over a field $\mathbb{k}$ is isomorphic to both its dual space $V^*$ and to its double dual $V^{**}$.       

‍ 

‍ 
‍ 
In the first case, if $\{v_1,\ldots,v_n\}$ is a basis for $V$, then $\{v_1^*,\ldots,v_n^*\}$ is a basis for $V^*$ where for each $i$, the map $v_i^*:V\to\mathbb{k}$ is given by 
$$v_i^*(v_j)=
\begin{cases} 
1, &\text{if $i=j$};\\ 
0 &\text{if $i\neq j$}. 
\end{cases}$$
Unfortunately, this isomorphism $V\overset{\cong}{\longrightarrow} V^*$ is not canonical . That is, a different choice of basis yields a different isomorphism. What's more, the isomorphism can't even materialize until we pick a basis.*

On the other hand, there is an isomorphism $V\overset{\cong}{\longrightarrow}V^{**}$ that requires no choice of basis: for each $v\in V$, let $\text{eval}_v:V^*\to\mathbb{k}$ be the evaluation map . That is, whenever $f:V\to \mathbb{k}$ is an element in $V^*$, define $\text{eval}_v(f):=f(v)$. Folks often refer to this isomorphism as natural . It's natural in the sense that it's there for the taking---it's patiently waiting to be acknowledged, irrespective of how we choose to "view" $V$ (i.e. irrespective of our choice of basis). This is evidenced in the fact that $\text{eval}$ does the same job on each vector space throughout entire category. One map to rule them all.** 

For this reason, the totality of all the evaluation maps assembles into a natural transformation (a natural isomorphism , in fact) between two functors!

To see this, let $(-)^{**}:\mathsf{Vect}_{\mathbb{k}}\to\mathsf{Vect}_{\mathbb{k}}$ be the the double dual functor $(-)^{**}$ that sends a vector space $V$ to $V^{**}$ and that sends a linear map $V\overset{\phi}{\longrightarrow}W$ to $V^{**}\overset{\phi^{**}}{\longrightarrow} W^{**}$, where $\phi^{**}$ is precomposition with $\phi^{*}$ (which we've defined before ). And let $\text{id}:\mathsf{Vect}_{\mathbb{k}}\to\mathsf{Vect}_{\mathbb{k}} $ be the identity functor.

Now let's check that $\text{eval}:\text{id}\Longrightarrow (-)^{**}$ is indeed a natural transformation .                  
 
‍ 
By picking a $v\in V$ and chasing it around the diagram below, notice that the square commutes if and only if $\text{eval}_v\circ \phi^*=\text{eval}_{\phi(v)}$. (Here I'm using the fact that $\phi^{**}(\text{eval}_v)=\text{eval}_v\circ \phi^*$.) 

Does this equality hold? Let's check! Suppose  $f:W\to\mathbb{k}$ is an element of $W^{*}$. Then
$$
\begin{align*}
\text{eval}_v(\phi^*(f))&=\text{eval}_v(f\circ \phi)\\
&=(f\circ\phi)(v)\\
&= f(\phi(v))\\
&=\text{eval}_{\phi(v)}(f).
\end{align*}
$$
Voila! And because each $V\overset{\text{eval}}{\longrightarrow} V^{**}$ is an isomorphism, we've got ourselves a natural ismorphism $\text{id}\Longrightarrow (-)^{**}$. 

 As per our discussion last time , this suggests that $\text{id}$ and $(-)^{**}$ are really the same functor up to a change in perspective. Indeed, this interpretation pairs nicely with the observation that any vector $v\in V$ can either be viewed as, well, a vector , or it can be viewed as an assignment that sends a linear function $f$ to the value $f(v)$. In short, $V$ is genuinely and authentically just like its double dual. 

They are - quite naturally - isomorphic. 

‍ 
‍ 

#### Example #3: representability and Yoneda

In our earlier discussion on functors we noted that a functor $F:\mathsf{C}\to\mathsf{Set}$ is representable if, loosely speaking, there is an object $c\in\mathsf{C}$ so that for all objects $x$ in $\mathsf{C}$, the elements of $F(x)$ are "really" just maps $c\to x$ (or maps $x\to c$, if $F$ is contravariant ). As an illustration, we noted that the functor $\mathscr{O}:\mathsf{Top}^{op}\to\mathsf{Set}$ that sends a topological space $X$ to its set $\mathscr{O}(X)$ of open subsets is represented by the Sierpinski space $S$ since 
$$\mathscr{O}(X)\cong \text{hom}_{\mathsf{Top}}(X,S)$$
where I'm using $\cong$ to denote a set bijection/isomorphism. So in other words, an open subset of $X$ is essentially the same thing as a continuous function $X\to S.$ (We discussed this in length here .)

Now it turns out that this $\cong$ is not just a typical, plain-vanilla  isomorphism. It's natural! That is, the ensemble of isomorphisms $\mathscr{O}(X)\overset{\cong}{\longrightarrow}\text{hom}_{\mathsf{Top}}(X,S)$ (one for each $X$) assemble to form a natural isomorphism between the two functors $\mathscr{O}$ and $\text{hom}_{\mathsf{Top}}(-,S)$.***

In general, then, we say a functor $F:\mathsf{C}\to\mathsf{Set}$ is representable if there is an object $c\in\mathsf{C}$ so that $F$ is naturally isomorphic to the hom functor $\text{hom}_{\mathsf{C}}(c,-)$, i.e. if $$F(x)\cong\text{hom}_{\mathsf{C}}(c,x) \qquad \text{naturally, for all $x\in \mathsf{C}$}$$ (or if $F$ is contravariant, $F(x)\cong\text{hom}_{\mathsf{C}}(x,c)$).  

Here's a very simple example. Suppose $A$ is any set and let $*$ denote the set with one element. Notice that a function from $*$ to $A$ has exactly one element in its image, i.e. the range of $*\to A$ is $\{a\}$ for some $a\in A$. This suggests that a map $*\to A$ is really just a choice of element in $A$! Intuitively then, the elements of $A$ are in bijection with functions $*\to A$,

 $$A\cong\text{hom}_{\mathsf{Set}}(*,A).$$
  
But more is true! The isomorphism $A\to \text{hom}_{\mathsf{Set}}(*,A)$ which sends $a\in A$ to the function, say, $\bar{a}:*\to A$, where $\bar{a}(*)=a$, is natural. That is, for any $A\overset{f}{\longrightarrow}B$, the following square commutes  

Commutativity just says that given an element $a\in A$, we can think of the element $f(a)$ as a map $*\to B$ in one of two equivalent ways: either send $a$ to $f(a)$ via $f$ and then think of $f(a)$ as a map $*\to B$. OR  first think of $a$ as a map $*\to A$, and then postcompose it with $f$. 

  In short, the identity functor $\text{id}:\mathsf{Set}\to\mathsf{Set}$ is represented by the one-point set $*$ since every function $*\to A$ is really just a choice of an element $a\in A$.

  Representability is really the launching point for the Yoneda Lemma which is "arguably the most important result in category theory." We'll certainly chat about Yoneda in a future post.

To whet your appetite, I'll quickly say that one consequence of the Lemma is that we are prompted to think of an object $x$ -- no longer as an object, but now -- as a (representable) functor $\text{hom}(x,-)$, similar to how we may think of a point $a\in A$ as a map $*\to A$.

‍ 
This perspective -- coupled with the idea that morphisms out of $x$ (i.e. the elements of $\text{hom}(x,-)$) are simply "the relationships of $x$ with other objects" -- motivates the categorical mantra that an object is completely determined by its relationships to other objects. As a wise person once said, "You tell me who your friends are, and I'll tell you who YOU are." The upshot is that this proverb holds in life as well as in category theory.

And that is The Most Obvious Secret of Mathematics !

‍ 
*One can show that there is no "natural" isomorphism of a vector space with its dual. For instance, see p. 234 of Eilenberg and Mac Lane's 1945 paper, "The General Theory of Natural Equivalences." 
** This sort of reminds me of the difference between pointwise and uniform convergence. A sequences of functions $\{f_n:X\to\mathbb{R}\}$ converges to a function $f$ pointwise if, from the vantage point of some $x\in X$, the $f_n$ are eventually within some $\epsilon$ of $f$. But that value of $\epsilon$ might be different at a different vantage point, i.e. at a different $x'\in X$. On the other hand, the sequence converges uniformly if there's an $\epsilon$ that does the job no matter where you stand, i.e. for all $x\in X$.  
***Here, $\text{hom}_{\mathsf{Top}}(-,S):\mathsf{Top}^{op}\to\mathsf{Set}$ is the contravariant functor that sends a topological space $X$ to the set $\text{hom}_{\mathsf{Top}}(X,S)$ of continuous functions $X\to S$ and that sends a continuous function $X\overset{f}{\longrightarrow} Y$ to its pullback $\text{hom}_{\mathsf{Top}}(Y,S)\overset{f^*}{\longrightarrow}\text{hom}_{\mathsf{Top}}(X,S).$ 

Share 

 Tweet 

 Share 

Related Posts 

#### Topology Book Launch

August 20, 2020 

in 
Topology 

#### Language, Statistics, & Category Theory, Part 1

June 29, 2021 

in 
Category Theory 

#### Viewing Matrices & Probability as Graphs

March 6, 2019 

in 
Probability 

#### Topology: A Categorical Approach

April 3, 2020 

in 
Topology 
 
Leave a comment!
