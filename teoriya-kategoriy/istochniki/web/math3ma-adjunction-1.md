<!-- SOURCE: https://www.math3ma.com/blog/what-is-an-adjunction-part-1 | captured 2026-07-19 | math3ma (Tai-Danae Bradley), free blog | curl+stdlib extract -->

# math3ma — What Is An Adjunction Part 1 (captured)

What is an Adjunction? Part 1 (Motivation) 

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

September 19, 2019 

• 
Category Theory 

#### What is an Adjunction? Part 1 (Motivation)

 Some time ago, I started a "What is...?" series introducing the basics of category theory: 
 
"What is a category ?" 
"What is a functor?" Part 1 and Part 2 
"What is a natural transformation?" Part 1 and Part 2 
Today, we'll add adjunctions to the list. An adjunction is a pair of functors that interact in a particularly nice way. There's more to it, of course, so I'd like to share some motivation first. And rather than squeezing the motivation, the formal definition, and some examples into a single post, it will be good to take our time: Today, the motivation. Next time, the formal definition. Afterwards, I'll share examples. Indeed, I will make the admittedly provocative claim that adjointness is a concept of fundamental logical and mathematical importance that is not captured elsewhere in mathematics. - Steve Awodey (in Category Theory , Oxford Logic Guides) 

#### So, what is an adjunction?

Mathematics is often concerned with pinning down an appropriate notion of "sameness" and asking the question, "When are two things the same?" (I am reminded of Jim Propp's excellent essay "Who Knows 2?" ) Category theory, in particular, shines brightly in this arena. It provides us with better words with which to both ask and answer this question and leads us to the notion of isomorphism : Two objects $X$ and $Y$ in a category are isomorphic if there is a morphism from one to the other that has both a left and a right inverse. An isomorphism, then, is like a process $X\to Y$ that can be completely reversed. When such a process exists, the objects are isomorphic. 
Sometimes, however, isomorphism is not the notion you want to work with. What if a process isn't exactly reversible on the nose , yet—given your goals—you'd prefer not to distinguish between the original and final states? 
This arises when we wish to compare two categories:  When are categories $\mathsf{C}$ and $\mathsf{D}$ isomorphic? Given a functor $F\colon \mathsf{C}\to\mathsf{D}$, can I find a functor $G\colon \mathsf{D}\to\mathsf{C}$ so that $$FG=\text{id}_{\mathsf{D}} \qquad\text{and} \qquad GF=\text{id}_\mathsf{C} \quad ?$$ (Here, $\text{id}_\mathsf{C}\colon \mathsf{C}\to\mathsf{C}$ is the identity functor on $\mathsf{C}$, and similarly for $\text{id}_\mathsf{D}$.) Oftentimes, the answer will be "no." That is, equality is often too demanding to be useful in mathematics. Here's an easy illustration: if $X$ and $Y$ are sets then $X\times Y$ is not equal to $Y\times X$. Why? Simply because sticking an $x$ in the first slot is not the same as sticking an $x$ in the second slot: $(x,y)\neq (y,x)$ for elements $x\in X$ and $y\in Y$. 
But if you simply want "the set of pairs of elements in $X$ and $Y$" then you'll be satisfied knowing that although $X\times Y$ and $Y\times X$ are not equal, they are isomorphic. That is, replacing equalities with isomorphisms provides us with desired flexibility. Isomorphisms rather than equalities are thus the tool of choice in category theory. 
With that in mind, let's revisit the equations above: $FG=\text{id}_{\mathsf{D}}$ and $GF=\text{id}_\mathsf{C}.$ When we replace these equalities with natural isomorphisms $$FG\cong \text{id}_{\mathsf{D}} \qquad\text{and} \qquad GF\cong \text{id}_\mathsf{C}$$ then $\mathsf{C}$ and $\mathsf{D}$ are called equivalent categories. Equivalence, then, is a better notion of "sameness" when comparing categories. 

#### Let's take this one step further.

We've just exchanged equalities $=$ for isomorphisms $\cong$, so what if we take this a step further and exchange the isomorphisms for regular morphisms? If we replace the natural isomorphisms with natural transformations $$FG \to \text{id}_{\mathsf{D}} \qquad\text{and} \qquad  \text{id}_\mathsf{C}\to GF$$ then the categories may no longer be equivalent. But this setup is still of great interest. 
It is called an adjunction , and $F$ and $G$ are called adjoint functors . 
 That's it! 
Well, almost. We also ask that the two natural transformations relate to each other in a nice way. But we'll get to that next time. Amazingly, there is much that follows from this simple adjustment. That is, by simply replacing equality $=$ with a (not necessarily invertible arrow) $\to$ we've opened up a vast world of mathematical possibilities. 

#### By way of analogy...

This happens elsewhere in mathematics, too. By "this" I mean the act of finding something interesting after loosening up a strict notion of sameness. 
In topology, for example, one is interested in distinguishing topological spaces. This amounts to asking if there is a homeomorphism —an isomorphism in the category of topological spaces—between them. Homeomorphisms are very nice, but there is a relaxed version known as a homotopy equivalence . Homotopy equivalence is a weaker notion than homeomorphism, so you might think it's no good. Au contrair e. These weak equivalences pave the way for the deeply rich field of homotopy theory . So I like to have this analogy in mind: 
 
I'm reminded of this idea in linear algebra, as well, though in a tangential sort of way. Suppose $U$ is an orthogonal $n\times n$ matrix. It represents an invertible linear map $\mathbb{R}^n\to\mathbb{R}^n$ whose inverse is precisely the adjoint $U^*$ of $U$. That is, $UU^*=I=U^*U$. Now imagine omitting some of the columns of $U$ so that it's an $n\times k$ rectangular matrix with $k<n$. This is not an outrageous request. Perhaps $U$ is the matrix obtained from a singular value decomposition, say $M=UDV^*$, whose smaller singular values you wish to disregard for some data compression task. This truncated $U$ is then a map from a smaller space $\mathbb{R}^k$ into a larger space $\mathbb{R}^n$. The remaining $n-k$ columns are still orthogonal, so $U^*U=I_k$, where $I_k$ is the identity on $\mathbb{R}^k$. Intuitively, this says that if you inject $\mathbb{R}^k$ as a subspace into $\mathbb{R}^n$, then project back onto it, you've not done anything at all. On the other hand, $UU^*$ is no longer the identity on $\mathbb{R}^n$. Intuitively, you can't squish all of $\mathbb{R}^n$ onto $\mathbb{R}^k$ and hope to undo the distortion damage. So $U^*$ is no longer the inverse of $U$, yet both matrices still encode valuable information about the data you're interested in. 
Speaking of linear maps and their adjoints, you might recall a special equality that relates them. If $f\colon V\to W$ is a linear map of Hilbert spaces, then its adjoint $f^*\colon W\to V$ satisfies the inner product equation 
$$\langle f\mathbf{v},\mathbf{w}\rangle = \langle \mathbf{v},f^*\mathbf{w}\rangle \qquad \text{for all $\mathbf{v}\in V$ and $\mathbf{w}\in W$}$$ 
As we'll see next time, an adjunction consists of a pair of functors that satisfy a nearly identical equation. For this reason, the functors participating in an adjunction are called adjoint functors. 
 
In summary, relaxing a notion of "sameness" gives us extra currency with which to explore new phenomena. So don't think of adjunctions as mere equivalence-wannabes. Instead, think of them as top notch, high class citizens in the categorical landscape. As Awodey shares in the same text quoted above, [The notion of adjoint functor] captures an important mathematical phenomenon that is invisible without the lens of category theory. 
Next time, we'll unwind the definition a bit more and, with the lens of category theory, be able to spot several examples in mathematics. 

Share 

 Tweet 

 Share 

Related Posts 

#### The Sierpinski Space and Its Special Property

October 6, 2016 

in 
Topology 

#### The Yoneda Embedding

September 6, 2017 

in 
Category Theory 

#### "One-Line" Proof: Fundamental Group of the Circle

April 24, 2017 

in 
Topology 

#### The Yoneda Perspective

August 30, 2017 

in 
Category Theory 
 
Leave a comment!
