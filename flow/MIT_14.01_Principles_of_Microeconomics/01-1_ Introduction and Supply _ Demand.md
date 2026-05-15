# 1. Introduction and Supply & Demand

## 元信息

- **序号**: 1
- **课程**: MIT_6.041_Probabilistic_Systems
- **处理时间**: 2026-05-15 18:45:18
- **来源**: 精修版

---

## 精修内容

# 1. Introduction and Supply & Demand

## 元信息

- **序号**: 1
- **课程**: MIT 14.01 Principles of Microeconomics
- **链接**: https://www.youtube.com/watch?v=OkTw766oCs
- **处理时间**: 2026-05-15 18:43:50
- **来源**: YouTube 自动生成字幕
- **条目数**: 2158

---

## 字幕内容

This is 14.01. I'm Jonathan Gruber, and this is microeconomics. Today, I want to cover three things: I want to talk about the course details, I want to talk about what microeconomics is, and then I'll start the substance of the course by talking about supply and demand.

A couple of points about the course. The course will have a distinct policy angle to it. I do economic policy; government policy is my thing. I think it's what makes economics exciting, and it offers an interesting angle to understand why we're learning what we're learning. Sometimes in an intro class, it's hard to understand why the heck you're doing things. However, that's just a slight flavor. If you're really more interested in this, I teach a whole course called 14.41. I'm not teaching it this year, but it'll be taught by a visitor in the spring, Kristin Butcher from Wellesley, and I'll be teaching it next year. That dives much more into these policy issues. So, I'm going to use government policy as an organizing theme, but it won't be the dominant theme of the class.

Finally, three points about my teaching style. I don't write everything on the board; we're not in high school anymore. You're actually responsible for what I say, not what I write. Partly that's because my handwriting is brutal, as you can tell already. So, what that means is please, please do not be afraid to ask me what the hell I just wrote on the board. There's no shame in that. Don't just lean to your neighbor and say, "What the hell is he writing on the board?" Ask me, because if you can't read it, I'm sure someone else can't read it, so feel free to ask.

In general, please feel free to engage with questions in this class. The other point of my teaching style is I talk way too fast. There's a mathematical function which is the longer I go without interruption, the faster I speak until I just spin off. So basically, please ask questions if anything's not clear or you just want to ask questions about some related tangent or whatever. Please feel free to do so. You might think, "How would that work in a class this big?" There are always way too few questions, even in a class this big. So never be afraid that it'll slow me down or whatever. Ask a question; we have plenty of time in the class, and you'll be doing your classmates a favor because it'll slow me down.

Finally, last point, I have this terrible tendency to use the term "guys" in a gender-neutral way. This class looks like it's a fairly healthy representation of both males and females. When I say "guys," I don't mean men, I mean people. So women, don't take it personally. "Guys" means economic agents, it means people, it doesn't mean men. It's just a bad tendency, drives my wife crazy, but I've decided it's better to just apologize up front than try to fix it throughout, which is impossible.

---

So, let's talk about what is microeconomics. How many people took AP high school econ? Okay. For how many was it taught really well? Okay, that's about right. That's why I did my high school online class; that's the answer I wanted to hear. So, tell your friends still in high school, if your high school econ teacher isn't great, tell them to go on edX and take the class and help out your friends still in high school.

So, what is microeconomics? Microeconomics is the study of how individuals and firms make decisions in a world of **scarcity**. Scarcity is what drives microeconomics. Basically, what microeconomics is is a series of **constrained optimization** exercises, where economic agents, be they firms or individuals, try to make themselves as well off as possible given their constraints.

Essentially, we have another course in the department called 14.13, Behavioral Economics, which gets into that much more. I will sprinkle it throughout, but not as much as I actually believe in it. In other words, the way we think about economics is it's best to get the basics down before you start worrying about the deviations. It's better to climb the tree before you start going out on the branches. Basically, what this course is about is **trade-offs**. It's about how, given that you're constrained, you trade off things to make yourself as well off as possible.

Behind this notion of trade-offs is going to be—I'll say about a hundred times this is the most important thing in the course, so just ignore that—but this is one of the most important things I'll say, one of the most important things in the course is the notion of **opportunity cost**. Opportunity cost is a very important concept that we teach. It's the first concept we teach, which is that every action or every inaction has a cost, in that you could have been doing something else instead. So if you buy a shirt, you could have bought pants. If you sit at home and watch TV, you could have been out working. Everything you do has a next best alternative you could have done instead, and that is called the opportunity cost.

That's a critical concept in economics, and that is why, in some sense, we are referred to casually as the **"dismal science."** Economics is referred to as the dismal science. First of all, I'm flattered we're considered a science. We're called the dismal science because our whole point is that nothing is free. There's always a trade-off, there's always an opportunity cost. Anything you do, you could be doing something else instead. Your constrained optimization means you're going to have to pass up one thing to do another. Now, some may call it dismal, but as a former MIT undergraduate, I call it fun.

This is why I think MIT is the perfect place to be teaching economics, because MIT engineering is all about constrained optimization. That's what engineering is. And economics is just the principles you learn in engineering applied in different contexts. If we think about the 2.007 contest, that still exists with the robots, right? The 2.007 contest is a contest where you're given a limited set of materials and you have to build a robot that does some task, like pushing ping-pong balls off a table or something like that. That's just constrained optimization. It's got nothing to do with economics, but it's constrained optimization. So just think of microeconomics as like engineering, but actually interesting. Think of microeconomics as engineering, but instead of building something to push a ping-pong ball off a table, you actually build people's lives and businesses and understand the decisions that drive our economy. So it's the same principles that you could think of for engineering classes, but applied to people's lives.

That's why, in fact, modern economics was born in this room, either this room or 26-100, by Paul Samuelson in the 1940s and 50s. He wrote the fundamental textbook that gave birth to modern economics because he was here and applied the kind of engineering principles of MIT to actually develop the field of modern economics. What we learn today was developed at MIT, so it's a great place to be learning it.

---

With that as background, let's turn to the first model we'll talk about this semester, which is the **supply and demand model**.

The way we're going to proceed in this course is going to drive you crazy because we're going to proceed by teaching very simplified models. As the very first question pointed out, we're teaching very simplified models. What is a model? A model is technically a description of the relationship between any two or more variables. But unlike the models used in all your other classes, these aren't laws, by and large. They're models. We don't have a relationship between energy and mass which you can write down as a law and we're done. We have models which are never 100% true, but always "pretty" true, with "pretty" being somewhere between 10 and 95 percent true.

The idea is to make a trade-off. We want to write down in our models a set of simplifying assumptions that allow us, with a relatively small set of steps, to capture relatively broad phenomena. There's a trade-off: on the one hand, we'd like a model that captures as well as possible the real world, like E=mc², but we want to do so in the most tractable way possible so that we can teach it from first principles. In economics, we tend to resolve that by erring on the side of tractability. That is why I can teach you the entire field of microeconomics in a semester, because we're going to make a whole huge set of simplifying assumptions to make things tractable. But the key thing is that you will be amazed at what these models will be able to do. With a fairly simple set of models, we'll be able to offer insights and explain a whole huge variety of phenomena, never perfectly, but always pretty well.

The line I like is from the statistician George Box, who said that "all models are wrong, but some are useful." Now, obviously, that doesn't apply to models in the hard sciences, but in the social sciences, that's true. I'm going to write down a set of models like that.

With every model I write down, my goal is to have you understand it at three levels.
1.  The first and most important level is the **intuitive level**. The level which you can pass what I call the "mom test": you can go home and explain it to your mom at Thanksgiving. (No offense to dads, we just call it the mom test).
2.  The second is **graphical**. Most of our models here will be developed in a graphical framework, using XY graphs, which we think delivers a lot of shorthand power.
3.  And the third is **mathematical**. The mathematical is probably the least important, but it's the easiest to test you on, so we're going to need to know things mathematically as well.

---

Let's start by considering the supply and demand model, using the famous example brought up by Adam Smith. Adam Smith is considered the father of economics, while Paul Samuelson is the father of modern economics. Adam Smith's 1776 book, *The Wealth of Nations*, did an incredible job of laying out the entire core of the economics field with no math, just words, but he just nailed it.

One of his most famous examples was the **water-diamond paradox**. He said, think about water and diamonds. Start with water: nothing is more important for life than water. It's the building block of all life. Even when we look for life on other planets, we start by looking for water. Now think of diamonds, one of the more frivolous things you can buy, certainly irrelevant to leading a successful, happy, or productive life, or any life. Yet, for most of us, water is free and diamonds are super expensive. How can this be?

The answer he posed is that what I first described was just **demand**. We demand lots of water; we demand fewer diamonds. But we have to match that with the concept of **supply**. The supply of water is almost infinite, while the supply of diamonds is somewhat limited (maybe not naturally, maybe it's through decisions of various businesses). What he developed is what we call the supply and demand "scissors": you can't just think of supply or demand in isolation; you have to put them together if you want to explain real-world phenomena, like the fact that water's cheap and diamonds are expensive.

Let's talk about an example: the market for roses. On the handout, we have a graph. On the x-axis is the quantity of roses, and on the y-axis is the price of roses. The blue downward-sloping line is the **demand curve**. I'm just giving you an overview now; over the next five or six lectures, we will dive into where this demand curve comes from. We'll go to first principles and build it back up. For now, what we know about a demand curve is it simply represents the relationship between the price of a good and how much people want it. We assume it is downward sloping: at higher prices, people want less of the good. It's pretty intuitive that if the price of roses is higher, people want fewer of them.

The yellow curve is the **supply curve**. After we've derived the demand curve, we'll spend about 12 lectures deriving the supply curve. That's a bit harder, but once again, we'll start from first principles and build it up. For now, you just need to know that's how much firms are willing to supply at a given price. As the price goes up, firms want to produce more roses. The higher price means you make more money, so you want to produce more of them. This is slightly less intuitive than demand, but for now, just go with the basic intuition.

Where the curves meet is the **market equilibrium**. That is the point where both consumers and producers are happy to make a transaction. In the graph, this is the point at three dollars and 600 roses. Consumers are happy because they are on their demand curve; they are willing to buy 600 roses at three dollars. Producers are happy because on their supply curve is the same point; they are willing to supply 600 roses at three dollars. That is the one point where consumers and producers are both satisfied with the transaction, therefore it's the equilibrium. This raises lots of questions: Where do the curves come from? How does equilibrium get achieved? Why the heck do we give roses? We will come to all these questions over the next set of lectures.

---

This model also raises another important distinction that we'll focus on this semester: distinguishing between **positive** versus **normative** analysis.
- **Positive analysis** is the study of the way things *are*.
- **Normative analysis** is the study of the way things *should be*.

Let me give you a great example: eBay auctions. Auctions are a terrific, textbook example of a competitive market. Demand comes from a bunch of people bidding; people who want it more bid more, so you get a downward-sloping demand curve. Supply is how many units are for sale. You bid until those two meet, and you have a market equilibrium.

A number of years ago, someone offered their kidney for auction on eBay. They said, "Look, I got two kidneys, you only need one to live. There are people out there who need a kidney. I'm putting my kidney on eBay for auction." Bidding went nuts. It started at $25,000 and climbed to $5 million before the auction was shut down and eBay decided they wouldn't allow you to sell your bodily parts on eBay.

This raises two questions. The first is the **positive question**: Why did the price go so high? The answer is low supply and high demand. Demand is incredibly high because you die without it. Supply is low because not a lot of us are willing to sell our kidneys on eBay. Low supply, high demand led to a high price. Adam Smith at work. That's the positive analysis.

But then there's the **normative question**: *Should* you be allowed to sell your kidneys on eBay? The standard economics answer to start would be, "Of course, you should." We're in a world where thousands of people die every year because there's a waiting list for a kidney transplant. These are people who would happily pay a lot of money to stay alive. Meanwhile, there are hundreds of millions of people walking around with two kidneys who only need one, and many of these people are poor and their lives could be changed by being paid a million dollars for their kidney. So, economists say, "Look, here's a transaction to make both parties better off." The person who gets the kidney gets to stay alive. The person who sells the kidney, in all probability, is fine and gets a life-changing amount of money.

So the question is, why not? Why would we want to stop this transaction? What are the counter-arguments?
1.  **Market Failures**: The first type of problem comes from what we call market failures, which are reasons why the market doesn't work in the wonderful way economists like to think it should. For example, there could be **fraud** (people might not be able to tell if they're getting a legit kidney) or **imperfect information** (do you know the odds of living a full life with only one kidney? We ought to know that before selling one).
2.  **Equity or Fairness**: A second problem is equity. We would end up with a world where only rich people would get kidneys. Currently, organs are allocated based on a waiting list, not on who is the richest.
3.  **Behavioral Economics**: A third class of failures is that people don't always make decisions in the perfectly rational, logical way we will model them. People make mistakes. They might not be evaluating the trade-offs correctly, even with perfect information, and could end up selling their kidney when it's not in their own long-term interest.

You can't get to the normative issues without the positive analysis. You have to be disciplined and start with the fundamental economic framework. Economics at its core is a "right-wing" science; it's all about how the market knows best and that governments only mess things up. That's a lot of what we'll learn, and then we'll talk about what's wrong with that view and how governments can improve things.

---

This leads to the last thing I want to talk about: how freely should an economy function? At one extreme, we have a **capitalistic economy**, where firms and individuals decide what to produce and consume, subject to some minimal rules of the road set by the government. This has led to tremendous growth in America, making it the wealthiest nation in the world. On the other hand, it has also led to tremendous inequality; we are by far the most unequal major nation in the world.

The other extreme is the **command economy**, like the pre-1989 Soviet Union. In this case, the government makes all production and consumption decisions. In theory, this ensured equity, but in practice, it didn't work well at all and led to the collapse of the Soviet economy. There were too many opportunities for corruption, and it's hard to control human nature.

Adam Smith talked about the **"invisible hand"** of the capitalist economy. This is the notion that consumers and firms, serving their own best interests, will do what is best for society. For now, we're going to define "best for society" as the most stuff gets produced and consumed that people value, what we'll call **maximum surplus**.

The way we're going to proceed in this course is we're going to start by talking about how Adam Smith's magic works.
- We'll start with **demand**: how consumers decide what they want given their resources, using the principle of **utility maximization**.
- Then we'll turn to **supply**: how firms decide what to produce, considering different market structures like perfect competition and monopoly.
- We'll put it together to get **market equilibrium** and talk about Smith's principles.
- Then, we'll talk about how it breaks down in reality, discussing market failures, equity, behavioral economics, and other factors.

The lectures are important, but the recitations are as well. Once we're in a steady state, the recitation will be about half new material and half working through problems to prepare you for the problem set. The problem set assigned will cover material taught up to that date. For example, problem set one, assigned next Friday, will cover everything learned through next Wednesday. This Friday, the section is all new material, covering the mathematics of supply and demand. I leave the math for the TAs, who are smarter than I am. Then we'll come back on Monday and start talking about what's underneath the demand curve.