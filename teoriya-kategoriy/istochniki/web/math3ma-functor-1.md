<!-- SOURCE: https://www.math3ma.com/blog/what-is-a-functor-part-1 | captured 2026-07-19 | math3ma (Tai-Danae Bradley), free blog | curl+stdlib extract -->

# math3ma — What Is A Functor Part 1 (captured)

What is a Functor? Definition and Examples, Part 1 

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

January 31, 2017 

• 
Category Theory 

#### What is a Functor? Definition and Examples, Part 1

Next up in our mini series on basic category theory: functors! We began this series by asking What is category theory, anyway?  and last week walked through the precise definition of a category  along with some examples. As we saw in example #3 in that post , a functor can be viewed an arrow/morphism between two categories. ...every sufficiently good analogy is yearning to become a functor. - John Baez 

#### What is a functor?

More precisely, a functor $F:\mathsf{C}\to\mathsf{D}$ from a category $\mathsf{C}$ to a category $\mathsf{D}$ consists of some data that satisfies certain properties. 

#### The Data

an object $F(x)$ in $\mathsf{D}$ for every object $x$ in $\mathsf{C}$ 
a morphism $F(x)\overset{F(f)}{\longrightarrow}F(y)$ in $\mathsf{D}$ for every morphism $x\overset{f}{\longrightarrow}y$ in $\mathsf{C}$ 

#### The Properties

$F$ respects composition, i.e. $F(g\circ f)=F(g)\circ F(f)$ in $\mathsf{D}$ whenever $g$ and $f$ are composable morphisms in $\mathsf{C}.$ 
$F$ sends identities to identities, i.e. $F(\text{id}_x)=\text{id}_{F(x)}$ for all objects $x$ in $\mathsf{C}.$ 

#### Example #1: a functor between groups

We noted last week that every group $G$ can be viewed as a one-object category called $\mathsf{B}G$. Suppose then that $\mathsf{B}G$ and $\mathsf{B}H$ are two such categories. What would a functor $F:\mathsf{B}G\to\mathsf{B}H$ look like? 

‍ 

To start, it must send the single object ${\color{RubineRed}\bullet}$ of $\mathsf{B}G$ to the single object ${\color{ProcessBlue}\bullet}$ of $\mathsf{B}H$. Moreover, any morphism ${\color{RubineRed}\bullet}\overset{g}{\longrightarrow} {\color{RubineRed}\bullet}$, which, you'll remember, is just a group element $g\in G$, must map to a morphism ${\color{ProcessBlue}\bullet}\overset{F(g)}{\longrightarrow} {\color{ProcessBlue}\bullet}$. That is, $F(g)$ must be an element of $H$.  The composition property requires that $F(g\circ g')=F(g)\circ F(g')$ for all group elements $g,g'\in G$. And finally, if ${\color{RubineRed}e}$ denotes the identity morphism on ${\color{RubineRed}\bullet}$ (i.e. the identity element in $G$), then we must have $F({\color{RubineRed}e})={\color{ProcessBlue}e}$ where ${\color{ProcessBlue}e}$ is the identity morphism on ${\color{ProcessBlue}\bullet}$ (i.e. the identity element in $H$).

So what's a functor $F:\mathsf{B}G\to\mathsf{B}H$? It's precisely a group homomorphism from $G$ to $H$! 

‍ 
 
‍ 
So in this example, a functor is just a   function (which happens to be compatible with the group structure). But what if the domain/codomain of a functor has more than one object in it?
  
‍ 
‍ 

#### Example #2: the fundamental group

There is a functor $\pi_1:\mathsf{Top}\to\mathsf{Group}$ that associates to every topological space* $X$ a group $\pi_1(X)$, called the fundamental group of $X$ , and which sends every continuous function $X\overset{f}{\longrightarrow}Y$ to a group homomorphism $\pi_1(X)\overset{\pi_1(f)}{\longrightarrow}\pi_1(Y)$.   

The elements of $\pi_1(X)$ are (homotopy classes of) maps of the circle into the space $X$. But don't worry if you're not familiar with the phrase "homotopy classes of." Just know that informally $\pi_1$ is a "hole-detector"--- it keeps track of the various loops in $X$ . And knowing that $\pi_1$ is functorial allows you to prove cool things like Brouwer's fixed point theorem . For instance, see the proof of Theorem 1.3.3 here .
  
Now it turns out that the fundamental group is an invariant of a topological space. In other words, if $X$ and $Y$ are homeomorphic spaces then their fundamental groups are isomorphic. (Even better, this sentence is still true if we replace "homeomorphic" by "homotopic" which is a slightly weaker notion of "sameness." ) This gives us a handy way to distinguish spaces: if $X$ and $Y$ have non isomorphic fundamental groups, then $X$ and $Y$ are guaranteed to be topologically different .

#### 
(Actually, there's nothing special about the number 1 here. For each $n\geq 1$, there is a functor $\pi_n:\mathsf{Top}\to\mathsf{Group}$ that sends $X$ to $\pi_n(X)$ which is again, informally, the group whose elements are maps of the $n$-dimensional sphere into $X$. The groups $\pi_n(X)$ for $n>1$ are called the higher homotopy groups of $X$. And when $X$ is a sphere, cool and spooky things happen.)

  In practice it can be helpful to think of a functor $F:\mathsf{C}\to\mathsf{D}$ as encoding an invariant of some sort.  

‍ 
 
‍ 
This is because if two objects $x$ and $y$ are "the same" in $\mathsf{C}$, then $F(x)$ and $F(y)$ must be "the same" in $\mathsf{D}$. By "the same," I'm referring to the precise notion of isomorphic: 

  In any category, a morphism $x\overset{f}{\longrightarrow}y$ is said to be an isomorphism if there exists a morphism $y\overset{g}{\longrightarrow}x$ so that $g\circ f=\text{id}_x$ and $f\circ g=\text{id}_y$.

Isomorphisms in $\mathsf{Set}$ are called bijections, isomorphisms in $\mathsf{Top}$ are called homeomorphisms, isomorphisms in $\mathsf{Man}$ (the category of smooth manifolds and smooth maps) are called diffeomorphisms, isomorphisms in $\mathsf{Vect}_{\mathbb{k}}$ (the category of $\mathbb{k}$-vector spaces with linear transformations) are called, well, isomorphisms, and so on.** So we can rephrase the above more formally: "If $f$ is an isomorphism between $x$ and $y$ then $F(f)$ is an isomorphism between $F(x)$ and $F(y)$." (The proof isn't tricky - it follows directly from the definitions!) 

Or, to put it simply, functors preserve isomorphisms . 
Well, I have a couple more examples of functors that I'm excited to share with you---one of them makes an appearance in a familiar equation from calculus!---but I'll save them for tomorrow . 

  Stay tuned!

*Technically, they are   pointed topological spaces, i.e.  spaces where you declare a certain point, called a basepoint , to be special/distinguished. So really, $\pi_1$ is from $\mathsf{Top}_*$ to $\mathsf{Group}$ where $\mathsf{Top}_*$ denotes the category of pointed spaces with basepoint-preserving maps as morphisms.
 
**Fun fact: Categories in which every morphism is an isomorphism are given a special name: groupoids . (Can you guess why?) Every group, then, is precisely a one-object groupoid. And yes! The fundamental groupoid of a topological space is a thing! Perhaps we'll chat about it in a future post....

Share 

 Tweet 

 Share 

Related Posts 

#### Language Modeling with Reduced Densities

July 9, 2020 

in 
Category Theory 

#### At the Interface of Algebra and Statistics

April 13, 2020 

in 
Probability 

#### Language, Statistics, & Category Theory, Part 1

June 29, 2021 

in 
Category Theory 

#### The Most Obvious Secret in Mathematics

September 12, 2016 

in 
Category Theory 
 
Leave a comment!
