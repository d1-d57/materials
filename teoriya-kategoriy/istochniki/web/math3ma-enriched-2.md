<!-- SOURCE: https://www.math3ma.com/blog/warming-up-to-enriched-category-theory-part-2 | captured 2026-07-19 | math3ma (Tai-Danae Bradley), free blog | curl+stdlib extract -->

# math3ma — Warming Up To Enriched Category Theory Part 2 (captured)

Warming Up to Enriched Category Theory, Part 2 

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

June 10, 2021 

• 
Category Theory 

#### Warming Up to Enriched Category Theory, Part 2

Let's jump right in to where we left off in part 1 of our warm-up to enriched category theory. If you'll recall from last time, we saw that the set of truth values $\{0, 1\}$ and the unit interval $[0,1]$ and the nonnegative extended reals $[0,\infty]$ were not just sets but actually preorders and hence categories. We also hinted at the idea that a "category enriched over" one of these preorders (whatever that means — we hadn't defined it yet!) looks something like a collection of objects $X,Y,\ldots$ where there is at most one arrow between any pair $X$ and $Y$, and where that arrow can further be "decorated with" —or simply replaced by — a number from one of those three exemplary preorders. 
 
With that background in mind, my goal in today's article is to say exactly what a category enriched over a preorder is. The formal definition — and the intuition behind it — will then pave the way for the notion of a category enriched over an arbitrary (and sufficiently nice) category, not just a preorder. 
En route to this goal, it will help to make a couple of opening remarks. 

#### Two things to think about.

First, take a closer look at the picture on the right. I've written "$\text{hom}(X,Y)$" in quotation marks because the notation $\text{hom}(-,-)$ is often used for a set of morphisms in ordinary category theory. But the  point of this discussion is that we're not just interested in sets! So we should use better notation: let's refer to the number associated to a pair of objects $X$ and $Y$ as $\mathcal{C}(X,Y)$, where the letter "$\mathcal{C}$" reminds us there's an (enriched) $\mathcal{C}$ategory being investigated. 
Second, for the theory to work out nicely, it turns out that preorders need a little more added to them. To see what I mean, think about the trademark feature of a category: compositionality. You know how the story goes. If $f\colon X\to Y$ and $g\colon Y\to Z$ are morphisms, then we ask for the existence of a third morphism $g\circ f\colon X\to Z$  called their composite . Said another way, we ask for a function between hom sets that maps a pair $(f,g)$ to the composition $g\circ f$ as illustrated below on the left. Importantly, we must use the Cartesian product of sets to make sense of "the pair $(f,g)$". 
This point is worth emphasizing. 
The Cartesian product gives the category $\mathsf{Set}$ a way to "multiply" sets together, and we use that multiplication to pin down the notion of composition. More formally, the Cartesian product makes $\mathsf{Set}$ into a symmetric monoidal category , with the one-point set $\ast$ as the monoidal unit. (Like a commutative monoid, a symmetric monoidal category has a way to "multiply" objects together, and it also has a special object that acts like a multiplicative unit.) Now, the key idea is that we want to replace $\mathsf{Set}$ with a preorder, and that means we'll want an analogous way to "multiply" elements in a preorder. 
 
This leads to the definition of a symmetric monoidal preorder , which is a commutative monoid $(\mathcal{V},\cdot,1)$ (here, $\mathcal{V}$ is a set, $\cdot$ is the monoidal product, and $1$ is the monoidal unit) equipped with a preorder $\leq$ that's compatible with the monoidal product, meaning that $u\cdot u'\leq v\cdot v'$ whenever $u\leq v$ and $u'\leq v'$ for all elements $u,u',v,v'\in \mathcal{V}$. You can check that the preorder of truth values and the unit interval are symmetric monoidal under usual multiplication of real numbers where $1$ is the monoidal unit. The preorder of nonnegative extended reals is symmetric monoidal under addition with $0$ as the monoidal unit. 
With this definition in hand, we can now say what it means to have a category enriched over one of these preorders. 

#### Let the enrichment begin.

Let $(\mathcal{V},\leq,\cdot,1)$ be a symmetric monoidal preorder. A category $\mathcal{C}$ enriched over $\mathcal{V}$ (or simply a $\mathcal{V}$-category ) consists of a set $\text{ob}(\mathcal{C})$ of objects and an element $\mathcal{C}(X,Y)\in\mathcal{V}$ for every pair of objects $X$ and $Y$ such that the following hold: 
$1\leq\mathcal{C}(X,X)$ for all objects $X$, 
$\mathcal{C}(X,Y)\cdot\mathcal{C}(Y,Z)\leq \mathcal{C}(X,Z)$ for all objects $X,Y,$ and $Z$. 
The second bullet is the enriched version of composition shown in the graphic above. And you may recognize the first bullet as the enriched version of identities from ordinary category theory. Indeed, in ordinary category theory, for each object $X$ we ask for a special morphism $\text{id}_X\colon X\to X$ called the identity at $X$. But picking out a special morphism in $\text{hom}(X,X)$ is the same thing as asking for a function to it from the one-point set, $\ast\to\text{hom}(X,X)$. Such a function is precisely a choice of an element in $\text{hom}(X,X)$, which we just call $\text{id}_X$. But $\ast$ is the monoidal unit in the category $\mathsf{Set}$! So let's just play "Mad Libs" for a second: replace $\mathsf{Set}$ with $\mathcal{V}$, and replace the unit $\ast$ with $1$, and replace an arrow $\to$ with $\leq$. Then voila — we end up with the first bullet above. 
 
And that's it! 
But perhaps the definition isn't as enlightening as some examples. So, what does a category enriched over truth values look like? And what about categories enriched over $[0,\infty]$ or $[0,1]$? Let's now say a few brief words about each. 

#### Categories enriched over truth values are preorders .

Yes, think about it! A category enriched over the preorder of truth values, which I'll now denote by $2:=\{0\leq 1\}$, consists of a set together with a number $2(X,Y)\in\{0,1\}$ for every pair of objects $X$ and $Y$ such that those two bullets above hold. And those two bullets, as you can check, are precisely reflexivity and transitivity. Intuitively then, the number $2(X,Y)$ can be viewed as an answer to the question, "Is $X\leq Y$?" If the answer is "yes," then $2(X,Y)=1$. If the answer is "no," then $2(X,Y)=0$. And conversely, every preorder can be viewed as a category enriched over 2 in this way. 
If you enjoy thinking visually, then you might imagine a preorder as a category whose morphisms are weighted by (or decorated with) truth values, where 0 is thought of as "false" and 1 is thought of as "true." Then a morphism weighted by a 1 is, well, just an arrow . But a morphism decorated with a 0 can be omitted. You probably don't need an example, but consider the category whose objects are the natural numbers and where there is an arrow $n\to m$ if and only if $n$ evenly divides into $m$. Below is a small picture of some of the morphisms in this category enriched over 2. 
 
Now let's kick things up a notch. What's a category enriched over $[0,\infty]$? 

#### Categories enriched over $[0,\infty]$ are generalized metric spaces .

A category $\mathcal{M}$ enriched over $[0,\infty]$ consists of a set together with an element $\mathcal{M}(X,Y)\in[0,\infty]$ for every pair of elements $X$ and $Y$, so that the two inequalities below hold. Here you'll have to remember from last time that we're viewing $[0,\infty]$ as a preorder opposite the usual way! There's an arrow $a\to b$ whenever $b$ is greater than or equal to $a$, and so all the $\leq$s are swapped. 
 
The first condition implies $\mathcal{M}(X,X)=0$ for all $X$, and the second condition is the triangle inequality. Sound familiar? The assignment $(X,Y)\mapsto\mathcal{M}(X,Y)$ is almost a metric! It's missing antisymmetry, and it can also take on infinity as a value, and it's also missing the requirement that $X=Y$ whenever $\mathcal{M}(X,Y)=0$. But that's okay. The structure we have here is still very interesting, as categories enriched over $[0,\infty]$ are called generalized metric spaces or sometimes Lawvere metric spaces and were first explored in a 1973 paper by William Lawvere. 
But what's the intuition for these not-quite-metric-space spaces? I really enjoyed John Baez's intuitive explanations in Lecture #31 in his (free!) online class on applied category theory. There he gives the name "Cost" to the monoidal preorder $[0,\infty]$, which hints at some of that intuition. Do take a look! I especially like what he says about dropping some of the axioms from the definition of a metric. I'll quote John directly: You might think that extra axioms are always good, because they let you prove more theorems. But you have to remember they impose a price: it means the axioms apply to fewer things, so constructing structures that obey these axioms becomes harder. So, Lawvere metric spaces are a great example of how category theory can lead us to refine and perfect existing ideas. 
And speaking of refining and perfecting existing ideas, what if we just went all out and allowed negative distances, because why not? Well, as it turns out, one can indeed make sense of enriching over the extended real line $[-\infty,\infty]$. What's more, it arises quite naturally in a discussion of the Legendre-Fenchel transform from physics. Simon Willerton has written this all out beautifully in this 2015 paper . 
Let's now close with a few brief words about categories enriched over $[0,1]$. 

#### Categories enriched over $[0,1]$ are... interesting!

Categories enriched over the unit interval were given the name "proximity sets" in this 2012 paper by Dusko Pavlovic and were later explored again in this 2017 PhD thesis by Jonathan Elliot. In both papers, one thinks of the value assigned to a pair of objects in a $[0,1]$-category as a sort of "proximity" between them. Both authors explored such enriched categories in the context of generalizing formal concept analysis , which I like to think of as a toy version of latent semantic analysis, or a toy version of the role of matrix factorizations in recommender systems . Simon Willerton also has nice blog post with some intuition about $[0,1]$-categories in the context of fuzzy logic. 
In any case, the picture I like to have in mind is the one on the right — a collection of objects with at most one arrow between any two of them, where that arrow is decorated with some number in $[0,1]$. But don't stare at it to closely. I just threw some numbers down, and they don't satisfy the composition axiom of a $[0,1]$-category. But you get the idea! 
Now, in addition to the papers above, one can have other interesting discussions about categories enriched over the unit interval. In fact, there's one particular example that I like very much: 
 Natural language. 
It's true! The text you're reading right now is part of an especially nice $[0,1]$-category! 
 But how? 
And what can one do with it? 
Yiannis Vlassopoulos and I first discussed some of these ideas in a paper last year, and I blogged about it here . Since then, some new insights were had. There's lots of interesting mathematics in this direction, and I'll tell you more another time. 
Be sure to check back later! 

#### Where to go from here?

I hope this mini-series was a helpful warmup to some of the basic ideas in enriched category theory. We never got around to discussing the most general definition, nor what the enriched version of functors , natural transformations , and (co)limits are. To learn the general story, check out chapter 3 of Emily Riehl's excellent Categorical Homotopy Theory . The Catsters channel on YouTube also has a friendly video series on enriched category theory. And speaking of friendly, chapter 2 of the wonderful Seven Sketches by Brendan Fong and David Spivak has a great exposition of some of the simple ideas discussed here, and more. Or if you're feeling really ambitious, the go-to book for experts is Basic Concepts of Enriched Category Theory by G. M. Kelly. 
Until next time! 

Share 

 Tweet 

 Share 

Related Posts 

#### Group Elements, Categorically

February 16, 2017 

in 
Category Theory 

#### Naming Functors

July 31, 2017 

in 
Category Theory 

#### Language Modeling with Reduced Densities

July 9, 2020 

in 
Category Theory 

#### Applied Category Theory 2020

March 2, 2020 

in 
Other 
 
Leave a comment!
