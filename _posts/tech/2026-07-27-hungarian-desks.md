---
layout: post
title: "Hungarian Desks: Assigning Office Seats with the Hungarian Algorithm"
image: /assets/images/covers/hungarian-desks.svg
excerpt: "How we replaced our office desk lottery with a weighted-bet form and the Hungarian algorithm to compute the seating that makes everyone happiest."
---

In nearly any company, but especially tech companies, how does one handle seating arrangements? Often this is done by department, but for smaller companies without so much space — and especially now with more flexible work-from-home and partial remote policies — a more fluid use of desk space is often preferable.

I wrote a little tool to solve this properly, which I've put up on GitHub as [schacon/hungarian-desks](https://github.com/schacon/hungarian-desks). Here's the thinking behind it.

## The Problem with Seating

At Chatterbug, and at GitHub before this, my companies have always had a pretty open seating policy where people could sit pretty much wherever they wanted in the office. Sometimes teams sat near each other, but often they were remote anyhow, so that wasn't possible. In fact, with remote companies it's often better to seat people who _are_ in the office apart from each other, so that they communicate asynchronously as well.

In fact, mixed seating is arguably good for cross-company communication and serendipitous interactions. At GitHub we even had a day every few months where we would play Musical Desks, where everyone who wanted to would pick up and move somewhere new. This is easier if everyone does it at the same time, so there are desks opening up at the same time.

## The Random Method

At Chatterbug when we moved into a new space, we needed to determine how to allot seats and the first version was a simple lottery. Each person's name is drawn and they choose what seat they want in the order drawn.

This has the fairness of randomness to it, but it's not actually ideal for optimizing the assignments. Someone could, for example, not care too much and choose a seat semi-randomly that someone else really wanted.

<figure>
  <img src="{{ "/assets/images/hungarian-lottery.svg" | relative_url }}" alt="A seat lottery where the first name drawn takes the seat another person wanted most">
  <figcaption>In the lottery, whoever's name is drawn first picks first — so someone who doesn't much care can grab the one seat another person really wanted.</figcaption>
</figure>

## The Hungarian Method

We tried to solve this issue with version 2 of the seat picker. In this version, we have people give us some information about a few top choices. Also, instead of just ranking them, we have them "bet" on the choices. This way if you don't really care or want to sit in a specific area, you can put the same bet on all 4 choices. Or if you really care, you can put most of your bet on a single choice.

This allows us to determine a "happiness" with a set of seats. We assign each user/seat combination a value from `0.0` to `1.0`, with zero being totally unhappy (ie, a random seat not in their list) and `1.0` being totally happy (ie, the choice they bet the most on). We weight the user's choices to be internally relative, so if one user bets `8` on one seat and `4` on another, they would get scores of `1.0` and `0.5` for those seats, since one is half as valuable to the user as the top choice. If the user bets the same value on all 4 choices, each seat is assigned `1.0` since the user would be just as happy with any of them.

<figure>
  <img src="{{ "/assets/images/hungarian-bets.svg" | relative_url }}" alt="Two people's bets across four seat choices normalized into happiness scores from 0 to 1">
  <figcaption>Each person spreads a fixed budget of "bets" across their top four choices. Bets are scored relative to that person's own biggest bet, giving a happiness value from 0 to 1 — so betting evenly (happy anywhere) and betting big on a single seat both work.</figcaption>
</figure>

Now we essentially have the data to do a cost matrix that we can treat as a classical [assignment problem](https://en.wikipedia.org/wiki/Assignment_problem), since the sets of seats and people are essentially a weighted bipartite graph. We can invert the values of the happiness score (so `0` is totally happy — no cost, and `1` is totally unhappy, the highest cost) and use that cost matrix as the input to an implementation of the [Hungarian algorithm](https://en.wikipedia.org/wiki/Hungarian_algorithm) to come up with a set of assignments that optimizes for low cost, and thus, highest total assignment happiness.

<figure>
  <img src="{{ "/assets/images/hungarian-cost-matrix.svg" | relative_url }}" alt="A people-by-desks happiness matrix with the optimal one-per-row assignment highlighted">
  <figcaption>Treating people and desks as a weighted bipartite graph, the Hungarian algorithm picks exactly one desk per person to maximize <em>total</em> happiness — here Ada gives up her own top pick (desk A, worth 0.90 to her) so Cleo can take it, because that trade makes the whole team happier.</figcaption>
</figure>

## The Airtable Solution

Now we just need everyone in the company to fill out a form telling us their top choices and bets, so we can calculate the optimal assignments. We decided to try the easiest route, which is to have everyone fill out an Airtable form, which gives us a nice simple database of all the users and their choices that is easily API accessible. Then we wrote a script to pull those choices down, do the math, make the assignments and upload the assignments (as well as the calculated "happiness" score for each user).

## Run it Yourself

To run this, you will need an Airtable base with two tables.

The first is a table named "Desks" with one mandatory field named "Name" that has the names of the assignable desks.

The second is a table named "Choices" that has the following fields:

* Email
* First Choice
* First Choice Weight
* Second Choice
* Second Choice Weight
* Third Choice
* Third Choice Weight
* Fourth Choice
* Fourth Choice Weight
* Result Desk
* Result Score

The "[Cardinal] Choice" fields should be a link field to the Desks table, as should the "Result Desk" field.

Then you can create a form view, share it with the company and when you have all your results, you can run:

```
$ AIRTABLE_BASE_KEY=[base-key] AIRTABLE_KEY=[api-key] ruby seating.rb
```

This will pull down all your choices, calculate the "costs" for each choice, determine the assignments and upload the desk assignment result to the "Result Desk" field, and the final score for that user into "Result Score". If you average the score field, you should get a good idea of how happy your team will be as a whole, on a scale from 0 to 1, `1.0` meaning everyone got their top choice.

The code is on GitHub at [schacon/hungarian-desks](https://github.com/schacon/hungarian-desks) if you'd like to try it or adapt it for your own office.
