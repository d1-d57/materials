<!-- SOURCE: https://www.math3ma.com/blog/what-is-a-natural-transformation | captured 2026-07-19 | math3ma (Tai-Danae Bradley), free blog | curl+stdlib extract -->

# math3ma — What Is A Natural Transformation (captured)

What is a Natural Transformation? Definition and Examples 

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

February 7, 2017 

• 
Category Theory 

#### What is a Natural Transformation? Definition and Examples

I hope you have enjoyed our little series on basic category theory. (I know I have!) This week we'll close out by chatting about natural transformations which are, in short, a nice way of moving from one functor to another. If you're new to this mini-series, be sure to check out the very first post,  What is Category Theory Anyway?  as well as What is a Category?  and last week's What is a Functor? ...the notion of category is best excused as that which is necessary in order to have the notion of functor. But the progression does not stop here. There are maps between functors, and they are called natural transformations. And it was in order to define these that Eilenberg and Mac Lane first defined functors. - Peter J. Freyd 
‍ 

#### What is a natural transformation?

Here's the formal definition. Given two functors $F$ and $G$, both from a category $\mathsf{C}$ to a category $\mathsf{D}$, a natural transformation $\eta:F\Longrightarrow G$ from $F$ to $G$ consists of some data that satisfies a certain property. 

#### The Data

a morphism $F(x)\overset{\eta_x}{\longrightarrow}G(x)$ for each object $x$ in $\mathsf{C}$ 

#### The Property

Whenever $x\overset{f}{\longrightarrow}y$ is a morphism in $\mathsf{C}$, $$G(f)\circ \eta_x=\eta_y\circ F(f).$$ In other words, the square below commutes.   
 
Notice that the natural transformation $\eta$ is the totality of  all  the morphisms $\eta_x$, so sometimes you might see the notation $$\eta=(\eta_x)_{x\in\mathsf{C}},$$ where each $\eta_x$ is referred to as a  component  of $\eta$. This is very similar to how a sequence $s$ is comprised of the totality of its terms $s=\{s_n\}_{n\in\mathbb{N}}$ or how a vector $\vec{v}$ is comprised of all of its components $\vec{v}=(v_1,v_2,\ldots).$ 
Simply put, a natural transformation is a collection of maps from one diagram to another. And these maps are special in that they commute with the arrows in the diagrams. For example, in the picture below, the black arrows below comprise a natural transformation between two functors* $F$ and $G$. 

‍ 
 
‍ 
or, cleaning things up a bit, 
‍ 

where each of the three rectangular faces in the prism is a commuting square that shows up in "The Property" above. To get a better feel for natural transformations, let's look at a few special cases. 
‍ 

#### Case #1: F and G are constant

Suppose $F,G:\mathsf{C}\to\mathsf{D}$ are both constant functors. That is, suppose $F$ sends every object in $\mathsf{C}$ to a single object $d$ in $\mathsf{D}$ and every morphism to $\text{id}_{d}$. Similarly suppose $G$ sends every object and morphism to a fixed $d'$ and $\text{id}_{d'}$ in $\mathsf{D}$. Then a natural transformation from $F$ to $G$ is simply a morphism $d\overset{\eta}{\longrightarrow} d'$. 

#### Case #2: F is constant

Now if $F$ is constant at some object $d$ in $\mathsf{D}$, and $G$ is any functor, then $\eta:F\Longrightarrow G$ consists of maps $d\overset{\eta_x}{\longrightarrow} G(x)$, one for each $x$ in $\mathsf{C}$, satisfying the equation $\eta_y=G(f)\circ\eta_x$ whenever $x\overset{f}{\longrightarrow}y$ is a morphism in $\mathsf{C}$. I've drawn a picture on the right, where for simplicity I've used the color ${\color{Magenta}\text{pink}}$ for the object $G(x)$, and {\color{Green}\text{green}} for the object $G(y)$ and so on. (So the vertices and edges of the bottom square represent the diagram given by $G$.) The equation $\eta_y=G(f)\circ\eta_x$ says that the three arrows that make up the each of the triangular sides of the tetrahedron must commute . So, for instance, traveling down $\eta_{\color{Magenta}\bullet}$ and then going across ${\color{Magenta}\bullet}\to {\color{Green}\bullet}$ is the same as traveling down $\eta_{\color{Green}\bullet}$. 
For good reasons, $\eta$ in this case is called a cone over $G$. 
‍ 

#### Case #3: G is constant

If, on the other hand, $G$ is constant at $d$ in $\mathsf{D}$ while $F$ is arbitrary, then a natural transformation consists of a collection of maps $F(x)\overset{\eta_x}{\longrightarrow} d$ so that $\eta_y\circ F(f)=\eta_x$ whenever $x\overset{f}{\longrightarrow}y$ is a morphism in $\mathsf{C}$. In other words, each of the triangular faces in the picture on the left, for example, must commute. As you can see, the scenario in case #3 is the same as that in case #2, but now the direction of the arrows $\eta_x$ have flipped. Not surprisingly, this type of $\eta$ is called a cone under $F$ (or sometimes a cocone ). 
‍ 
 You've no doubt come across a (co)limit or two, though perhaps without knowing it. The empty set, the one point set, the intersection, union, and product of sets, the kernel of a group, the quotient of a topological space, the direct sum of vector spaces, the free product of groups, the pullback of a fiber bundle, inverse limits and direct limits are all examples of either a limit or a colimit. Each is special in that it forms a "universal" cone over a particular functor/diagram! 

 This deserves much more than a few sentences of attention, so we'll  chat about more (co)limits in a future post.

#### Case 4: each $\eta_x$ is an isomorphism

Suppose now that $F$ and $G$ are any functors from $\mathsf{C}$ to $\mathsf{D}$, and let $x\overset{f}{\longrightarrow}y$ be any morphism in $\mathsf{C}$. In the case when each component $F(x)\overset{\eta_x}{\longrightarrow} G(x)$ of $\eta$ is an isomorphism , the naturality condition $\eta_y\circ F(f)=G(f)\circ \eta_x$ is equivalent to  $F(f)=\eta_y^{-1}\circ G(f)\circ\eta_x$ since $\eta_y$ is invertible.

‍ 
 
‍ 
I've made the objects gray so that we can focus more on the arrows. In fact, let's clean up the diagram on the right even more: 

So when each $\eta_x$ is an isomorphism, the naturality condition is a bit like a conjugation! It's also reminiscent of a homotopy from $G$ to $F$. Both viewpoints suggest that when each $\eta_x$ is an isomorphism, $F$ and $G$ are really the same functor up to a change in perspective . When this is the case, the natural transformation $\eta$ is called a natural isomorphism , and $F$ and $G$ are said to be naturally isomorphic. 
‍ 

#### Example #1: group actions & equivariant maps

We've mentioned previously that every group $G$ can be viewed as a category $\mathsf{B}G$ with one object $\bullet$ and a morphism $\bullet\overset{g}{\longrightarrow}\bullet$ for each group element $g$. On this category, we can define a functor $\mathsf{B}G\to\mathsf{Set}$ that sends the one object $\bullet$ in $\mathsf{B}G$ to exactly one set, call it $X$, and that sends a group element $g$ to a function $g\cdot-:X\to X$ given by $x\mapsto g\cdot x$. The functoriality conditions actually determine a left action of $G$ on $X$! (Check this!) In other words, every functor $\mathsf{B}G\to\mathsf{Set}$ encodes a group action, and the image of the single object under this functor is a $G$-set.

So what's a natural transformation in this setup? Suppose $A,B:\mathsf{B}G\to\mathsf{Set}$ are two functors with $A(\bullet)=X$ and $B(\bullet)=Y$ and let $\bullet\overset{g}{\longrightarrow}\bullet$ be a group element in $G$. Then $\eta:A\Longrightarrow B$ consists of exactly one function $\eta:X\to Y$ that satisfies $\eta(g(x))=g(\eta(x))$ for every $x\in X$.

This equality follows from the commuting square below. As with all such diagrams, simply pick an element in one of the corners (here, I've picked a little blue $x\in X$, top-left) and chase it around. Notice, the two horizontal maps are exactly the same $X\overset{\eta}{\longrightarrow}Y$, despite the fact that they're drawn in two different locations on the screen.

In words, the naturality condition says that for any point $x$ in $X$, first "translating" $x$ by $g\in G$ to the point $gx$ and then sending it to $Y$ via $\eta$ is the same as first sending $x$ to $Y$ via $\eta$ and then translating that point by $g$. In short, natural transformations are $G$-equivariant maps! 

  I have a few more more examples to share, but I'll save them until next time . Check back in a few days!

‍ 
*Here, I'm imagining $F$ and $G$ to be functors from a little, indexing category 

into some other category (pick your favorite). 

Share 

 Tweet 

 Share 

Related Posts 

#### What is a Functor? Definition and Examples, Part 1

January 31, 2017 

in 
Category Theory 

#### Naming Functors

July 31, 2017 

in 
Category Theory 

#### What is an Adjunction? Part 3 (Examples)

September 26, 2019 

in 
Category Theory 

#### Limits and Colimits, Part 1 (Introduction)

January 2, 2018 

in 
Category Theory 
 
Leave a comment!
