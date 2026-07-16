# Category Theory Illustrated - Categories

> Источник: [https://abuseofnotation.github.io/category-theory-illustrated/02_category/](https://abuseofnotation.github.io/category-theory-illustrated/02_category/)
> Автор: Boris Marinov (abuseofnotation)
> Сохранено: 2026-07-16
> Лицензия: **Creative Commons Attribution-NonCommercial 4.0 (CC BY-NC 4.0)** (http://creativecommons.org/licenses/by-nc/4.0/) — сверено 2026-07-16.
> ⚠ **NonCommercial.** Курс, для которого собирается материал, — платный. Прямое заимствование картинок без разрешения автора конфликтует с NC. Решение за владельцем.

---

# From Sets to Categories

In this chapter, we will see some more set-theoretic constructs, but we will also introduce their category-theoretic counterparts in an effort to gently introduce the concept of a category itself.

When we are finished with that, we will try (and almost succeed) to define categories from scratch, without actually relying on set theory.

## Products

In the previous chapter, we needed a way to construct a set whose elements are *composite* of the elements of some other sets e.g. when we discussed mathematical functions, we couldn’t define $+$ and $-$ because we could only formulate functions that take one argument. Similarly, when we introduced the primitive types in programming languages, like `Char` and `Number`, we mentioned that most of the types that we actually use are *composite* types. So how do we construct those?

So, consider a set $A$ (containing $a$’s) and a set $B$ (containing $B$’s)

![Product parts](../02_category/product_parts.svg)

We introduce a new set that combines those two sets into one, their product set.

![Product](../02_category/product.svg)

> The *Cartesian product* (or *tuple*) of sets $A$ and $B$ (denoted $A \times B$) is the set of *ordered pairs* that contain one element of the set $A$ and one element of the set $B$. Or formally speaking: $A \times B = { (a, b) }$ where $a ∈ A, b ∈ B$ ($∈$ means “is an element of”).

**Task 1**: Why is this called a product? Hint: How many elements does it have?

Naturally, the product comes equipped with two functions, one for each property, which allow you to take a pair and extracts the value of the property,

![Product](../02_category/product_functions.svg)

For each set $C$, that is a product of $A$ and $B$, there are two functions $C \to A$ and $C \to B$, called the product’s *projections* that retrieve back its (the product’s) constituent values).

(in programming terms, we would dub these the “getters”)

### Triple product

There are occasions where we want to combine not two, but three sets into a product (e.g. $A \times B \times C$). But we don’t need to define the concept of triple product separately: we can achieve it by combining the first and second one into a product and then combining their product with the third set, (so it will be $(A \times B) \times C$.

![Triple product](../02_category/triple_product.svg)

There is another way to make a triple product of three sets — combining the second and the third one and then combining the result with the first one (so $A \times (B \times C)$, but it doesn’t actually matter which one you use — if we view isomorphic sets as equal, the end results would be the same i.e.

> The two ways of combining three sets into a triple product are isomorphic, $(A \times B) \times C \cong A \times (B \times C)$.

![Triple product](../02_category/triple_product_associativity.svg)

You might recognize this diagram from the section on functional composition. It means that the cartesian product operation is (like functional composition), *associative*.

### Products as Objects

In the previous chapter, we established the correspondence of various concepts in programming languages and set theory — sets resemble types, and functions resemble methods/subroutines. This picture is made complete with products, that are like stripped-down *classes* (also called *records* or *structs*) — the sets that form the product correspond to the class’s *properties* (also called *members*) and the functions for accessing them are like what programmers call *getter methods* e.g. the famous example of object-oriented programming of a `Person` class with `name` and `age` fields is nothing more than a product of the set of strings, and the sets of numbers. And, as we showed, objects with more than two values can be expressed as compositions of nested products.

### Using Products to define Numeric Operations

Products can also be used for expressing functions that take more than one argument (and this is indeed how multi-param functions are implemented in some languages, like the ones from the ML family). For example, “plus” is a function from the set of products of two numbers to the set of numbers, so, $+: \mathbb{Z} \times \mathbb{Z} → \mathbb{Z}$.

![The plus function](../02_category/plus.svg)

By the way, such functions (ones that take two objects of one type and return a third object of the same type) are called *operations*.

### Defining products in terms of sets—Internal definition

A product is, as we said, a set of *ordered* pairs (formally speaking $A \times B ≠ B \times A$). So, to define a product we must define the concept of an ordered pair. So how can we do that?

![An ordered pair of two elements](../02_category/pair.svg)

Note that an ordered pair of elements is not just a set containing the two elements (that would be an *unordered pair*)

![An unordered pair of two elements: just a set containing two elements](../02_category/unordered_pair.svg)

but it also contains information about which of those objects comes first and which one goes second in the pair—some mathematical operations (such as addition) don’t care about order, others (such as subtraction) do. And in programming, we have the ability to assign names to each property of an object, which accomplishes the same purpose—allows us to access a specific property of the object, not just any random property.

So, if an ordered pair isn’t a set, does that mean that we have to define it as a “primitive” type like we defined sets if we want to use them? That’s possible, but there is another approach. We can define a construct that is *isomorphic* to the ordered pair, using only sets. And mathematicians have come up with multiple ingenious ways to do that. Here is the first one, which was suggested by Norbert Wiener in 1914. Note the smart use of the fact that the empty set is unique.

![A pair, represented by sets](../02_category/pair_as_set_2.svg)

The next one was suggested by Felix Hausdorff in the same year. In order to use that one, we just have to define $1$, and $2$ first.

![A pair, represented by sets](../02_category/pair_as_set_3.svg)

Suggested in 1921 by Kazimierz Kuratowski, this one uses just the component of the pair.

![A pair, represented by sets](../02_category/pair_as_set_1.svg)

All of these definitions work by *zooming in* into the individual elements of the product. We may think of this as a *low-level* approach to the definition, one which which focuses on the product’s *internal* structure. But, more interesting, at least for category theory, is the *high-level* approach — instead of zooming in we *zoom out*, we stay completely oblivious to the contents of our sets and focus only on the functions that are associated with the product.

### Defining products in terms of functions—external definition

Now, we will look into a category-theoretic definition of the product set. We call this definition *external* because it is based not on the internal structure that the object has, but on it’s external behavior (which is defined by the functions that come from and go to it). And because it is strongly related to external diagrams.

Such definitions are driven by a conceptual model of the object we want to define. For example, we can agree that a product of $A$ and $B$ is some sort of combination that contains $A$ and $B$ (and nothing more).

Now, based on that conceptual model, we must, given two sets, devise a way to pinpoint the set that is their product, by looking at the functions that come from/to them.

So, we said that a product of $A$ and $B$ contains an $A$ and $B$. So, what are the functions that can fulfils these criteria? Of course that would be the projections, the functions for retrieving back the two elements: $A \times B \to A$ and $A \times B \to B$.

![Product](../02_category/product_functions.svg)

Now if we switch to the (semi) external view, this diagram already provides some definition of what a product is:

![Product, external diagram](../02_category/product_external.svg)

> The product of $A$ and $B$, denoted $A \times B$, is a set such that:

> 1. There exist two “projection” functions $A \times B \to A$ and $A \times B \to B$…

In other words, if we have a set $C$ for which there are functions $C \to A$ and $A \times B \to B$, then $C$ can potentially be equal to $A \times B$.

However, this definition is not complete, as the product $A$ and $B$, is not the *only* set for which such functions can be defined. For example, a set of triples, that we already examined (or the triple product) $A \times B \times X$ for any element $X$ also qualifies. Any other set that would happen to have some functions to $A$ and $B$, and would, by this definition, be “impostor product”.

![Product, external diagram](../02_category/product_candidates.svg)

To expose those impostors, we go back to our conceptual definition. Remember that we said $A \times B$ contains an element of $A$, an element of $B$ *and nothing more*. This tells us that each of these impostors $I$ can be *converted* to $A \times B$, i.e. that there is an arrow $I \to A \times B$ . Why? As we said, all such sets would be *more complex* than the product. And you can always have a function that converts a more complex structure to a simpler one by just throwing information away.

![Product, external diagram](../02_category/product_morphisms.svg)

We can know that this arrow would exist for every product because any element of the impostor set $I$, containing an element of $A$, an element of $B$ *and something more*, there exist an element of the set $A \times B$ that contains the same element of $A$ and the same element of $B$ (and nothing more). So, we can define a function $I \to A \times B$, that throws away that extra information.

And even more interestingly, the projection functions (for retrieving the elements) $I \to A$ and $I \to B$, because of which $I$ is an impostor, can be defined in terms of this function $I \to A \times B$.

As an example, take the set of triples, $A \times B \times X$ for any $X$. The canonical function that converts it to a product $A \times B \times X \to A \times B$ is the function that just removes the third element $X$.

![Triple product, internal diagram](../02_category/product_triple_internal.svg)

And we can see that the projections can be easily defined using this function.

![Triple product, internal diagram](../02_category/product_triple_internal_diagram.svg)

That is, if we dub this function $g: A \times B \times X \to A \times B$ and let $f^{1}$ and $f^{2}$ be the projections of the product ($f^{1} : A \times B \to A$ and $f^{2} : A \times B \to B$), then, the arrow that connects the triple $A \times B \times X$ to $A$ and $B$ are just the compositions $f^{1}\circ g$ and $f^{2} \circ g$. It is almost as if $A \times B \times X$ *is only connected to $A$ and $B$ because of this function*.

![Triple product, external diagram](../02_category/product_triple.svg)

More formally, we can define the product in the following way.

> The product of $A$ and $B$, denoted $A \times B$, is a set such that:

> 1. There exist two “projection” functions $f^{1}: A \times B \to A$ and $f^{2}: A \times B \to B$.

> 2. For any impostor product $I$, that also has such projection functions ($I \to A$ and $I \to B$), there must also exist a unique function (called universal morphism) with the type signature $g: I \to A \times B$, that converts the impostor product to the real product, such that the projections of the impostor would be just the composition of $g$ with the projections of the product i.e. $f^{1}\circ g: I \to A $ and $f^{2} \circ g: I \to B$.

We prove that a given set is a product by giving a formula for the function $g$, such that it fits our criteria. Given functions $g^{1}: I \to A$ and $g^{2}: I \to B$, the function $g$ would be just the function that makes up a pair of the results of those two functions, so if $i$ is an element of $I$, then $g = (i) \to (g^{1}(i), g^{2}(i))$.

So, the function $g$ exist for every object $I$.

> The product of $A$ and $B$, denoted $A \times B$, defined in such a way that all the paths in this diagram are equivalent, for all objects $I$, that are connected to $A \times B$.

> ![Product, universal property](../02_category/product_universal_property.svg)

You would see a lot of similar definitions and diagrams in this book. In category theory, we often (always) define properties that a given object might possess, by defining a structure such that all similar objects can be converted to it. This is what we call a *universal property*, but it is too early to go into more detail, (after all we haven’t even yet said what category theory is).

### Isomorphism and equality

If we remember the three definitions of products in terms of sets and set structure, that we saw earlier and try to determine which of them is the “real” product, which is defined by the universal property, we will see that they *all* are the real product. This is because they are all isomorphic to one another. This is OK: when we represent things using universal properties, isomorphism is treated as equality.

> If a set $C$ satisfies a given universal property (such as being the product of $A$ and $B$), then any set isomorphic to $C’$ would also satisfy it.

(This is so, because you can easily construct the universal morphism from $C’$ from the universal morphism of $C$).

We say that the product of two sets is “unique up to *an isomorphism*. This is a shorthand for “there are actually more than one of it, but they are all isomorphic to each other, so we don’t care”.

This is the same viewpoint that we often adopt in programming, especially when we work on the higher level: although there might be many different implementations list or a pair, or many different formats in which a given data can be stored, as long as we have a way to convert one to the other (and vice versa they are all the same to us.

## Sums

We will now study a construct that is pretty similar to the product but at the same time is very different. Similar because, like the product, it is a relation between two sets which allows you to unite them into one, without erasing their structure. But different as it encodes a very different type of relation — a product encodes an *and* relation between two sets, while the sum encodes an *or* relation.

![Sum or coproduct](../02_category/coproduct.svg)

> The sum of two sets $A$ and $B$, denoted $A + B$ is a set that contains all elements from $A$ combined with all elements from $B$.

### Defining sums in terms of sets—internal definition

As with the product, representing sums in terms of sets is not so straightforward e.g. when a given object is an element of both sets, then it appears in the sum twice which is not permitted, because a set cannot contain the same element twice.

And, as with the product, there is a low-level way to express a sum using sets alone. Incidentally, we can use pairs.

![A member of a coproduct, examined](../02_category/coproduct_member_set.svg)

### Defining sums in terms of functions—external definition

As you might already suspect, the interesting part is expressing the sum of two sets using functions. To do that, we have to go back to the conceptual part of the definition. We said that sums express an *or* relation between two things.

A property of every *or* relation is that if something is an $A$ that something is also an $A \vee B$ (The $\vee$ symbol means *or* by the way). For example, if my hair is *brown*, then my hair is also *either blond or brown*. This is what *or* means, right? This property can be expressed as a function, two functions actually — one for each set that takes part in the sum relation (for example, if parents are either mothers or fathers, then there surely exist functions $mothers → parents$ and $fathers → parents$).

![Coproduct, external diagram](../02_category/coproduct_external.svg)

As you might have already noticed, this definition is pretty similar to the definition of the product from the previous section — the difference being reversed arrows. And the similarities don’t end here. As with products, we have sets that can be thought of as *impostor* sums — ones for which these functions exist, but which also contain additional information.

![Coproduct, external diagram](../02_category/coproduct_candidates.svg)

All these sets express relationships which are more vague than the simple sum, and therefore given such a set, there would exist a unique function that would distinguish it from the true sum. The only difference is that, unlike the functions that define products, this time this function goes *from the sum* to the impostor.

![Coproduct, external diagram](../02_category/coproduct_morphisms.svg)

Here is the definition:

> The sum of $A$ and $B$, denoted $A + B$, is a set, such that:

> 1. There exists two “projection” functions $A \to A + B$ and $B \to A + B$.

> 2. For any impostor sum $I$, that also has such projection functions ($A \to I$ and $B \to I$), there must also exist a unique function with the type signature $g: A + B \to I$, that converts the real sum to the impostor sum, such that the projections of the impostor sum be just the composition of $g$ with the projections.

## Interlude: Categorical Duality

The concepts of product and sum might already look similar in a way when we view them through their internal diagrams. The *external* view makes this similarity precise — these two diagrams are one and the same diagram, only their arrows are flipped — many-to-one relationships become one-to-many and the other way around.

![Coproduct and product](../02_category/coproduct_product_duality.svg)

The universal properties that define the two constructs are the same as well — if we have a sum $A + B$, for each impostor sum, such as $A + B + X$, there exists a trivial function $A + B \to A + B + R$.

And, if you remember, with products the arrows go the other way around — the equivalent example for a product would be the function $A \times B \times R \to A \times B $

This fact uncovers a deep connection between the concepts of the *product* and *sum*, which is not otherwise apparent — they are each other’s opposites. *Product* is the opposite of *sum* and *sum* is the opposite of *product*.

In category theory, concepts that have such a relationship are said to be *dual* to each other. So, the concepts of *product* and *sum* are dual. This is why sums are known in a category-theoretic setting as *converse product*, or *coproduct* for short. This naming convention is used for all dual constructs in category theory.

## Defining the rest of set theory externally categorically

So far in the book, we saw some amazing ways of defining set-theoretic constructs without looking at the set elements and by only using external diagrams.

In the first chapter, we defined functions and functional composition with this diagram.

![Functional composition](../02_category/functions_compose_sets.svg)

And now, we also defined products and sums.

![Coproduct and product](../02_category/coproduct_product_duality.svg)

What’s even more amazing, is that we can define *all of set-theory*, based just on the concept of functions, as discovered by the category theory pioneer Francis William Lawvere.

### Defining set elements externally

Traditionally, everything in set theory is defined in terms of two things: *sets* and *elements*, so, if we want to define it using *sets* and *functions*, we must define the concept of a *set element* in terms of functions.

To do so, we will use the singleton set.

![The singleton set](../02_category/elements_singleton.svg)

OK, let’s start by taking a random set which we want to describe.

![A set of three elements](../02_category/elements_set.svg)

And let’s examine the functions from the singleton set, to that random set.

![Functions from the singleton set](../02_category/elements_singleton_functions.svg)

It’s easy to see that there would be exactly one function for each element of the set. So we may say that:

> Each element of a set $X$ is isomorphic to a function \(1 \to X\) (where \(1\) means the singleton set).

So, we can say that what we call “elements” of a set are the functions from the singleton set to it.

So, our example set would look like this.

![Functions from the singleton set](../02_category/elements_singleton_functions_partly_external.svg)

However, our diagram is not yet fully external, as it depends on the idea of the singleton set, i.e. the set with one *element*. Furthermore, this makes the whole definition circular, as we cannot define the concept of a one-element set, without the concept of element.

### Defining the singleton set externally

We define the singleton set externally in the same way as we did define products and sums - by using a unique property that the singleton set has. In particular, in the last chapter we learned the following:

> There is a unique function from any set to any singleton set.

If $1$ is the singleton set, then we have exactly one function $X \to 1$ for all objects \(X\) i.e. $\forall X \exists! (X \to 1)$ (where $\exists!$ means “Exists unique”).

![Terminal object](../02_category/terminal_object_internal.svg)

It turns out that this property defines the singleton set uniquely i.e. there is no other set that has it, other than the sets that are isomorphic to the singleton set. This is simply because, if there are two sets that have it, those two sets would also have unique functions between *themselves* so they would be isomorphic to one another. More formally, if we have two sets $X$ and $Y$ such that $\exists!X \to 1 \land \exists!Y \to 1$ and they both hold this property (“exactly one function from any other set to this set”) then we also have $X \cong Y$.

![Terminal object](../02_category/terminal_object_internal_isomorphisms.svg)

And because there is no other set, other than the singleton set that has this property, we can use it as a definition of the singleton set:

> The singleton set $1$ is one such that there exist a unique functions from any other set to it i.e. we have $\forall X \exists! X \to 1$, then $1$ is the singleton set.

![Terminal object](../02_category/terminal_object.svg)

With this, we acquire a fully external definition (up to an isomorphism) of the singleton set, and thus a definition of a set element — the elements of a given set…

![A set of three elements](../02_category/elements_set.svg)

…are just the functions from the singleton set to that set.

![Functions from the singleton set](../02_category/elements_external.svg)

Note that from this property it follows that the singleton set has exactly one element, which confirms that our definition is correct.

![Functions from the singleton set](../02_category/singleton_elements_external.svg)

**Task 2:** Why exactly does it follow (check the definition)?

### Defining the empty set externally

The empty set is, of course, the set that has no elements, but how would we say this without referring to elements?

In the previous chapter, we noted an interesting property of the empty set:

> There is a unique function from the empty set to any other set.

And, again, since the empty set is the only set that has this property, we can reverse the above statement and use it as a definition:

> The empty set is a set such that there exists a function from it to any other set.

*Task 3:* why is the function from the empty set unique?

![Initial object](../02_category/initial_object.svg)

Observant readers will notice the similarities between the diagrams depicting the initial and terminal object (yes the two concepts are, of course, dual of each other).

![Initial terminal duality](../02_category/initial_terminal_duality.svg)

Some *even more* observant readers (folks, keep it down please, you are *too observant*) may also notice the similarities between the product/coproduct diagrams and the initial/terminal object diagrams.

![Coproduct and product](../02_category/coproduct_product_duality.svg)

The similarity of the diagrams, is due to a similar general approach of defining things — in both cases we find the property that makes a given concept useful and then define the concept so it has this property*.

### Functional application

After seeing the functional definition of set elements, we might be inclined to ask the following: If elements are represented by functions, then how do you *apply* a given function to an element of a set, (and retrieve an element of another set)?

![Functional application - internal diagram](../02_category/application_internal_function.svg)

The answer is surprisingly simple — *selecting* an element from a set is the same as constructing a function from the singleton set to that element.

![Functional application - internal diagram](../02_category/application_internal.svg)

And then *applying* a function to an element is the same as *composing* the element function, with the function we want to apply.

![Functional application - external diagram](../02_category/application_external.svg)

The result is the function that represents the element returned by the applied function.

> Let $g$ be an element of set $X$, let the function $g: 1 \to X$ represent that element, and let $f: X \to Y$ be any function from $X$ to some other set. Then, the composition of the two functions $f \circ g: 1 \to Y$ is exactly the function that would represent the element which is the result of calling the function $f$ with the value of $g$ as an argument $f(g)$.

### Conclusion

This was a taste of Lawvere’s Elementary Theory of the Category of Sets (ETCS) which constitutes a rigorous definition of set theory (equivalent to ZFC set theory) using only the concept of a function.

We can cover this theory in it’s entirety, listing all axioms that are needed, but for now it is probably more important to understand why do we want it in the first place?

The short answer: because it is more general than the traditional definition, this new definition also applies to objects that are not exactly sets but are *like* sets in some respects.

You may say that they apply to entirely different *categories of objects* (nudge, nudge).

### Categories briefly

Maybe it is about time to see what a category is. Here is a short definition: A category consists of objects (an example of which are sets) and morphisms that go from one object to another (which behave as functions) and that are composable. We can say a lot more about categories, and even present a formal definition, but for now, it is sufficient for you to remember that sets are one example of a category and that categorical objects are like sets, except that we don’t *see* their elements i.e. category-theoretic notions are captured by the external diagrams, while strictly set-theoretic notions can be captured by internal ones.

![Category theory and set theory compared](../02_category/set_category.svg)

When we are within the realm of sets, we can view each set as a collection of individual elements. In category theory, we don’t have such a notion. However, taking this notion away allows us to define concepts such as the sum and product sets in a whole different and more general way. Plus we always have a way to “go back” to set theory, using the tricks from the last section.

| Category Theory | Set theory |
|---|---|
| Category | N/A |
| Objects and Morphisms | Sets and functions |
| N/A | Element |

By switching to external diagrams, we lose sight of the particular (the elements of our sets), but we gain the ability to zoom out and see the whole universe where we have been previously trapped.

### Sets VS Categories

One remark before we continue: in the last section, we may have made it seem like category theory and set theory are somehow competing with each other. Perhaps that notion would be somewhat correct if category and set theory were meant to describe *concrete* phenomena, in the way that the theory of relativity and the theory of quantum mechanics are both supposed to explain the physical world. Concrete theories are conceived mainly as *descriptions* of the world, and as such it makes sense for them to be connected in some sort of hierarchy.

In contrast, abstract theories, like category theory and set theory, are more like *languages* for expressing such descriptions — they still can be connected, and *are* connected in more than one way, but there is no inherent hierarchical relationship between the two and therefore arguing over which of the two is more basic, or more general, is just a chicken-and-egg problem, as you will see in the next chapter.

## Categories again

> “…deal with all elements of a set by ignoring them and working with the set’s definition.” — Dijkstra (from “On the cruelty of really teaching computing science”)

All category theory books, including this one, start by talking about set theory. Looking back, I really don’t know why this is the case — books that focus on a given subject usually don’t start off by introducing an *entirely different subject*, (before even starting to talk about the main one). Perhaps the set-first approach *is* the best way to introduce people to categories. Or perhaps using sets to introduce categories is one of those things that people do just because everyone else does it. But, one thing is for certain — we don’t *need* to study sets in order to understand categories. So now I would like to start over and talk about categories as a foundational concept. So let’s pretend like this is a new book, I wonder if I can dedicate this to a different person, like Tom Lehrer, who passed away in 2025 while the first edition still wasn’t finished). But anyways.

### Objects and morphisms

A category is a collection of objects (things) where the “things” can be anything you want. Consider, for example, these colorful gray balls:

![Balls](../02_category/elements.svg)

A category consists of a collection of objects as well as some arrows connecting objects to one another. We call the arrows *morphisms*. They have a source object and target object (for now you can think of them as functions).

![A category](../02_category/category.svg)

Wait a minute, we said that all sets form a category, but at the same time, any one set can be seen as a category in its own right (just one which has no morphisms). This is true and very characteristic of category theory — one structure can be examined from many different angles and may play many different roles, often in a recursive fashion.

This particular equivalence (a set as a category with no morphisms) is, however, rarely useful. Not because it’s incorrect in any way, but rather because category theory is *all about the morphisms* — if the *arrows* in set theory are nothing but a connection between the sets that serve as their source and a destination, in category theory it’s the *objects* that are nothing but a source and destination for the arrows that connect them to other objects. This is why, in the diagram above, the arrows, and not the objects, are colored: if you ask me, the category of sets should really be called *the category of functions*.

Speaking of which, note that objects in a category can be connected by multiple arrows and that having the same source and target sets does not in any way make arrows equivalent, as in set theory there are, for example, an infinite number of functions that go from number to boolean, and the fact that they have the same input type and the same output type (or the same *type signature*, as we like to say) does not in any way make them equivalent to one another.

![Two sets connected with multiple functions](../02_category/set_arrows.svg)

There are some types of categories that have only one morphism between two objects (in each direction), but we will talk about them in a later chapter.

### Composition

The most important requirement for a structure to be called a category is that *two morphisms can make a third*, or in other words, that morphisms are *composable*.

Given three objects and two successive arrows with between them, we can make a third arrow (in set theory, it is equivalent to the consecutive application of the first two).

![Composition of morphisms](../02_category/composition.svg)

Formally, this requirement sounds like this:

> The composition operator is an operator, usually denoted with the symbol $\circ$, such that for any objects $A$, $B$ and $C$, for each pair of morphisms $g: A \to B$ and $f: B \to C$, there exists a third morphism $(f \circ g): A \to C$.

![Composition of morphisms in the context of additional morphism](../02_category/composition_arrows.svg)

If you remember, in set theory, we picked functions, as opposed to the other types of relations because they are composable. Here we just invent the concept of a morphism and define it to be composable (in the same way as we invented the (co)products and later the empty and singleton set). Let’s see where this definition gets us.

Note, that functional composition is read from right to left. e.g. applying $g$ and then applying $f$ is written $f \circ g$ and not the other way around. (You can think of it as a shortcut to $f(g(a))$). We can read $\circ$ as “after”, e.g. $f \;\text{after}\; $g.

### The law of identity

To have numbers, you have to have a zero. The zero of category theory is what we call the “identity morphism” for each object. In short, this is a morphism that doesn’t do anything.

![The identity morphism (but can also be any other morphism)](../02_category/identity.svg)

It’s important to mark this morphism because there can be (let’s again add this very important, and by now probably also very boring, reminder) many morphisms that go from one object to the same object (for example, in the category of sets, we deal with a multitude of functions that have the set of numbers as source and target, such as $\operatorname{negate}$, $\operatorname{square}$, $\operatorname{add\ one}$, and are not at all the identity morphism).

Wait, we had The way identity is formalized in an interesting way:

> The identity morphisms of each object $A$, $B$, denoted $ID_{A}: A \to A$, $ID_{B}: B \to B$ etc. are such that for any $f: A \to B$ we have $f \circ ID_{A} = ID_{B} \circ f = f$

So they really “does nothing”.

A structure must have an identity morphism for each object in order for it to be called a category — this is known as the *law of identity*.

**Task 4:** What is the identity morphism in the category of sets?

### The law of associativity

Composition is special not only because you can take any two morphisms with appropriate signatures and make a third, but because you can do so indefinitely, i.e. for each $n$ successive arrows, each of which has as a source object the target object of the previous, we can draw one (exactly one) arrow that is equivalent to the consecutive application of all $n$ arrows.

![Composition of morphisms with many objects](../02_category/composition_n_objects.svg)

If we carefully review the definition above, we can see that it can be reduced to multiple applications of the following definition.

> An operation is associative if given 3 sequential morphisms $f$ $g$ $h$, combining $h$ and $g$ with it and then combining the end result with $f$ should be the same as combining $h$ to the result of $g$ and $f$: $(h \circ g) \circ f = h \circ (g \circ f)$).

This definition can be expressed using the following diagram, which would only commute if the formula is true (given that all our category-theoretic diagrams are commutative, we can say, in such cases, that the formula and the diagram are equivalent).

![Composition of morphisms with many objects](../02_category/composition_associativity.svg)

This formula (and the diagram) is the definition of a property called *associativity*. Being associative is required for functional composition to really be called functional composition (and thus for a category to really be called a category). It is also required for our diagrams to work, as diagrams can only represent associative structures (imagine if the diagram above would not commute, that would be super weird).

Associativity is not just about diagrams. For example, when we express relations using formulas, associativity just means that brackets don’t matter in our formulas (as evidenced by the definition $(h \circ g) \circ f = h \circ (g \circ f)$).

And it is not only about categories either, it is a property of many other operations on other types of objects as well e.g. if we look at numbers, we can see that the multiplication operation is associative e.g. $(1 \times 2) \times 3 = 1 \times (2 \times 3)$. While division is not $(1 / 2) / 3 \neq 1 / (2 / 3)$.

### Commuting diagrams

The diagrams above use colours to illustrate the fact that the green morphism is equivalent to the other two (and not just some unrelated morphism), but in practice this notation is a little redundant, as the *only* reason to draw diagrams in the first place is to represent paths that are equivalent to each other. All other paths would just belong in different diagrams.

![Composition of morphisms - a commuting diagram](../02_category/composition_commuting_diagram.svg)

As we mentioned briefly in the last chapter, all diagrams that are like that (ones in which any two paths between two objects are equivalent to one another) are called *commutative diagrams* (or diagrams that *commute*). All diagrams in this book (except the incorrect ones, nudge nudge) commute.

More formally, a commuting diagram is a diagram in which given two objects $a$ and $b$ and two sequences of morphisms between those two objects, we can say that those sequences are equivalent.

The diagram above is one of the simplest commuting diagrams.

Despite the fact that all diagrams in books commute, in general, **not all diagrams commute**. That is, there are many morphisms with the same type signature that are not equivalent to one another.

### Formal definition

For future reference, let’s restate what a category is:

> A category is a collection of *objects* (we can think of them as points) and *morphisms* (arrows) that go from one object to another, where:

> 1. Each object has to have an identity morphism.

> 2. There should be a way to compose two morphisms with an appropriate type signature into a third one, in a way that is associative.

This is it.

And, because categories behave as sets, many set-theoretic definitions are also valid for categories, for example, if we rewrite the definition of a set product, change “set” to “object” and “function” to “morphism”, we get the general definition of a categorical product:

> The product of $A$ and $B$, denoted $A \times B$, is a set an object, such that:

> 1. There exists two “projection” functions morphisms $A \times B \to A$ and $A \times B \to B$.

> 2. For any impostor product $I$, that also has such projection functions morphisms ($I \to A$ and $I \to B$), there must also exist a unique function morphism with the type signature $g: I \to A \times B$, that converts the impostor product to the real product, such that the above two functions morphisms would be just the composition of $g$ with the projections of the product.

So, we have been doing category theory from the first chapter, after all.

## Addendum: Why are categories like that?

*Why* are categories defined by those two laws and not some other two (or one, three, four etc.). laws? From one standpoint, the answer to that seems obvious — we study categories because they *work*. I mean, look at how many applications there are… But at the same time, category theory is an abstract theory, so everything about it is kinda arbitrary: you can remove a law — and you get another theory that looks similar to category theory (although it might actually turn out to be quite different in practice). Or you can add one more law and get yet another theory (there are indeed such laws and such theories, and we will cover them later). So if this specific set of laws works better than any other, then this fact demands an explanation. Not a *mathematical* explanation (e.g. we cannot in any way *prove* that this theory is better than some other one), but an explanation nevertheless. What follows is *my* attempt to provide such an explanation, regarding the laws of *identity* and *associativity*.

### Identity and isomorphisms

The reason the identity law is required is by far the more obvious one. Why do we need to have a morphism that does nothing? It’s because morphisms are the basic building blocks of our language, we need the identity morphism to be able to speak properly. For example, once we have the concept of identity morphism defined, we can define a category-theoretic definition of an *isomorphism*, based on it (which is important, because the concept of an isomorphism is very important for category theory).

As we said in the previous chapter, an isomorphism between two objects ($A$ and $B$) consists of two morphisms — ($A → B$ and $B → A$), such that their compositions are equivalent to the identity functions of the respective objects. Formally, objects $A$ and $B$ are isomorphic if there exist morphisms $f: A → B$ and $g: B → A$ such that $f \circ g = ID_{B}$ and $g \circ f = ID_{A}$.

And here is the same thing expressed with a commuting diagram.

![Isomorphism](../02_category/isomorphism.svg)

Like the previous one, the diagram expresses the same (simple) fact as the formula, namely that going from one object ($A$ or $B$) to the other and then back again to the starting object is the same as applying the identity morphism i.e. doing nothing.

### Associativity and reductionism

Associativity — what does it mean and why is it there? In order to tackle this question, we must first talk about another concept — the concept of *reductionism*:

Reductionism is the idea that the behaviour of complex phenomena can be understood in terms of a number of *simpler* and more fundamental phenomena. In other words, that things keep getting simpler and simpler as they get “smaller” (or when they are viewed from a lower level). An example of reductionism is the idea that the behaviour of matter can be understood completely by studying the behaviours of its constituents i.e. atoms (the word means “undividable”).

Whether the reductionist view is *universally valid*, i.e. whether it is possible to devise a *theory of everything* that describes the whole universe with a set of very simple laws, is a question over which we can argue until that universe’s inevitable collapse. What is certain, though, is that *reductionism underpins all our understanding*, especially when it comes to science and mathematics — each scientific discipline is based on a set of simple *fundaments* (e.g. elementary particles in particle physics, chemical elements in chemistry etc.) on which it builds on its much more complex theories. And the reductionist view is captured by the law of associativity. And also by the closely-related law of commutativity, which we will examine in the next chapter.
