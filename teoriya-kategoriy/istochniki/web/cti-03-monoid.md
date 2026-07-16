# Category Theory Illustrated - Monoids

> Источник: [https://abuseofnotation.github.io/category-theory-illustrated/03_monoid/](https://abuseofnotation.github.io/category-theory-illustrated/03_monoid/)
> Автор: Boris Marinov (abuseofnotation)
> Сохранено: 2026-07-16
> Лицензия: **Creative Commons Attribution-NonCommercial 4.0 (CC BY-NC 4.0)** (http://creativecommons.org/licenses/by-nc/4.0/) — сверено 2026-07-16.
> ⚠ **NonCommercial.** Курс, для которого собирается материал, — платный (~150 участников). Прямое заимствование картинок без разрешения автора конфликтует с NC-пунктом лицензии. См. MANIFEST.md и отчёт захода — решение за владельцем (можно писать автору, можно рисовать свои иллюстрации по мотивам идеи, не копируя).

---


![](/category-theory-illustrated/logo.svg)

# Monoids etc

Since we are done with categories, let’s look at some other structures that are also interesting — monoids.

## What are monoids

Like categories, monoids/groups are abstract systems consisting of a set of elements and operations, however, the operations look different than the operations we have for categories. Here is the definition:

A monoid is defined by a collection/set of elements $A$ (called the monoid’s underlying set ), together with an associative monoid operation — a rule for combining two elements that produces a third element one of the same kind — $A \circ A \to A$. 
Also, there should be an identity element $I$, such that $I \circ A = A$ and $A \circ I = A$.

Let’s take our familiar colorful balls.

![Balls](../03_monoid/balls.svg)

We can define a monoid based on this set by specifying an operation for “combining” two balls into one. An example of such an operation would be blending the colours of the balls as if we are mixing paint.

![An operation for combining balls](../03_monoid/balls_operation.svg)

You can probably think of other ways to define a similar operation. This will help you realize that there can be many ways to create a monoid from a given set of set elements i.e. the monoid is not the set itself, it is the set together with the operation .

### Associativity

The monoid operation should, like functional composition, be associative i.e. the way in which elements are grouped when applying the operation does not make any difference.

![Associativity in the color mixing operation](../03_monoid/balls_associativity.svg)

When an operation is associative, this means we can use all kinds of algebraic operations to any sequence of terms (or in other words to apply equation reasoning), like for example we can replace any element with a set of elements from which it is composed, or add a term that is present at both sides of an equation and retain the equality of the existing terms.

![Associativity in the color mixing operation](../03_monoid/balls_arithmetic.svg)

### The identity element

Actually, not any (associative) operation for combining elements makes for a monoid (it makes for a semigroup , which is also a thing, but that’s a separate topic). To be a monoid, a set must feature what is called an identity element of the operation, a concept of which you are already familiar from both sets and categories — it is an element that when combined with any other element gives back that same element (not the identity but the other one). Or simply $x • i = x$ and $i • x = x$ for any $x$.

In the case of our color-mixing monoid, the identity element is the white ball (or perhaps a transparent one, if we have one).

![The identity element of the color-mixing monoid](../03_monoid/balls_identity.svg)

As you probably remember from the last chapter, functional composition is also associative and it also contains an identity element, so you might start suspecting that it forms a monoid in some way. This is indeed the case, but with one caveat, which we will talk about later.

## Basic monoids

To keep the suspense, before we discuss the relationship between monoids and categories, we are going through see some simple examples of monoids.

### Monoids and numbers

Mathematics is not only about numbers, however, numbers do tend to pop up in most of its areas, and monoids are no exception. The set of natural numbers $\mathbb{N}$ (\(\{ 0, 1, 2, 3 ...\}\)) forms a monoid when combined with the all too familiar operation of addition (or under addition as it is traditionally said). This monoid is denoted $\left< \mathbb{N},+ \right>$ (in general, all monoids are denoted by specifying the set and the operation, enclosed in angle brackets).

![The monoid of numbers under addition](../03_monoid/numbers_addition.svg)

If you see a $1 + 1 = 2$ in your textbook you know you are either reading something very advanced, or very simple, although I am not really sure which of the two applies in the present case.

Anyways, the natural numbers also form a monoid under multiplication as well.

![The monoid of numbers under multiplication](../03_monoid/numbers_multiplication.svg)

Task 1: Which are the identity elements of those monoids?

Task 2: Go through other mathematical operations and verify that they are monoidal.

Task 3: The natural numbers form a monoid under multiplication, but not a group. Find out why.

### Monoids and boolean algebra

Thinking about operations that we covered, we may remember the boolean operations and and or . The operation and forms a monoid on the set, consisting of just two values ${ True, False }$, in which $True$ is the identity element (the symbol $\land$ means and ).

![Logical operations that form monoids](../03_monoid/logic_monoid.svg)

The operation or also forms a similar monoid.

Task 4: Prove that and $\land$ is associative by expanding the formula $(A \land B) \land C = A \land (B \land C)$ with all possible values. Do the same for or . Task 5: Which are the identity elements of the or operations?

## Monoid operations in terms of sets

We now know what the monoid operation is, and we even saw some simple examples. However, we never defined the monoid rule/operation formally i.e. using the language of set theory with which we defined everything else. Can we do that? Of course we can — everything can be defined in terms of sets.

We said that a monoid consists of two things: a set (let’s call it $A$), and a monoid operation that acts on that set. Since $A$ is already defined in set theory (because it is just a set), all we have to do is define the monoid operation.

Defining the operation is not hard at all. Actually, we have already done it for the operation $+$ — in Chapter 2, we said that addition can be represented in set theory as a function that accepts a product of two numbers and returns a number (formally $+: \mathbb{Z} \times \mathbb{Z} \to \mathbb{Z}$).

![The plus operation as a function](../03_monoid/plus_operation.svg)

Every other monoid operation can also be represented in the same way — as a function that takes a pair of elements from the monoid’s set and returns one other monoid element.

![The color-mixing operation as a function](../03_monoid/color_mixing_operation.svg)

Formally, we can define a monoid from any set $A$, by defining an (associative) function with type signature $A \times A \to A$. That’s it. Or to be precise, that is one way to define the monoid operation. And there is another way, which we will see next. Before that, let’s examine some other types of structures.

## Other monoid-like objects

Monoid operations obey two laws — they are associative and there exists an identity element . In some cases, we come across operations that also obey other laws that are also interesting. Imposing more (or less) rules to the way in which objects are combined results in the definition of other monoid-like structures.

### Commutative (abelian) monoids

Looking at the monoid laws and the examples we gave so far, we observe that all of them obey one more rule (law) which we didn’t specify — the order in which the operations are applied is irrelevant to the end result.

![Commutative monoid operation](../03_monoid/monoid_commutative.svg)

Such operations (ones for which combining a given set of elements yields the same result no matter which one is first and which one is second) are called commutative operations. Monoids with operations that are commutative are called commutative monoids .

As we said, addition is commutative as well — it does not matter whether I have given you 1 apple and then 2 more, or if I have given you 2 first and then 1 more.

![Commutative monoid operation](../03_monoid/addition_commutative.svg)

All monoids that we examined so far are also commutative . We will see some non-commutative ones later.

### Groups

A group is a monoid such that for each of its elements, there is another element which is the so-called “inverse” of the first one where the element and its inverse cancel each other out when applied one after the other. Plain-English definitions like this make you appreciate mathematical formulas more:

A group is a monoid in which every element $A$, has an inverse element, denoted usually as $-A$, such that $A \circ -A = I$ (where $I$ is the identity element).

If we view monoids as a means of modelling the effect of applying a set of (associative) actions, we use groups to model the effects of actions which are also reversible .

A nice example of a group, which is related to a monoid we covered, is the set of integers under addition — the operation is again ($+$), but the objects are the integers $\mathbb{Z}$, not the natural numbers $\mathbb{N}$ (so it’s not \(\{ 0, 1, 2, 3 ...\}\), but \(\{... -3, -2 -1, 0, 1, 2, 3 ...\}\)). The negative numbers are added, as the natural numbers don’t have inverses. The inverse of each number is its opposite number (positive numbers’ inverse are negatives and vice versa).

In this instance, the above formula becomes $x + (-x) = 0$

The study of groups is a field that is much bigger than the theory of monoids (and perhaps bigger than category theory itself). And one of its biggest branches is the study of “symmetry groups” which we will look into next.

### Summary

Before we move on — the algebraic structures that we saw above can be summarized based on the laws that define them in this table:

And now on to symmetry groups.

## Symmetry groups and group classifications

An interesting kind of groups/monoids are the groups of symmetries of geometric figures. Given some geometric figure, a symmetry is an action after which the figure is not displaced (e.g. it can fit into the same mold that it fitted before the action was applied).

We won’t use the balls this time, because in terms of symmetries, they have just one position and hence just one action — the identity action (which is its own reverse, by the way).

Instead, let’s take this triangle, which, for our purposes, is the same as any other triangle. We are not interested in the triangle itself, but in its rotations. The only thing we need to make ourselves believe is that this is an “unrotated” triangle i.e. the one which represents the identity rotation.

![A triangle](../03_monoid/symmetry_group.svg)

### Groups of rotations

Let’s first review the group of ways in which we can rotate our triangle i.e. its rotation group . A geometric figure can be rotated without displacement in positions equal to the number of its sides, so, for our triangle, there are 3 positions.

![The group of rotations in a triangle](../03_monoid/symmetry_rotation.svg)

Connecting the dots (or the triangles in this case) shows us that there are just 3 possible rotations that get us from any state of the triangle to any other one — a 120-degree rotation (i.e. flipping the triangle one time) and a 240-degree rotation (i.e. flipping it twice, or equivalently, flipping it once in the opposite direction) and the identity action of 0-degree rotation.

![The group of rotations in a triangle](../03_monoid/symmetry_rotation_actions.svg)

The rotations of a triangle form a monoid — the rotations are objects (of which the zero-degree rotation is the identity) and the monoid operation which combines two rotations into one is just the operation of performing the first rotation and then performing the second one.

Note once again that the elements in the group are the rotations , not the triangles themselves, actually the group has nothing to do with triangles, as we shall see later.

### Cyclic groups/monoids

The diagram that enumerates all the rotations of a more complex geometrical figure looks quite messy at first.

![The group of rotations in a more complex figure](../03_monoid/symmetry_rotation_square.svg)

But it gets much simpler to grasp if we notice the following: although our group has many rotations, and there are more still for figures with more sides (if I am not mistaken, the number of rotations is equal to the number of the sides), all those rotations can be reduced to the repetitive application of just one rotation , (for example, the 120-degree rotation for triangles and the 45-degree rotation for octagons). Let’s make up a symbol for this rotation.

![The group of rotations in a triangle](../03_monoid/symmetry_rotation_cyclic.svg)

Symmetry groups that have such “main” rotation are called cyclic

Groups and monoids that have an object that is capable of generating all other objects by its repeated application, are called cyclic groups . The group’s “main” object is called the generator .

All rotation groups/monoids are cyclic groups. Another example of a cyclic monoid is, yes, the natural numbers under addition, with $+1$ as the generator.

![The monoid of natural numbers under addition](../03_monoid/numbers_cyclic.svg)

The group of integers under addition is cyclic too — here we can use $+1$ or $-1$ as the generator (as whichever of the two we choose, we would get the other one by applying the inverse law).

![The group of integers under addition](../03_monoid/integers_cyclic.svg)

Wait, how can this be a cyclic group when there are clearly no cycles? This is because the integers are an infinite cyclic group.

A number-based example of a finite cyclic group is the group of integers under modular arithmetic (sometimes called “clock arithmetic”). Modular arithmetic’s operation is based on a number called the modulus (let’s take $12$ for example). In it, each number is mapped to the remainder of the integer division of that number and the modulus .

For example: $1 \pmod{12} = 1$ (because $1/12 = 0$ with $1$ remainder) $2 \pmod{12} = 2$ etc.

But $13 \pmod{12} = 1$ (as $13/12 = 1$ with $1$ remainder) $14 \pmod{12} = 2$, $15 \pmod{12} = 3$ etc.

In effect, numbers “wrap around” forming a group with as many elements as the modulus number. For example, a group representation of modular arithmetic with modulus $3$ has 3 elements.

![The group of numbers under addition](../03_monoid/numbers_modular.svg)

All cyclic groups that have the same number of elements (or that are of the same order ) are isomorphic to each other (careful readers might notice that we haven’t yet defined what a group isomorphism is, even more careful readers might already have an idea about what it is).

For example, the group of rotations of the triangle is isomorphic to the group of integers under the addition with modulo $3$.

![The group of numbers under addition](../03_monoid/symmetry_modular.svg)

All cyclic groups are commutative (or “abelian” as they are also called).

Task 6: Show that there are no other groups with 3 objects, other than $Z_3$.

There are commutative groups that are not cyclic, but, as we shall see below, the concepts of cyclic groups and commutative groups are deeply related.

### Group isomorphisms

We already mentioned group isomorphisms, but we didn’t define what they are. Let’s do that now:

An isomorphism between two groups is an isomorphism ($f$) between their respective sets of elements, such that for any $a$ and $b$ we have $f(a \circ b) = f(a) \circ f(b)$.

Visually, the diagrams of isomorphic groups have the same structure.

![Group isomorphism between different representations of S3](../03_monoid/group_isomorphism.svg)

As in category theory, in group theory isomorphic groups are considered instances of one and the same group. For example, the one above is called $Z_3$.

### Finite groups

Like with sets, the concept of an isomorphism in group theory allows us to identify common finite groups.

The smallest group is just the trivial group $Z_1$ that has just one element.

![The smallest group](../03_monoid/trivial_group.svg)

The smallest non-trivial group is the group $Z_2$ which has two elements.

![The smallest non-trivial group](../03_monoid/smallest_group.svg)

$Z_2$ is also known as the boolean group , due to the fact that it is isomorphic to the ${ True, False }$ set under the operation that negates a given value.

Like $Z_3$, $Z_1$ and $Z_2$ are cyclic.

## Group/monoid products

We already saw a lot of commutative groups that are also cyclic, but we didn’t see any commutative groups that are not cyclic. So let’s examine some of those like. Here, instead of looking into individual examples, we will present the general way in which commutative non-cyclic groups are produced — it is by uniting cyclic groups using the concept of group product .

Given any two groups, we can combine them to create a third group, comprised of all possible pairs of elements from the two groups and of the sum of all their actions.

Let’s see how the resulting group looks after taking the product of the following two groups (which, having just two elements and one operation, are both isomorphic to $Z_2$). To make it easier to imagine them, we can think of the first one as based on the vertical reflection of a figure and the second, as the horizontal reflection.

![Two trivial groups, each with two elements](../03_monoid/groups_product.svg)

(again we have to pick an element of each group to represent the identity rotatiom, so, pretend that the left versions of the figures are the “unflipped” versions, while the right ones are flipped (although it can work the other way around too))

We get the set of elements of the new group by taking the Cartesian product of the set of elements of the first group and the set of elements of the second.

![Two trivial groups and their product group, containg all combinations of an element from the first with the ](../03_monoid/groups_product_four.svg)

And the actions of a product group are comprised of the actions of the first group, combined with the actions of the second, where each action is applied only to the element that is a member of its original group, leaving the other element unchanged.

![Klein four](../03_monoid/klein_four_as_product.svg)

The product of the two groups presented is called the Klein four-group and it is the simplest non-cyclic commutative group.

Another way to present the Klein four-group is the group of symmetries of a non-square rectangle .

![Klein four](../03_monoid/klein_four.svg)

Task 7: Show that the two representations are isomorphic.

Here are some examples of how elements of the Klein four-group are combined.

![Klein four](../03_monoid/klein_four_examples.svg)

(i.e. horizontal/vertical rotations cancel each other out, while a horizontal rotation doesn’t cancel out a vertical one.)

The Klein four-group is non-cyclic (because there are not one, but two generators) — vertical and horizontal spin. It is, however, still commutative , because the ordering of the actions still does not matter for the end result. Actually, the Klein four-group is the smallest non-cyclic group .

### Cyclic product groups

In the previous chapter, we saw one non-cyclic product group (the Klein four-group), which was a product of cyclic groups . Most product groups (even the product of cyclic groups) would be non-cyclic, because it would have the generators of both groups that comprise it, i.e. even if the two original groups are cyclic and thus have 1 generator each, their product would still have 2 generators. But the product of two cyclic groups would still be cyclic if the number of elements of those groups (their orders ) don’t have a common divisor other than 1 (i.e. if they are relatively prime numbers ).

So, if you combine two groups with orders that have some common divisor (as $2$ and $2$, which are both divided by 2), then, their product would not be cyclic. But, if you combine two groups with orders that are relatively prime, (like $2$ and $3$) you would get a cyclic group.

Furthermore, the product of two relatively prime groups would be isomorphic to a cyclic group of the same order, as the product of the orders of its components e.g. the product of $Z_2$ and $Z_3$ is isomorphic to the group $Z_6$ ($Z_2\times Z_3 \cong Z_6$)

![Chinese reminder theorem](../03_monoid/chinese_remainder_theorem.svg)

(the generator just adds 1 to each of the two groups)

This is a consequence of an ancient result, known as the Chinese Remainder theorem .

### Commutative product groups

Product groups are commutative , provided that the groups that form them are commutative. We can see that this is true by noticing that, although there are multiple generators, each generator acts only on its own part of the group, so the generators don’t interfere with each other.

### Fundamental theorem of Finite abelian groups

Products provide one way to create non-cyclic commutative groups — by creating a product of two or more cyclic groups. The fundamental theory of finite abelian groups (or of finite commutative groups as we call them here) is a result that tells us that this is the only way to produce non-cyclic commutative groups i.e.

All finite commutative groups are either cyclic or products of cyclic groups.

We can use this law to gain an intuitive understanding of what commutative groups are, but also to test whether a given group can be broken down to a product of more elementary groups.

## Dihedral groups

Now, let’s finally examine a non-commutative group — the group of rotations and reflections of a given geometrical figure. It is the same as the last one, but here besides the rotation action that we already saw (and its composite actions), we have the action of flipping the figure vertically, an operation which results in its mirror image:

![Reflection of a triangle](../03_monoid/reflection.svg)

Those two operations and their composites result in a group called $Dih3$ that is not commutative i.e. it is non-commutative (and is furthermore the smallest non-commutative group).

![The group of rotations and reflections in a triangle](../03_monoid/symmetry_reflection.svg)

Task 8: Prove that this group is indeed not commutative.

Task 9: Besides having two main actions, what is the defining factor that makes this and any other group non-commutative?

Groups that represent the set of rotations and reflections of any 2D shape are called dihedral groups .

## Groups/monoids as categories

Now it’s the place for the grand reveal — groups/monoids are categories . More precisely, monoids are a specific type of categories , (and groups too).

This is not to say that the definition that we examined, where we describe them as sets and binary operations, is a lie. It just says that there is an alternative, categorical definition, which is equivalent to it. Let’s dive in.

### Monoid elements as objects

When we defined monoids, we presented their elements as objects and their operation — as a function/morphism that converts two objects into a third one. Then, we introduced a way for representing such operations using set theory — as functions that take a pair of elements from the monoid’s set and return one other monoid element.

![The color-mixing operation as a function](../03_monoid/color_mixing_operation.svg)

Under this correspondence, this specific mixing in the color-mixing monoid…

![Monoid operation](../03_monoid/operation_group.svg)

…corresponds to this specific point in the above function (point, being a mapping of a specific element of the set).

![Monoid operations as functions from pair of objects to a third object: (A X B) -> C)](../03_monoid/operation_pairs.svg)

However, this is not the only way to represent multi-argument functions set-theoretically — there is another, equally interesting way, that doesn’t rely on any data structures, but only on functions.

### Monoid elements as morphisms

We saw that for some groups, like the groups of symmetries and rotations, the group elements can be understood not as objects but as actions . This is actually true for all other groups as well, e.g. the red ball in our color-blending monoid can be seen as the action of adding the color red to the mix, the number $2$ in the monoid of addition can be seen as the operation $+2$ etc.

Formally, any function that takes a pair of objects, can be transformed to a function that takes one object and returns a function that takes the other one and returns the result.

![Monoid operations as functions (A X B) -> C) = A -> B -> C](../03_monoid/operation_functions.svg)

This transformation is called currying in the name of Haskell Curry, although it was invented some years earlier by Moses Schönfinkel ( Schönfinkelisation didn’t stick out for some reason). So, Schönfinkel discovered that the following two expressions are isomorphic.

![The equivalence of curried and uncurried functions](../03_monoid/curry.svg)

Let’s take a step back and examine the groups/monoids that we covered so far in light of this equivalence e.g. let’s examine the symmetric group $Z_3$:

![The group of rotations in a triangle - group notation](../03_monoid/symmetry_rotation_actions.svg)

The elements of this group can be viewed as functions which take a figure and rotate it a given amount of degrees.

![The group of rotations in a triangle - set notation](../03_monoid/symmetry_rotation_functions.svg)

And, we can represent the group operation itself as functional composition.

![The group of rotations in a triangle - set notation and normal notation](../03_monoid/symmetry_rotation_set.svg)

Formally, the 3 elements of $Z_3$ can be seen as 3 bijective (invertible) functions from a set of 3 elements to itself (in group-theoretic context, these kinds of functions are called permutations , by the way).

We can do the same for the addition monoid — numbers can be seen not as quantities (as in two apples, two oranges etc.), but as operations , (e.g. as the action of adding two to a given quantity).

Formally, the operation of the addition monoid, that we saw above has the following type signature.

$+: \mathbb{Z} \times \mathbb{Z} \to \mathbb{Z}$

Because of the isomorphism we presented above, this function is equivalent to the following function.

$+: \mathbb{Z} \to (\mathbb{Z} \to \mathbb{Z})$

When we apply an element of the monoid to that function (say $2$), the result is the function $+2$ that adds 2 to a given number.

$+2: \mathbb{Z} \to \mathbb{Z}$

And because the monoid operation is always given in the context of a given monoid, we can view the element $2$ and the function $+2$ as equivalent in the context of the monoid.

$2 \cong +2$

In other words, in addition to representing the monoid elements in the set as objects that are combined using a function, we can represent them as functions themselves.

### Monoid operations as functional composition

As we said, when monoid elements are represented as functions, the monoid operation is represented as functional composition . The functions that represent the monoid elements have the same set as source and target, or the same signature , as we say (formally, they are of the type $A \to A$ for some $A$). Because of that, they all can be composed with one another, and the result of such compositions would also have the same signature.

![The group of rotations in a triangle - set notation](../03_monoid/symmetry_rotation_cayley.svg)

This is true for all monoids, e.g. number functions can also be combined using functional composition.

$+2 \circ +3 \cong +5$

So, basically, the functions that represent the elements of a monoid also form a monoid, under the operation of functional composition (and the functions that represent the elements that form a group also form a group).

Task 10: Which are the identity elements of function groups?

Task 11: Show that the functions representing inverse group elements are also inverse.

### Cayley’s theorem

Let’s recap: in the previous section, we showed how the elements of every group/monoid correspond to functions from the monoid’s underlying set to itself (AKA to permutations), and we said that those permutations make up a monoid of their own, under functional composition — the monoid of permutations, let’s call it.

![The group of rotations in a triangle - set notation](../03_monoid/symmetry_rotation_cayley.svg)

One thing that we didn’t say in the prev section: every such permutation group/monoid is isomorphic to the monoid from which it is constructed.

![The group of rotations in a triangle --- set notation and normal notation](../03_monoid/symmetry_rotation_comparison.svg)

This is a result known as the Cayley’s theorem. In short:

Any group is isomorphic to its corresponding permutation group.

Or formally, if we use $Perm$ to denote the permutation group then Cayley’s theorem states that $Perm(A) \cong A$ for any $A$.

Or in other words, representing the elements of a monoid/group as permutations actually yields a representation of the monoid itself (sometimes called its standard representation ) e.g. a triangle is a figure such that if you flip it two times it would go back to the original position (and everything that you can flip two times and go back to the original position is a triangle).

Cayley’s theorem is a very important result, so the fact that it does not look impressive in this context only shows the power of the categorical framework (and how much we learned).

### Monoids as categories

We saw that converting the monoid’s elements to actions/functions yields an accurate representation of the monoid in terms of sets.

![The group of rotations in a triangle - set notation](../03_monoid/symmetry_rotation_cayley.svg)

However, it is obvious that it is the functions of the monoids, not their sets that are important (after all, with monoids you have the same set everywhere) , so we can try depicting it as a categorical (external) diagram.

![The group of rotations in a triangle - categorical notation](../03_monoid/symmetry_rotation_external.svg)

But wait, if the monoids’ underlying sets correspond to objects in category theory, then the corresponding category would have just one object. And so the correct representation would involve just one point from which all arrows come and to which they go.

![The group of rotations in a triangle - categorical notation](../03_monoid/symmetry_rotation_category.svg)

So a monoid, any monoid, can be seen as a category with one object

### Formal definition

Let’s check if that is really true, by reviewing the definition of a category:

A category is a collection of objects (we can think of them as points) and morphisms (arrows) that go from one object to another, where:

- Each object has to have an identity morphism.
- There should be a way to compose two morphisms with an appropriate type signature into a third one in a way that is associative.
Let’s see what these laws imply for categories with one object:

- Each object has to have an identity morphism.
For categories with just one object, there would also be one identity morphism. And monoids do have an identity object , which when viewed categorically corresponds to that identity morphism:

- There should be a way to compose two morphisms with an appropriate type signature into a third one in a way that is associative.
But if the category has one object, all morphisms would have the same type signature (they would just be $A \to A$). So then all morphisms would be composable with one another . The monoid operation does exactly that — given any two objects (or two morphisms, if we use the categorical terminology), it creates a third.

We see that aside from the little-confusing fact that monoid objects are morphisms when viewed categorically, this describes exactly what monoids are.

A monoid, any monoid, can be seen as a category with one object —the morphisms of the category are the monoid elements, the identity morphism is the identity element and the monoid operation is composition of morphisms. The converse is also true: any category with one object can be seen as a monoid

Philosophically, defining a monoid as a one-object category corresponds to the view of monoids as a model of how a set of (associative) actions that are performed on a given object alter its state. Provided that the object’s state is determined solely by the actions that are performed on it, we can leave it out of the equation and concentrate on how the actions are combined. And as per usual, the actions (and elements) can be anything, from mixing colors, to adding quantities to a given set of things etc.

## Group/monoid presentations

In the previous section, we proved that monoids are indeed equivalent to one-object categories. However, the implications of this statement still seem a bit baffling: Does this mean that all monoids and monoids (even ones with different underlying sets!) are kinda one and the same? The answer is that they are indeed similar, at least when we are viewing isomorphic monoids as one and the same monoid. The only differences between them can be traced in these two things:

- The number of morphisms that they have.
- The laws governing the composition of those morphisms.
Formally, the set of generators and laws that defines a given monoid is called the presentation of a monoid and every monoid can be defined by specifying its presentation. And this observation leads to a whole new way of defining a monoid/monoid.

### Cyclic monoids

Let’s imagine one specific set of categories: categories that, besides having one object, also have just one morphism (besides the identity).

![Presentation of an infinite cyclic monoid](../03_monoid/infinite_cyclic_presentation.svg)

Those category corresponds exactly to cyclic monoids/monoids (the morphism is the generator).

And the difference between all cyclic monoids/monoids is determined solely by the laws.

### Z3

Let’s turn our attention to the second component of the presentation — the laws describing the result of the composition of given two morphism.

In our case with cyclic monoids, we are talking about the result of composing the only morphism that forms the monoid with itself.

Here is one law that we may define:

When you compose the generator with itself 3 times, you get identity morphism.

We can denote it like this:

![Presentation of a finite cyclic monoid](../03_monoid/finite_cyclic_presentation.svg)

So, what is the monoid that this law defines? To find out, we start composing the monoid generator with itself, and then applying the law, until we find all possible sequences of compositions.

![Presentation of a finite cyclic monoid](../03_monoid/finite_cyclic_presentation_elements.svg)

(because if we compose the morphism with itself one more time we will be back to the identity).

As you can already guess, this monoid is just our familiar monoid $Z_3$ — the monoid of triangle rotations, or the modular arithmetic with modulo 3.

And what would happen if we reformulating the law so instead of 3 it says some other number $n$.

When you compose the generator with itself $n$ times, you get identity morphism.

This would yield all other cyclic monoids: $Z_1$ $Z_2$ $Z_3$ etc…

### Klein-four

We can represent product monoids this way too. Let’s take Klein four-monoid as an example, The Klein four-monoid has two generators that it inherits from the monoids that form it (which we considered as vertical and horizontal rotation of a non-square rectangle) each of which comes with one law.

![Presentation of Klein four](../03_monoid/klein_four_presentation.svg)

To make the representation complete, we add the law for combining the two generators.

![Presentation of Klein four - third law](../03_monoid/klein_four_presentation_third_law.svg)

And then, if we start applying the two generators and applying the laws, we get the four elements of the monoid.

![The elements of Klein four](../03_monoid/klein_four_presentation_elements.svg)

### Free monoids

We saw how picking a different selection of laws gives rise to different types of monoids. But what would we get if we pick no laws at all ? These monoids (we get a different one depending on the set of morphisms we pick) are called free monoids , as in “free from laws” (or as in, “you can upgrade the set of generators to a monoid for free”).

The free monoid with just one generator is isomorphic to the monoid of natural numbers.

![The free monoid with one generator](../03_monoid/infinite_cyclic_presentation_elements.svg)

We can make a free monoid from the set of colorful balls — the monoid’s elements would be sequences of all possible combinations of the balls.

![The free monoid with the set of balls as a generators](../03_monoid/balls_free.svg)

### The universal property of free monoids

Free monoids a special one, in that you can define a function that converts it to any other monoid which has the same set of generators, By just applying the monoid’s laws.

For example, if we take the free monoid with just one generator, and apply to it’s elements the law of $Z_3$, we get… a function from it to $Z_3$,

![The free monoid with one generator](../03_monoid/infinite_cyclic_presentation_z3.svg)

And if we take the free monoid of balls, and we apply the laws of the color-mixing monoid, we would get a function from the free monoid of balls to the color-mixing monoid.

![Converting the elements of the free monoid to the elements of the color-mixing monoid](../03_monoid/balls_free_color_mixing.svg)

Task 14: Write up the laws of the color-mixing monoid.

If we put on our programmers’ hat, we will see that the type of the free monoid under the set of generators T (which we can denote as FreeMonoid<T> ) is isomorphic to the type List<T> and that the intuition behind the special property that we described above is actually very simple: keeping objects in a list allows you to convert them to any other structure i.e. when we want to perform some manipulation on a bunch of objects, but we don’t know exactly what this manipulation is, we just keep a list of those objects until it’s time to do it.

# Buy full version

Ko-fi

Patreon

Gumroad

# Subscribe for updates

# Contents

About

Sets

Categories

Monoids

Orders

Logic

Types

Functors

Natural transformations

# Created by Jencel Panic

personal blog

email

mastodon

twitter

Github

Made with Jekyll Book Boilerplate . 

            Drawn in Inkscape . 

            Set in Mell Sans .

This work is licensed under a Creative Commons Attribution-NonCommercial 4.0 International License .

Presentation mode
