<!-- SOURCE: https://www.math3ma.com/blog/language-statistics-category-theory-part-1 | captured 2026-07-19 | math3ma (Tai-Danae Bradley), free blog | curl+stdlib extract -->

# math3ma — Language Statistics Category Theory Part 1 (captured)

Language, Statistics, & Category Theory, Part 1 

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

June 29, 2021 

• 
Category Theory 

#### Language, Statistics, & Category Theory, Part 1

In the previous post I mentioned a new preprint that John Terilla, Yiannis Vlassopoulos, and I recently posted on the arXiv. In it, we ask a question motivated by the recent successes of the world's best large language models: What's a nice mathematical framework in which to explain the passage from probability distributions on text to syntactic and semantic information in language? 
To understand the motivation behind this question, and to recall what a "large language model" is, I'll encourage you to read the opening article from last time . In the next few blog posts, I'll give a tour of mathematical ideas presented in the paper towards answering the question above. I like the narrative we give, so I'll follow it closely here on the blog. You might think of the next few posts as an informal tour through the formal ideas found in the paper. 
Now, where shall we begin? What math are we talking about? 
Let's start with a simple fact about language. 

#### Language is algebraic.

By "algebraic," I mean the basic sense in which things combine to form a new thing. We learn about algebra at a young age: given two numbers $x$ and $y$ we can multiply them to get a new number $xy$. We can do something similar in language. Numbers combine to give new numbers, and words and phrases in a language combine to give new expressions. Take the words red and firetruck , for example. They can be "multiplied" together to get a new phrase: red firetruck . 
 
Here, the "multiplication" is just concatenation — sticking things side by side. This is a simple algebraic structure, and it's inherent to language. I'm concatenating words together as I type this sentence. That's algebra! Another word for this kind of structure is compositionality, where things compose together to form something larger. 
 
So language is algebraic or compositional. 
I've touched on this idea before in a promo video I made for my PhD thesis last year, which you can see on the right. The video also mentions a second mathematical structure inherent to language, which turns out to be crucial to this discussion. But before getting there, let me first suggest a thought. 
Since language is algebraic, it's intriguing to think about what kind of mathematical tools are at our disposal. One could, for instance, revisit old ideas from abstract algebra to see if there are any new insights to be had in the context of language. 
As an example of this, think about this famous 1957 quote by linguist John Firth: "You shall know a word by the company it keeps." 
This is a pithy way of saying that information about the meaning of a word is captured by its environment, that is, by the totality of expressions in which it appears. I think something similar can be said of people, too. You can learn a lot about a person by knowing the company they keep: who they spend time with, who's in their social network, and so on. So, as Firth's saying goes, the "social network" of a word gives you information about that word. 
Now, how might an algebraist think about this? 

#### Ideals as a proxy for meaning

An algebraist might try to formalize Firth's quote by simply identifying the meaning of a word with something like the two-sided principal ideal associated to that word. A principal ideal is the name given to a certain algebraic structure (a subset of a ring) with a "magnetic" property: if $x$ is an element in the ideal, then any expression obtained by "multiplying" $x$ on the left or right with some other element is also in the ideal. So a principle ideal is a set that attracts everything that has an $x$ in it, like a magnet. 
 
The concept of a word like "red" is thus identified with the principal ideal consisting of all expressions that contain that word: red ruby, bright red ruby, red rover, blood red , red blooded, the worker’s and peasant’s red army, red meat, red firetruck, bright red lipstick , and so on. 
And why stop here? You could push the analogy further by bringing in ideas from algebraic geometry, as well. We actually hint at such directions on page 2–3 of the preprint, and there's lots one could explore at this point. But I'd like to steer the discussion in a different direction. 
You should know upfront that this algebraic way of thinking is inspirational, but incomplete. Language has more structure that we haven't yet mentioned. Not only is it algebraic, it is also statistical . The expression "red firetruck" occurs more frequently in English than "red idea", and this also contributes to the meaning of the word "red." The probability of someone saying "I have a red idea" is quite small, as the number of times that expression has been uttered is pretty low. This is the second mathematical structure explored in the video above. 
But ideals don't know anything about probabilities or statistics. 
So, some refinement is needed. 
Let's then hold onto our algebraic inspiration but switch to a different set of mathematical tools — one that is better suited to merge both the algebraic and statistical structures in language. Which set of tools? Well, the algebraic perspective of viewing ideals as a proxy for meaning is consistent with certain perspectives from category theory , and the latter provides an excellent setting in which to merge the algebraic and statistical structures in language. 
How so? 

#### Language is a category.

Let's consider a category whose objects are strings of symbols from some finite set (i.e. elements from a free monoid, if you like), and where there is a morphism between two strings if one is contained as a substring of the other. If the finite set consists of English words, for example, then the picture to have in mind is a bunch of English expressions with arrows between them: there's an arrow from red to beautiful red ruby, but there is no arrow between red and hot dog . 
 
There is at most one arrow between any two expressions, and so this is a very simple category. In fact, it's really just a preordered set ; that is, is a set equipped with a reflexive and transitive binary relation given by substring containment. The axioms of a category are thus easy to verify. Identity morphisms are provided by reflexivity, and composition of morphisms is provided by transitivity. 
So, language is a category. Let's call it $\mathsf{L}$. 
What can we do with it? 
To start, we might wonder what category theory's most important theorem has to say about it. I'm referring to the Yoneda lemma , whose statement we've discussed in detail here on the blog . Intuitively, the Yoneda lemma says that a fixed object in this category — indeed, in any category — is uniquely determined by the totality of its relationships to all other objects in the category. In other words, all relevant information about a word such as "red" is contained in the entirety of expressions that contain that word. 
Sounds a bit John Firth-y, doesn't it? 
 
Not surprisingly, "the entirety of expressions" has a formal mathematical definition that's worth understanding. Here's how to think about it. Consider again the word "red" and choose any expression $y$ in the category $\mathsf{L}$. There are only two options: either "red" and $y$ are related to each other or they aren't; that is, either there is an arrow from "red" to $y$ or there is not. Simple. But let's try to rephrase this a little more mathematically: if we consider "the set of all arrows from 'red' to $y$," then — as we've just observed — either this set contains exactly one element, or it contains no elements at all. 
Now suppose we do this for every possible expression $y$: for every $y$ in $\mathsf{L}$ we can associate to it a set whose cardinality is either 1 or 0, depending on whether or not "red" sits inside of $y$. So if you know all the sets with cardinality 1, then you know "the entirety of expressions" that contain the word "red." This assignment of a set to every object in $\mathsf{L}$ is sufficiently nice that it has a name: it's an example of a functor . 
Let me summarize what we've just said. For each object $x$ in $\mathsf{L}$ (i.e. for each string of English words), there is a functor $\mathsf{L}(x,-)\colon\mathsf{L}\to\mathsf{Set}$, which is simply an assignment of a particular set, denoted by $\mathsf{L}(x,y)$, to each expression $y$ in $\mathsf{L}$. If there is an arrow from $x$ to $y$ in $\mathsf{L}$ (that is, if $x$ is contained in $y$) then the set $\mathsf{L}(x,y)$ contains exactly one element in it — namely, the arrow $x\to y$ — and so it's isomorphic to the one-point set $\ast$. Otherwise, if there is no arrow $x\to y$, then $\mathsf{L}(x,y)$ is the empty set. 
 
This particular functor has a sophisticated name: $\mathsf{L}(x,-)$ is called the representable copresheaf associated to $x$, and the assignment $x\mapsto\mathsf{L}(x,-)$ is called the Yoneda embedding . The image of this embedding for a fixed $x$ captures the "entirety of expressions" that contain $x$. 
While the terminology may be new, the concept should sound familiar. If $x$ is the word "red," for instance, then the set of all expressions $y$ in $\mathsf{L}$ that map to $\ast$ under the functor $\mathsf{L}(\text{red},-)$ is precisely the principal ideal associated to "red." So the algebraic and category theoretical perspectives are consistent with each other, and ideals and copresheaves can both be viewed as a first approximation to the meanings of words. 
 
Even so, the category theoretical route has certain advantages over the algebraic one.  

#### Advantages to the category theoretical approach

I'll spend the next few posts elaborating on this, but it starts with the fact that arbitrary functors $\mathsf{L}\to\mathsf{Set}$ themselves form the objects of a new category called the copresheaf category on $\mathsf{L}$, denoted by $\mathsf{Set}^\mathsf{L}$. A functor such as $\mathsf{L}(\text{red},-)$ from above is one example of a copresheaf, but you can probably think of other ways to assign a set to the word "red." The category $\mathsf{Set}^\mathsf{L}$ just collects all of those possible ways. 
The upshot of the discussion so far is that the language category $\mathsf{L}$ captures something of syntax: it just tells us "what goes with what." If we want to glean information about the semantics of words, however, then we're prompted to pass to this new category $\mathsf{Set}^\mathsf{L}$ via the Yoneda embedding. For as we've just seen, the Yoneda embedding sends each word in language to the network of ways that word fits into the language, and the latter carries something of the meaning of that word. 
 
Even better, the category $\mathsf{Set}^\mathsf{L}$ is an example of a topos , which is known to be an appropriate setting in which to discuss logic. We won't use the tools of topos theory here — so don't worry about the definition — but I mention it by way of inspiration: having a topos prompts a few elementary thoughts on logic, which we now have room to explore (and otherwise wouldn't in the mere algebraic setting). 
As an example, think about disjunction . 
If we wish to represent the concept of a word like red by an ideal, then what would represent the disjunction of two concepts, say red or blue ? The union of two ideals is not another ideal, so the algebra quickly breaks down. But the situation is much better in category theory. It turns out that the "union" of two copresheaves is indeed another copresheaf, and so we can get a very concrete representation of the concept red or blue in the category $\mathsf{Set}^\mathsf{L}$. 
 
I'll explain this next time, but notice I put union in quotation marks above. That's because the construction I'm referring to is really the coproduct of copresheaves, which is analogous to the union of sets in that both are examples of colimits in category theory. It's not necessary to know about colimits to understand the "coproduct of $\mathsf{L}(\text{red},-)$ and $\mathsf{L}(\text{blue},-)$" — it's a very simple construction, and I'll share the details in the next post. But in the mean time, if you'd like to learn more about the general theory of categorical colimits (and the dual notion of limits), then I'd recommend this introductory article here on the blog. 
You may also wonder about conjunction ( red and blue) and implication (red implies blue) and other operations from logic. Can these operations be realized in our copresheaf category of language, as well? 
I'll say more next time. And don't forget that this isn't yet the full story. What about statistics? We'll get to that, too. 
Until then! 

Share 

 Tweet 

 Share 

Related Posts 

#### "One-Line" Proof: Fundamental Group of the Circle

April 24, 2017 

in 
Topology 

#### What is an Adjunction? Part 3 (Examples)

September 26, 2019 

in 
Category Theory 

#### The Most Obvious Secret in Mathematics

September 12, 2016 

in 
Category Theory 

#### Limits and Colimits Part 3 (Examples)

January 21, 2019 

in 
Category Theory 
 
Leave a comment!
