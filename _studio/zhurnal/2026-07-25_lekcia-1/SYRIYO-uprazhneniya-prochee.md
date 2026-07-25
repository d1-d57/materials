# СЫРЬЁ — упражнения из прочих источников (каркас Л1)

> Механическая выгрузка. Отбор НЕ сделан.

## Leinster, «Basic Category Theory», глава 1

**1.3.26.** . Of course, we say that functors F and G are naturally isomorphic if there exists a natural isomorphism from F to G. Since natural isomorphism is just isomorphism in a particular category (namely, [A , B]), we already have notation for this: F  G. Definition 1.3.12 F Given functors A G // B , we say that F(A)  G(A) naturally in A if F and G are naturally isomorphic. This alternative terminology can be understood as follows. If F(A)  G(A) naturally in A then certainly F(A)  G(A) for each individual A, but more is true: we can choose isomorphisms αA : F(A) → G(A) in such a way that the naturality axiom (1.3) is satisfied. Example 1.3.13 Let F, G : A → B be functors from a discrete categor

**1.3.32.** . □ This result can be compared to the theorem that every bijective group homomorphism is an isomorphism (that is, its inverse is also a homomorphism), or that a natural transformation whose components are isomorphisms is itself an isomorphism (Lemma 1.3.11). Those two results are useful because they allow us to show that a map is an isomorphism without directly constructing an inverse. Proposition 1.3.18 provides a similar service, enabling us to prove that a functor F is an equivalence without actually constructing an ‘inverse’ G, or indeed an η or an ε (in the notation of Definition 1.3.15). A corollary of Proposition 1.3.18 invites us to view full and faithful functors as, essentially, i

**1.3.29.** , ( ˆ ) is natural in the pair (A, X) if and only if it is natural in A for each fixed X and natural in X for each fixed A. So, it remains to check these two types of naturality. f Naturality in A states that for each X ∈ [A op , Set] and B −→ A in A , the 98 Representables square −◦H f [A op , Set](HA , X) / [A op , Set](HB , X) (ˆ) (ˆ)  X(A)  / X(B) Xf commutes. For α : HA → X, we have α _ / α ◦ Hf _   α ◦ H f B (1B ) / (X f )(αA (1A )),  αA (1A )  so we have to show that α ◦ H f B (1B ) = (X f )(αA (1A )). Indeed,  α ◦ H f B (1B ) = αB ((H f )B (1B )) = αB ( f ◦ 1B ) = αB ( f ) = (X f )(αA (1A )), where the first step is by definition of composition in [A op , Set], the second is b


## Фетисов, «Лекция 1. Категории и функторы» (НМУ) — русский, перекодирован из CP1251

*Полный текст лекции: `teoriya-kategoriy/istochniki/pdf/ru-fetisov-lekciya-1-TEXT.txt`*

**Упражнение 2. Пусть** F : A Ч B ? C  бифунктор. Доказать, что 1. Для любого a ? A правило Fa (b) = F (a, b), Fa (f ) = F (1a , f ) задајт функтор Fa : B ? C. h : a ? a0 определяет естественное преобразование ?h : Fa ? Fa0 по правилу ?h (b) = F (h, 1b ). 2. Любая стрелка

**Упражнение 3. Доказать изоморфизм следующих категорий:** 7 1. [A, B]op ' [Aop , B op ] 2. [A, B op ]op ' [Aop , B]

