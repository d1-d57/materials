# What is an Adjunction? Part 3 (Examples)

> Источник: [https://www.math3ma.com/blog/what-is-an-adjunction-part-3](https://www.math3ma.com/blog/what-is-an-adjunction-part-3)
> Автор: Tai-Danae Bradley (math3ma)
> Сохранено: 2026-07-16

---


![](https://cdn.prod.website-files.com/5b1d421032996833ff2a7704/5b651c50884ddb291aa16208_newM.avif)

# What is an Adjunction? Part 3 (Examples)

Welcome to the last installment in our mini-series on adjunctions in category theory. We motivated the discussion in Part 1 and walked through formal definitions in Part 2 . Today I'll share some examples. In Mac Lane's well-known words , "adjoint functors arise everywhere," so this post contains only a tiny subset of examples. Even so, I hope they'll help give you an eye for adjunctions and enhance your vision to spot them elsewhere.

An adjunction, you'll recall, consists of a pair of functors $F\dashv G$ between categories $\mathsf{C}$ and $\mathsf{D}$ together with a bijection of sets, as below, for all objects $X$ in $\mathsf{C}$ and $Y$ in $\mathsf{D}$.

![](https://cdn.prod.website-files.com/5b1d427ae0c922e912eda447/5d8641a38d9d4bbd9c20bd3c_adjunction2.jpg)

In Part 2 , we illustrated this bijection using a free-forgetful adjunction in linear algebra as our guide. So let's put "free-forgetful adjuctions" first on today's list of examples.

## Free-Forgetful Adjunctions

Whenever a functor $U\colon \mathsf{D}\to\mathsf{C}$ ignores some data or structure in $\mathsf{D}$ and has a left adjoint $F\colon \mathsf{C}\to\mathsf{D}$, the left adjoint will have a "free" flavor. Since the right adjoint is "forgetful" (this does not have an official definition), such an adjunction $F\dashv U$ is called a free-forgetful adjunction .

Last week we saw this with sets and real vector spaces. Another illustration lies in the connection between directed graphs and categories. Both involve vertices/objects and edges/morphisms. So how exactly are they related? Every directed graph gives rise to a category, and every category is a directed graph (with extra data). More formally, there is an adjunction involving the category $\mathsf{DirGraph}$ of directed graphs and the category $\mathsf{Cat}$ of categories.

![](https://cdn.prod.website-files.com/5b1d427ae0c922e912eda447/5d87a281e171f8d8cd872b49_ff_adj.jpg)

In the picture above, the functor $F$ turns a graph $G$ into a category $FG$ by viewing vertices as objects and edges as morphisms. It also inserts identity arrows at each vertex, and declares the set of morphisms between two vertices to be the set of all finite paths between them. Composition is then concatenation of paths. On the other hand, the functor $U$ assigns to a category $\mathsf{C}$ its underlying graph $U\mathsf{C}$. It just forgets the identity and composition axioms, which aren't needed to specify a graph. The bijection enjoyed by this adjunction is

![](https://cdn.prod.website-files.com/5b1d427ae0c922e912eda447/5d87a6fee171f8413887b607_ff_bij.jpg)

which says something along the lines of, "If you'd like to view a graph $G$ as a diagram in some category $\mathsf{C}$, then you're in luck, because there's exactly one way to turn that graph into a category $FG$ so that the diagram $G$ in $\mathsf{C}$ is a functor $FG\to \mathsf{C}$." This calls to mind an idea we've seen before: diagrams are functors.

## Product-Hom Adjunction

The next example gives a nice categorical relationship between multiplication and exponentiation. Early in life, one learns that $x^{y\times z}=(x^y)^z$ holds whenever $x,y,z$ are numbers. Later in life, one learns that this holds for sets , too:

![](https://cdn.prod.website-files.com/5b1d427ae0c922e912eda447/5d87a8da9d174b491c7f89f7_prod_hom.jpg)

This is called the product-hom adjunction . To unravel it, let's use the notation $X^Y$ to mean the set of functions from $Y$ to $X$, that is $X^Y:=\text{hom}(Y,X)$. This is nice, since if $X$ has 2 elements and $Y$ has 3 elements then there are exactly 8 functions from $Y$ to $X$, i.e. $|\text{hom}(Y,X)|=2^3=|X|^{|Y|}$.

Now, how is the above bijection an adjunction? For any set $Y$ there is a functor $Y\times -\colon\mathsf{Set}\to\mathsf{Set}$ that assigns to a set $Z$ the Cartesian product $Y\times Z$. There is another functor $\hom(Y,-)\colon \mathsf{Set}\to\mathsf{Set}$ that assigns to a set $Z$ the set of all functions $\text{hom}(Y,Z)$. Then $Y\times -$ is left adjoint to $\text{hom}(Y,-)$.

![](https://cdn.prod.website-files.com/5b1d427ae0c922e912eda447/5d88c6ce16ac241fbf45c647_prod_hom2.jpg)

In other words, the bijection below holds for all sets $X$ and $Z$.

![](https://cdn.prod.website-files.com/5b1d427ae0c922e912eda447/5d87f1258d9d4b1c2097388e_prod_hom3.jpg)

Indeed, every function $f\colon Y\times Z\to X$ gives rise to a function $\hat{f_z}\colon Y\to X$ by fixing a variable $z\in Z$, namely $\hat{f_z}(y):=f(y,z)\in X$. Likewise, any function $g\colon Z\to X^Y$ gives rise to a function $\hat{g}\colon Y\times Z\to X$ by $\hat{g}(y,z):=gz(y)$. In computer science, you'll recognize this as currying .

Other areas of math have their own version of the product-hom adjunction. For instance, if $X,Y,Z$ are topological spaces with chosen basepoints, then there is a "based" version of the Cartesian product of spaces called the smash product, denoted by a wedge $\wedge$ . For example, "multiplying" two circles with the Cartesian product results in a torus, $S^1\times S^1$. But if you further smash the two circles together, then you'll get a sphere. So the smash product of circles $S^1\wedge S^1$ is a sphere. Here's a nice gif from Wikipedia:

![](https://cdn.prod.website-files.com/5b1d427ae0c922e912eda447/5d878e6b9bbb8aa420ed2f8c_smash.gif)

So an analogue of the product $\times$ is the smash product $\wedge$, and the analogous adjunction $(Y\wedge-)\dashv \text{hom}(Y,-)$ is called the smash-hom adjunction . In the special case when $Y=S^1$ is the circle, the two functors $S^1\times -$ and $\text{hom}(S^1,-)$ are called the suspension and loop functors and the resulting adjunction is the suspension-loop adjunction . It appears in a nice one-line proof that the fundamental group of the circle is $\mathbb{Z}$.

## Galois Connections

The next adjunction we'll consider is called a G alois connection. This is my favorite example because it subsumes so many phenomena in mathematics. A Galois connection is, simply put, an adjunction between functors on posets.

I'll explain. First, know that every poset (partially ordered set) is a category. A poset is a set $P$ in which a partial order $\leq$ has been defined. As a category, the objects are the elements in $P$ and there is exactly one morphism $p\to p'$ whenever $p\leq p'$. In particular, there is at most one arrow between any two elements, that is, $\text{hom}(p,p')$ is always a set with either 0 or 1 elements. Using the definition of a partial order, you can verify that the axioms of a category are indeed satisfied.

A function $f\colon P\to Q$ between posets that preserves the order—meaning it satisfies $fp\leq fp'$ whenever $p\leq p'$—is called a monotone function. Crucially, a monotone function is precisely a functor when we view the posets as categories. (Below we'll be interested in a function $f$ that's order -reversing , so that $fp\geq fp'$ whenever $p\leq p'$. It's still a functor—it's just a contravariant one.)

In this general setting, an adjunction consists of opposing monotone functions $f\colon P\to Q$ and $g\colon Q\to P$ that satisfy

![](https://cdn.prod.website-files.com/5b1d427ae0c922e912eda447/5d868c4fe9eb993201f9bf3e_poset.jpg)

Lots of things you might care about are posets, so there are numerous Galois connections throughout mathematics. Here's one example I especially enjoy:

#### Formal Concept Analysis

Given a set $X$ consider the power set $2^X$, i.e. the set of all subsets of $X$. It's a poset by inclusion: $A\leq B$ if and only if $A\subseteq B\subseteq X$. So in particular, it's a category. Now here's a nice fact I like:

Any relation $R$ on $X\times Y$ defines a Galois connection.

A relation is another name for a subset $R\subseteq X\times Y$. If, for example, $X$ is a set of animals and $Y$ is a set of features, then $R$ could be the set of all pairs $(x,y)$ such that animal $x$ possesses feature $y$. Naturally, we might be interested in subsets of animals possessing certain features, and vice versa. This motivates the following two functions, $f$ and $g$:

![](https://cdn.prod.website-files.com/5b1d427ae0c922e912eda447/5d86885e9d174be6ee3707de_galois1.jpg)

These functions are order reversing (as you can check) and they satisfy the following:

![](https://cdn.prod.website-files.com/5b1d427ae0c922e912eda447/5d86897bf54e2a3d1a6629e2_iff.jpg)

Right away, you'll notice this isn't quite the adjunction condition specified above: $f$ and $g$ both appear on the right -hand side of the subset containments! No worries. This is another flavor of adjunction: $f$ and $g$ are called mutually right adjoints, and this is an example of what's sometimes called an antitone Galois connection.

As an aside, pairs of subsets $(A,B)\in 2^X\times 2^Y$ for which equality above holds—i.e. $fA=B$ and $A=gB$—have a special name: they're called formal concepts . They are the focal point of interest in formal concept analysis , a nice part of order theory dealing with hierarchy of concepts in data. For more on formal concepts and category theory, you might be interested in this blog series by Simon Willerton on the $n$-Category Café.

Galois connections arising from relations are just one example. There are many more, including:

- the connection between fields and groups in Galois theory (from which this adjunction derives is name)
- the connection between the floor function $\lfloor -\rfloor$ and the ceiling function $\lceil -\rceil$
- the connection between covering spaces and fundamental groups in topology
- the connection between polynomials and their roots in algebraic geometry
- the connection between syntax and semantics à la William Lawvere
The list goes on, and the Wikipedia entry showcases most of these examples and more.

## Data Migration

Our last example of adjunctions comes from applied category theory , namely data migration . Today's post is already quite long, so I'll try to keep this brief. A database—tables of information—can be represented by a directed graph, $G$. The columns are vertices and an edge is a relationship between columns. In the airline example below, the column of "Economy Seats" corresponds to one vertex, which is connected to "Price" since every seat has a cost associated to it.

![](https://cdn.prod.website-files.com/5b1d427ae0c922e912eda447/5d8fc76519b70ffa90d3e663_database1.jpg)

The graph keeps track of the database's "syntax." To reinstate the actual data, we need to attach meaning. We need, for example, a principled way of "imagining the leftmost vertex represents the set of economy seats." To do this, we take the free category $\mathsf{G}:=FG$ on the graph (as in the free-forgetful adjunction above!) and define a functor from that category to the category of sets. In short, a database is encoded by functor $ \mathsf{G}\to \mathsf{Set}$.

![](https://cdn.prod.website-files.com/5b1d427ae0c922e912eda447/5d8ccebb8735f7a173be9603_principled.jpg)

Now suppose we have another database, whose graph $H$ gives rise to a category $\mathsf{H}:=FH$, and suppose the two databases are related so that there is a functor  $J\colon \mathsf{H}\to\mathsf{G}$. (Perhaps one database is a more detailed version of another.) Asking for a migration of data from $G$ to $H$ amounts to asking for a functor $\mathsf{H}\to\mathsf{Set}$ given a functor $\mathsf{G}\to\mathsf{Set}$. Is it possible? Sure! Just precompose with $J$. This defines a nice way to get from the category $\mathsf{Set}^\mathsf{G}$ of databases (functors) on $G$ to the category $\mathsf{Set}^\mathsf{H}$ of databases (functors) on $H$:

![](https://cdn.prod.website-files.com/5b1d427ae0c922e912eda447/5d8fc780ab15307ecadc70f2_database2.jpg)

But can we migrate data in the other direction? Given a functor $\mathsf{H}\to \mathsf{Set}$, can we use $J$ to extend it to a functor out of $\mathsf{G}$? For this, we turn to Kan extensions —the name given to solutions to this kind of extension problem. I use plural here because there are both left and right Kan extensions . (This is a consequence of the fact that morphisms have direction: left or right.) There's a lot of rich theory behind this (you'll need to know about limits and colimits—I've written an introduction here !), but the upshot is that the two Kan extensions provide two ways to migrate data from $H$ to $G$. Moreover, they define two adjunctions :

![](https://cdn.prod.website-files.com/5b1d427ae0c922e912eda447/5d8cd47d4a878c4ca6c7c1ea_database3.jpg)

I've gone through all this rather quickly, but I think it gives a nice glimpse of applied category theory. A thorough explanation can be found in David Spivak's Category Theory for the Sciences and in the newer An Invitation to Applied Category Theory with Brendan Fong, which is also free on the arXiv as Seven Sketches in Compositionality . (See Section 3.4, "Adjunctions and Data Migration," from which I borrowed the example above.) John Baez also explains the idea nicely in his free online course on applied category theory. Do check them out!

### Notes on Applied Category Theory

### Limits and Colimits, Part 2 (Definitions)

### Group Elements, Categorically

### Language, Statistics, & Category Theory, Part 1
