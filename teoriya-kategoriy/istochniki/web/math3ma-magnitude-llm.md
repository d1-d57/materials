<!-- SOURCE: https://www.math3ma.com/blog/magnitude-enriched-categories-and-llms | captured 2026-07-19 | math3ma (Tai-Danae Bradley), free blog | curl+stdlib extract -->

# math3ma — Magnitude Enriched Categories And Llms (captured)

Magnitude, Enriched Categories, and LLMs 

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

February 1, 2025 

• 
Other 

#### Magnitude, Enriched Categories, and LLMs

It's hard for me to believe, but Math3ma is TEN YEARS old today. My first entry was published on February 1, 2015 and is entitled " A Math Blog? Say What? " As evident from that post, I was very unsure about creating this website. At the time, writing about mathematics seemed very niche — though, I guess it still is — and the thought of sharing my musings publicly was quite intimidating. But as I mentioned in that first article, I started Math3ma simply as a study tool for learning graduate-level mathematics. (Hence the name: "mathema = lesson" in Greek.) And yet I had lots of doubts about whether my articles would resonate with anyone. So the tone in that first article was pretty apologetic. Needless to say, I've been amazed by all that's happened in the past ten years because of Math3ma. Thanks to all of you who've visited the site over the years! 

#### A Mathematical Framework for Language Inspired by LLMs

Although I blog less frequently now, I've been working on a paper in category theory and (large) language (models) with Juan Pablo Vigneaux , who's done a lot of work at the intersection of topology and information theory . We recently uploaded the preprint to the arXiv, so I figured today's a good day to tell you about it. It's called " The Magnitude of Categories of Texts Enriched by Language Models. " 

#### What's this about?

The story begins with a 2021 paper I coauthored with John Terilla and Yiannis Vlassopoulos that describes a category theoretical framework for language inspired by large language models (LLMs). I've blogged about that paper before , but let me give you a quick summary. 
When I say "framework," I don't mean we proposed a model for language and tried to make the case that it's a good one, per se. Instead, we just looked at what LLMs have access to — namely, loads of strings of text — and started identifying some mathematical structure that's there. So, what structure is there ? Well, in corpora of text, you have access to which strings are contained in other strings. For instance, the word curiosity is contained in the expression curiosity killed the cat . And you also have access to the statistics of those containments. For instance, there is, intuitively, some nonzero probability that killed the cat will follow the word curiosity, and we can think of LLMs as approximating such probabilities. 
So? We think category theory is helpful towards addressing this question — not just because we like category theory (we do), but because it allows you to bring few assumptions to the table and still get pretty far. Here's what I mean by that. 
Consider all strings from some finite set, like an alphabet or set of tokens. Then, let's draw an arrow from one string $x$ to another string $y$ if and only if $x$ is a substring of $y$. You can check this defines a preorder (it's reflexive and transitive) which means it's a very simple example of a category ! The objects are texts in a language, and morphisms are provided by substring containment. 
 
That's nice, but this category doesn't know about probabilities. It'd be better to decorate the arrows with something like the conditional probability of seeing curiosity killed the cat given the prefix curiosity as "input," for instance. And it'd be even better if those probabilities fit nicely into an existing categorical framework, rather than being added in some ad-hoc way. And indeed, that turns out to be the case. This desiderata fits perfectly into a richer version of category theory called enriched category theory . Part of our work in 2021 was fleshing this theory out, and part of the paper with Juan Pablo is connecting the theory explicitly to the probabilities generated by an LLM. 

#### Okay, so what?

It seems we haven't really done much, and indeed, we haven't. We merely have some texts with arrows and probabilities between them. Doesn't seem like a big deal. But now's a good time to mention that this ties in nicely with the Distributional Hypothesis from linguistics, which says that words with similar meanings appear in similar contexts. Or, to quote a famous saying by John Firth from 1957, "You shall know a word by the company it keeps." Something similar is true in mathematics, where "You shall know a mathematical object by the company it keeps." That's essentially what the Yoneda Lemma says, which is a famous theorem in category theory that I've written about before. 
Now let's put two and two together. LLMs can produce coherent strings of text just given knowledge about which strings are contained in other strings along with the statistics of those containments. Evidently, they learn something about meaning in language. And the Yoneda Lemma tells us that we, too, can learn something about "meanings" of mathematical objects by looking at how they relate to one another. So let's port that idea back over to language. 
Given a string $x$, the Yoneda Lemma motivates us to consider the totality of all strings $y$ that contain $x$, in a way that also accounts for the probabilities of those containments. (This is like the "context" of $x$.) So, we're moved to consider a mapping that associates each string in our category to the network of ways that string fits into the language. And when you write down what all that really means, it turns out to be a(n enriched) functor ! This particular functor is called the enriched Yoneda embedding , which happens to have a special place in category theory. In other words, the thing you care about in language (the contexts of words) turns out to be a thing that category theorists also care about (the Yoneda embedding). 
The upshot is that every string corresponds to a functor that essentially represents , in some sense, the meaning of that string. And it turns out there are other functors, too — not only those corresponding to individual strings — and moreover, the collection of all these functors forms a very nice category (called "a category of enriched co-presheaves") with very rich mathematical structure (it's "complete, co-complete, and Cartesian closed"). What's more, we can think of this functor category as a place where semantic information resides, due to our perspective gained from the Yoneda Lemma/Distributional Hypothesis. And because this functor category has lots of nice mathematical structure, it additionally gives us a way to combine these meaning representations of strings in a way that is reminiscent of logical operations. There's a lot to unpack here, and we flesh out those details in the 2021 paper. 
Moving beyond theory, a team at the AWS AI Lab also gave experimental evidence for some of these ideas and wrote a nice blog post about their work here . 
 A slide from a talk I gave at UCLA's IPAM in November 2024. Full deck is here . 

#### From Probabilities to Geometry

So you see? We started with very little, namely substring containment enriched with probabilities, and we got somewhere pretty interesting. And we're not done yet! This entire story has a geometric counterpart, because probabilities can be mapped to distances by the negative logarithm $-\ln\colon[0,1]\to[0,\infty]$! (In terms of enriched category theory, this amounts to changing the base of enrichment.) That is, instead of decorating the arrow from $x$ to $y$ with the probability of seeing $y$ given $x$, you can decorate it with the negative log of that probability. In this way, texts that are likely continuations of $x$ are close, and texts that don't extend $x$ are infinitely far away. 
Doing this allows us to repeat the entire story — enriching the category of strings, passing to a functor category of semantics, and performing operations on meaning representations — from a more geometric perspective. 
Categories enriched over $[0,\infty]$ in this way are examples of generalized metric spaces , which are metric spaces whose metric doesn't necessarily satisfy positivity or symmetry. And there are LOTS of things you can do with generalized metric spaces. For instance, Yiannis Vlassopoulos and Stéphane Gaubert recently found a connection between all of these ideas and tropical geometry. 
Juan Pablo and I explored a different geometric idea, namely that of magnitude — a concept with origins in mathematical biology that essentially measures the "effective size" of a metric space. (For an easy, short introduction to magnitude, see Section 4 of this paper by Simon Willerton.) More precisely, magnitude is a numerical invariant that's closely related to the Euler characteristic in topology, and in 2011 Tom Leinster extended the notion of magnitude to enriched category theory. Last year, Juan Pablo published a new combinatorial method to compute magnitude, so we applied his theory to our category of language and we compute its magnitude. What's neat is that entropy pops out at the end! 
Categorical magnitude has a very interesting history, and there is so much more I could say, but this post is already becoming quite long. For additional details, check out this thread I wrote on X/Twitter, if you're interested. 
 
Okay sure, here's a thread on our preprint 🧵 https://t.co/Wk94JPWG8e 

It's a blend of two existing ideas in category theory: 1) magnitude and 2) a (generalized) metric space associated to an LLM. I'll say a little about each, and how we relate them....

1/ https://t.co/dslNJnrnV6 pic.twitter.com/MnuoWpAOrW — Tai-Danae Bradley (@math3ma) January 16, 2025 
I also recently gave a talk at the Institute for Pure and Applied Mathematics at UCLA on some of the ideas in today's post. The audience mostly consisted of biologists, cognitive scientists, and other folks outside of mathematics, so I gave the talk without assuming folks had prior knowledge of category theory. But of course, if you want even more details, check out our paper. 

#### On Quantum Machine Learning

On a completely separate note, I've also been working on a project in quantum machine learning for the past year or so, and my collaborators — Arthur Parzygnat (MIT), Andrew Vlasic (Deloitte), Anh Pham (Deloitte) — and I recently uploaded a preprint to the arXiv, as well, called " Towards Structure-Preserving Quantum Encodings ." This one takes a categorical perspective on uploading classical data onto a quantum computer in the context of machine learning. 
 
Perhaps I'll write about this one another day? 
Happy 10th birthday, Math3ma! 🎉 

Share 

 Tweet 

 Share 

Related Posts 

#### The Sierpinski Space and Its Special Property

October 6, 2016 

in 
Topology 

#### What is a Functor? Definition and Examples, Part 1

January 31, 2017 

in 
Category Theory 

#### Limits and Colimits, Part 1 (Introduction)

January 2, 2018 

in 
Category Theory 

#### Group Elements, Categorically

February 16, 2017 

in 
Category Theory 
 
Leave a comment!
