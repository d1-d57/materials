<!-- SOURCE: https://www.math3ma.com/blog/what-is-an-adjunction-part-2 | captured 2026-07-19 | math3ma (Tai-Danae Bradley), free blog | curl+stdlib extract -->

# math3ma — What Is An Adjunction Part 2 (captured)

What is an Adjunction? Part 2 (Definition) 

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

September 24, 2019 

• 
Category Theory 

#### What is an Adjunction? Part 2 (Definition)

 Last time I shared a light introduction to adjunctions in category theory. As we saw then, an adjunction consists of a pair of opposing functors $F$ and $G$ together with natural transformations $\text{id}\to\ GF$ and $FG\to\text{id}$. We compared this to two stricter scenarios: one where the composite functors equal the identities, and one where they are naturally isomorphic to the identities. The first scenario defines an isomorphism of categories. The second defines an equivalence of categories. An adjunction is third on the list. 
 
In the case of an adjunction, we also ask that the natural transformations—called the unit and counit —somewhat behave as inverses of each other. This explains why the ${\color{red}\text{arrows}}$ point in opposite directions. (It also explains the "co.") Except, they can't literally be inverses since they're not composable: one involves morphisms in $\mathsf{C}$ and the other involves morphisms in $\mathsf{D}$. That is, their (co)domains don't match. But we can fix this by applying $F$ and $G$ so that (a modified version of) the unit and counit can indeed be composed. This motivates the formal definition of an adjunction. 

#### The Definition

Here it is: 
 Definition : An adjunction between categories $\mathsf{C}$ and $\mathsf{D}$ is a pair of functors $F\colon\mathsf{C}\to\mathsf{D}$ and $G\colon \mathsf{D}\to\mathsf{C}$ together with natural transforamtions $\eta\colon \text{id}_\mathsf{C}\to GF$, called the unit , and $\epsilon\colon FG\to\text{id}_\mathsf{D}$, called the counit , so that for all objects $X$ in $\mathsf{C}$ and $Y$ in $\mathsf{D}$ the two triangles below commute. When $F$ and $G$ are part of an adjunction, we'll write $F\dashv G$ and say that $F$ and $G$ are adjoint functors , with $F$ being the left adjoint of $G$ and $G$ being the right adjoint of $F$. 
 
There are a couple things to unwind here. First, how should we understand the unit $\eta$ and counit $\epsilon$? Second, why the names "left/right adjoint"? 
Let's address the first question first. 

#### Bringing the Definition to Life

I'll start by sharing a little schema that's used over and over again in various guises throughout mathematics: 
 We often start with a set $B$. 
 Example: take $B$ to be a set with three elements. 
 The elements in $B$ are then used as building blocks to construct a bigger mathematical object $FB$, which contains the original $B$ and more. 
 Example: take $FB$ to be the three-dimensional real vector space with basis $B$. 
 As a consequence, we observe that whenever another object also "contains" $B$, it automatically contains $FB$, too. 
 Example: if $V$ is any vector space and there is a mapping $f$ from $B$ to $V$, then you automatically have a linear transformation $FB\to V$. It's obtained by extending $f$ linearly. 
This is a typical kind of extension problem. You have a little set $B$. You build a bigger object $FB$ with it. You say, "Yikes, $FB$ is large and messy. How can I ever define a map out of it?" Then you breathe a sigh of relief. You need only define your map on the smaller, more manageable $B$. The rest takes care of itself. 
I've illustrated the schema above with a standard situation from linear algebra. When you want to define a linear map between vectors spaces, it's always enough to define the map on the basis vectors of the domain space, rather than on every single vector. Since the map must be linear, you know what it must be on an arbitrary vector once you know what it is on the basis vectors. 
Be careful, though. 
In Step 3 above, I wrote "...a mapping $f$ from $B$ to $V$..." This is vague. What kind of a morphism is $f$? Is it a function? Is it a linear transformation? Since $B$ is a set and $V$ is a set-with-extra-data (remember, a vector space is a set together with other things ), $f$ should probably just be a function between sets. 
The category theory confirms this. Indeed, lurking behind our three-step schema is an adjunction. En route to unveiling it, now's a good time to know that the unit natural transformation $\eta\colon \text{id}_{\mathsf{C}}\to GF$ of any adjunction $F\dashv G$ always satisfies the following property: 
 
What does this mean? Let's relate it back to our linear algebra example. Suppose $\mathsf{D}=\mathsf{Vect}_{\mathbb{R}}$ is the category of real vector spaces, and $\mathsf{C}=\mathsf{Set}$ is the category of sets. Define $F\colon\mathsf{Set}\to\mathsf{Vect}_{\mathbb{R}}$ to be the functor that assigns to a set $B$ the real vector space $FB$ whose basis is $B$. (If you want to be fancy, you can refer to $FB$ as the "free $\mathbb{R}$-module on $B$.") Define $U\colon \mathsf{Vect}_{\mathbb{R}}\to\mathsf{Set}$ to be the functor sending any vector space $V$ to the underlying set $UV$ of vectors in $V$. (The letter "$U$" is for underlying .) That is, $U$ totally forgets the vector space data of $V$ and views it as a set. I'll let you think about what these functors should do to morphisms. Then $F$ and $U$ are part of an adjunction called a free-forgetful adjunction . 
The unit $\eta\colon \text{id}_{\mathsf{Set}}\to UF$ of this adjunction is a natural transformation consisting of a function $\eta_B\colon B \to UFB$ for each set $B$. This function simply includes the set $B$ into the underlying set of the vector space $FB$. For example, if $B$ is the three-element set $\{x,y,z\}$ then $\eta_B$ injects it into the set whose elements are all linear combinations of $x,y$ and $z$, which we can simply think of as $\mathbb{R}^3$. 
 
Moreover, each function $\eta_B$ satisfies the property introduced above: 
 
This is exactly the three-step schema described above, written in math-speak. We start with a set $B$. We use it to build a vector space $FB$. This vector space naturally contains the original set $B$ by way of the inclusion $\eta_B\colon B\to UFB$. And any time another vector space "contains" $B$ via some $f\colon B\to UV$, it must "contain" $FB$, too, by way of $U\hat{f}\colon UFB \to UV$. 
Notice the clarity of the language: In the schema, I made vague reference to "...a mapping $f$ from $B$ to $V$." The category theory explicitly places the discussion in the category of sets: $f$ is a function from the set $B$ to the set $UV$. The property above tells us that to every such function, there is exactly one linear map $\hat{f}\colon FB\to V$ so that $f=U\hat{f}\circ \eta_B$, which is to say that $\hat{f}$, as a linear map, agrees with $f$ on basis elements. In other words, $\hat{f}$ is the unique map that extends $f$ linearly from the basis set $B$ to the entire vector space $FB$. That this property is satisfied by the unit of the adjunction is precisely why we only need to define linear maps on basis elements. 
There are other free-forgetful adjunctions outside of linear algebra. Free groups, free monoids, free modules over a ring, free rings on an abelian group, etc. all fit into the same story. More generally, whenever some functor "forgets" some data or structure and has a left adjoint, that left adjoint will have a "free" flavor to it. 

#### What about the counit?

So far the discussion has been about the unit of an adjunction. I'll say a few brief words about the counit of our example, as counits of general adjunctions share a similar story. 
The counit $\epsilon\colon FU\to \text{id}_{\mathsf{Vect}_\mathbb{R}}$ of our free-forgetful adjunction $F\dashv U$ is a natural transformation consisting of linear transformations $\epsilon_V\colon FUV\to V$, where $V$ is a vector space. Note that $UV$ is the set of all vectors in $V$, and $FUV$ is the vector space with one basis vector for each element in $UV$. So $FUV$ is massive! The linear map $\epsilon_V$ takes linear combinations of elements in the set $UV$—which are just vectors in $V$—and simply views them as vectors in $V$. As an example, if $V$ has bases $\mathbf{x,y,z}$ then: 
 
So the counit here is saying, "A linear combination of linear combinations of vectors in $V$ is itself a vector in $V$, so just view, or evaluate, that sum as that vector." What's more, each linear map $\epsilon_V$ satisfies the following property: 
 
This property says that, since linear combinations of linear combinations of vectors in $V$ are themselves vectors in $V$, maps into $V$ are what you think they are. 
In general, the letter $\epsilon$ should remind you of "e" for "evaluation," as counits of adjunctions often have a "just evaluate the obvious thing" kind of flavor. 

#### Repackaging the Definition

Thus far we've taken a closer look at the unit and counit of an adjunction. But what about the name ? Why are the functors  "adjoints"? And why do they come in "left" and "right" versions? The answer lies in a repackaging of the definition. Here is a different, but equivalent way, to understand adjunctions: 
 Definition : An adjunction between categories $\mathsf{C}$ and $\mathsf{D}$ is a pair of functors $F\colon\mathsf{C}\to\mathsf{D}$ and $G\colon \mathsf{D}\to\mathsf{C}$ together with a bijection $\text{hom}_{\mathsf{D}}(FX,Y)\cong \text{hom}_{\mathsf{C}}(X,GY)$ for all objects $X$ in $\mathsf{C}$ and $Y$ in $\mathsf{D}$, which is natural in both $X$ and $Y$. Call the image $\hat{f}$ of a map $f$ under this bijection the adjunct or transpose of $f$. 
 
"Natural in both $X$ and $Y$" means we require $\text{hom}_{\mathsf{D}}(FX,-)\cong \text{hom}_{\mathsf{C}}(X,G-)$ to be a natural isomorphism for each $X$ and $\text{hom}_{\mathsf{D}}(F-,Y)\cong \text{hom}_{\mathsf{C}}(-,GY)$ to be a natural isomorphism for each $Y$. 
The upshot is that $F\dashv G$ if maps $FX\to Y$ are the same as maps $X\to GY$. In our free-forgetful adjunction, the bijection $\text{hom}_{\mathsf{Vect}_\mathbb{R}}(FB,V)\cong \text{hom}_{\mathsf{Set}}(B,UV)$ says that there is a one-to-one correspondence between functions $B\to UV$ and linear transformations $FB\to V$. If you have one, then you can get the other. 
Hopefully this sheds light on the notation $F\dashv G$. In the bijection above, $F$ appears on the left and is called the left adjoint of $G$, while $G$ appears on the right and is called the right adjoint of $F$. Moreover, the isomorphism $\text{hom}_{\mathsf{D}}(FX,Y)\cong \text{hom}_{\mathsf{C}}(X,GY)$ looks almost identical to the property that a linear map between Hilbert spaces $f\colon V\to W$ shares with its adjoint $\hat{f}\colon W\to V$: $$\langle f\mathbf{v},\mathbf{w}\rangle = \langle \mathbf{v},\hat{f}\mathbf{w}\rangle \qquad\text{for all $\mathbf{v}\in V$ and $\mathbf{w}\in W$}$$ which explains the terminology. 
(Unfortunately, I'm not aware of a way to view Hilbert spaces as categories so that linear maps and their adjoints are literal categorical adjunctions. But see John Baez's " Higher-Dimensional Algebra II: 2-Hilbert Spaces " for a categorification of the situation.) 
 I'll leave you to verify that the two definitions of adjunctions are equivalent, as claimed. Here are some hints: 
The transpose of the identity of $FX$ under the isomorphism $\text{hom}_{\mathsf{D}}(FX,FX)\overset{\cong}{\longrightarrow} \text{hom}_{\mathsf{C}}(X,GFX)$ is the unit $\eta$ of the adjunction. 
The transpose of the identity of $GY$ under the isomorphism $\text{hom}_{\mathsf{D}}(FGY,Y) \overset{\cong}{\longleftarrow}\text{hom}_{\mathsf{C}}(GY,GY)$ is the counit $\epsilon$ of the adjunction. 
Pay careful attention to the naturality conditions appearing in each definition! 
With these hints, you can also verify that the unit and counit do indeed satisfy the universal properties that we explored above. 
 
This wraps up our investigation into the formal definition of categorical adjunctions. In the next post, I'll share some examples that appear in both pure and applied settings. 

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

#### At the Interface of Algebra and Statistics

April 13, 2020 

in 
Probability 

#### Group Elements, Categorically

February 16, 2017 

in 
Category Theory 
 
Leave a comment!
