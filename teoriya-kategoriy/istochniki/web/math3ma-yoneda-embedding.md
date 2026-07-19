<!-- SOURCE: https://www.math3ma.com/blog/the-yoneda-embedding | captured 2026-07-19 | math3ma (Tai-Danae Bradley), free blog | curl+stdlib extract -->

# math3ma — The Yoneda Embedding (captured)

The Yoneda Embedding 

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

September 6, 2017 

• 
Category Theory 

#### The Yoneda Embedding

 Last week  we began a discussion about the Yoneda lemma. Though rather than stating the lemma (sans motivation) ,  we took a leisurely stroll through an implication of its corollaries - the Yoneda perspective, as we called it : An object is completely determined by its relationships to other objects, 
i.e. by what the object "looks like" from the vantage point of each object in the category. 
But this left us wondering,  What are the mathematics behind this idea?   And what are the actual corollaries?  In this post, we'll work to discover the answers. To begin, let's put concrete math behind these three abstract expressions: 
"...a relationship  between two objects..." 
"...the vantage point of   each object in a category..." 
"...an object is completely characterized by..." 
We'll unwind the expressions one by one. In what follows, let $\mathsf{Set}$ denote the category of sets and let $\mathsf{C}$ be any category. 
‍ 
 
‍ 

#### A "relationship between two objects" is a morphism.

Let's say that two objects $X$ and $Y$ in $\mathsf{C}$ share a relationship if there is a morphism between them. For example, if $X$ is a topological space with the discrete topology , there are lots of relationships - lots continuous functions - from $X$ to $Y$ for any space $Y$. In fact, all maps out of a discrete space are continuous. 
 
On the other hand, there are very few relationships between objects in the category of fields - there are no field homomorphisms between fields of different characteristics! 
‍ 
 
‍ 

#### "...the vantage point of each object..."   is encoded by a functor

To analyze an object $X$ "from the vantage point of all objects in $\mathsf{C}$," we need a way to keep track of the network of relationships that $X$ shares with all objects in $\mathsf{C}$. This "network" is precisely the set of all morphisms both to and from $X$, i.e. the sets $$
\text{hom}(Z,X)\qquad\text{and}\qquad\text{hom}(X,Z)\qquad\text{for all $Z$ in $\mathsf{C}$.}
$$ Notice that we want a different set for each $Z$ in $\mathsf{C}$. An efficient way to handle this is via the contravariant functor $\text{hom}(-,X):\mathsf{C}^{op}\to\mathsf{Set}$ that sends $Z$ to the set $\text{hom}(Z,X)$ and a morphism $f:Z\to W$ to its pullback $f^*$ defined by precomposing with $f$. Likewise, the sets $\text{hom}(X,Z)$ for all $Z$ in $\mathsf{C}$ lie in the image of the (covariant) functor $\text{hom}(X,-)\colon \mathsf{C}\to\mathsf{Set}$.

#### "...an object is 'completely determined by'..." means you know it up to isomorphism.

To say "an object $X$ is completely determined by ..." means that $X$ is— up to isomorphism —the only object characterized by whatever comes after the ellipsis. In the first paragraph of this post, it was "...their relationships to other objects." (Though typically, a universal property follows the ellipsis. This is no surprise. In light of the Yoneda Perspective the two addendums go hand in hand!) The upshot is that if $Y$ relates to all other objects in$\mathsf{C}$ in the same way that $X$ does—that is, if $Y$ looks just like $X$ from the vantage point of the full category—then $X$ and $Y$ must be isomorphic.
 
For example, suppose $X$ and $Y$ are topological spaces and let $\bullet$ denote the one-point space and $I$ and $S^1$ the unit interval and the circle. Then,

$X$ and $Y$ have the same cardinality if and only if $\text{hom}(\bullet,X)\cong\text{hom}(\bullet,Y)$. 
 $X$ and $Y$ have the same path space if and only if $\text{hom}(I,X)\cong\text{hom}(I,Y)$. 
 $X$ and $Y$ have the same (free) loop space if and only if $\text{hom}(S^1,X)\cong\text{hom}(S^1,Y)$. 
 
The last two bullets hold by definition of path and loop space. (They are, respectively, the space of all continuous functions from $I$ and $S^1$ to $X$.) The first bullet holds simply because a map $\bullet\to X$ is the same as a choice of point in $X$. We might even say that $\bullet\to X$ is  a "$\bullet$-shaped element" of $X$. Similarly, a path $I\to X$ can be thought of as an "$I$-shaped element" of $X$, while a loop $S^1\to X$ is an "$S^1$-shaped element." Essentially we're using $\bullet$, $I$ and $S^1$ to probe $X$ and $Y$. And to obtain a complete picture, we must probe them with—i.e. view the from the vantage point of— all spaces. 
 
With the mathematics in place, the slogan "an object $X$ is completely determined by its relationships to other objects" now crystallizes into two points: 

#### point #1. Everything we need to know about Xis encoded in hom(--, X). In effect, the object X represents   the functor hom(--, X).

‍ 

#### point #2.  X and Y are isomorphic if and only if their represented functors hom(--,X) and hom(--,Y) are isomorphic.
‍

Let's think about point #1 now and revisit point #2 next time. So look at point #1 again. Can we really identify an object with a functor ? There's clearly an assignment
$$ X\mapsto \text{hom}(-,X)$$ since any object $X$ in the category $\mathsf{C}$ gives rise to a functor $\text{hom}(-,X)$ in... well... in what? Where does $\text{hom}(-,X)$ live? It, too, lives in a category! As we mentioned long ago , there is a category $\mathsf{Set}^{\mathsf{C}^{op}}$ whose objects are functors $\mathsf{C}^{op}\to\mathsf{Set}$  and whose morphisms are natural transformations. Therefore (and you should verify this) there is a functor $\mathscr{Y}\colon\mathsf{C}\to \mathsf{Set}^{\mathsf{C}^{op}}$ that sends an object $X$ to $\text{hom}(-,X)$ and a morphism $f\colon X\to Y$ to the natural transformation $f_*\colon \text{hom}(-,X)\to \text{hom}(-,Y)$. Each component of this natural transformation is given by postcomposing with $f$. Functors in thecategory $\mathsf{Set}^{\mathsf{C}^{op}}$ are called presheaves, and the presheaves we're interested in—i.e. those of the form $\text{hom}(-,X)$—are called representable functors . But we need to justify this nomenclature. Does $X$ truly, faithfully, and to the fullest extent represent the functor $\text{hom}(-,X)$?
 
The answer is "yes" under one condition: as $\mathscr{Y}$ sends $X$  to the presheaf category, it should preserve relationships that $X$ shares with objects in $\mathsf{C}$. In other words, for each relationship between $X$ and $Y$, there should exist exactly one relationship (natural transformation) between $\text{hom}(-,X)$ and $\text{hom}(-,Y)$. More formally, for every pair $X,Y$ in $\mathsf{C}$, the function $$\text{hom}(X,Y)\to\mathsf{Nat}(\text{hom}(-,X),\text{hom}(-,Y))$$ defined by $f\mapsto f_*$ should be a bijection. (The notation $\mathsf{Nat}(-,-)$ means the set of natural transformations from [blank] to [blank].) If $\mathscr{Y}$ satisfies this condition, then it is called fully faithful * and is said to embed the category $\mathsf{C}$ into $\mathsf{Set}^{\mathsf{C}^{op}}$.   

But the question remains—is it true? Is the function
$$\text{hom}(X,Y)\to\mathsf{Nat}(\text{hom}(-,X),\text{hom}(-,Y))$$ that sends $f$ to $f_*$ a bijection? Injectivity is clear: if $f,g\colon X\to Y$ are distinct morphisms, then their pushforwards $f_*$ and $g_*$ are distinct. But what about surjectivity? Given any natural transformation $\eta\colon\text{hom}(-,X)\to\text{hom}(-,Y)$, is there a morphism $f\colon X\to Y$ so that $\eta=f_*$? That is,

#### does every natural transformation between representable functors arise from a morphism between their representing objects?

‍ 
There could be tons of natural transformations $\text{hom}(-,X)$ and $\text{hom}(-,Y)$! And there's no good reason to expect any of them should come from a morphism $X\to Y$. 
 Except there is . 
Because the answer is yes! 

#### YES!

‍
For every natural transformation $\eta\colon \text{hom}(-,X)\to\text{hom}(-,Y)$ there is exactly one morphism $f\colon X\to Y$ such that $\eta=f_*$.

And THIS is an immediate consequences of the Yoneda lemma.
 
The result is that $\mathscr{Y}$ fully and faithfully embeds $\mathsf{C}$ into $\mathsf{Set}^{\mathsf{C}^{op}}$. (This is the formal way of phrasing "point #1" above.) And for this reason, $\mathscr{Y}$ is called the Yoneda embedding. 
But this—the fact that morphisms $X\to Y$ are in bijection with natural transformations $\text{hom}(-,X)\to\text{hom}(-,Y)$—is merely a consequence of the Yoneda lemma. As we'll see next week , it says something much stronger! It tells us something about natural transformations $\text{hom}(-,X)\to F$ for any functor $F:\mathsf{C}^{op}\to\mathsf{Set}$. 
 
*More generally, given any functor $F:\mathsf{C}\to\mathsf{D}$, there is a function $\text{hom}_{\mathsf{C}}(X,Y)\to\text{hom}_{\mathsf{D}}(F(X),F(Y))$ given by $f\mapsto F(f)$. If this map is an injection, $F$ is called faithful , if it is a surjection, $F$ is called full , and if it is a bijection, $F$ is called fully faithful. And here's a handy chart for naming other types functors. 
 
‍ 
 In this series: 

Share 

 Tweet 

 Share 

Related Posts 

#### "One-Line" Proof: Fundamental Group of the Circle

April 24, 2017 

in 
Topology 

#### Language, Statistics, & Category Theory, Part 1

June 29, 2021 

in 
Category Theory 

#### What is a Category? Definition and Examples

January 23, 2017 

in 
Category Theory 

#### At the Interface of Algebra and Statistics

April 13, 2020 

in 
Probability 
 
Leave a comment!
