<!-- SOURCE: https://www.math3ma.com/blog/language-modeling-with-reduced-densities | captured 2026-07-19 | math3ma (Tai-Danae Bradley), free blog | curl+stdlib extract -->

# math3ma — Language Modeling With Reduced Densities (captured)

Language Modeling with Reduced Densities 

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

July 9, 2020 

• 
Probability 

• 
Category Theory 

• 
Algebra 

#### Language Modeling with Reduced Densities

Today I'd like to share with you a new paper on the arXiv —my latest project in collaboration with mathematician Yiannis Vlassopoulos (Tunnel). To whet your appetite, let me first set the stage. A few months ago I made a 10-minute introductory video to my PhD thesis , which was an investigation into mathematical structure that is both algebraic and statistical. In the video, I noted that natural language is an example of where such mathematical structure can be found. Language is algebraic , since words can be concatenated to form longer expressions.  Language is also statistical , since some expressions occur more frequently than others. 
As a simple example, take the words "orange" and "fruit ." W e can stick them together to get a new phrase, "orange fruit." Or we could put "orange" together with "idea" to get "orange idea ."  That might sound silly to us, since the phrase "orange idea" occurs less frequently in English than "orange fruit ." But that's the point. These frequencies contribute something to the meanings of these expressions. So what is this kind of mathematical structure? As I mention in the video, it's helpful to have a set of tools to start exploring it, and basic ideas from quantum physics are one source of inspiration. I won't get into this now—you can watch the video or read the thesis! But I do want to emphasize the following: In certain contexts, these tools provide a way to see that statistics can serve as a proxy for meaning. I didn't explain how in the video. I left it as a cliffhanger. 
But I'll tell you the rest of the story now. 
As with many good things in life, it begins with the Yoneda lemma—or rather, the Yoneda perspective . 

#### The Yoneda Perspective

Let's think back to language for a moment. To understand the meaning of the word "orange," for instance, it's helpful to know something about how that word fits into language. We noted that "orange idea" is not a meaningful expression in English, although "orange fruit" is. So the meaning of "orange" is somehow built into the network of ways that it fits into other expressions. I have the following picture in mind, where an arrow indicates when one expression is contained in another. 
 
This is very much like the Yoneda lemma in category theory, which informally says that a mathematical object is completely determined by the network of relationships that object has with other objects in its environment. I like to call this maxim the "Yoneda Perspective" and have blogged about it before . And it's the same perspective we're taking above. Want to distinguish between meanings of words? Then look at the network of ways they relate to other words. 
 But actually ... this isn't the whole story. It's merely the algebraic part. There's also statistics! 
In other words, it's not enough to know that "orange"  can go with "fruit" or with "chrysanthemum" or with "safety vest." There's additional information to be aware of, namely the statistics of these expressions. So intuitively, we'd like to decorate, or enrich, the network with something like conditional probabilities. And here comes the best part. 
‍ This is more than just intuition. 
 ‍ This idea can be made precise! And that's what our new paper is about. We use ideas from linear algebra and category theory to anchor this intuition on firmer ground. As a bonus, we're also able to model a preliminary form of hierarchy in language. There are a few other aspects to the paper, but these are the ideas I'd like to emphasize here. 
Let's look at some of the details. 

#### Diving Deeper

We begin by modeling expressions in language as sequences of symbols from some finite set $X$. For simplicity, we start with the set $X^N$ of all sequences of a fixed length $N$ and consider any joint probability distribution $\pi\colon X^N\to\mathbb{R}$ on that set. Using these ingredients, we then describe a recipe for assigning to any sequence $s$ of length at most $N$ a special kind of linear operator $\rho_s$. We describe a way of assigning to any word or expression $s$ in a language a particular linear operator $\rho_s$. This operator is jam-packed with information. 
We obtain the operator $\rho_s$ by passing from classical probability theory to quantum probability theory in a way discussed previously on this blog and in Chapter 3 of my thesis . Briefly, we use the joint distribution $\pi$ to define a rank 1 density operator $\rho$; that is, a self-adjoint, positive semidefinite operator with trace 1. Then we compose $\rho$ with a standard basis vector representation ("one hot encoding") of an expression $s$, and finally we apply the quantum analogue of marginalization, namely the partial trace . The process of marginalizing is a bit like reducing your attention to a smaller subsystem, and so the resulting operator $\rho_s$ is called a reduced density operator. (We have to normalize to ensure it has unit trace, but that's a small detail.) 
The matrix representation for $\rho_s$ is quite illuminating. We show that its diagonal entries are conditional probabilities that $s$ will be followed by other expressions in the language! To illustrate, we include several easy, hands-on examples* as well as pictures. For instance, here's a tensor network diagram to illustrate the passage from $\pi$ to $\rho$ to $\rho_s$ just described. 
 
Now, I claimed that $\rho_s$ is jam-packed with information. Indeed, it knows a lot about the "network of ways that $s$ fits into other expressions in the language." From the perspective of the Yoneda lemma, the "meaning" of the word $s$ is neatly packaged into the linear operator $\rho_s$. 
The precise math statement behind this is as follows. We show that the operator $\rho_s$ decomposes as a weighted sum of operators, one operator $\rho_{s'}$ for every expression $s'$ that contains $s$, where the weights are conditional probabilities $\pi(s'|s)$. As an example, think back to the network of the word "orange" illustrated above. Now imagine replacing every expression (like "ripe small orange") with a matrix. Then the matrix for "orange" is equal to the sum of all the other matrices, after multiplying each matrix by a particular probability. 
 
So these operators $\rho_s$ capture something of the environment—and hence the meanings—of the words $s$ that they represent! 
But wait, there's more ! 
In some cases, we prefer to work with an "unnormalized" version, $\hat\rho_s$, whose trace may be less than one. Doing so allows us to see that our passage $s\mapsto\hat\rho_s$ fits neatly into the world of category theory. In particular, we show that the assignment $s\mapsto\hat\rho_s$ is a functor between categories enriched** over probabilities. 
That's right. We define a category for language and a category for the linear operators that represent language. We incorporate statistics by enriching** these categories over a probabilities (explained below), and we show that the assignment $s\mapsto\hat\rho_s$ respects this categorical structure. This might sound grandiose, but it's quite simple. Our categories are preordered sets; that is, sets equipped with a partial order $\leq$ that isn't necessarily antisymmetric. And our "enrichment" is just a fancy way of labeling, or decorating, the $\leq$ with probabilities. The assignment $s\mapsto\hat\rho_s$ is simply a function that respects these labels. 
In more detail, we show the following three things: 
 Language forms a category enriched over probabilities . We define a category whose objects are valid expressions in language—that is, valid sequences from the alphabet $X$—and we write $s\leq s'$ if the sequence $s'$ contains $s$ as a subsequence. One checks that $\leq$ is a preorder, and so the $\leq$ are the morphisms of the category. For instance, we have that orange $\leq$ small orange $\leq$ ripe small orange, while orange $\not\leq$ cold iced tea}. But we're not merely interested in whether or not "orange" is contained in "small orange fruit," we're interested in the probability ! So we then replace the hom- set $\text{hom}(s,s')$ with a hom- probability, which we choose to be conditional probability $\pi(s'|s)$. This gives us a category enriched over the unit interval $[0,1]$, viewed as a monoidal category. See Proposition 5.1 . 
 Operators associated to expressions also form a category enriched over probabilities. Because our operators $\hat\rho_s$ are positive semidefinite, they form a preordered set—and hence a category—under the Loewner order . As an immediate consequence, we can model a simple kind of hierarchy in language. For instance, the operators associated to orange and small orange are comparable under the Loewner order, as one finds that $\hat\rho_{\text{orange}}\geq\hat\rho_{\text{small orange}}$. This models the intuitive idea that orange is a more abstract concept than something that's both small and orange . But again, we're really interested in the probabilities associated to this, so we proceed to enrich this category over $[0,1]$ in a similar way. See Proposition 5.2 . 
 The assignment $s\mapsto \hat\rho_s$ is an enriched functor between enriched categories. Finally, we show that the function $s\mapsto \hat\rho_s$ is compatible with probabilities in a sensible way—in other words, we show that the main construction of the paper is actually a functor between categories enriched over $[0,1]$. See Theorem 5.1 . 
Et voila! 

#### Wrapping up

In the end, we accomplished what we set out to do. Motivated by the Yoneda perspective, we use probabilities to "decorate" the network of ways a word fits into other expressions in language. We show that this algebraic and statistical information is packaged neatly into a linear operator associated to that word. And we conclude that the recipe to do so has a nice, categorical explanation. 
In closing, notice that the simple form of hierarchy we're able to model is totally dependent on the sequential structure of language. So while we can represent the intuitive idea that "orange" is a more abstract notion than "small orange," we don't have a way to conclude that "color" is more abstract than "orange," simply because the word "color" doesn't contain "orange" as a subsequence. So there's more work to be done. What's more, in practice, the linear maps $\hat\rho_s$ will operate on ultra-large-dimensional spaces, and so storing and manipulating them on a computer won't be feasible for real-world datasets. But the ideas we present in the paper are naturally adaptable to tensor network techniques, which are well-suited for dealing with operators on large-dimensional spaces. In fact, tensor networks also complement our algebraic and statistical perspective of language in other nice ways , and I'm hopeful they'll be useful in exploring more complex concept hierarchies later on. 
To be continued! 
 
*Heads up: In this blog post, all of my examples involve the word "orange." We switch it up in the paper. There, most of our examples involve the word "dog." 
**I haven't properly blogged about enriched category theory on Math3ma before, but I might get around to it if there's enough interest. 

Share 

 Tweet 

 Share 

Related Posts 

#### Announcing Applied Category Theory 2019

January 5, 2019 

in 
Category Theory 

#### Commutative Diagrams Explained

July 5, 2017 

in 
Other 

#### The Most Obvious Secret in Mathematics

September 12, 2016 

in 
Category Theory 

#### Applied Category Theory 2020

March 2, 2020 

in 
Other 
 
Leave a comment!
