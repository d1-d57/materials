<!-- SOURCE: https://www.math3ma.com/blog/group-elements-categorically | captured 2026-07-19 | math3ma (Tai-Danae Bradley), free blog | curl+stdlib extract -->

# math3ma — Group Elements Categorically (captured)

Group Elements, Categorically 

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

February 16, 2017 

• 
Category Theory 

• 
Algebra 

#### Group Elements, Categorically

 On Monday we concluded our mini-series on basic category theory  with a discussion on natural transformations and functors . This led us to make the simple observation that the elements of any set are really just functions from the single-point set {✳︎} to that set. But what if we replace "set" by "group"? Can we view group elements categorically as well? 
 The answer to that question is the topic for today's post, written by guest-author Arthur Parzygnat . Arthur is a mathematics postdoctoral fellow at the University of Connecticut, and, incidentally, was the first person to introduce me to categories as an undergraduate! 
‍ 
 
‍ 

 An element $x$ of a set $X$ can equivalently be described in terms
of a function $x:\{*\}\to X$ from any one element set into $X.$ 
Similarly, a point $x$ in a topological space $(X,\tau)$ can be described in terms
of a function $x:\{*\}\to(X,\tau)$ from the single point space into $(X,\tau).$ 
This same idea works in several categories of mathematical objects. 

#### Definition 1. Let $\mathscr{C}$ be a category with a terminal object $T$ and let $X$ be an object of $\mathscr{C}.$
A point of $X$ is a morphism $x:T\to X.$ 

‍ 
In many examples, such as the ones mentioned above, 
this produces the usual notion of a point. However, it fails with categories whose objects have additional algebraic structure
and the morphisms respect this algebraic structure. For instance, in the category of vector spaces and linear transformations, the terminal object is a $0$-dimensional vector space, which we'll denote 
by $\mathbf{0}.$ If $V$ is a real vector space, there is only a single linear transformation $\mathbf{0}\to V$ since the zero
vector must be preserved. On the other hand, linear transformations of the form $\mathbb{R}\to V$ do describe elements of $V$ (the image of the number 1). Furthermore, $\mathbb{R}$ is the monoidal unit for the tensor product of vector spaces. 

#### Definition 2. Let $(\mathscr{C},\otimes,I)$ be a monoidal category (the other data are not explicitly written here) with monoidal unit $I.$ Let $X$ be an object of $\mathscr{C}.$ A point of $X$ is a morphism $x:I\to X.$ 

With this definition and an appropriate choice of monoidal structure, all the examples from above describe elements in the usual sense. Unfortunately, this still does not describe elements in all
categories with algebraic structure. For example, in the category of
groups, the terminal object and the monoidal unit for the direct
product of groups are both the group $\{e\}$ with a single element, the identity. For any group $G,$ there is only a single morphism $\{e\}\to G$ sending the identity to the identity. Although group elements in $G$ can be described by a morphism $\mathbb{Z}\to G,$ $\mathbb{Z}$ is not a terminal object, nor is it a unit
for the monoidal structure. There are a few possible ways to proceed. 
 
Find an appropriate monoidal structure on groups 
where $\mathbb{Z}$ plays the role of a unit. 
Generalize our definition of a point even further. 
Change the way we think about the totality of groups. 

  I have no idea how to do the first and if it's even possible. 
One possibility for the second option is known as the ``functor of points'' perspective, though we prefer another option. 
The third option is not only possible, but it offers an interesting perspective to  how group elements are different from other types of elements.  First note that every group can be viewed as a category with a single object. Normally, we think of the totality of groups as an ordinary category. However, viewing a group as a one object category, the totality of groups becomes a 2-category since the totality of categories has a canonical structure of a 2-category. 
Morphisms are functors, and the data of such a functor
is equivalent to the data of a group homomorphism. A natural transformation

consists of a single element $h\in H$ satisfying
$$
h\varphi(g)=\psi(g)h\qquad\forall\;g\in G.
$$
In other words, the homomorphisms $\psi$ and $\varphi$ are conjugate
by some element $h\in H.$ Composition of natural transformations 
corresponds to group multiplication.  

In particular, all natural transformations between groups are invertible. Hence, the set of all natural transformations from a group
homomorphism to itself forms a group. (Can you guess which subgroup it is?) Of course, unless you've specifically chosen your group homomorphisms, it's probably not likely that there exists a natural transformation between them. But, in some special cases, there are many such natural transformations. In fact, the group of all natural transformations  

‍ 

is canonically isomorphic to $G$ itself. Here $!:\{e\}\to G$ is the unique group homomorphism from the single element group to $G.$ 
Therefore, group elements are more appropriately associated with ``processes'' instead of static ``elements,'' which is appropriate anyway because we think of groups as symmetries of other mathematical objects. More precisely, we can make the following definition. 
‍ 

#### Definition 3. Let $\mathscr{C}$ be a 2-category with a terminal object $T.$ Let $C$ be an object of $\mathscr{C}$ and 
let $X:T\to C$ and $Y:T\to C$ be elements in $C.$ A process $f$ from $X$ to $Y$ in $C$ is a 2-morphism in $\mathscr{C}$ of the form 

#### Example 1

Let $\mathscr{C}$ be the 2-category of groups viewed as one-object categories. Then $T=\{e\}$ is a single element group. 
Set $C:=G$ to be any group $G.$ Set $X:=\;!$ and $Y:=\;!$ to be the unique group homomorphisms from $\{e\}$ to $G.$ Finally, set $f:=g$ to be any element $g$ of $G.$  This shows that a group element is an example of a process. 

#### Example 2

Let $\mathscr{C}$ be the 2-category of categories. 
Then $T$ is a 2-category with a single object, a single 1-morphism, and a single 2-morphism. Let $C$ be a category (such as the category of sets). Let $X$ and $Y$ be objects of $C$ (such as two sets). 
Let $f:X\to Y$ be a morphism in $C$ (a function in the case of sets).
Then this is an example of a process, consistent with our usual notion of a process as a morphism between two objects in a category. If we wanted to, we could also replace the 2-category $\mathscr{C}$ and terminal object $T$ in the definition of a process by a monoidal 2-category with a unit in a similar fashion to what was done to include vector spaces in the discussion of elements. I encourage you to come up with other examples in this case. 

Share 

 Tweet 

 Share 

Related Posts 

#### The Yoneda Embedding

September 6, 2017 

in 
Category Theory 

#### Announcing Applied Category Theory 2019

January 5, 2019 

in 
Category Theory 

#### The Fibonacci Sequence as a Functor

December 14, 2020 

in 
Category Theory 

#### "One-Line" Proof: Fundamental Group of the Circle

April 24, 2017 

in 
Topology 
 
Leave a comment!
