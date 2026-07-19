<!-- SOURCE: https://www.math3ma.com/blog/language-statistics-category-theory-part-3 | captured 2026-07-19 | math3ma (Tai-Danae Bradley), free blog | curl+stdlib extract -->

# math3ma — Language Statistics Category Theory Part 3 (captured)

Language, Statistics, & Category Theory, Part 3 

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

July 28, 2021 

• 
Category Theory 

#### Language, Statistics, & Category Theory, Part 3

Welcome to the final installment of our mini-series on the new preprint " An Enriched Category Theory of Language ," joint work with John Terilla and Yiannis Vlassopoulos. In Part 2 of this series, we discussed a way to assign sets to expressions in language — words like "red" or "blue" – which served as a first approximation to the meanings of those expressions. Motivated by elementary logic, we then found ways to represent combinations of expressions — "red or blue" and "red and blue" and "red implies blue" — using basic constructions from category theory. 
 
I like to think of Part 2 as a commercial advertising the benefits of a category theoretical approach to language, rather than a merely algebraic one. But as we observed in Part 1 , algebraic structure is not all there is to language. There's also statistics! And far from being an afterthought, those statistics play an essential role as evidenced by today's large language models discussed in Part 0 . 
Happily, category theory already has an established set of tools that allow one to incorporate statistics in a way that's compatible with the considerations of logic discussed last time. In fact, the entire story outlined in Part 2 has a statistical analogue that can be repeated almost verbatim . In today's short post, I'll give lightning-quick summary. 
It all begins with a small, yet crucial, twist. 

#### Incorporating Statistics

As you'll recall, the main ingredient in Part 2 was a category $\mathsf{L}$ of language. The objects in this category are expressions in a language, i.e. strings of words, and there is an arrow between two expressions if one contains the other as a substring. To bring statistics into the picture, we now simply "decorate" that arrow with conditional probability of substring containment. So whereas before there was an arrow from "red" to "red firetruck," now we imagine labeling that arrow with the probability of the expression "red firetruck" given the presence of the word "red." 
 
"Where do these probabilities come from?" you ask. Well, it's precisely these conditional probabilities of continuing texts that existing large language models learn via machine learning. As we explain in the paper, "While one may be skeptical about assigning a probability distribution on the set of all possible texts, we find it perfectly reasonable to say there is a nonzero probability that cat food will follow I am going to the store to buy a can of, and practically speaking, that probability can be estimated." So here's the picture I have in mind: 
 
Although decorating arrows may seem like a small step, it turns out to fit in perfectly with enriched category theory , which is the version of category theory where the set of arrows between two objects is not just a set, but is actually an object in some other category. (For a friendly introduction to these ideas, check out our recent mini-series, " Warming Up to Enriched Category Theory .") In our setting of language, decorating an arrow with a number amounts to replacing the set consisting of a single arrow with a probability. As we've explained previously on the blog, this intuitive idea is made rigorous by what's called "enriching over the unit interval $[0,1]$ ," where $[0,1]$ is viewed as category whose objects are numbers between 0 and 1 and where morphisms are provided by the usual ordering $\leq$. 
 
There's a little work to be done to make all this precise. But after doing so, the final result is category $\mathcal{L}$ of language enriched over probabilities. It's very much like our original ordinary category $\mathsf{L}$ except now the statistics of language are woven in. And with that simple first step, we are then able to repeat all of the ideas explored in Part 2 where plain old sets are replaced with probabilities ! 
For instance, the functor representing the word "red" $\mathsf{L}(\text{red},-)\colon\mathsf{L}\to\mathsf{Set}$ that we introduced last time is now replaced with an analogous "enriched" functor $\mathcal{L}(\text{red},-)\colon\mathcal{L}\to [0,1]$. The former assigned to any word $y$ a particular set , and the latter now assigns to it a number . And we define that number to be the conditional probability that $y$ is an expression that extends the word "red," much like the "firetruck" example above. 

#### Revisiting Elementary Logic

We can then repeat the discussion surrounding elementary logic in Part 2 in this new enriched setting and form disjunction, conjunction, and implication between these "statistical" version of our functors, which again capture something of the meanings of expressions, but now in more holistic statistical sense. Things get a little more technical here, since one has to understand the appropriate version of products, coproducts, and internal homs in an enriched setting. (This takes us into the theory of weighted limits and colimits .) But the outcome turns out to be very simple to understand, and the details are discussed in the paper, so we won't dive into them here. 
 
I'll close with the remark that the unit interval $[0,1]$ is isomorphic to the category of nonnegative extended reals $[0,\infty]$ via the map $x\mapsto -\ln(x)$, and so we can also view language as a category enriched over $[0,\infty]$, which we think of as distances rather than probabilities. Such categories are called generalized metric spaces (for reasons explained here ), and it's interesting to ponder language from this metric-space perspective. It turns out to have close ties with tropical algebra and tropical geometry, an idea we explore towards the end of the paper. 
It's all on the arXiv. Hope you'll check it out! 

Share 

 Tweet 

 Share 

Related Posts 

#### Naming Functors

July 31, 2017 

in 
Category Theory 

#### What is an Adjunction? Part 3 (Examples)

September 26, 2019 

in 
Category Theory 

#### Applied Category Theory 2020

March 2, 2020 

in 
Other 

#### A Diagram is a Functor

January 10, 2018 

in 
Category Theory 
 
Leave a comment!
