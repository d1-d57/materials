<!-- SOURCE: https://www.math3ma.com/blog/limits-and-colimits-part-1 | captured 2026-07-19 | math3ma (Tai-Danae Bradley), free blog | curl+stdlib extract -->

# math3ma — Limits And Colimits Part 1 (captured)

Limits and Colimits, Part 1 (Introduction) 

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

January 2, 2018 

• 
Category Theory 

#### Limits and Colimits, Part 1 (Introduction)

I'd like to embark on yet another mini-series here on the blog. The topic this time? Limits and colimits in category theory ! But even if you're not familiar with category theory, I do hope you'll keep reading. Today's post is just an informal, non-technical introduction. And regardless of your categorical background, you've certainly come across many examples of limits and colimits, perhaps without knowing it! They appear everywhere  -  in topology, set theory, group theory, ring theory, linear algebra, differential geometry, number theory, algebraic geometry. The list goes on. But before diving in, I'd like to start off by answering a few basic questions. 
‍ 

#### What ARE limits and colimits?

They are a (and in some sense,  the most efficient)  way to construct a new object from an existing collection of objects. For example, suppose we were given a bunch of sets. Plain, old, vanilla-flavored sets. Can we use these to construct new sets? Definitely. We can isolate a single element and form a one-point set . We can isolate no  elements and form the empty set . We can form a quotient set. We can take a few sets and form their Cartesian product  or their fibered product,  or we can form their disjoint union . We can also look at their intersection or their (not-necessarily disjoint) union . And if we have a function from one set to another, we can look at the preimage of an element in its range. 
Each of the bold-faced words is an example of either a limit or a colimit.  
 
‍ 
‍ 

#### What's the difference between a limit and a colimit?

You'll notice that constructions above seem to come in two flavors. 

#### flavor #1: taking sub-things 

A single element, an intersection, a preimage, a product. These are all formed by picking out a sub-collection of elements from given sets, contingent on some condition. (Let's think of the product as a subset of itself. Bear with me.)  These are examples of limits. 

#### flavor #2: gluing things together 

A set with no elements, disjoint unions, not-necessarily-disjoint unions, and quotients are all formed by assembling or 'gluing' things together. (Let's think of forming the empty set by 'gluing'  no things together. Bear with me.)  These are examples of colimits.   
 
In practice, limits tend to have a "sub-thing" feel to them, whereas colimits tend to have a "glue-y" feel to them. That's terribly imprecise, but it's an intuitive feel for how mathematicians construct things. More formally, the defining property of a limit is characterized by maps whose domain  is the limit. On the other hand, the defining property of a colimit is characterized by maps whose codomain is the colimit. In this sense, limits and colimits are dual to each other.  
You'll notice I used the word "maps" instead of "functions." That's because set theorists aren't the only people who like to construct new things from existing things. As I mentioned in the opening paragraph, limits and colimits appear all across the mathematical landscape. A direct sum of abelian groups, the kernel of a group homomorphism, the direct product of vector spaces, the free product of groups, the least upper bound of a poset, and a CW complex are all examples of limits and colimits. 
‍ 
‍ 

#### What are some prerequisites for learning more about (co)limits?

Although category theory wasn't a prerequisite for today's post, it is  necessary for the remaining posts in this series. I'll assume familiarity with categories  and functors and natural transformations.  For a bird's eye view of the subject, check out What is Category Theory, Anyway?   At that link, you'll also find a list of suggested resources for further reading.  
 
By the way, in every discussion of limits and colimits there is a heavy emphasis on maps  - homomorphisms, functions, linear transformations, continuous functions, smooth functions, you name it. In fact, limits and colimits are defined in terms of a universal property . This emphasis on maps, or relationships ,   is a trademark of category theory and has roots in what I like to call the Yoneda perspective , which is the categorical maxim   that objects are completely determined by their relationships to other objects.I recommend taking a look at that post to get a better feel for how categorically-minded mathematicians think. With that said, you'll also want to be familiar with commutative diagrams . 
‍ 

#### Are (co)limits related to limits of sequences in topology and analysis?

No, not that I'm aware of. But there is one  similarity. In analysis, we ask for the limit OF a sequence. In category theory, we also ask for the (co)limit OF   something. But that "something" is not a sequence of points. 
So,  what is it ? 
That's where we'll pick up next time. 
‍ 
 
‍ 
 In this series: 

Share 

 Tweet 

 Share 

Related Posts 

#### Topology: A Categorical Approach

April 3, 2020 

in 
Topology 

#### The Yoneda Lemma

September 14, 2017 

in 
Category Theory 

#### Matrices as Tensor Network Diagrams

May 15, 2019 

in 
Algebra 

#### What is a Functor? Definition and Examples, Part 1

January 31, 2017 

in 
Category Theory 
 
Leave a comment!
