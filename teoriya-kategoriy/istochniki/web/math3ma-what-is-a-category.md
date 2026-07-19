<!-- SOURCE: https://www.math3ma.com/blog/what-is-a-category | captured 2026-07-19 | math3ma (Tai-Danae Bradley), free blog | curl+stdlib extract -->

# math3ma — What Is A Category (captured)

What is a Category? Definition and Examples 

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

January 23, 2017 

• 
Category Theory 

#### What is a Category? Definition and Examples

As promised, here is the first in our triad of posts on basic category theory definitions: categories, functors, and natural transformations. If you're just now tuning in and are wondering what is category theory, anyway?   be sure to   follow the link to find out! Category theory takes a bird's eye view of mathematics. From high in the sky, details become invisible, but we can spot patterns that were impossible to detect from ground level. - Tom Leinster 

#### What is a category?

 A category $\mathsf{C}$ consists of some data that satisfy certain properties: 

#### The Data

a class of objects , $x,y,z,\ldots$ 
a set* of morphisms between pairs of objects; $x\overset{f}{\longrightarrow} y$ means "$f$ is a morphism from $x$ to $y$," and the set of all such morphisms is denoted $\text{hom}_{\mathsf{C}}(x,y)$ 
a composition rule: whenever the codomain of one morphism matches the domain of another, there is a morphism that is their composition, i.e. given $x\overset{f}{\longrightarrow} y$ and $y\overset{g}{\longrightarrow} z$ there is a morphism $x\overset{g\:\circ f}{\longrightarrow} z$. 

#### The Properties

Each object $x$ has an identity morphism $x\overset{\text{id}_x}{\longrightarrow} x$ which satisfies $\text{id}_y\circ f=f=f\circ\text{id}_x$ for any $x\overset{f}{\longrightarrow} y$. 
The composition is associative : $(h\circ g)\circ f = h\circ(g\circ f)$ whenever $$x\overset{f}{\longrightarrow}y\overset{g}{\longrightarrow}z\overset{h}{\longrightarrow}w.$$ 
Here's a picture of a category with four objects--depicted as bold dots instead of letters--and some morphisms between them. The gray arrow at each object indicates its identity morphism. 
‍ 
 
 Last time I listed a few examples of categories but never provided the proofs. To make sure you're comfortable with the definition, try proving a few of them. For example, to form the category of groups, we declare the objects to be groups and the morphisms to be group homomorphisms. But we should check: is the composition of two group homomorphisms another group homomorphism? (Or is it merely a function?) Is this composition associative? And is the identity function from a group to itself a group homomorphism? (Or, again, is it merely a function?) 
I also mentioned briefly that every poset (a set with a binary relation that is reflexive, transitive, and antisymmetric) is a category. This turns out to be a useful example, so let's be explicit. 
‍ 

#### Example #1: a poset

Every poset $P$ forms a category. The objects are the elements of $P$ and there is a morphism $x\to y$ whenever $x\leq y$. 

Composition holds because of transitivity: if $x\leq y$ and $y\leq z$ then $x\leq z$.

The identity-morphism property holds because of reflexivity: $x\leq x$ is always true. Therefore there is an arrow $x\overset{\text{id}_x}{\longrightarrow} x$ satisfying $f\circ\text{id}_x=f$ for any morphism $f$,

and similarly $\text{id}_y\circ f=f$. 

Associativty holds too. (What would the picture for this look like?) In particular, we've just shown that $\mathbb{Z},\mathbb{Q}$, and $\mathbb{R}$ are all categories! We could have deduced this from the next example as well.

#### Example #2: a group

Every group $G$ can be viewed as a category---called $\mathsf{B}G$ (for cool reasons )---with a single object which we'll denote by $\bullet$. There is a morphism $\bullet\overset{g}{\longrightarrow}\bullet$ for each element $g\in G$, and composition holds since $G$ is closed under the group operation. That is, if $g,h\in G$ so that $\bullet\overset{g}{\longrightarrow}\bullet\overset{h}{\longrightarrow}\bullet$ are two composable morphisms, then there is a third morphism $\bullet\overset{hg}{\longrightarrow}\bullet$ that is their composition, namely the one corresponding to the element $hg\in G$. Finally, the group identity $e\in G$ serves as the identity morphism for $\bullet$, and associativity holds because the group operation is associative.

‍ 
‍ 

#### Example #3: new categories from old ones

A very natural question that you might ask upon discovering new mathematical ideas is How can I construct new objects from given ones?** In particular one could ask, How can I make a new category from old ones? There are several ways to go about this. Given two categories $\mathsf{C}$ and $\mathsf{D}$, you might try defining their product $\mathsf{C}\times\mathsf{D}$. (This paves the way for monoidal categories .) What do you think the objects in $\mathsf{C}\times\mathsf{D}$ should be? The morphisms? 

  Additionally, every category $\mathsf{C}$ has an opposite category $\mathsf{C}^{op}$. The only difference between a category and its opposite is the direction in which the arrows/morphisms point. That is, the objects in $\mathsf{C}^{op}$ are exactly the same as objects in $\mathsf{C}$, but there is a morphism $x\to y$ in $\mathsf{C}^{op}$ whenever there is morphism $y\to x$ in $\mathsf{C}$. (Check that $\mathsf{C}^{op}$ really does satisfy the definition of a category.) In other words,
$$
\text{hom}_{\mathsf{C}^{op}}(x,y)=\text{hom}_{\mathsf{C}}(y,x).
$$

Another example of a category formed from existing ones is  $\mathsf{Cat}$. Here, the objects are categories*** $\mathsf{C},\mathsf{D},\mathsf{E}, \mathsf{F},\ldots,$ and the morphisms between them are functors. I'm jumping the gun a bit on this one since I haven't defined functors on the blog yet, but I think it's worth a mention. As we discussed last time, it's helpful to think of a morphism/arrow as a relationship between its domain and codomain. So naturally, we might take interest in relationships, i.e. functors , between categories.

You can also construct a new category $\mathsf{D}^\mathsf{C}$ from given categories $\mathsf{C}$ and $\mathsf{D}$ by declaring the objects to be functors $F:\mathsf{C}\to\mathsf{D}$. (The notation $\mathsf{D}^\mathsf{C}$ is quite suggestive .) Here a morphism between two functors $F:\mathsf{C}\to\mathsf{D}$ and $G:\mathsf{C}\to\mathsf{D}$ is a natural transformation , often denoted by a double arrow $F\Longrightarrow G$. In the special case when $\mathsf{D}=\mathsf{Set}$, the objects of $\mathsf{Set}^{\mathsf{C}^{op}}$ are given the name presheaves . Again, I'm jumping the gun here, but I expect these examples to resurface later on the blog, so now is a good time to mention them.

We'll chat about functors next week and natural transformations the following week. I encourage you to revisit Example #3 once you're familiar with these notions.

Until next week!
  
‍ 
 
‍ 
 *A category $\mathsf{C}$ where for all objects $x,y$, $\text{hom}_{\mathsf{C}}(x,y)$ is small enough to be an honest-to-goodness set is called a locally small category. In other words, a category is locally small if there aren't too many morphisms between the objects. Most of the categories you're familiar with--$\mathsf{Set},\mathsf{Top},\mathsf{Group}$, etc.--are locally small. In future posts, let's always assume our categories have this property, unless otherwise stated.

**For instance, the intersection of sets is another set, the direct product of groups is another group, the tensor product of vector spaces is another vector space, the product of compact topological spaces is another compact topological space, and so on.
 
***For size considerations, the categories in $\mathsf{Cat}$ are assumed to be small. A category $\mathsf{C}$ is called small if it doesn't contain too many objects and if there aren't too many morphisms between those objects, i.e. if both $\text{ob}(\mathsf{C})$ (all the objects in $\mathsf{C}$) and $\text{hom}_{\mathsf{C}}(x,y)$ are honest-to-goodness sets. 

Share 

 Tweet 

 Share 

Related Posts 

#### Matrices as Tensor Network Diagrams

May 15, 2019 

in 
Algebra 

#### Language Modeling with Reduced Densities

July 9, 2020 

in 
Category Theory 

#### Announcing Applied Category Theory 2019

January 5, 2019 

in 
Category Theory 

#### Language, Statistics, & Category Theory, Part 3

July 28, 2021 

in 
Category Theory 
 
Leave a comment!
