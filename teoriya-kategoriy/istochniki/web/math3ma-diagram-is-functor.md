<!-- SOURCE: https://www.math3ma.com/blog/a-diagram-is-a-functor | captured 2026-07-19 | math3ma (Tai-Danae Bradley), free blog | curl+stdlib extract -->

# math3ma — A Diagram Is A Functor (captured)

A Diagram is a Functor 

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

January 10, 2018 

• 
Category Theory 

#### A Diagram is a Functor

 Last week  was the start of a mini-series on limits and colimits in category theory . We began by answering a few basic questions, including, "What ARE (co)limits?" In short, they are a way to construct new mathematical objects from old ones. For more on this non-technical answer, be sure to check out Limits and Colimits, Part 1 . Towards the end of that post, I mentioned that (co)limits aren't really related to limits of sequences  in topology and analysis (but see here ). There is, however, one similarity. In analysis, we ask for the limit of  a sequence. In category theory, we also ask for the (co)limit OF   something. But if that "something" is not a sequence, then what is it? 
Answer: a diagram. 
We've talked about diagrams before: for a quick refresher,  check out this post . Today I'd like to give you a different way to think about diagrams - namely, as functors!  In other words, I hope to convince you that 

#### a diagram is a functor . 

Once we adopt this viewpoint, we'll be ready to look at the formal definition of limits and colimits. Now, how can we view diagrams as functors? Suppose $F:\mathsf{I}\to\mathsf{C}$ is a functor between categories $\mathsf{I}$ and $\mathsf{C}$. We'll call $\mathsf{I}$ an indexing category , and for the sake of illustration let's suppose it's a simple one: 

I've labeled the objects in $\mathsf{I}$ with colors and there is an identity arrow for each object, though I haven't drawn them. Let's also suppose that the horizontal arrow arrow is the composition of the two diagonal arrows.
 
So what's a functor $F$ out of this category? 
It's simply a choice of three objects and three arrows in $\mathsf{C}$.

Here $F({\color{Magenta}\bullet})=A$ and $F({\color{RoyalBlue}\bullet})=B$  and $F({\color{Green}\bullet})=C$, and the image of the three arrows in $\mathsf{I}$ are the arrows $f,g$ and $h$ in $\mathsf{C}$ where $f=h\circ g$. So you see? That's all there is to it! The image of $F$ is no more and no less than a diagram in $\mathsf{C}$. We might even call it an "$\mathsf{I}$-shaped diagram" since different shapes for $\mathsf{I}$ lend to different shapes of diagrams. For example,

In short, a diagram is a functor. 

‍ 

#### By the way...

This idea of identifying a  map  with its  image  is nothing new. After all, a  sequence  of real numbers is technically a function $x:\mathbb{N}\to\mathbb{R}$, though we usually write $x_n$ for the image $x(n)$ and think of the sequence as the collection $\{x_n\}_{n\in\mathbb{N}}$ rather than the function $x$ itself.           
 
Likewise the formal definition of a path in a topological space $X$ is: "a continuous function from the closed unit interval into $X$," i.e. $p:[0,1]\to X$. But when we think about paths, we often have the image $p(I)\subset X$ of $p$ in mind. 
 
‍ 
And in differential geometry, a vector field on a differentiable manifold $M$ is a section of the tangent bundle, i.e. a map $\phi$ from $M$ into its tangent bundle $TM$ such that the composition of $\phi$ with the projection $TM\to M$ is the identity on $M$. Of course that was a mouthful, and so we often just think of a vector field as a collection of tangent vectors - one attached to each point on the manifold. That is, we identify $\phi$ with its image.

These examples are all similar to the statement, "a diagram is a functor."              
 
‍ 
 
‍ 

#### Back to (co)limits...

Now that we can view diagrams as functors, we can make sense of maps between diagramas , i.e. natural transformations between functors. As we'll see next time, the (co)limit of a diagram $F$ is a particular natural transformation between $F$ and another diagram of  a particular shape. What's neat is that if $F$ is shaped like one of those diagrams drawn in the table above, then the (co)limit is given a familiar name, like intersection, union, Cartesian product, kernel, direct sum, and quotient! 

We'll explore all the details in the coming weeks.

Share 

 Tweet 

 Share 

Related Posts 

#### What is a Natural Transformation? Definition and Examples

February 7, 2017 

in 
Category Theory 

#### Language, Statistics, & Category Theory, Part 3

July 28, 2021 

in 
Category Theory 

#### Commutative Diagrams Explained

July 5, 2017 

in 
Other 

#### What is a Good Quantum Encoding? Part 1

July 1, 2025 

in 
Physics 
 
Leave a comment!
