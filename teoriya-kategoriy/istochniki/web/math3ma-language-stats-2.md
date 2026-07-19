<!-- SOURCE: https://www.math3ma.com/blog/language-statistics-category-theory-part-2 | captured 2026-07-19 | math3ma (Tai-Danae Bradley), free blog | curl+stdlib extract -->

# math3ma — Language Statistics Category Theory Part 2 (captured)

Language, Statistics, & Category Theory, Part 2 

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

July 7, 2021 

• 
Category Theory 

#### Language, Statistics, & Category Theory, Part 2

 Part 1 of this mini-series opened with the observation that language is an algebraic structure. But we also mentioned that thinking merely algebraically doesn't get us very far. The algebraic perspective, for instance, is not sufficient to describe the passage from probability distributions on corpora of text to syntactic and semantic information in language that wee see in today's large language models . This motivated the category theoretical framework presented in a new paper I shared last time, whose abstract is shown on the right. But even before we bring statistics into the picture, there are some immediate advantages to using tools from category theory rather than algebra. One example comes from elementary considerations of logic, and that's where we'll pick up today. 
Let's start with a brief recap. 

#### Previously on Math3ma...

Last time we defined a category of language $\mathsf{L}$ whose objects are expressions in English (strings of words) and where there is a morphism between two expressions if one is contained as a substring of the other. This category is pretty bare-bones; it just tells us "what goes with what," a bit like syntax. To glean something about semantics we then passed to a better category $\mathsf{Set}^\mathsf{L}$ whose objects are functors $F\colon \mathsf{L}\to\mathsf{Set}$, which are just ways to assign a set to each expression in language in a way that's compatible with the substring containment of those expressions. Explicitly, a functor $F\colon \mathsf{L}\to\mathsf{Set}$ is an assignment of a particular set $F(y)$ to each expression $y$ in language with the property that if $y$ is contained as a substring of $z$, then $F(y)\subseteq F(z).$ Such functors are also called copresheaves , though let's just call them "functors" for now. 
 
The upshot is that different assignments yield different functors, and the main example to have in mind is the one introduced last time: For each expression $x$ in $\mathsf{L}$ there is a functor $F=\mathsf{L}(x,-)\colon \mathsf{L}\to\mathsf{Set}$ that assigns to an expression $y$ the set $F(y)=\mathsf{L}(x,y)$, which is defined to be the one-point set $\ast$ if $x$ is contained in $y$, or the empty set otherwise. As an example, if $x$ is the word "red," then we have 
 
where I am using the symbol $\leq$ as shorthand for " red is contained in $x$." Explicit examples include $\mathsf{L}(\text{red, beautiful red ruby})\cong \ast$ whereas $\mathsf{L}(\text{red, hot dog})=\varnothing$. Intuitively then, the functor $\mathsf{L}(\text{red},-)$ picks out the totality of ways that "red" fits into all other expressions in English. We're therefore inclined to think of it as a first approximation of the meaning of "red." 
 
We also mentioned that the category of functors $\mathsf{Set}^\mathsf{L}$ has rich mathematical structure, more so than the syntax category $\mathsf{L}$. Technically speaking, $\mathsf{Set}^\mathsf{L}$ has all colimits and all limits and is also Cartesian closed , among other nice things. The formal definitions aren't important for now. But having these properties (whatever they are) means we can make sense of the logical notions of disjunction and conjunction and implication inside the category $\mathsf{Set}^\mathsf{L}$, and hence — and quite crucially — between the "meanings" of expressions in language. 
Think about disjunction, for a moment. 
 
Suppose we have a pair of sets: The set $A$ of all things that have the color red (red lipstick, the French flag, stop signs,...) and the set $B$ of all things that have the color blue (a robin's egg, the French flag, blueberries,...). What is the set of all things that have either red or blue? It's another set, namely their union $A\cup B$. Nothing difficult there. But I mention this by way of analogy: just like we can take the union of sets, we can also perform an analogous operation on functors. But instead of calling it "the union," we give it different name: the coproduct. As we'll see below, the coproduct of the two functors representing "red" and "blue" is another functor that represents their disjunction, the concept of "red or blue." 
Before explaining the idea, you should know that "functors" and "coproducts" between them are standard concepts from category theory. You can find the definitions in any one of your favorite books on the subject. The newness for us is in reinterpreting these old ideas in new ways, in the context of language. So our present discussion can be viewed as a venture into "non-traditional applied mathematics," an idea we advocated a few weeks ago . 
In any case, here's the point: The functor $\mathsf{L}(\text{red},-)$ is a stand-in for the concept "red," and the functor $\mathsf{L}(\text{blue},-)$ is a stand-in the concept "blue." And so we have asked: 
 What functor might be a stand-in for the concept of "red or blue"? 
Answer: the coproduct . 

#### What is the meaning of "red or blue"?

The coproduct of functors $\mathsf{L}(\text{red},-)$ and $\mathsf{L}(\text{blue},-)$ is another functor from $\mathsf{L}$ to $\mathsf{Set}$, which we denote with a disjoint union symbol, $\mathsf{L}(\text{red},-)\sqcup\mathsf{L}(\text{blue},-)$. 
 
The notation may seem cumbersome, but this functor is extremely simple to understand. As with any functor from $\mathsf{L}$ to $\mathsf{Set}$, the coproduct assigns to each expression $y$ in language a particular set. In a happy turn of events, this set is actually built up from things we already know. We know what the set $\mathsf{L}(\text{red},y)$ is, since it's defined above. And so we also know what the set $\mathsf{L}(\text{blue},y)$ is. The coproduct simply assigns to $y$ the disjoint union of these two sets. 
 
After staring at this a little while, we can restate this more explicitly: The functor $\mathsf{L}(\text{red},-) \sqcup \mathsf{L}(\text{blue},-)\colon \mathsf{L}\to\mathsf{Set}$ assigns to a given expression $y$ one of three possible outputs: either 1)  the one-point set $\ast$ if $y$ contains the word "red" or the word "blue" but not both, or* 2) a set that's isomorphic to a two-element set if $y$ contains both "red" and "blue"; or 3) the empty set if $y$ contains neither "red" nor "blue." Here's a picture I have in mind: 
 
The output of the coproduct of our two functors representing "red" and "blue" is therefore nonempty on the union of all expressions in the language that contain "red" or "blue." And this is consistent with the role of union as logical "or" among sets. Voila! 
Now that we've just explored the string of analogies disjunction ~ union ~ coproduct (imagine the squiggle ~ means "is analogous to"), it's natural to wonder about the dual situation. Now that we know something about disjunction, what about conjunction? That is, what does category theory have to say about the concept "red and blue"? 
Thinking back to plain old sets, the set of all things that have both red and blue is simply the intersection $A\cap B$ of those two sets $A$ and $B$ defined above. So in some sense, unions are dual to intersections in the way that disjunction is dual to conjunction . What's more, there is an analogous story in category theory, as well. Coproducts of functors also have a dual construction, and it turns out to be a nice candidate for the conjunction of concepts in language. It's called the product . 

#### What is the meaning of "red and blue" ? 

Like the coproduct, the product of functors $\mathsf{L}(\text{red},-)$ and $\mathsf{L}(\text{blue},-)$ is another functor from $\mathsf{L}$ to $\mathsf{Set}$, which we denote with a multiplication symbol, $\mathsf{L}(\text{red},-)\times\mathsf{L}(\text{blue},-)$. 
 
And again like the coproduct, the notation might look cumbersome, though it's very easy to understand. This functor assigns to each expression $y$ in the category $\mathsf{L}$ a particular set, which again happens to be built up from the individual pieces we already know. In this case, it's the Cartesian product of the individual sets $\mathsf{L}(\text{red},y)\times \mathsf{L}(\text{blue},y)$. That means it consists of all pairs $(a,b)$ where $a$ is an element in the first set, and $b$ is an element in the second set. Importantly, this set of pairs is non-empty only when $\mathsf{L}(\text{red},y)$ and $\mathsf{L}(\text{blue},y)$ are each nonempty — that is, when the expression $y$ contains "red" and when $y$ contains "blue." In that case, the Cartesian product consists of the single pair $(\ast,\ast)$ and is thus itself isomorphic to $\ast$. So the product of our two functors makes the following assignment: 
 
The output of the product is therefore nonempty on the intersection of expressions that contain "red" with those that contain "blue," and this pairs well with the role of intersection as logical "and" among sets. Voila! 
Here's the picture I like to have in mind: 
 
So, we can make some sense of disjunction and conjunction in our category of functors on language. This is a nice advantage over a merely algebraic approach to language. As we mentioned last time, one might be tempted to represent the meaning of words by the two-sided principal ideals associated to them. But the union of ideals isn't an ideal! So it's not immediately clear how to proceed in that setting. But as we've just seen, the situation is much clearer in category theory. 
In fact, we can do even more. 
The category $\mathsf{Set}^\mathsf{L}$ has enough structure that we can make sense of logical implication as well. This construction takes a little more work to explain, so I'll just give you the Reader's Digest version below. But first, here's the intuition to keep in mind. (Or just skip to the next section for the punchline.) It turns out our category of functors $\mathsf{Set}^\mathsf{L}$ has structure that is very similar to that found in a Heyting algebra . A Heyting algebra is the name given to a set equipped with a partial order $\leq$ that has all finite meets $\wedge$ and joins $\vee$ and has the additional feature that for every pair of elements $b$ and $c$ there is a third element denoted $b\Rightarrow c$, read "$b$ implies $c$," that is characterized by the following: 
 
for all elements $a,b,c$. Heyting algebras, as many of you know, are nice places to do propositional intuitionistic logic. Importantly, that "if and only if" statement above is actually an example of a categorical adjunction , and a more sophisticated analogue of this adjunction exists in our language category of functors. In other words, the category $\mathsf{Set}^{\mathsf{L}}$ is "like" a Heyting algebr, in that it is Cartesian closed . Roughly speaking, this means that for every pair of functors $B,C\colon \mathsf{L}\to\mathsf{Set}$ there another functor called the internal hom , which I'll denote by $B\Rightarrow C$. It is characterized by the following bijection of sets: 
 
for all functors $A,B,C$ where $\times$ is the product operation described above. Notice that if you replace the times symbol $\times$ by a meet $\wedge$, and if you replace the isomorphism $\cong$ by "if and only if," then this looks similar to the implication condition in a Heyting algebra above. Except, things have ramped up pretty quickly. To understand this beefed-up situation, you have to know what a natural transformation is! So let's not worry about all of this. I mention it only for those who are curious. (The details may be found in Section 1.2.3 of our preprint .) 
The good news is that it's relatively easy to describe the functor $B\Rightarrow C$ in the very special case we're interested in, namely when $B=\mathsf{L}(\text{red},-)$ is the functor representing the concept "red" and when $C=\mathsf{L}(\text{blue},-)$ is the functor representing the concept "blue." 
As we'll now see, the internal hom $\mathsf{L}(\text{red},-)\Rightarrow\mathsf{L}(\text{blue},-)$ is another functor that represents the concept of "red implies blue." 
But what does that mean, exactly? 

#### What is the meaning of "red implies blue?"

Like the coproduct and the product of the functors $\mathsf{L}(\text{red},-)$ and $\mathsf{L}(\text{blue},-)$, the internal hom between them is another functor from $\mathsf{L}$ to $\mathsf{Set}$, which I'll denote with an implication symbol**, $\mathsf{L}(\text{red},-)\Rightarrow\mathsf{L}(\text{blue},-)$. 
 
As before, this is a functor from $\mathsf{L}$ to $\mathsf{Set}$, and so it assigns to each expression $y$ a particular set $(\mathsf{L}(\text{red},-)\Rightarrow\mathsf{L}(\text{blue},-))(y)$. Explaining the recipe to construct this set takes a little more work than I'd like to do now, so I'll summarize it this way: It turns out that the set assigned to $y$ under this implication functor is built up from all expressions in language that contain both "red" and "blue," along with expressions containing "blue" but not "red," along with  expressions containing neither "blue" nor "red." Here's a picture I have in mind: 
 
Notice how this pairs perfectly with the familiar truth table associated to implication below on the left! In fact, unwinding the implication functor gives us an analogous "truth table" for functors as shown below on the right. All details are provided in Section 1.2.3 of the paper for those who are interested. 

#### Nice, but where are the statistics?

Hopefully it's now evident that exploring language from a category theoretical perspective has advantages over a mere algebraic approach. As we've seen today, there there's a nice, systematic way to pass from a category of syntax $\mathsf{L}$ to a category of semantics $\mathsf{Set}^\mathsf{L}$, where one has tools to combine the meanings of expressions in the latter just by following a few elementary thoughts on logic. 
This is good, but it's still not the whole story. As we mentioned last time , language also exhibits statistical structure and this plays a pivotal role, as evidenced in the success of today's statistical language models . So what we'd really like to do is retrace our steps and incorporate statistics into our language category $\mathsf{L}$ and then pass to the statistical version of the semantics category and have our discussions of elementary logic there. 
So that's what we'll do next time! 
 
*This second set was inadvertently listed as the one-point set in our preprint. Thanks to Michael Vejdemo-Johansson for pointing this out! 
**Category theorists typically denote internal homs with square brackets, though I'm making a departure from this here. 
‍ 
‍ 

Share 

 Tweet 

 Share 

Related Posts 

#### Limits and Colimits, Part 2 (Definitions)

January 30, 2018 

in 
Category Theory 

#### What is a Category? Definition and Examples

January 23, 2017 

in 
Category Theory 

#### What is a Natural Transformation? Definition and Examples, Part 2

February 13, 2017 

in 
Category Theory 

#### Language, Statistics, & Category Theory, Part 3

July 28, 2021 

in 
Category Theory 
 
Leave a comment!
