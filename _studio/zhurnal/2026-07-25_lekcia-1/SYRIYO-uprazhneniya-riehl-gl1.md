# СЫРЬЁ — упражнения Riehl, глава 1 (каркас Л1)

> Механическая выгрузка: `pdftotext` + regex по `riehl-category-theory-in-context.pdf`.
> Глава 1 у Riehl = ровно аппарат Л1: 1.1 категории · 1.2 двойственность · 1.3 функториальность · 1.4 естественность · 1.5 эквивалентность категорий · 1.6 диаграммный поиск · 1.7 2-категория категорий.
> Текст обрезан на 900 символов — этого хватает, чтобы судить о нетривиальности; полный текст в книге по номеру.
> **Отбор НЕ сделан.** Задача следующего шага — отсеять тривиальные («проверьте очевидное») и оставить те, где есть трюк, идея или исследовательское утверждение.


## 1.1

**1.1.i.** (i) Consider a morphism f : x → y. Show that if there exists a pair of morphisms g, h : y ⇒ x so that g f = id x and f h = idy , then g = h and f is an isomorphism. (ii) Show that a morphism can have at most one inverse isomorphism.

**1.1.ii.** Show that the collection of isomorphisms in a category C defines a subcategory, the maximal subgroupoid inside C. 16This is not simply an example; it is a definition. 17To justify our default notion of ring, see Poonen’s “Why all rings should have a 1” [Poo14]. The relationship between unital and non-unital rings is explored in greater depth in §4.7. 1.2. DUALITY 9

**1.1.iii.** For any category C and any object c ∈ C, show that: (i) There is a category c/C whose objects are morphisms f : c → x with domain c and in which a morphism from f : c → x to g : c → y is a map h : x → y between the codomains so that the triangle f x c g y h commutes, i.e., so that g = h f . (ii) There is a category C/c whose objects are morphisms f : x → c with codomain c and in which a morphism from f : x → c to g : y → c is a map h : x → y between the domains so that the triangle h x f y g c commutes, i.e., so that f = gh. The categories c/C and C/c are called slice categories of C under and over c, respectively.

**1.1.iv.** The category Htpy is formed as a quotient of the category Top by an equivalence relation on its hom-sets. A binary equivalence relation ∼ on the hom-sets of a category is called a congruence if it respected by pre- and postcomposition: if f ∼ g then h f k ∼ hgk. (i) Suppose C is a category and ∼ is a congruence on its hom-sets. Define a new category whose objects are the same as the objects of C and whose morphisms are defined to be ∼-equivalence classes of parallel morphisms in C. (ii) Prove that the homotopy relation defines a congruence on the category Top. That is, if f, g : X ⇒ Y are homotopic and k : W → X and h : Y → Z are arbitrary continuous functions, show that h f k and hgk are homotopic as well. 1.2. Duality The dual of any axiom for a category is also an axiom . . . A simple metamathematical argument thus proves the duality principle. If any statement about a category is ded


## 1.2

**1.2.i.** Defining C/c to be (c/(Cop ))op , deduce Exercise 1.1.iii(ii) from Exercise 1.1.iii(i).21

**1.2.ii.** Prove Lemma 1.2.11 by proving either (i) or (i’) and either (ii) or (ii’), then arguing by duality. Conclude that the monomorphisms in any category define a subcategory of that category and dually that the epimorphisms also define a subcategory.

**1.2.iii.** What are the monomorphisms in the category Field of fields?

**1.2.iv.** Show that the inclusion Z ,→ Q is both a monomorphism and an epimorphism in the category Ring of rings. Conclude that a map that is both monic and epic need not be an isomorphism, as there are no ring homomorphisms from Q to Z.

**1.2.v.** (i) Show that a morphism f : x → y is a split epimorphism in a category C if and only if for all c ∈ C, the postcomposition function f∗ : C(c, x) → C(c, y) is surjective. (ii) Argue by duality that f is a split monomorphism if and only if for all c ∈ C, the precomposition function f ∗ : C(y, c) → C(x, c) is surjective.

**1.2.vi.** Prove the following results and then state and prove their duals. (i) Split epimorphisms are epimorphisms. (ii) A morphism that is both a monomorphism and a split epimorphism is necessarily an isomorphism.

**1.2.vii.** Regarding a poset (P, ≤) as a category, define the supremum of a subcollection of objects A ∈ P in such a way that the dual statement defines the infimum. Prove that the supremum of a subset of objects is unique, whenever it exists, in such a way that the dual proof demonstrates the uniqueness of the infimum. 21More precisely, the categories C/c and (c/(Cop ))op are isomorphic, in a sense to be made precise in §1.3. But as a consequence of this isomorphism, we could define C/c to be (c/(Cop ))op if we wished to do so. 

**1.2.viii.** The categorical statement that “every epimorphism is a split epimorphism” is referred to as the external axiom of choice. Find examples of categories in which this axiom holds and categories in which it fails. 1.3. Functoriality . . . every sufficiently good analogy is yearning to become a functor. John Baez, “Quantum Quandaries: A Category-Theoretic Perspective” [Bae06] A key tenet in category theory, motivating the very definition of a category, is that any mathematical object should be considered together with its accompanying notion of structure-preserving morphism. In “General theory of natural equivalences” [EM45], Eilenberg and Mac Lane argue further: . . . whenever new abstract objects are constructed in a specified way out of given ones, it is advisable to regard the construction of the corresponding induced mappings on these new objects as an integral part of their definition. 


## 1.3

**1.3.i.** What is a functor between groups, regarded as one-object categories?

**1.3.ii.** What is a functor between preorders, regarded as categories?

**1.3.iii.** Find an example to show that the objects and morphisms in the image of a functor F : C → D do not necessarily define a subcategory of D.

**1.3.iv.** Verify that the constructions introduced in Definitions 1.3.11 and 1.3.13 are functorial.

**1.3.v.** What is the difference between a functor Cop → D and a functor C → Dop ? What is the difference between a functor C → D and a functor Cop → Dop ? State and proof a result describing the interaction between functors and split epimorphisms and explain all four dual variants.

**1.3.vi.** Given functors F : D → C and G : E → C, show that there is a category, called the comma category F ↓G, which has • as objects, triples (d ∈ D, e ∈ E, f : Fd → Ge ∈ C), and 31In the axioms of Zermelo-Fraenkel set theory, elements of sets (like everything else in its mathematical universe) are themselves sets. The axiom of regularity prohibits a set from being an element of itself. As X < X, we are free to add the element X as a disjoint basepoint. • as morphisms (d, e, f ) → (d′ , e′ , f ′ ), pairs of morphisms (h : d → d′ , k : e → e′ ) so that the square Fd f Gk Fh Fd Ge ′ f′ Ge′ commutes in C, i.e., so that f ′ · Fh = Gk · f . Define a pair of projection functors dom : F ↓G → D and cod : F ↓G → E.

**1.3.vii.** Define functors to construct the slice categories c/C and C/c of Exercise 1.1.iii as special cases of comma categories constructed in Exercise 1.3.vi. What are the projection functors?

**1.3.viii.** Lemma 1.3.8 shows that functors preserve isomorphisms. Find an example to demonstrate that functors need not reflect isomorphisms: that is, find a functor F : C → D and a morphism f in C so that F f is an isomorphism in D but f is not an isomorphism in C.

**1.3.ix.** For any group G, we may define other groups: • the center Z(G) = {h ∈ G | hg = gh ∀g ∈ G}, a subgroup of G, • the commutator subgroup C(G), the subgroup of G generated by elements ghg−1 h−1 for any g, h ∈ G, and • the automorphism group Aut(G), the group of isomorphisms ϕ : G → G in Group. Trivially, all three constructions define a functor from the discrete category of groups (with only identity morphisms) to Group. Are these constructions functorial in • the isomorphisms of groups? That is, do they extend to functors Groupiso → Group? • the epimorphisms of groups32? That is, do they extend to functors Groupepi → Group? • all homomorphisms of groups? That is, do they extend to functors Group → Group?

**1.3.x.** Show that the construction of the set of conjugacy classes of elements of a group is functorial, defining a functor Conj : Group → Set. Conclude that any pair of groups whose sets of conjugacy classes of elements have differing cardinalities cannot be isomorphic. 1.4. Naturality It is not too misleading, at least historically, to say that categories are what one must define in order to define functors, and that functors are what one must define in order to define natural transformations. Peter Freyd, Abelian categories [Fre03] Any finite-dimensional k-vector space V is isomorphic to its linear dual, the vector space V ∗ B Hom(V, k) of linear functionals V → k, because these vector spaces have the same dimension. This can be proven through the construction of an explicit dual basis: 32A non-trivial theorem demonstrates that a homomorphism ϕ : G → H is an epimorphism in Group if and only i


## 1.4

**1.4.i.** Suppose α : F ⇒ G is a natural isomorphism. Show that the inverses of the component morphisms define the components of a natural isomorphism α−1 : G ⇒ F.

**1.4.ii.** What is a natural transformation between a parallel pair of functors between groups, regarded as one-object categories?

**1.4.iii.** What is a natural transformation between a parallel pair of functors between preorders, regarded as categories?

**1.4.iv.** Characterize all natural transformations from the identity functor on Set to the functor (−)+ : Set → Set that adds a new disjoint point. Are there any natural transformations in the other direction?

**1.4.v.** Prove that the maps ιA : T A ↣ A and πA : A ↠ A/T A in the short exact sequence (1.4.5) each define the components of natural transformations between endofunctors of the category Ab of abelian groups.

**1.4.vi.** In the notation of Example 1.4.9, prove that distinct parallel morphisms f, g : c ⇒ d define distinct natural transformations f∗ , g∗ : C(−, c) ⇒ C(−, d) and f ∗ , g∗ : C(d, −) ⇒ C(c, −) by post- and precomposition.

**1.4.vii.** Recall the construction of the comma category for any pair of functors F : D → C and G : E → C described in Exercise 1.3.vi. From this data, construct a canonical natural transformation α : F dom ⇒ G cod between the functors that form the boundary of the square

**1.4.viii.** Given a pair of functors F, G : Cop × C → D, a family of morphisms αc : F(c, c) → G(c, c) in D indexed by c ∈ C defines the components of a dinatural transformation α : F ⇒ G if for any f : c → c′ in C, the following diagram commutes in D: Specialize this condition to the case where F and G are defined by restricting a covariant functor H : C → D and a contravariant functor K : Cop → D, respectively, along the projection functors π2 : Cop × C → C and π1 : Cop × C → Cop .

**1.4.ix.** Given a pair of functors F : A × B × Bop → D and G : A × C × Cop → D, a family of morphisms αa,b,c : F(a, b, b) → G(a, c, c) in D indexed by a ∈ A, b ∈ B, and c ∈ C defines the components of an extranatural transformation α : F ⇒ G if for any f : a → a′ , g : b → b′ , and h : c → c′ the following For each morphism f from c to c' in C, the components of a dinatural transformation alpha from F to G fit into a commutative hexagon involving the applications of the functors F and G to pairs involving f and an identity arrow at c or at c'. 1.5. EQUIVALENCE OF CATEGORIES 31 diagrams commute in D: A natural transformation between functors F and G from C to D may be encoded by a functor H from the product of C with the walking arrow category 2 to D with the property that H restricts along the domain object of 2 to the functor F and restricts along the codomain object of 2 to the functor G. The le


## 1.5

**1.5.i.** Prove Lemma 1.5.1.

**1.5.ii.** Segal defined a category Γ in [Seg74] as follows: Γ is the category whose objects are all finite sets, and whose morphisms from S to T are the maps θ : S → P(T ) such that θ(α) and θ(β) are disjoint when α , β. The composite of θ : S → P(T ) and S ϕ : T → P(U) is ψ : S → P(U), where ψ(α) = ϕ(β). β∈θ(α) op Prove that Γ is equivalent to the category Fin∗ , the opposite of the category of finite pointed sets. In particular, the functors introduced in Example 1.3.2(xi) define presheaves on Γ.

**1.5.iii.** Prove Lemma 1.5.10.

**1.5.iv.** Show that a full and faithful functor F : C → D both reflects and creates isomorphisms. That is, show: (i) If f is a morphism in C so that F f is an isomorphism in D, then f is an isomorphism. (ii) If x and y are objects in C so that F x and Fy are isomorphic in D, then x and y are isomorphic in C. By Lemma 1.3.8, the converses of the statements (i) and (ii) hold for any functor.

**1.5.v.** Find examples to show functors that are either full or faithful but not both need not either reflect or create isomorphisms.

**1.5.vi.** (i) Prove that the composite of a pair of full, faithful, or essentially surjective functors again has the same properties. (ii) Prove that if C ≃ D and D ≃ E, then C ≃ E. Conclude that equivalence of categories is an equivalence relation.43

**1.5.vii.** Characterize the categories that are equivalent to discrete categories.

**1.5.viii.** Klein’s Erlangen program studies groupoids of geometric spaces of various kinds. Prove that the groupoid Affine of affine planes is equivalent to the groupoid Proj| of projective planes with a distinguished line, called the “line at infinity.” The morphisms in each groupoid are bijections on both points and lines (preserving the distinguished line in the case of projective planes) that preserve and reflect the incidence relation. The functor Proj| → Affine removes the line at infinity and the points it contains. Explicitly describe an inverse equivalence.

**1.5.ix.** Consider the functors I : Ab → Group (inclusion), I : Ring → Ab (forgetting the multiplication), (−)× : Ring → Group (taking the group of units), I : Ring → Rng 43A second, more direct proof of this result appears as Exercise 1.7.v. 1.6. THE ART OF THE DIAGRAM CHASE 39 (inclusion), I : Field → Ring (inclusion), and U : R Mod → Ab (forgetful). Determine which functors are full, which are faithful, and which are essentially surjective. Do any define an equivalence of categories? (Warning: A few of these questions conceal researchlevel problems, but they can be fun to think about even if full solutions are hard to come by.) 1.6. The art of the diagram chase The diagrams incorporate a large amount of information. Their use provides extensive savings in space and in mental effort. In the case of many theorems, the setting up of the correct diagram is the major part of the proof. We therefore 


## 1.6

**1.6.i.** Show that any map from a terminal object in a category to an initial one is an isomorphism. Conclude that if such a map exists, then both objects are zero objects.

**1.6.ii.** Show that the concepts of initial and terminal object are not evil. (i) Argue that any object that is isomorphic to an object that is either initial or terminal is again initial or terminal respectively. (ii) Prove that for any pair of equivalent categories, if either has an initial or terminal object then both do.

**1.6.iii.** Identify the zero object in the category Set∂ of sets and partial functions.

**1.6.iv.** Show that any faithful functor reflects monomorphisms. That is, if F : C → D is faithful, prove that if F f is a monomorphism in D, then f is a monomorphism in C. Argue by duality that faithful functors also reflect epimorphisms. Conclude that in any concrete category, any morphism that defines an injection of underlying sets is a monomorphism and any morphism that defines a surjection of underlying sets is an epimorphism.

**1.6.v.** (i) Find an example to show that a faithful functor need not preserve epimorphisms. Argue by duality, or by another counterexample, that a faithful functor need not preserve monomorphisms. (ii) More specifically, find a concrete category that contains a monomorphism whose underlying function is not injective. Find a concrete category that contains an epimorphism whose underlying function is not surjective. Exercise 4.6.vi explains why the former examples may seem less familiar than the former.

**1.6.vi.** Show that any small category C admits a faithful functor to Set that sends an object c ∈ C to the set of generalized elements of c, i.e., to the set of all morphisms in C with codomain c. Extend this construction to a functor and prove that this functor is faithful. (Hint: consider the “universal generalized element of c,” defined by idc .) 1.7. The 2-category of categories A number of important facts about natural transformations are proven by diagram chasing. In this section, we define “vertical” and “horizontal” composition operations for natural transformations. The upshot is that categories, functors, and natural transformations assemble into a 2-dimensional categorical structure called a 2-category, a definition that is stated at the conclusion. In French, a natural transformation is called a morphisme de foncteurs. Indeed, for any fixed pair of categories C and D, there is a funct


## 1.7

**1.7.i.** Prove that if C is small and D is locally small, then DC is locally small by defining a monomorphism from the collection of natural transformations between a fixed pair of functors F, G : C ⇒ D into a set. (Hint: Think about the function that sends a natural transformation to its collection of components.)

**1.7.ii.** Redefine the horizontal composition of natural transformations introduced in Lemma 1.7.4 using vertical composition and whiskering.

**1.7.iii.** Prove Lemma 1.7.7.

**1.7.iv.** Show that for any category C, the collection of natural endomorphisms of the identity functor idC defines a commutative monoid, called the center of the category. The proof of Proposition 1.4.6 demonstrates that the center of Abfg is the multiplicative monoid (Z, ×, 1).

**1.7.v.** Suppose the functors and natural isomorphisms C F D η : idC  GF ϵ : FG  idD E η′ : idD  G′ F ′ ϵ ′ : F ′G′  idE G D F′ G′ define equivalences of categories C ≃ D and D ≃ E. Prove (again) that there is a composite equivalence of categories C ≃ E by defining composite natural isomorphisms idC  GG′ F ′ F and F ′ FGG′  idE .

**1.7.vi.** Prove that a bifunctor F : C × D → E determines and is uniquely determined by: (i) A functor F(c, −) : D → E for each c ∈ C. (ii) A natural transformation F( f, −) : F(c, −) ⇒ F(c′ , −) for each f : c → c′ in C, defined functorially in C. In other words, prove that there is a bijection between functors C × D → E and functors C → ED . By symmetry of the product of categories, these classes of functors are also in bijection with functors D → EC .

**1.7.vii.** Revisit the bifunctor of Definition 1.3.13 and the families of natural transformations described in Example 1.4.9 from the perspective of Exercise 1.7.vi. This previews one of the most fundamental constructions in category theory (see Corollary 2.2.8). CHAPTER 2 Universal Properties, Representability, and the Yoneda Lemma . . . a mathematical object X is best thought of in the context of a category surrounding it, and is determined by the network of relations it enjoys with all the objects of that category. Moreover, to understand X it might be more germane to deal directly with the functor representing it. Barry Mazur, “Thinking about Grothendieck” [Maz16] The aim in this chapter is to explain what it means to say that the natural numbers is the universal discrete dynamical system, that the Sierpinski space is the universal space with an open subset, or that the complete graph on n-vert

