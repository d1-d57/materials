<!-- SOURCE: https://www.math3ma.com/blog/warming-up-to-enriched-category-theory-1 | captured 2026-07-19 | math3ma (Tai-Danae Bradley), free blog | curl+stdlib extract -->

# math3ma — Warming Up To Enriched Category Theory 1 (captured)

Warming Up to Enriched Category Theory, Part 1 

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

June 8, 2021 

• 
Category Theory 

#### Warming Up to Enriched Category Theory, Part 1

 It's no secret that I like category theory. It's a common theme on this blog, and it provides a nice lens through which to view old ideas in new ways — and to view new ideas in new ways! Speaking of new ideas, my collaborators and I are planning to upload a new paper on the arXiv soon. I've really enjoyed the work and can't wait to share it with you. But first, you'll have to know a little something about enriched category theory . (And before that , you'll have to know something about ordinary category theory... here's an intro !) So that's what I'd like to introduce today. 
It's a warm up, if you will. 

#### What is enriched category theory?

As the name suggests, it's like a "richer" version of category theory, and it all starts with a simple observation. (Get your category theory hats on, people. We're jumping right in!) 
In a category, you have some objects and some arrows between them, thought of as relationships between those objects. Now in the formal definition of a category, we usually ask for a set's worth of morphisms between any two objects, say $X$ and $Y$. You'll typically hear something like, "The hom set $\text{hom}(X,Y)$ bla bla...."
‍ 
 
Now here's the thing. Quite often in mathematics, the set $\text{hom}(X,Y)$ may not just be a set. It could, for instance, be a set equipped with extra structure. You already know lots of examples. Let's think about about linear algebra, for a moment. 
If we have a pair of real vector spaces, say $V$ and $W$, then the set of linear transformations $V\to W$ has lots of structure: if $f,g\colon V\to W$ are linear transformations, then their sum $f+g$ is also a linear transformation from $V$ to $W$, and so is the scalar multiple $kf$ for any real number $k$. In fact, the point here is that the set $\hom(V,W)$ of linear transformations is itself a real vector space. So the hom sets evidently have "richer" structure. They are enriched! Now, linear algebra is just one example. You can think of others!  The set of continuous functions between a pair of topological spaces can itself be given a topology; the set of homomorphisms between a pair of abelian groups is itself an abelian group; and so on. 
And that's the main idea behind enriched category theory. (Well, that's the gist. The theory gets deep quickly.) 
You have a category $\mathsf{C}$, and the hom sets between the objects in $\mathsf{C}$ are themselves objects in some other category, which is often called the base category or the category over which $\mathsf{C}$ is enriched . In the examples above, the categories were each enriched over themselves , but it's totally fine to have a category $\mathsf{C}$ enriched over a different category. 
 
Admittedly, the graphic above isn't the whole story. For the math to really work out, we have to be a little careful with the axioms for composition of morphisms and identity morphisms, and so there's a little more to say. Indeed, there is a very formal definition of an enriched category, but I'm not sharing it just yet. We're still warming up! In fact, I want to dial things back even further and consider the following super simple scenario. 

#### Let's take it down a notch.

Suppose we have a pair of objects $X$ and $Y$, and let's further suppose there is at most one morphism from $X$ to $Y.$ This is much simpler than our examples above from linear algebra, group theory, and topology, where in principle there could've been loads of morphisms. But we want to keep things simple for now. 
So, suppose we're in a situation where either there's an arrow $X\to Y$ or there's not. 
Now, let's also consider the possibility that that arrow can be "decorated" with — or simply replaced by — some number. Perhaps that number indicates the degree to which that arrow is there. Or perhaps it represents the amount of effort it takes to "get" from $X$ to $Y$. Or maybe it represents the probability ( or some fuzziness*) of going from $X$ to $Y$. Or the distance it takes to travel from $X$ to $Y$. Or maybe it just represents the Boolean truth-value of whether or not that arrow is even there. Use your imagination! 
 
Imagination is good, but so is thinking systematically. So let's rope things in a bit. I really like those last three suggestions — truth values, distances, and probabilities — and I'd like us to be little more formal about it. To that end, let's say the arrow $X\to Y$ can be either be decorated with a number from the two-element set $\{0,1\}$ (thought of as truth values), or perhaps the unit interval $[0,1]$ (thought of as probabilities or some fuzziness), or perhaps the set of nonnegative extended reals $[0,\infty]$ (thought of as distances). 
 
See the analogy, here? Earlier, the collection of arrows from $X$ to $Y$ was an object in the category $\mathsf{Vect}$ of vector spaces, or the category $\mathsf{Top}$ or topological spaces, or the category $\mathsf{AbGrp}$ of abelian groups, or.... But now the "collection" consisting of the single arrow $X\to Y$ is basically just an element in the set $\{0,1\}$, or the set $[0,1]$, or the set $[0,\infty]$, or... 
 
See where we're going with this? I'll summarize it as a question and answer: 
 Question :  Is there a way to view the sets $\{0,1\}$ and $[0,1]$ and $[0,\infty]$ as categories so that the number "$\text{hom}(X,Y)$" is actually an object in that category? And is there a more formal way to talk about categories "enriched" over these categories? 
 Answer: YES and YES! 
And rather than belaboring this point any longer, let's cut to the chase. 

#### Ramping back up.

Each of the three sets above are examples of preordered sets, which are very easy-to-understand kinds of categories. A preordered set, or simply a preorder , is a set equipped with a reflexive and transitive relation typically denoted by $\leq$. If the relation is also antisymmetric, then it's actually a partially-ordered set , i.e. a poset. But it turns out that just having a preorder means you automatically have yourself a category. The objects are elements in the set, and morphisms are provided by $\leq$. Identity morphisms are provided by reflexivity, and composition is provided by transitivity. 
So, every preorder is a category. 
In particular, there is a category $\{0\leq 1\}$ of truth values, whose only two objects are the numbers $0$ and $1$ and where the only non-identity morphism is $0\leq 1$. The unit interval  $[0,1]$ is also a category, since it's a preorder with the usual ordering $\leq$. You can think of having a morphism $0.3\to 0.75$ since $0.3\leq 0.75$. And the nonnegative extended reals $[0,\infty]$ are also a preorder, but for historical reasons (i.e. Lawvere — we'll get to him later!), we'll view it as a category where there's an arrow between real numbers $a\to b$ whenever $a\geq b$, which is the opposite of the usual ordering.  
Now a word of caution: don't let the simplicity of these preorders fool you. Categories enriched over them pave the way for tons of nice examples, and lovely theory, and current threads of research. 
But wait — what exactly IS a category enriched over a preorder? 
I'll tell you next time. 
There's so much more to say, but this post is already quite long. 
Stay tuned! 
 
*If you're already an expert on enriched category theory, then you'll know that when folks enrich over $[0,1]$, they're usually thinking about fuzzy logic . And you'll also know that fuzzy logicians are pretty adamant that you not think of elements in $[0,1]$ as probabilities. But let's allow ourselves to be flexible about this. 

Share 

 Tweet 

 Share 

Related Posts 

#### The Fibonacci Sequence as a Functor

December 14, 2020 

in 
Category Theory 

#### What is a Natural Transformation? Definition and Examples, Part 2

February 13, 2017 

in 
Category Theory 

#### The Yoneda Perspective

August 30, 2017 

in 
Category Theory 

#### Viewing Matrices & Probability as Graphs

March 6, 2019 

in 
Probability 
 
Leave a comment!
