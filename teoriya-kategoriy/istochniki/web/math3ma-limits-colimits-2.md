<!-- SOURCE: https://www.math3ma.com/blog/limits-and-colimits-part-2 | captured 2026-07-19 | math3ma (Tai-Danae Bradley), free blog | curl+stdlib extract -->

# math3ma — Limits And Colimits Part 2 (captured)

Limits and Colimits, Part 2 (Definitions) 

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

January 30, 2018 

• 
Category Theory 

#### Limits and Colimits, Part 2 (Definitions)

Welcome back to our mini-series on categorical limits and colimits! In Part 1 we gave an intuitive answer to the question, "What are limits and colimits?" As we saw then, there are two main ways that mathematicians construct new objects from a collection of given objects: 1) take a "sub-collection," contingent on some condition or 2) "glue" things together. The first construction is usually a limit, the second is usually  a colimit. Of course, this might've left the reader wondering, "Okay... but what are we taking the (co)limit of ?" The answer? A diagram . And  as we saw a couple of weeks ago, a diagram is really a functor. 
We are now ready to give the formal definitions (along with more intuition). First, here's a bit of setup. 

#### The Setup

 In what follows, let $\mathsf{C}$ denote any category and let $\mathsf{I}$ be an indexing category . Note that given any object $X$ in $\mathsf{C}$, there is a constant functor - let's also call it $X$ - from $\mathsf{I}$ to $\mathsf{C}$. This functor sends every object to $X$ and every morphism to the identity of $X$.

 Therefore , given any functor (ahem, diagram ) $F:\mathsf{I}\to\mathsf{C}$, we can make sense of a natural transformation  between $X$ and $F$. Such a natural transformation consists of a collection of morphisms between $X$ and the objects in the diagram $F$. Moreover, these morphisms must commute  with all the morphisms that appear in diagram. If the arrows point from  $X$ to  the diagram $F$, then the setup is called a cone over $F$, as we previously discussed here . If, on the other hand, the arrows point from  the diagram $F$ to  $X$, then it's called a cone under $F$ (or sometimes a cocone ).

 Notice that a cone is comprised of two things: an object  AND a collection of arrows to or from it. Now here's the punchline: 

#### The limit of a diagram $F$ is a special cone over $F$.

#### The colimit of $F$ is a special cone under $F$.

Let's take a look at the formal definitions. I'll give a lite version first, followed by the full version.

#### Definitions (Lite Version)

‍ 

#### Definition (limit): The limit of a diagram $F$ is the "shallowest" cone over $F$.

By  "shallowest" (not a technical term) I mean in the sense of the picture to the right. There may be many cones -- many objects with maps pointing down to the diagram $F$ (depicted as a blob) -- over $F$, but the limit is the cone that is as close as possible to the diagram $F$. Perhaps this is why "limit" is a good choice of terminology. You might imagine all the cones over $F$ as cascading down to the limit .            
 
If we let gravity pull all the arrows down, then we obtain the dual notion: a colimit. 

#### Definition (colimit): The colimit of a diagram $F$ is the "shallowest" cone under $F$.

Again, by "shallowest" (not a technical term) I mean in the sense of the picture on the left. There may be many cones under $F$, but the colimit is the one that's closest to the diagram. It's the shallowest. 
Okay, this is all very handwavy and not very informative. To capture the mathematics behind "shallowest," we'll use a universal property. I'll comment on intuition below. 

#### Definition: Limit (Full Version)

The definitions themselves can be stated very succinctly. But like  little onions, they have several layers, which we will peel away slowly to minimize the shedding of tears. 
 
 Definition (1): The limit of a diagram $F:\mathsf{I}\to\mathsf{C}$ is the universal cone over $F$.
 
 Let's unwind this a bit...

 Definition (2): The limit of a diagram $F:\mathsf{I}\to\mathsf{C}$ is an object  $\text{lim }F$ in $\mathsf{C}$ together with a natural transformation $\eta:\text{lim }F\Rightarrow F$ with the following property: for any  object $X$ and for any  natural transformation $\alpha\colon X\Rightarrow F$, there is a unique morphism $f\colon X\to \text{lim }F$ such that $\alpha=\eta\circ f$. 
 
 Let's unwind this a bit more... 
 Definition (3):  The  limit  of a diagram $F:\mathsf{I}\to\mathsf{C}$ is an object  $\text{lim }F$ in $\mathsf{C}$ together with morphisms $\eta_A:\text{lim }F\to A$, for each $A$ in the diagram, satisfying $\eta_B=\phi_{AB}\circ \eta_A$ for every morphism $\phi_{AB}\colon A\to B$ in the diagram. Morever, these maps have the following property: for any object $X$ and for any collection of morphisms $\alpha_A:X\to A$ satisfying $\alpha_B=\phi_{AB}\circ \alpha_A$, there exists a unique morphism $f\colon X\to\text{lim }F$ such that $$\alpha_A=\eta_A\circ f \qquad\text{for all objects $A$ in the diagram.}$$  
 
In summary, for all objects $X$ in $\mathsf{C}$: 

‍ 

#### Definition: Colimit (Full Version)

 Definition (1) : The colimit of a diagram $F:\mathsf{I}\to\mathsf{C}$ the universal cone under $F$.      
 Let's unwind this a bit...

 Definition (2): The colimit of a diagram $F:\mathsf{I}\to\mathsf{C}$ is an object  $\text{colim }F$ in $\mathsf{C}$ together with a natural transformation $\epsilon:F\Rightarrow \text{colim }F$ with the following property: for any  object $X$ and for any  natural transformation $\beta\colon F\Rightarrow X$, there is a unique morphism $g\colon \text{colim }F\to X$ such that $\beta= g\circ \epsilon$. 

  Let's unwind this a bit more... 
 
 Definition (3):  The  colimit  of a diagram $F:\mathsf{I}\to\mathsf{C}$ is an object  $\text{colim }F$ in $\mathsf{C}$ together with morphisms $\epsilon_A:A\to\text{colim }F$, for each $A$ in the diagram, satisfying $\epsilon_A=\epsilon_B\circ \phi_{AB}$ for every morphism $\phi_{AB}\colon A\to B$ in the diagram. Morever, these maps have the following property: for any object $X$ and for any collection of morphisms $\beta_A: A\to X$ satisfying $\beta_A=\beta_B\circ \phi_{AB}$, there exists a unique morphism $g\colon \text{colim }F\to X$ such that $$\beta_A= g \circ \epsilon_A\qquad\text{for all objects $A$ in the diagram.}$$ 

In summary, for all objects $X$ in $\mathsf{C}$: 

#### a little intuition  +   a little exercise

 I once heard (or read?) Eugenia Cheng  refer to a universal property as a way to describe a special role  than an object—or in our case, a cone—plays. I like that analogy, and it's exactly what's going on with limits. (Similar sentiments hold for colimits.) Let me elaborate:

Out of all the cones over a diagram $F$, there is exactly one  that plays the role of limit, namely the pair $(\text{lim}F,\eta)$. Of course  you might  come across another cone $(X,\alpha)$ that plays a very  similar role. Perhaps $\alpha$ behaves very similarly to $\eta.$ BUT -- and this is the punchline -- this behavior is no coincidence! The natural transformation $\alpha$ "behaves" like $\eta$ because  it is built up from $\eta$! More precisely, it has $\eta$ as a factor: $\alpha=\eta\circ f$ for some unique morphism $f$!
 
By way of analogy, think of the role that the number 2 plays among the integers. Out of all the integers, we might say that 2 is the quintessential candidate for "an integer which possesses the quality  of 'two-ness,'" that is, of being even. Of course there are other integers $a$ that play a similar role. In particular, if $a$ is an even integer, then it also possesses the quality of "two-ness." But this is no coinicidence! An even integer is even because  it is built up from 2! More precisely, it has 2 as a factor: $a=2k$, for some unique integer $k$! 
 
 These two equations $a=2k$ and $\alpha=\eta\circ f$ are analogous. In fact, they're more than analogous....

‍ 

#### EXERCISE

Let $\mathsf{C}$ be the category $2\mathbb{Z}$ of even integers. A morphism $n\to m$ in this category is an integer $k$ such that $n=mk$. For example, 3 defines an arrow $6\overset{3}{\longrightarrow} 2$ because $6=2\times 3$. On the other hand, there is no arrow $8\longrightarrow 6$.  Show that $2$ is the limit of a particular diagram in $2\mathbb{Z}$.   
That is, come up with an indexing category $\mathsf{I}$ and a functor $\mathsf{I}\to2\mathbb{Z}$  
 (Next question: does this diagram have a colimit? If so, what is it?) 

‍ 
I'll close with one final thought. Once we get used to the ideas/definitions above, we discover that limits and colimits have very familiar names, depending on the shape of the indexing category $\mathsf{I}$!            
 
In the next two posts, I'll justify some of these claims by giving explicit examples of limits and colimts in the category $\mathsf{Set}$. 
 
Until then!      
 
 In this series: 

Share 

 Tweet 

 Share 

Related Posts 

#### Warming Up to Enriched Category Theory, Part 1

June 8, 2021 

in 
Category Theory 

#### The Fibonacci Sequence as a Functor

December 14, 2020 

in 
Category Theory 

#### Notes on Applied Category Theory

September 18, 2018 

in 
Category Theory 

#### A Diagram is a Functor

January 10, 2018 

in 
Category Theory 
 
Leave a comment!
