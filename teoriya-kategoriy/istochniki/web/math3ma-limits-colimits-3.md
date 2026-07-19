<!-- SOURCE: https://www.math3ma.com/blog/limits-and-colimits-part-3 | captured 2026-07-19 | math3ma (Tai-Danae Bradley), free blog | curl+stdlib extract -->

# math3ma — Limits And Colimits Part 3 (captured)

Limits and Colimits Part 3 (Examples) 

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

January 21, 2019 

• 
Category Theory 

#### Limits and Colimits Part 3 (Examples)

Once upon a time, we embarked on a mini-series about limits and colimits in category theory.  Part 1  was a non-technical introduction that highlighted two ways mathematicians often make new mathematical objects from existing ones: by taking a subcollection of things, or by gluing things together. The first route leads to a construction called a limit, the second to a construction called a colimit . 
 
The formal definitions of limits and colimits were given in  Part 2 . There we noted that one speaks of "the (co)limit of [something]." As we've seen previously , that "something" is a diagram— a functor from an indexing category to your category of interest. Moreover, the shape of that indexing category determines the name of the (co)limit: product, coproduct, pullback, pushout, etc. 
In today's post, I'd like to solidify these ideas by sharing some examples of limits. Next time we'll look at examples of colimits. What's nice is that all of these examples are likely familiar to you—you've seen (co)limits many times before, perhaps without knowing it! The newness is in viewing them through a categorical lens.  
Let's start by fixing some notation: 
The category $\mathsf{Set}$ has sets as objects and functions as morphisms. 
The category $\mathsf{Top}$ has topological spaces as objects and continuous functions as morphisms. 
The category $\mathsf{Group}$ has groups as objects and group homomorphisms as morphisms. 
The category $\mathsf{Ring}$ has unital rings as objects and unit-preserving ring homomorphisms as morphisms. 
The category $\mathsf{FVect}$ has finite-dimensional vector spaces over a fixed field as objects and linear transformations as morphisms. 
Any poset $P$ is a category: it has its elements $p,q,\ldots$ as objects and there is a morphism $p\to q$ whenever $p\leq q$. The next two bullets are examples. 
The natural numbers $\mathbb{N}$ (let's include 0) form a poset: natural numbers $n,m,\ldots$ are the objects of this category and we'll write $n\leq m$ and/or draw an arrow $n\overset{k}{\longrightarrow} m$ whenever $m=nk$ for some integer $k$, that is, whenever $m$ is divisible by $n$. For example, there's an arrow $2\overset{4}{\longrightarrow} 8$ but there is no arrow from $2$ to $5$.  
The extended set of non-negative real numbers $[0,\infty]$ is also a poset: there is an arrow $x\overset{\leq}{\longrightarrow}y$ whenever $x\leq y$ in the usual sense. 
Now, recall from Part 2 that the limit of a diagram consists of two things: an  object  and  map(s) out of that object.  These data satisfy a certain property, namely the  universal property as outlined before . Below I'll list five examples of limits: (1) terminal object, (2) product, (3) pullback, (4) inverse limit, (5) equalizer. Each example will contain seven sub-examples: one for each of the seven categories listed above. In these sub-examples, I'll only identify the object  and the map(s)  that comprise the limit. You're welcome to verify that the universal property is satisfied. In particular, try to show the existence of the unique map into the limit. That's the key to everything! (I've done it for us in Example 1.) 

#### Example 1: Terminal object 

In a category $\mathsf{C}$, the limit of the empty diagram—the diagram with no objects and no morphisms—is called the  terminal object . The terminal object is an object $t$ in $\mathsf{C}$ with the property that for  every  object $c$ there is a unique morphism $c\to t$. The terminal object, then, is an object for which there's only one way to map to it—all objects terminate at it.  
 
Here are some examples. 

#### In $\mathsf{Set}$

The terminal object in $\mathsf{Set}$ is the one-point set $\ast$. If $S$ is any set, there is only one possible function $S\to\ast$, namely the one that sends everything to $\ast$. 

#### In $\mathsf{Top}$

The terminal object in $\mathsf{Top}$ is the  one-point space  $\ast$, i.e. the one-point set equipped with the indiscrete topology. If $X$ is any space, there is only  one  possible continuous function $X\to\ast$, namely the one that sends everything to $\ast$. 

#### In $\mathsf{Group}$

The terminal object in $\mathsf{Group}$ is the group with one element $\{e\}$. If $G$ is any group, there is only one possible group homomorphism $G\to\{e\}$, namely the one that sends everything to $e$. 

#### In $\mathsf{Ring}$

The terminal object in $\mathsf{Ring}$ is the zero ring $\{0\}$ whose single element is $0=1$. If $R$ is any ring, there is only one ring homomorphism $R\to \{0\}$, namely the one that sends everything to 0. 

#### In $\mathsf{FVect}$

The terminal object in $\mathsf{FVect}$ is the zero vector space $\{\mathbf{0}\}$ whose single vector is $\mathbf{0}$. If $V$ is any vector space, there is only one linear transformation $V\to\{0\}$, namely the one that sends everything to $\mathbf{0}$. 

#### In a Poset

The terminal object in a poset $P$ is its greatest element , if it exists. That is, it's an element $g$ such that $p\leq g$ for all elements $p$ in $P$. 

#### In $\mathbb{N}$

The terminal object in the poset $\mathbb{N}$ is $0$ since $0$ is divisible by every natural number. 

#### In $[0,\infty]$

The terminal object in the poset $[0,\infty]$ is $\infty$ since $x\leq \infty$ is true for all $x$ in the set. 

#### A remark

Not every category has a terminal object. But if it does, then it's unique. For example, the full (non-extended) real line $\mathbb{R}$ is a poset without a greatest element, therefore it's a category without a terminal object! 

#### Example 2: Product 

In a category $\mathsf{C}$, the limit of a discrete diagram , i.e. one that has the shape $\bullet\quad\bullet\quad \bullet\quad\cdots$ is called the  product . The product consists of an object $c$ together with a morphism from $c$ to each object in the diagram, satisfying the universal property.  

#### In $\mathsf{Set}$

If the $A_1\quad A_2 \quad\cdots$ are sets, then their product is comprised of 
the Cartesian product $\prod_i A_i$. Concretely, this the set whose elements are sequences $(a_1,a_2,\ldots)$ where the $i$th entry $a_i$ is an element in $A_i$. 
projection maps $\prod_iA_i\to A_i$ into each of the factors. 
Although the discrete diagram (in red) above has just countably many sets, it may consist of arbitrarily many of them. The Axiom of Choice says that the limit of  that  diagram exists. 

#### In $\mathsf{Top}$

In $\mathsf{Top}$, the product of topological spaces $X_1\quad X_2\quad \ldots$ is comprised of 
the Cartesian product $\prod_i X_i$ equipped with the product topology . Concretely, the points in this space are sequences $(x_1,x_2,\ldots)$ where the $i$th factor $x_i$ is an element in $X_i$.  
projection maps $\prod_i X_i\to X_i$ to each of the factors.  
The product topology is the  coarsest  topology on $\prod_i X_i$ for which these projection maps are continuous. 

#### In $\mathsf{Group}$

In $\mathsf{Group}$, the product of groups $G_1 \quad G_2 \quad\cdots$ is comprised of 
their direct product $\prod_i G_i$. Concretely, it's a group whose elements are sequences $(g_1,g_2,\ldots)$. The group operation is given componentwise. The identity element is the sequence $(e_1,e_2,\ldots)$ where $e_i$ is the identity in $G_i$.  
projection maps $\prod_i G_i\to G_i$ to each of the factors. One has to verify that the projection $(g_1,g_2,\ldots)\mapsto g_i$ for each $i$ is a group homomorphism. 

#### In $\mathsf{Ring}$

In $\mathsf{Ring}$, the product of rings $R_1 \quad R_2 \quad\cdots$ is comprised of 
their direct product $\prod_i R_i$. Concretely, it's a ring whose elements are sequences $(r_1,r_2,\ldots)$ where $r_i\in R_i$. Addition and multiplication are given componentwise. The unit is the sequence of units.  
projection maps $\prod_iR_i\to R_i$ down to each of the factors. One has to verify that the projection $(r_1,r_2,\ldots)\mapsto r_i$ for each $i$ is a ring homomorphism. 

#### In $\mathsf{FVect}$

In $\mathsf{FVect}$, the product of vector spaces $V_1 \quad V_2\quad\cdots$ is comprised of 
their direct product $\prod_iV_i$. Concretely, it's a vector space whose elements are sequences $(\mathbf{v}_1,\mathbf{v}_2,\ldots)$ where $\mathbf{v}_i\in V_i$. Addition and scalar multiplication are given componentwise. The zero vector is the sequence of zero vectors. Note: If there are only finitely many $V_i$, then the direct product is the same as—literally the SAME as—the direct sum, which, as we'll see in Part 4, is the colimit (a.k.a coproduct) of the same diagram. 
projection maps $\prod_i V_i\to V_i$ down to each of the factors. One has to verify that the projection $(v_1,v_2,\ldots)\mapsto v_i$ for each $i$ is a linear transformation. 

#### In a Poset

In a poset $P$, the product of a set of elements $p_1,p_2,\ldots$ is 
the greatest lower bound , or meet , $\bigwedge_ip_i$ of $\{p_1,p_2,\ldots\}$ 

#### In $\mathbb{N}$

In the poset $\mathbb{N}$, the product of a set of integers $n_1,n_2,\ldots$ is 
the greatest common divisor  of $n_1,n_2,\ldots$ 

#### In $[0,\infty]$

In the poset $[0,\infty]$ the product of a set of non-negative numbers (possibly infinity) $x_1,x_2,\ldots$ is 
the minimum of $x_1,x_2,\ldots$ 

#### A remark

Products may not always exist! For example the category of fields and field homomorphisms does not have all products. That's because the characteristic of a field puts a restriction on morphisms to/from it. Likewise, not every poset has all products. But a special name is given to posets for which the product of every finite subset exists. They are called  meet-semilattices .  

#### Interlude 

By now you've surely noticed things were getting redundant. The products in $\mathsf{Set, Top, Group, Ring,}$ and $\mathsf{FVect}$ all feel the same. In each case, the limit of the discrete diagram is just the Cartesian product, endowed with extra structure when needed. That's because topological spaces, groups, rings, and vector spaces are ultimately just sets with extra stuff. A topological space is a set with a topology. A group is a set with an associative binary operation. A ring is a set with two associative binary operations, one of which is also commutative. A vector space is a set with an associative binary operation and with an action from a field. 
In short, $\mathsf{Set, Top, Group, Ring,}$ and $\mathsf{FVect}$ are examples of concrete categories . That's the name giving to a category whose objects are ultimately just sets. ( Here's the technical definition .) Not all categories are concrete categories, but all the ones in this discussion are—even posets!  
Anyway, the remaining three examples—pullbacks, inverse limits, and equalizers—will have the same feel: the limit of a particular diagram in $\mathsf{Set, Top, Group, Ring, FVect}$ will be a set (the same set in each case) endowed with the appropriate structure. For that reason, I'll simply give the general description. We'll also be able to simplify our discussion of limits in posets, but I'll say more on that later. 
Something else to notice: In a discrete diagram, which was the focus of Example 2, there were no morphisms between objects. For instance, when we looked at the Cartesian product of sets $A\times B$, there was no mention of a function $A\to B$. That won't be the case in Examples 3, 4, and 5. There, the objects in the diagrams will have morphisms between them, and defining those morphisms in different ways will lead to different things. 
Speaking of the product, it's often fruitful to look at a subset of the product $A\times B$ rather than the full thing. That is, it's often interesting to consider only those pairs $(a,b)$ where $a$ and $b$ relate to each other in a certain way. Which way ? Examples 3 and 4—pullbacks and inverse limits—provide an answer. 
 
‍ 

#### Example 3: Pullback 

In a category $\mathsf{C}$, the limit of a diagram of the shape ${\color{gray}\bullet}\longrightarrow \bullet \longleftarrow\circ$ is called a  pullback or fibered product . Explicitly, the pullback consists of an object $c$ together with two morphisms $c\to {\color{gray}\bullet}$ and $c\to\circ$ satisfying the universal property.  

#### In $\mathsf{Set},\mathsf{Top},\mathsf{Group}, \mathsf{Ring},$ and $\mathsf{FVect}$

If $\mathsf{C}$ is any one of these five categories, then the pullback is a subobject of a Cartesian product. Explicitly, if $A,B,C$ are objects in $\mathsf{C}$, then the pullback of the diagram $A\overset{f}{\longrightarrow} C\overset{g}{\longleftarrow} B$ consists of 
the sub(set/space/group/ring/space) of the product $A\times B$ consisting of those pairs $(a,b)$ such that $fa=gb$. This object is often denoted $A\times_C B$.  
two morphisms $A\times_C B\to A$ and $A\times_C B\to B$. The first projects onto the first factor, $(a,b)\mapsto a$; the second projects onto the second factor, $(a,b)\mapsto b$. 
Diagrammatically, the situation looks like this: 
 
To emphasize: what $A\times_C B=\{(a,b)\mid fa=gb\}$ actually "looks like" will totally depend on how the morphisms $A\overset{f}{\longrightarrow} C\overset{g}{\longleftarrow} B$ are defined. They're part of the data you start with, so you get to decide what they are. Your decision will influence $A\times_C B$. Sadly, the notation doesn't indicate this. Maybe something like $A \times_{C,f,g} B$ would be better. Er, maybe not. Here are a few examples of pullbacks in $\mathsf{Set}$. 
 Example 1: Cartesian product 
If $C=\ast$ is the one-point set, then both $A\overset{f}{\longrightarrow}\ast$ and $B\overset{g}{\longrightarrow}\ast$ are the unique functions that send everything to $\ast$. (As we know, $\ast$ is the terminal object in $\mathsf{Set}$!) So the pullback of the diagram is the set of all pairs $(a,b)$ such that both $a$ and $b$ map to $\ast$ under $f$ and $g$. But every pair satisfies this! The pullback of the diagram is thus the entire set $A\times B$. 
 
 Example 2: Preimage of a function 
If instead $B=\ast$ is the one-point set, and $C$ is any set, then a function $\ast\overset{g}{\longrightarrow} C$ picks out an element $c\in C$. So for any function $A\overset{f}{\longrightarrow}C$, the pullback is the subset of elements in $A$ that map to $c$ under $f$. In other words, it's the preimage of $c$ under $f$. 
 
 Example #3: Intersection 
If $A$ and $B$ are subsets of $C$ and if $f$ and $g$ are inclusion maps, then the pullback of the diagram consists of all pairs $(a,b)$ such $a$ and $b$ are equal after you remember that they both live in the larger set $C$ (i.e. after you include them into $C$ via $f$ and $g$). That's just the fancy way of asking for the elements in $A$ and $B$ that are equal to each other. And that's another way of asking for the elements in $A$ that are also in $B$ and vice versa. So the pullback is the intersection $A\cap B$! 

#### In a Poset

In a poset $P$, the pullback of a diagram $p\overset{\leq}{\longrightarrow}r\overset{\geq}{\longleftarrow}q$ is—as in the case of the discrete diagram—the  greatest lower bound  or meet of $p$ and $q$. To see why this is true, it helps to spell out the universal property: 

#### In $\mathbb{N}$

In the poset $\mathbb{N}$, the pullback of a diagram $n\overset{k}{\longrightarrow}a\overset{\ell}{\longleftarrow}m$ is the greatest common divisor of $n$ and $m$. To see why this is true, it helps to spell out the universal property: 

#### In $[0,\infty]$

In the poset $[0,\infty]$, the pullback of a diagram $x\overset{\leq}{\longrightarrow}z\overset{\geq}{\longleftarrow}y$ is the minimum of $x$ and $y$. To see why this is true, it helps to spell out the universal property: 

#### A remark

You'll notice that the pullback in a poset is the same as the product.  Is that a coincidence?  No! As it turns out, the limit of  any  non-empty diagram in a poset is  always  the greatest lower bound of the elements in the diagram.  
 
This follows from the universal property. In particular, the presence of morphisms in the diagram doesn't obviate the fact that whatever the limit is, it must be 1) smaller than every element in the diagram and 2) bigger than any other element that's  also  smaller than every element in the diagram. But that's what it means to be the greatest lower bound! 

#### Example 4: Inverse Limit 

In a category $\mathsf{C}$, the limit of a diagram of the shape $\bullet\leftarrow\bullet\leftarrow\bullet\leftarrow\cdots$ is called an inverse limit. It consists of an object $c$ together with morphisms $c\to \bullet$ that make each triangle commute (see below) and which satisfy the universal property.  

#### In $\mathsf{Set},\mathsf{Top},\mathsf{Group}, \mathsf{Ring},$ and $\mathsf{FVect}$

If $\mathsf{C}$ is any one of these five categories, then the inverse limit is a certain subset of the Cartesian product of the objects in the diagram, equipped with the appropriate structure. Explicitly, if $A_1,A_2,\ldots$ are objects in $\mathsf{C}$ then the inverse limit of the diagram $$A_1\overset{f_1}{\longleftarrow} A_2\overset{f_2}{\longleftarrow}  A_3\overset{f_3}{\longleftarrow} \cdots$$ consists of 
a sub(set/space/group/ring/space) of the product $\prod_iA_i$. Which subset? The one containing all sequences $(a_1,a_2,\ldots)$ where the $i$th factor is in the image of the $i$th map $f_i$, i.e. so that $f_i(a_{i+1})=a_i$. This subobject is sometimes denoted $\varprojlim A_i$. 
morphisms $\varprojlim A_i\to A_i$ that project a sequence $(a_1,a_2,\ldots)$ onto its $i$th factor $a_i$. 
Diagrammatically, the situation looks like this: 
 
I'd like to emphasize that the inverse limit—which sounds fancy—is just a subset (or space or group or...) of the Cartesian product—which is not so fancy. So the notation $\varprojlim A_i$ is just meant to denote the totality of all things that look like $(a_1,a_2,\ldots).$ Well, not all those things. Only those that satisfy this equation: $$(a_1,a_2,a_3,\ldots)= (fa_2,fa_3,fa_4,\ldots)$$ which is to say that each entry $a_i$ is obtained by applying the appropriate map $f_i$ to the following entry $a_{i+1}$. If we were to erase  the $f_i$ from the graphic above, then the diagram would be a discrete diagram and its limit would be the full Cartesian product! So adding those morphisms between the $A_i$ puts a restriction on the kind of sequences we're interested in. 
By the way, the diagram above is a commutative diagram, which means each little triangle commutes: When we start with a sequence $(a_1,a_2,\ldots)$ and project it onto the third factor, $a_3$, say, we can then apply $f_2$ to get $f_2(a_3)$. But that should be the same  as just projecting down to the second factor $a_2$. And it is! By commutativity, $f_2(a_3)=a_2$. Here's an example in $\mathsf{Set}$. 
 Example #1: Intersection 
 
 Example #2: (Classical) limit 
Do categorical limits relate to the usual $\epsilon-\delta$ limits in any way? I like Emily Riehl's Example 4.10 here. 

#### In a poset such as $\mathbb{N}$ or $[0,\infty]$

As per our remarks above, the inverse limit in a poset is the greatest lower bound of the elements that appear in the diagram. 

#### A remark

When reading about inverse limits (on  Wikipedia , say) you might've seen the "additional" requirements that the $f_i$ must compose with each other and that each object $A_i$ has an identity morphism. Indeed, the diagram $A_1\leftarrow A_2\leftarrow\cdots$ is the image of a functor from the indexing category $\bullet\leftarrow\bullet\leftarrow\cdots$. That indexing category has both composite and identity arrows, even though we've not drawn them, and functors preserve these things. 
As another remark, I've indexed our objects $A_i$ using $\mathbb{N}$ with the usual ordering $\leq$, but any poset will do. 

#### Example 5: Equalizer 

In a category $\mathsf{C}$, the limit of a diagram with two parallel arrows is called the  equalizer.  (As before, each bullet is an object in $\mathsf{C}$.) The equalizer consists of an object $c$ together with a morphism $c\to \bullet$ into the first bullet satisfying the universal property.  

#### In $\mathsf{Set},\mathsf{Top},\mathsf{Group}, \mathsf{Ring},$ and $\mathsf{FVect}$

When $\mathsf{C}$ is any one of these five categories, the equalizer is a subobject of the first object in the diagram; the morphism is given by inclusion. Explicitly, if $A$ and $B$ are objects in $\mathsf{C}$, then the equalizer of the diagram on the right consists of 
the sub(set/space/group/ring/space) $eq(f,g)$ of elements $a\in A$ satisfying $fa=ga$.  
the inclusion map $eq(f,g)\hookrightarrow A$. 
Diagrammatically, the situation looks like this: 
 
As before, what $eq(f,g)$ actually "looks like" will totally  depend how the morphisms $f$ and $g$ are defined. And why the name equalizer ? You can think of it as comprised of all the elements in $A$ that become equal after passing through $f$ and $g$. Here are a couple of examples. The first is in $\mathsf{Set}$. The second is in $\mathsf{Group}$. 
 Example #1: Preimage of a function 
 
The next example is exactly the same, except $A$ and $B$ are groups and $b=e$ is the identity element. 
 Example #2: Kernel 

#### In a poset such as $\mathbb{N}$ or $[0,\infty]$

As per our remarks above, the inverse limit in a poset is the  greatest lower bound  of the two elements that appear in the diagram. In particular, it's just the element on the left! 

#### Some Takeaways... 

After reading through these examples, you may've gotten the feeling that a limit is, in some sense, either a product  or a subobject of the product, where the subobject is determined by a set of  equations . This is more than just a feeling! It's a theorem . If a category has all  products  and all  equalizers , then it has all limits! Categories that have all ( small ) limits are given a special name: complete . (This is a nod to complete metric spaces.) Six examples in this post—$\mathsf{Set, Top, Group, Ring}, \mathbb{N},$ and $[0,\infty]$—are all complete categories. 
Next time* in Part 4, we'll repeat today's discussion with colimits in place of limits. As expected, the duality comes by "reversing all the arrows." But don't let that fool you into thinking nothing interesting will happen! As it turns out, colimits are a little more involved than limits. Indeed, gluing things together requires more work than just looking at them. 
To wrap up today's discussion, here's a summary of today's post along with a preview for next time. 

* I know, I know. T here's a year's gap between Part 2 and Part 3! Yikes. It's been a busy year, friends. In fact, I haven't had the chance to write Part 4 yet, but I suspect it won't take another year. In the mean time, I do hope you'll enjoy today's math! 
 
 In this series: 

‍ 
‍ 

Share 

 Tweet 

 Share 

Related Posts 

#### Language, Statistics, & Category Theory, Part 1

June 29, 2021 

in 
Category Theory 

#### Topology: A Categorical Approach

April 3, 2020 

in 
Topology 

#### At the Interface of Algebra and Statistics

April 13, 2020 

in 
Probability 

#### What is a Functor? Definition and Examples, Part 1

January 31, 2017 

in 
Category Theory 
 
Leave a comment!
