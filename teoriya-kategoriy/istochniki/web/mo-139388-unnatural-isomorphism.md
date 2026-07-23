SOURCE: https://mathoverflow.net/questions/139388 · дата извлечения: 2026-07-23 · способ: встроенный браузер (mcp__Claude_Browser: navigate + get_page_text + javascript_tool). WebFetch на mathoverflow.net дал ошибку "Claude Code is unable to fetch from mathoverflow.net" — прямой хост-сайд фетч заблокирован, страница добыта через рендер в браузерной панели.

# Example of an unnatural isomorphism

Вопрос: 64 голоса · автор Bugs Bunny (community wiki) · задан 14 авг 2013, 7:30 · изменён (последнее изменение обсуждения) 7 лет 5 мес назад · просмотров: 9k · тег: ct.category-theory · 13 ответов.

## Тело вопроса

Can anyone give an example of an unnatural isomorphism? Or, maybe, somebody can explain why unnatural isomorphisms do not exist.

Consider two functors F,G:C→D. We say that they are unnaturally isomorphic if F(x)≅G(x) for every object x of C but there exists no natural isomorphism between F and G. Any examples?

Just to clarify the air, V and V∗ for finite dimensional vector spaces ain't no gud: one functor is covariant, another contravariant, so they are not even functors between the same categories. A functor should mean a covariant functor here.

**Ключевые комментарии к вопросу:**
- Martin Brandenburg: "A better terminology would be 'pointwise isomorphic'."
- LSpice (2021, повод для написания дубля-вопроса 390929): "'Just to clarify the air' is a marvellous phrase."

---

## Ответы (все 13, порядок — как на сайте, сортировка "Highest score")

### 72 голоса — Martin Brandenburg (community wiki, 5 revisions; финальная правка 18 авг 2013, 6:50)
*Это САМЫЙ высокоголосный ответ вопроса и он составной — содержит СРАЗУ четыре примера в одном посте (историческая правка добавила пример Sym/Ord как "example 1" в 2013 г.):*

> If F,G:C→D are functors such that F(x)≅G(x) for every x∈C, I would call F,G "pointwise isomorphic". You ask for examples of non-isomorphic functors which are pointwise isomorphic. There are plenty natural examples.
>
> Consider the interval category I={0→1}. The category of functors I→C is isomorphic to the category of morphisms in C. Of course for most C there are non-isomorphic morphisms in C whose domain and codomain are isomorphic or even equal. For example take the identity and a constant map on a nontrivial set or space.
>
> Let C be the category of finite sets with bijections as morphisms. Then we have the functor Sym:C→C which maps every set to its set of permutations, and the functor Ord:C→C which maps every set to its set of total orderings; the action on morphisms is "conjugation". These functors are pointwise isomorphic, but not isomorphic (in fact between these functors there is no natural transformation at all). Actually this example (when restricted to sets of a given size) can be seen as a special case of the next one.
>
> Let G be a group (or monoid), considered as a category with one object ⋆. Then a functor G→Set is the same as a G-set. In fact, the category of G-sets is isomorphic to the category of functors G→Set. The value at ⋆ is the underlying set. Of course for G≠1 there are non-isomorphic G-sets whose underlying sets are isomorphic (for example the underlying set of G with the regular action and with the trivial action of G).
>
> If C denotes the category of finite abelian groups, then Tor₁^ℤ and ⊗_ℤ : C×C→C are pointwise isomorphic (since Tor₁(ℤ/n,ℤ/m)≅ℤ/gcd(n,m)≅ℤ/n⊗_ℤℤ/m), but they are not isomorphic (for example since Tor₁^ℤ is not right exact in the second or first variable).

Комментарии под ответом: Karol Szumiło называет пример Sym/Ord "самым просветляющим среди всех примеров в ответах на этот вопрос"; Eric Wofsey указывает, что тот же пример прозрачнее как частный случай G-множеств (Sₙ, трансляция vs сопряжение); Martin Brandenburg подтверждает, что пример Sym/Ord добавлен позже (18 авг 2013) и стал "example 1".

### 63 голоса — Mark Grant (community wiki; отвечено 14 авг 2013, 8:04)
> The Universal Coefficient Theorem for, say, singular cohomology should give examples. For any abelian group G and n>0, the functors from spaces to abelian groups given by
> X↦Hⁿ(X;G), X↦Ext(H_{n−1}(X),G)⊕Hom(H_n(X),G)
> are isomorphic, but not naturally so. See Hatcher's "Algebraic Topology", Chapter 3.1 (in particular Exercise 11 at the end of that section).

### 50 голосов — Jeremy Rickard (community wiki; отвечено 14 авг 2013, 8:25)
> For a simpler, but arguably more artificial, example than Mark's, take C to be the category with one object and two morphisms. Then the identity functor C→C is "unnaturally isomorphic" to the functor that sends both morphisms to the identity map.

Комментарий Qiaochu Yuan: категория с одним объектом и двумя морфизмами не определена однозначно — есть два варианта (f²=id или f²=f); Rickard отвечает, что подходит любой.

### 30 голосов — Dan Petersen (community wiki; отвечено 14 авг 2013, 9:03)
> Your non-example of vector spaces and their duals can be souped up to a real example.
>
> Let C be the groupoid of finite-dimensional vector spaces and linear isomorphisms. Then there are two obvious functors C→C^op: the linear dual, and the natural isomorphism C→̃C^op that one has for any groupoid. These functors are unnaturally isomorphic.

Комментарии: Eric Wofsey уточняет — "второй функтор переводит любое отображение в его обратное"; Robert Furber (2016) — важный нюанс: если взять группоид конечномерных вещественных гильбертовых пространств и ОРТОГОНАЛЬНЫХ отображений (вместо всех линейных изоморфизмов), скалярное произведение даёт естественный изоморфизм между этими же функторами. Т.е. неестественность именно от того, что берутся ВСЕ линейные изоморфизмы.

### 21 голос — HenrikRüping (community wiki, 2 revisions; правка 26 окт 2015)
> The geometric realization of a simplicial set and the geometric realization of its barycentric subdivision are always homeomorphic. However there cannot be a natural isomorphism between these two functors. (Look at the diagram of simplicial sets Δ¹←Δ²→Δ¹. The maps are induced by 1,2,3↦1,1,2 and 1,2,3↦1,2,2).

(Требует симплициальных множеств/топологии — вне уровня аудитории курса.)

### 19 голосов — Qiaochu Yuan (community wiki; отвечено 14 авг 2013, 8:30)
> Take C=BG for some group G and take D=Set. A functor BG→Set is a G-set. Two G-sets are unnaturally isomorphic iff they have the same cardinality, and it's easy to find two G-sets of the same cardinality which are not isomorphic as G-sets, e.g. find a group with two non-conjugate subgroups of the same index.

Комментарий James Cranch: проще всего конструируется для ЛЮБОЙ нетривиальной G — сравнить действие G на себе умножением и тривиальное действие G на себе.

### 15 голосов — Eric Wofsey (community wiki, 2 revisions; правка 13 апр 2017)
> Here's a nice example that recently came up in an MSE question. Let k be a field and let Vect be the category of k-vector spaces and Aff be the category of k-affine spaces. Every vector space is an affine space, giving a forgetful functor F:Vect→Aff. On the other hand, every affine space has an associated vector space of the same dimension (the vector space of formal differences), giving a functor G:Aff→Vect. The composition GF:Vect→Vect is naturally isomorphic to the identity. The composition FG:Aff→Aff, on the other hand, is only unnaturally isomorphic to the identity: it takes every affine space to another affine space of the same dimension, but this cannot be made compatible with morphisms.

### 8 голосов — Arrow (community wiki, 3 revisions; правка 15 фев 2019)
> The structure theorem for finitely generated abelian groups furnishes for each A an isomorphism A≅T(A)⊕A/T(A) where T is torsion. This is a family of pointwise isomorphisms between 1_(Ab_f.g.) and the functor T⊕(1/T).
>
> **Claim.** These functors are not naturally isomorphic. In particular, the isomorphisms of the structure theorem are not natural.
>
> **Proof.** The endomorphism monoid of the identity functor is the multiplicative monoid ℤ. This can be seen by looking at naturality squares mapping out of ℤ and using its universal property as the free abelian group on a single generator. On the other hand, the functor T⊕(1/T) admits a nilpotent endomorphism [matrix (0 α; 0 0)] where α:1/T⇒T is given componentwise by A/T(A)→T(A)⊕A/T(A)→T(A). Thus 1, T⊕(1/T) have non-isomorphic endomorphism monoids whence they are themselves non-isomorphic functors.

Комментарий Julian Rosen: проще увидеть через нарушение точности/инъективности — T⊕1/T не является точным (унифицирует оба морфизма ℤ→ℤ/2ℤ).

### 7 голосов — Ronnie Brown (community wiki, 3 revisions; правка 16 авг 2013)
> I gave a more elaborate example to the Universal Coefficient splitting being non natural in my paper "Cohomology with chains as coefficients", Proc. London Math. Soc. (3) 14 (1964), 545–565 [...]. It is proved there that for chain complexes K,L which are free and are zero below dimension 0, there is an isomorphism for any abelian group G: H*(K⊗L,G)≅H*(K,H*(L,G)), which can be chosen to be natural with respect to maps of K but not with regard to maps of L, nor [...] maps of G.

### 5 голосов — guest (community wiki; отвечено 26 ноя 2018, 21:20)
> It seems that the functor on the category infinite sets that adds one disjoint point * to any set is not naturally isomorphic to the identity functor.

Комментарий David Roberts: не существует даже естественного преобразования φ:(–)⊔1⇒id, так как это заставило бы каждую биекцию сохранять базовую точку, добавленную к каждому множеству, — а это неверно.

### 3 голоса — Luca Bressan (community wiki; правка 14 авг 2013, 9:34)
> Here is an example of unnaturally isomorphic functors for which there does not exist any non-trivial natural transformation between them.
>
> Let C=ℕ^op, D=Ab, and consider F,G:C→D defined by F(n)=G(n)=ℤ for all n∈ℕ, F(m≤n)(x)=2^(n−m)x, G(m≤n)(x)=3^(n−m)x for all x∈ℤ.
>
> Suppose η={ηₙ:F(n)→G(n)} is a natural transformation. Then for any n we have that η₀(2ⁿx)=3ⁿηₙ(x), so 2ⁿη₀(x)=3ⁿηₙ(x). But then 3ⁿ∣η₀(x) for all n, which implies that η₀(x)=0, and so η=0 [для нетривиального η — поправка внесена после комментария Ricardo Andrade].

### 3 голоса — Joshua Grochow (community wiki, 2 revisions; правка 13 апр 2017)
> I'm pretty sure one can also categorify the fact that for ordinary complex representations of finite groups, number of irreducible representations = number of conjugacy classes. As in this closely related question [mathoverflow.net/questions/21606], one has a bijection (which categorifies to a pointwise isomorphism) but not a natural one.
>
> (The two functors [...] are contravariant functors from the category of finite groups to the category of k-linear categories. The first is F₁(G)=rep_ℂ(G). The second, F₂, takes a finite group G to the k-linear category freely generated by the conjugacy classes of G. [...])

### 0 голосов — Michael Barr (community wiki; отвечено 14 окт 2013, 18:58)
> Although there are already too many answers, let me just add the observation that one of the real motivations for The General Theory of Natural equivalences, was to understand the distinction between the fact that a finite dimensional vector space is isomorphic to its dual space, but naturally isomorphic to its second dual.

Комментарий Emil Jeřábek: "Which is undoubtedly the reason why this example is mentioned in the question itself."

---

## Linked / Related вопросы (список с сайта, для дальнейшей разведки)

**Linked:**
- 35 — No canonical isomorphism — https://mathoverflow.net/questions/390929/no-canonical-isomorphism
- 42 — Bijection between irreducible representations and conjugacy classes of finite groups — https://mathoverflow.net/questions/102879/
- 23 — Orbit structures of conjugacy class set and irreducible representation set under automorphism group — https://mathoverflow.net/questions/21606/
- 5 — What is the intuitive difference between these two simplicial subdivision functors? — https://mathoverflow.net/questions/456612/
- 8 — Constructing unnatural transformations — https://mathoverflow.net/questions/202560/

**Related:**
- 4 — About a General Definition of Profunctor — /questions/84807/
- 30 — What is a self-dual category? — /questions/92355/
- 8 — Constructing unnatural transformations — /questions/202560/
- 5 — Equivalence of natural transformations — /questions/223495/
- 9 — Does the existence of a derived functor imply existence of model structure? — /questions/261478/
- 8 — functors reflecting "isomorphism relations"? — /questions/353164/
- 11 — How can we make precise the notion that a finite-dimensional vector space is not canonically isomorphic to its dual via category theory? — /questions/385955/
- 11 — What is the category of covariant and contravariant functors? — /questions/389072/
- 4 — Isomorphism of coends — /questions/396137/

---

## ПРИЛОЖЕНИЕ — релевантные ответы из связанных вопросов (проверено тем же способом: браузер, 2026-07-23)

### Из вопроса 390929 "No canonical isomorphism" (35 голосов у вопроса; дубль-маркер, ссылается на 139388)

**35 голосов — Mark Wildon** (community wiki, 3 revisions; правка 23 апр 2021):
> Let X be a set. Permutations of X are in bijection with total orderings on X, but (unless |X|≤1) there is no canonical bijection.
>
> In terms of Joyal's theory of species, the species of total orders and of permutations are not isomorphic (i.e. the functors are not naturally isomorphic). But for any particular set X, there is a bijection between Ord(X) and Perm(X).
>
> This example is mentioned in the blog post *A visual telling of Joyal's proof of Cayley's formula* of [Tom] Leinster, giving a version of Joyal's proof of Cayley's formula that there are n^(n−2) labelled trees on an n-set. [...]

(Это тот же пример Sym/Ord, но с прямой связкой к формуле Кэли о числе деревьев — комбинаторный крючок.)

**20 голосов — Greg Martin** (отвечено 23 апр 2021, 7:02):
> For a more elementary example: any two cyclic groups of order n are isomorphic, but (when n≥3) there is no preferred isomorphism between any two given cyclic groups of order n. (This is essentially the same as the fact that a cyclic group of order n≥3 does not have a canonical generator.)

Комментарий Oscar Cunningham: ещё элементарнее — любые два множества мощности n изоморфны, но (при n≥2) канонической биекции между ними нет.

**14 голосов — Mees de Vries** (отвечено 23 апр 2021, 19:42):
> A deliberately extreme example: an isomorphism of sets is a bijection, and two sets are isomorphic when they have the same cardinality. There is generally no preferred bijection between sets of the same cardinality. For example, there is no canonical choice of bijection between commonly used sets like ℕ,ℤ,ℚ,ℤ²,ℚ̄.

**8 голосов — Zach Teitler** (отвечено 24 апр 2021, 0:50):
> ℝ[x]/(x²+1) is isomorphic to ℂ, but there's not a canonical isomorphism as x can map to i or −i. I suppose it's just a special case of {±i} as a ℤ/2ℤ torsor.

**21 голос — Maxime Ramzi**, **20 голосов — Igor Khavkine** (расслоения/связности), **20 голосов — Alexander Betts** (фундаментальная группа в разных точках) — все три требуют топологии/расслоений, вне уровня аудитории курса.

### Из вопроса 102879 "Bijection between irreducible representations and conjugacy classes of finite groups" (42 голоса у вопроса)

**30 голосов — Gjergji Zaimi** (отвечено 22 июл 2012, 17:32):
> In general there is no natural bijection between conjugacy classes and irreducible representations of a finite group. To see this think of abelian groups for example. The conjugacy classes are the elements of the group, while the irreducible representations are elements of the dual group. These are isomorphic, via the Fourier transform, but not canonically.

**51 голос — Qiaochu Yuan** — развёрнутый ответ через двойственность Хопф-алгебр (Z(k[G]) ↔ Ccl(G)); технически продвинутый, вне уровня аудитории, но подтверждает: "canonical bases of two canonically dual vector spaces, but these bases are not dual to each other, so I don't get a bijection this way."

### Из вопроса 385955 "...vector space is not canonically isomorphic to its dual..." (11 голосов у вопроса)

**17 голосов — Simon Henry** (отвечено 9 мар 2021, 19:30) — независимое подтверждение и явный механизм "спасательного" примера (тот же дух, что у Dan Petersen, 30 голосов, в основном вопросе):
> If you look at the category of finite dimensional vector spaces and linear isomorphisms between them, here V↦V∗ can be made into an actual (covariant) endofunctor of this category [...] an invertible arrow f:V→W induces (f∗)⁻¹:V∗→W∗. And there you can concretely show that there is no natural isomorphism between this functor and the identity.
>
> Indeed, choosing an isomorphism V≃V∗ gives you a non-degenerate bilinear form on V and you can always find an automorphism of V that does not preserve this bilinear form, which is exactly what the naturality on isomorphisms would mean!

(Комментарий Chris Schommer-Pries под самим вопросом 385955 формулирует то же самое ещё компактнее через категорию Pair пар (V,μ) с невырожденным спариванием μ:V⊗V→K и forgetful-функтор в Vect без сечения.)
