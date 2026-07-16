# The Yoneda Lemma

> Источник: [https://www.math3ma.com/blog/the-yoneda-lemma](https://www.math3ma.com/blog/the-yoneda-lemma)
> Автор: Tai-Danae Bradley (math3ma)
> Сохранено: 2026-07-16

---


![](https://cdn.prod.website-files.com/5b1d421032996833ff2a7704/5b651c50884ddb291aa16208_newM.avif)

# The Yoneda Lemma

Welcome to our third and final installment on the Yoneda lemma! In the past couple of weeks, we've slowly unraveled the mathematics behind the Yoneda perspective , i.e. the categorical maxim that an object  is completely determined by its relationships to other objects.

Last week we divided this maxim into two points:

### point #1 Everything we need to know about X is encoded in hom(--,X). In effect, the object X represents the functor hom(--,X).

### point #2 X and Y are isomorphic if and only if their represented functors hom(--,X) and hom(--,Y) are isomorphic.

Point #1, we noticed, is the informal way of saying that the Yoneda embedding $\mathscr{Y}:\mathsf{C}\to\mathsf{Set}^{\mathsf{C}^{op}}$ that sends an object $X$ to the functor $\text{hom}(-,X),$ is fully faithful. In other words, the function from $\text{hom}(X,Y)$ (a set of morphisms) to $\mathsf{Nat}(\text{hom}(-,X),\text{hom}(-,Y))$ (a set of natural transformations) that sends $f$ to $f_*$ is a bijection. (Here, $f_*$ sends a morphism $g:Z\to X$ to the composition $f\circ g:Z\to Y$.)

![](https://cdn.prod.website-files.com/5b1d427ae0c922e912eda447/5b58b746fc79dd1e5e4f6ff3_bij.jpg)

This means that for every $f:X\to Y$, there is exactly one natural transformation $\text{hom}(-,X)\to\text{hom}(-,Y)$, cooked up from $f$ itself. Conversely, if $\eta:\text{hom}(-,X)\to\text{hom}(-,Y)$ is any natural transformation, there is exactly one morphism $X\to Y$ that's obtained from $\eta$ itself. And this is where we left off last time.

Now here's a simple - yet crucial - observation: notice the set $\text{hom}(X,Y)$ lies in the image of the functor $\text{hom}(-,Y):\mathsf{C}^{op}\to \mathsf{Set}$! "But," you ask, "why is that important?"

Because it allows us to rephrase last week's result in the following way:

#### For any object $X$ in $\mathsf{C}$, natural transformations $\text{hom}(-,X)\to \text{hom}(-,Y)$ are in bijection with elements in the set $\text{hom}(X,Y)$.

‍ Pretty pithy, right? And you know what's amazing? It's true not only for functors of the form $\text{hom}(-,Y)$. It's true for ALL functors from $\mathsf{C}^{\text{op}}$ to $\mathsf{Set}$.

All of them!

And that is the Yoneda Lemma.

## The Yoneda Lemma

#### For any functor $F\colon \mathsf{C}^{op}\to\mathsf{Set}$ and any object $X$ in $\mathsf{C}$, natural transformations $\text{hom}(-,X)\to F$ are in bijection with  elements in the set $F(X)$. That is, $$\mathsf{Nat}(\text{hom}(-,X),F)\cong F(X).$$

Do you see the import here? The set of natural transformations $\text{hom}(-,X)\to F$ could be m-a-s-s-i-v-e , a dense forest of unknowable, untamable, and frankly unhelpful  weeds. "Except," the Yoneda lemma tells us, " it's not !" The only natural transformations that exist are those which can be cooked up from elements in the set obtained by evaluating $F$ at the object of interest, $X$. And what's the recipe? Given an element $c\in F(X)$, define $\eta:\text{hom}(-,X)\to F$ by declaring $\eta_Y:\text{hom}(Y,X)\to F(Y)$ to be the morphism that sends a map $g:Y\to X$ to the element $Fg(c)$ in $F(Y)$ where $Fg$ denotes the image of $g$ under $F.$

![](https://cdn.prod.website-files.com/5b1d427ae0c922e912eda447/5b58b7da767dc70860ab5ef9_1bijection.jpg)

On the flip side, any natural transformation $\eta:\text{hom}(-,X)\to F$ gives rise to an element in $F(X)$, namely  $\eta_X(\text{id}_X)$. Here $\eta_X$ denotes the morphism $\text{hom}(X,X)\to F(X)$ and $\text{id}_X$ is the identity morphism on $X$.

‍ It remains to check that these assignments really are inverses of each other (and that $\eta$ is a bona fide natural transformation). But as Tom Leinster once said , "To understand the question is very nearly to know the answer... there is only one possible way to proceed." An immediate consequence of the Yoneda lemma is the content of last week's discussion , restated here:

## First Corollary (Point #1)

#### Corollary 1: The Yoneda embedding $\mathscr{Y}:\mathsf{C}\to\mathsf{Set}^{\mathsf{C}^{op}}$ is fully faithful.

Injectivity of the map $\text{hom}(X,Y)\mapsto\mathsf{Nat}(\text{hom}(-,X),\text{hom}(-,Y))$ given by $f\mapsto f_*$ is clear. (If $f\neq g$ then $f_*\neq g_*$.) The Yoneda lemma gives us surjectivity. To see this, set $F=\text{hom}(-,Y)$ in the statement of the  lemma. Then we have a bijection $$\mathsf{Nat}(\text{hom}(-,X),\text{hom}(-,Y))\cong \text{hom}(X,Y).$$ Now suppose $\eta:\text{hom}(-,X)\to\text{hom}(-,Y)$ is any natural transformation. We need to show the existence of a morphism $f:X\to Y$ so that $\eta=f_*$. Here, "$\eta=f_*$" means that for every object $W$ in $\mathsf{C}$ and for any map $g:W\to X$, $$\eta_W(g)=f\circ g.$$ So what should the map $f$ be? There's really only one choice! According to the Yoneda lemma, $\eta$ gives rise to exactly one morphism $\eta_X(\text{id}_X):X\to Y$. So let's choose that one! That is, $$\text{let }\; f:=\eta_X(\text{id}_X).$$ Now we just need to verify that this works. But by definition, the phrase "$\eta$ is a natural transformation" means  for any pair of objects $Z,W\in\mathsf{C}$ and for any map $g:W\to Z$ we have the equality $\eta_W\circ g^*=g^*\circ\eta_Z,$ which is to say, for any $h:Z\to X$, $$\eta_W(h\circ g)=\eta_Z( h)\circ g$$

![](https://cdn.prod.website-files.com/5b1d427ae0c922e912eda447/5b58b8167d582b0829d8f61e_natural.jpg)

Since this holds for all $Z$ and $h$, it holds in the special case when $Z=X$ and $h= \text{id}_X\in \text{hom}(X,X)$. Now the naturality condition gives us exactly what we want: $\eta_W(g)=fg$ for all $g:W\to X$. And hence $\eta = f_*$.

So an object $X$ is effectually the same as its representable functor. So far, we've focused on the contravariant functors $\text{hom}(-,X)$, but it turns out there's a contravariant version of the Yoneda embedding (and a version of the Yoneda lemma for covariant functors $F$) and so there's an analogous "Corollary 1" with $\text{hom}(-,X)$ replaced by $\text{hom}(X,-)$. But the essence is the same—$X$ is determined by is relationships to other objects.

Better yet, it is completely determined by its relationships to other objects. The word "completely" is given to us by point #2 mentioned above, which is actually a second corollary of the Yoneda lemma.

## Second Corollary (Point #2)

#### Corollary 2: $X\cong Y$ if and only if $\text{hom}(-,X)\cong\text{hom}(-,Y)$.

One direction follows simply because $\mathscr{Y}$ is a functor: if $X$ and $Y$ are isomorphic, then so are $\text{hom}(-,X)$ and $\text{hom}(-,Y)$. The converse follows because $\mathscr{Y}$ is fully faithful. This is a general fact: if $F:\mathsf{C}\to\mathsf{D}$ is a fully faithful functor and if $F(X)\cong F(Y)$, then $X\cong Y$. (Proof in footnote.*)

![](https://cdn.prod.website-files.com/5b1d427ae0c922e912eda447/5b58b84dbb845c0b94831e5a_probe2.jpg)

We saw an illustration of this last week: two topological spaces $X$ and $Y$ have the same cardinality if and only if $\text{hom}(\bullet,X)\cong \text{hom}(\bullet,Y)$; they have the same path space if and only if $\text{hom}(I,X)\cong\text{hom}(I,Y)$; they have the same loop space if and only if $\text{hom}(S^1,X)\cong\text{hom}(S^1,Y)$; and so on. Probing $X$ and $Y$ with various spaces gives us more information. Probing them with all spaces gives us all information .

Of course, looking at maps out of $X$ provides useful information, too. For instance, $X$ is connected if and only if every map $X\to \{0,1\}$ is constant. Interestingly enough, if we consider the same set $\{0,1\}$ endowed with the Sierpinski topology, then ( as we've seen before ) the set $\text{hom}(X,\{0,1\})$ captures the full topology on $X$. Further, maps - when considered up to homotopy - from $X$ to an Eilenberg-MacLane space give rise to the homology groups of $X$. On the other hand, homotopy classes of maps from the $n$-sphere into $X$ form the homotopy groups of $X$.

The heavy emphasis on morphisms is really  a consequence of the Yoneda perspective (and hence the Yoneda lemma); it's all about relationships!

![](https://cdn.prod.website-files.com/5b1d427ae0c922e912eda447/5b58b869899aa01f3ef901d2_summary.jpg)

I'd like to close this series with one more example. The Yoneda lemma is sometimes described as a generalization of Cayley's theorem from group theory. And rightly so. We can use the Yoneda lemma to prove Cayley's theorem.

![](https://cdn.prod.website-files.com/5b1d427ae0c922e912eda447/5b527d2844acede360b8e7ae_hline.jpg)

## Cayley's theorem: a proof

Any group $G$ can be viewed as a category, call it $\mathsf{B}G$, with a single object $\bullet$ and a morphism for each group element. A functor $F$ from $\mathsf{B}G^{op}$ to $\mathsf{Set}$ is a right $G$-set. It sends $\bullet$ to a set $X$ and a morphism (i.e. group element) $g$ to the function $X\to X$ that multiplies on the right by $g$. In particular, when $F=\text{hom}(-,\bullet)$, the set $\text{hom}(\bullet,\bullet)$ is $G$ itself viewed as a right $G$-set. Then according to the Yoneda lemma, we have a bijection

![](https://cdn.prod.website-files.com/5b1d427ae0c922e912eda447/5b58b89a7d582b3721d8f61f_cayley1.jpg)

The right-hand side is simply the set of all elements in $G$. But what about the left-hand side? First notice that natural transformations $\text{hom}(-,\bullet)\to \text{hom}(-,\bullet)$ are simply $G$-equivariant functions $G\to G$.

But which $G$-equivariant functions are they? According to the bijection in Corollary 1, they are constructed from elements in $G$. In short, the set $\mathsf{Nat}(\hom(\bullet,\bullet),\hom(\bullet,\bullet))$ is nothing more than the set of all functions $f_g:G\to G$ defined by $x\mapsto xg$. And these are precisely automorphisms of $G$ that arise from multiplication by a fixed element!

![](https://cdn.prod.website-files.com/5b1d427ae0c922e912eda447/5b58b8914f9143108f13053f_cayley2.jpg)

The left-hand side is therefore a subgroup of the group of all permutations on $G$.  Moreover, this subgroup is—by the Yoneda lemma—isomorphic to the group $G$ itself. And this is Cayley's theorem. (Edit Dec. 2022: The graphic above is misleading, though. Check out this StackExchange post .)

![](https://cdn.prod.website-files.com/5b1d427ae0c922e912eda447/5b527d2844acede360b8e7ae_hline.jpg)

## Further Reading

For more on the Yoneda lemma, I highly recommend Tom Leinter's Basic Category Theory as well as his incredibly clear The Yoneda Lemma: What's it All About? I also recommend Emily Riehl's Category Theory in Context (her examples are particularly enriching) and, for some really meaty math, the nLab . At those links, you'll notice that there's a third classic corollary of the Yoneda lemma, which we did not cover in this series. Perhaps in a future post!

If you enjoyed the "probing objects with other objects" idea, you'll be happy to know that it's part of a philosophy of generalized points . For more, check out Leinster's Doing Without Diagrams and William Lawvere's An Elementary Theory of the Category of Sets (the 2005 version).

Finally, there's a neat result called the density theorem (e.g. Theorem 6.5.8 here ) that tells us every functor $F:\mathsf{C}^{op}\to\mathsf{Set}$ is really built up from the represented functors $\text{hom}(-,X)$. Formally, every such $F$ is a colimit of certain $\text{hom}(-,X)$. This is really a fantastic result (and has wonderful mathematics - like Kan extensions! - behind it). But I'll postpone the discussion - we haven't talked about colimits or limits ! Yet.

‍

![](https://cdn.prod.website-files.com/5b1d427ae0c922e912eda447/5b527d2844acede360b8e7ae_hline.jpg)

‍

* Proof. Suppose $h:F(X)\to F(Y)$ is an isomorphism with inverse $h^{-1}$. Because $F$ is fully faithful, there is a unique morphism $f:X\to Y$ so that $Ff=h$. Similarly, there is a unique morphism $g:Y\to X$ so that $Fg=h^{-1}$. Then $\text{id}_{F(X)}=h^{-1}\circ h=Fg\circ Ff=F(fg)$. But $F(\textit{id}_X)$ also maps to $\text{id}_{F(X)}$. Therefore, $fg=\textit{id}_X$ since $F$ is faithful. A similar argument shows $gf=\textit{id}_Y$ and so $f$ is an isomorphism.

‍

![](https://cdn.prod.website-files.com/5b1d427ae0c922e912eda447/5b527d2844acede360b8e7ae_hline.jpg)

‍

In this series:

![](https://cdn.prod.website-files.com/5b1d427ae0c922e912eda447/5b438abd25243f5c17a8c87f_perspective.jpg)

![](https://cdn.prod.website-files.com/5b1d427ae0c922e912eda447/5b438aa625243f5674a8c879_embedding.jpg)

![](https://cdn.prod.website-files.com/5b1d427ae0c922e912eda447/5b438a8295bee1190f213315_lemma.jpg)

### The Sierpinski Space and Its Special Property

### Commutative Diagrams Explained

### The Yoneda Embedding

### What is an Adjunction? Part 1 (Motivation)
