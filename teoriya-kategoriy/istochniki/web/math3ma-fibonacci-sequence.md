<!-- SOURCE: https://www.math3ma.com/blog/fibonacci-sequence | captured 2026-07-19 | math3ma (Tai-Danae Bradley), free blog | curl+stdlib extract -->

# math3ma — Fibonacci Sequence (captured)

The Fibonacci Sequence as a Functor 

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

December 14, 2020 

• 
Category Theory 

#### The Fibonacci Sequence as a Functor

Over the years, the articles on this blog have spanned a wide range of audiences, from fun facts ( Multiplying Non-Numbers ), to undergraduate level ( The First Isomorphism Theorem, Intuitively ), to graduate level ( What is an Operad? ), to research level . Today's article is more on the fun-fact side of things, along with—like most articles here—an eye towards category theory. 
So here's a fun fact about greatest common divisors (GCDs) and the Fibonacci sequence $F_1,F_2,F_3,\ldots$, where $F_1=F_2=1$ and $F_n:=F_{n-1} + F_{n-2}$ for $n>1$. For all $n,m\geq 1$, 
 
In words, the greatest common divisor of the $n$th and $m$th Fibonacci numbers is the Fibonacci number whose index is the greatest common divisor of $n$ and $m$. ( Here's a proof.) Upon seeing this, your "spidey senses" might be tingling.  Surely  there's some structure-preserving map $F$ lurking in the background, and this identity means it has a certain nice property. But what is that map? And what structure does it preserve? And what's the formal way to describe the nice property it has? 
The short answer is that the natural numbers $\mathbb{N}=\{1,2,3,\ldots\}$ form a partially ordered set (poset) under division, and the function $F\colon \mathbb{N}\to\mathbb{N}$ defined by $n\mapsto F_n:=F(n)$ preserves meets : $F_n\wedge F_m = F(n\wedge m)$. When viewing $\mathbb{N}$ from this perspective, the meet of two natural numbers is precisely their GCD: $n\wedge m = \text{gcd}(n,m).$ Now, a poset in which every nonempty finite subset has a meet is called a meet-semilattice , and the natural numbers are an example. You can always find the GCD of a finite subset of natural numbers. And a meet-preserving function between meet-semilattices, such as our $F$ above, is called a meet-semilattice homomorphism. 
 ‍ Short and sweet. 
But posets, meets, and meet-semilattice homomorphisms can all be re-expressed in the language of category theory: posets are categories ; meets are categorical limits , and meet-semilattice homomorphisms are functors with a nice property. This shift in perspective is a bit overkill, but it's fun to think about! 
 
In particular, the category of natural numbers that we'll define below is one of my favorite introductory examples. What's more, unwinding these ideas will take us through a tour of basic ideas discussed previously on the blog— categories , functors , and categorical limits —which may be helpful for anyone learning the subject. 
So let's begin! I want to show you how the natural numbers form a category with a nice property: it has all limits. Moreover, the identity $\text{gcd}(F_n,F_m)=F_{\text{gcd}(n,m)}$ is another way of saying our Fibonacci function $F\colon \mathbb{N}\to\mathbb{N}$ is a functor that preserves limits, which is to say it's a continuous functor . 
Let's go through these claims one-by-one. 

#### The natural numbers $\mathbb{N}$ are a category .

Consider a category whose objects are natural numbers $\mathbb{N}=\{1,2,3,\ldots\}$ and whose morphisms are given by divisibility. That is, given two natural numbers $n$ and $m$, there is a morphism $n\to m$ if and only if $n$ evenly divides $m$. I've drawn a few objects and (nonidentity) morphisms below, but there are infinitely many more. 
 
It's quick to check this does indeed define a category: there's an identity morphism $n\to n$ for each $n\in \mathbb{N}$ since $n$ divides evenly into itself, and composition of morphisms $n\to m\to p$ follows from transitivity of divisibility. 
In fact, looking under the hood, divisibility defines a partial order on the set $\mathbb{N}$; that is, it's a reflexive, antisymmetric, and transitive relation. Equipped with this partial, the set $\mathbb{N}$ is a poset . Alternatively, as we've just shown, we can also view $\mathbb{N}$ as category: the identity morphisms $n\to n$ are provided by reflexivity $n\mid n$, and composition $n\to m\to p$ is provided by transitivity. In fact, this is a very simple category: there is at most one morphism between any two objects. Every poset viewed as a category has this property. 
In what follows, let's be flexible when thinking of $\mathbb{N}$ as a poset or a category—moving between the two is simply a change in perspective. 

#### The category $\mathbb{N}$ has all finite limits , given by the GCD.

As we discussed long ago , limits and colimits in category theory are a (and in some sense the ) most efficient way of constructing new mathematical objects from old. 
 
For instance, given a bunch of natural numbers, how might we combine them to get a new number? There are lots of possibilities: we could add them, subtract them, multiply them, divide them, compute their GCD, and so on. The last option is decidedly different from the rest because it satisfies something called a universal property. 
We won't get into the details, but recall that the GCD of $n$ and $m$ is their meet in the poset $\mathbb{N}$. So not only is the GCD a lower bound on $n$ and $m$, it's the larg est of all lower bounds. The "est" here is what clues us in to a universal property lying in the background. Indeed, in the eyes of category theory, $\text{gcd}(n,m)$ is called the categorical product of $n$ and $m$, which is a general construction that appears all across the mathematical landscape. Other examples of products include, meets in general posets, the Cartesian product of sets $X\times Y$, the direct sum of finite-dimensional vector spaces $V\oplus W$, the Cartesian product of topological spaces (hello Multiplying Non-Numbers! ), and lots more. 
In fact, not only is $\text{gcd}(n,m)$ the product of $n$ and $m$, it's also their pullback , their inverse limit , and their equalizer ! These are all examples of more general constructions called categorical limits . In a poset viewed as a category, these different constructions all happen to coincide with each other. In particular, in our category $\mathbb{N}$, all of these lofty terms simply become the GCD. We've discussed this in detail before . 
 
Now, recall that the poset $\mathbb{N}$ is a meet-semilattice , which is the name given to posets in which the meet of every nonempty finite subset exists. Not surprisingly, this concept has a generalization in category theory. There, meets are replaced by limits , and a category in which the limit of every finite collection of objects (called a diagram , more formally) exists is called a finitely complete category . So every meet-semilattice with a greatest element, such as $\mathbb{N}$, is an example of a finitely complete category.* 

#### The Fibonacci sequence is a functor .

Let's now recall the function $F\colon\mathbb{N}\to\mathbb{N}$ defined by assigning to each natural number $n$ the $n$th Fibonacci number, $F(n):=F_n$. When viewing $\mathbb{N}$ as a category, $F$ is a functor. This follows from the fact that $$n\mid m \quad\text{implies}\quad F_n\mid F_m$$ for all $n,m\geq 1$ or equivalently, that for each $n\geq 1$, one has $F_{n}\mid F_{nk}$ for all $k\in\mathbb{N}$, which can be proved by induction on $n$. To see this, know that a functor between categories is an assignment on objects (that's the $n\mapsto F_n$ part) and on morphisms. The latter means for every morphism $n\to m$ we need a morphism $F_n\to F_m$. But that's precisely the divisibility implication above. Reflexivity and transitivity of division further guaratee that $F$ preserves identity morphisms as well as composition. 
More generally, functors between posets viewed as categories are precisely order-preserving functions. 
 
And now we're ready for the punchline! 

#### This functor is continuous .

In category theory, a functor between categories $F\colon\mathsf{C}\to\mathsf{D}$ is called continuous if it preserves limits. Said more formally, one starts with something called a diagram $X$ in $\mathsf{C}$, as mentioned earlier. Then one computes the limit $\text{lim} X$ of that diagram in $\mathsf{C}$, if it exists, and one says $F$ is continuous if there is an isomorphism $F(\text{lim} X)\cong \lim (FX)$. 
It turns out that when both categories $\mathsf{C}$ and $\mathsf{D}$ are meet-semilattices, a continuous functor between them reduces to something simple: a meet-semilattice homomorphism . In our case, that amounts to a function $F\colon \mathbb{N}\to\mathbb{N}$ that satisfies the following properties for all $n,m\geq 1$: 
[$F$ is a functor] It's compatible with the partial order: $n\mid m$ implies $F(n)\mid F(m)$. 
[$F$ preserves limits.] It preserves meets; that is, there is an equality $F(n\wedge m) = F(n)\wedge F(m).$ 
And as we noted earlier, meets $\wedge$ in $\mathbb{N}$ are greatest common divisors! Thus, taking $F$ to be the Fibonacci sequence $n\mapsto F_n$, the equality in item (2) brings us back to where we started: $F(n\wedge m) = F(n) \wedge F(m)$ is precisely the condition that $F_{\text{gcd}(n,m)}= \text{gcd}(F_n,F_m)$. 
 
 Et voila! 
 
To summarize, the Fibonacci sequence $n\mapsto F_n$ can be thought of as a continuous functor from the complete category $\mathbb{N}$ to itself. More simply, it's a meet-semilattice homomorphism between the natural numbers when viewed as a poset under divisibility. 
Now, I'll be the first to admit—the categorical language is a bit overloaded for such a simple idea. But it's fun to peak into the world of abstraction, and see how familiar things are special cases of something much more general! And by the way, there's nothing too special about the Fibonacci numbers here—any strong divisibility sequence  can be recast in this way! 
 
*Thanks to a reader for catching the original (and incorrect) omission of the word finite . (See comment below.) 

Share 

 Tweet 

 Share 

Related Posts 

#### Commutative Diagrams Explained

July 5, 2017 

in 
Other 

#### A Diagram is a Functor

January 10, 2018 

in 
Category Theory 

#### Limits and Colimits, Part 1 (Introduction)

January 2, 2018 

in 
Category Theory 

#### At the Interface of Algebra and Statistics

April 13, 2020 

in 
Probability 
 
Leave a comment!
