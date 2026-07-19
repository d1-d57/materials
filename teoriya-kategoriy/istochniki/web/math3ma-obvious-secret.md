<!-- SOURCE: https://www.math3ma.com/blog/the-most-obvious-secret-in-mathematics | captured 2026-07-19 | math3ma (Tai-Danae Bradley), free blog | curl+stdlib extract -->

# math3ma — The Most Obvious Secret In Mathematics (captured)

The Most Obvious Secret in Mathematics 

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

September 12, 2016 

• 
Category Theory 

• 
Algebra 

• 
Analysis 

• 
Geometry 

• 
Other 

• 
Set Theory 

• 
Topology 

#### The Most Obvious Secret in Mathematics

Yes, I agree. The title for this post is a little pretentious.   It's certainly possible that there are other  mathematical secrets that are more  obvious than this one, but hey, I got your attention, right? Good . Because I'd like to tell you about an overarching theme in mathematics - a mathematical mantra, if you will. A technique that mathematicians use all the time  to, well, do math.  
I'm calling it a 'secret' because until recently, I've rarely (if ever?) heard it stated explicitly .  This suggests to me that it's one of those things that folks assume you'll just eventually pick up. Hopefully. Like some sort of unspoken rule of mathematics. But a few weeks ago while chatting with my advisor *, I finally heard this unspoken rule uttered! Explicitly. Repeatedly , in fact. And at that time I realized it needs to be ushered further into the spotlight. Today's post, then, is my invitation to you to come listen in on that conversation. 
So enough with the chit-chat! What's the secret? Here 'tis: 
  A mathematical object is determined by its relationships to other objects.  
‍ 
Practically speaking, this suggests that 
  an often fruitful way to discover properties of an object is NOT to investigate the object itself, but rather to study the collection of maps to or from the object. 
  
Or to be a little less formal, 
  you can learn a lot about an object by studying its interactions with other things. 
  
By "object" I mean things like sets or groups or measurable spaces or vector spaces or topological spaces or.... And by "maps" I mean the appropriate version of 'function':  functions, group homomorphisms, measurable functions, linear transformations, continuous functions, and so on. 
So now do you see why I'm calling this an obvious  secret? We students have been using this technique - though perhaps unknowingly - since we were mathematical infants! We learned about functions in our younger days. We've labored over properties of real-valued functions and their (anti)derivatives throughout Calculus. We became well-acquainted with linear transformations and their corresponding matrices in linear algebra. We battled with homomorphisms during the first week of undergrad abstract algebra. We finally learned the real  definition of a continuous map in point-set topology. The list goes on and on.  
See how pervasive this idea is? It's obvious! 
 And that's my point. 
Because have you ever stopped to really think about it? 
At first glance, perhaps it seems a little odd that "best" way to study an object is to divert your attention away  from the object and focus on something else. But we do this all the time. Take people-watching, for instance. You can learn a lot about a person simply by looking at how they relate to the folks around them. And the same is true in mathematics. 

‍ 
I've hinted at this theme briefly in a previous post , but I'd like to list a few examples to further convince you. Keep in mind, though, that this is a philosophy that permeates throughout all of mathematics. So what I'm sharing below is peanuts compared to what's out there. But I hope it's enough to illustrate the idea. 

#### In analysis...

One word: sequences ! Recall (or observe) that a sequence $\{x_n\}=\{x_1,x_2,\ldots\}$ is - yes, a long list of numbers but ultimately - a function $\phi:\mathbb{N}\to\mathbb{R}$, where $x_n=\phi(n)$. By using sequences to 'probe' the real line $\mathbb{R}$, we learn that $\mathbb{R}$ has no "holes" - if you point your infinitesimally small finger anywhere on the real line, you'll always land on a real number. This property of $\mathbb{R}$ is called completeness , and it is investigated by special types of sequences called Cauchy sequences . Another good example is curvature. Need to measure how much a curve or surface is bending in space? Then you'll want to think about second derivatives which, assuming the curve/surface is "nice enough," are themselves continuous functions to $\mathbb{R}$!** 

#### In group theory...

By looking at homomorphisms from arbitrary groups to special types of groups called symmetric groups , we discover that the raison d'être of a group is to shuffle things around! This is captured in Cayley's Theorem, a major result in group theory, which says that every group is isomorphic to a group of permutations or, less formally, a group is to math what a verb is to language. In fact, this (not the theorem, per se, but the idea) is historically how groups were first understood and is precisely what motivated Galois to lay down the foundations of the discipline of mathematics that bears his name . You might recall that we've chatted previously about the verb-like behavior of groups in this non-technical introduction to Galois theory .

#### In topology...

‍ 

Want to know if your topolgical space $X$ is connected? Just check that any continuous map from it to $\{0,1\}$ is constant! Want to determine how many 'holes' $X$ has?  Study continuous functions from the circle, $S^1$, into it! This leads to the fundamental group , $\pi_1$. Want to know many higher dimensional 'holes' there are? Look at continuous functions from the $n$-sphere into it! This leads to the higher homotopy groups , $\pi_n$. Want to know what the topology on any given space is? Simply look at  the collection of  continuous functions from it to a little two-point space ! In fact, this last example is really quite paradigmatic, and I'd like to elaborate a bit more. So stay tuned for next time! 

In the mean time, how many examples of today's not-so-secret secret can you think of? I'd love to hear 'em. Let me know in the comments below!   
‍ 
 
‍ 
*Yes! I have an advisor now! And since my written qualifying exams are out of the way, the next thing on my to-do list is passing the oral qual . I've also picked up a teaching assignment this year. For both of these reasons, blogging has been - and may continue to be - a little bit slow. But although my posts may become less frequent, I'm hoping the content will be richer. I'm almost positive they'll be more topology/category-flavored, too. 
** This is really a statement about differential geometry rather than analysis, for it generalizes nicely for things called manifolds . In fact, the whole premise behind differential geometry is a great example of today's theme. The idea is that globally, a manifold $M$ may be so complicated and wonky that we don't have many tools to probe it with. But - following the old adage, How do you eat an elephant? One bite at a time. - the impossible becomes possible if we just consider $M$ little patches at a time. Why? Because locally manifolds look exactly like Euclidean space, $\mathbb{R}^n$. (Take the earth, for example. Even though it's round, it looks flat locally. ) And since we have tons of tools at our disposal in $\mathbb{R}^n$ (like calculus!), we can apply them to the little patches of our manifold too. 

Share 

 Tweet 

 Share 

Related Posts 

#### Limits and Colimits Part 3 (Examples)

January 21, 2019 

in 
Category Theory 

#### Brouwer's Fixed Point Theorem (Proof)

January 18, 2018 

in 
Topology 

#### What is an Adjunction? Part 2 (Definition)

September 24, 2019 

in 
Category Theory 

#### The Yoneda Perspective

August 30, 2017 

in 
Category Theory 
 
Leave a comment!
