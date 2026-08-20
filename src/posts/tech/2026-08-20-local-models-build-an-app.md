---
layout: post
title: "Twenty Cards, Three Models: Can a Local LLM Build a Real App?"
image: /assets/images/covers/local-models-build-an-app.svg
excerpt: "I gave three models the same twenty issue cards and told them to build a working Twitter clone. Two finished every card, passed every test, cleared every build — and served a 500 in the browser."
---

## The setup

- Second benchmark, after the short-task gauntlet — this one measures whether a model can **build something**, not answer questions.
- The app: **Chirp**, a small Twitter clone. Next.js App Router, `node:sqlite`, vitest, CSS Modules. No UI framework, no component library.
- **20 issue cards** in priority order: database → seed → design tokens → shell → feed → auth → posting → follows → likes → replies → search.
- Each card is one or two files, with acceptance criteria, required tests, and a design gate.
- The loop: implement a card → write tests → run the **full suite** → fix regressions → commit → next card. A reserved wrap-up phase at the end repairs and verifies.
- The runner grades by **running the tests itself**, never by trusting the model's summary.
- Three models: **Qwen3.8 27B MTP** and **Muse Glimmer 30B** locally on an M5 Max, **GPT-5.6 Sol** via API as a reference line.

## The three headline runs, side by side

![GPT-5.6 Sol, Muse Glimmer and Qwen3.8 home feeds side by side with their stats](/assets/images/local-models-build-an-app/three-way.png)

- Same spec, same cards, same harness, same machine.
- Two of these three finished all 20 cards. Only one of *those two* serves a page.

## The scoreboard

![Bar chart of cards completed out of 20, coloured by whether the app runs](/assets/images/local-models-build-an-app/chart-cards-done.svg)

| model | budget | cards | tests | retries | build | **runs?** | elapsed |
|---|---|---|---|---|---|---|---|
| GPT-5.6 Sol | 90 min | **20/20** | 88 | 0 | ok | **yes** | **51 min** |
| Muse Glimmer 30B | 3 hr | **20/20** | 79 | 0 | ok | **no — 500** | 136 min |
| Qwen3.8 27B MTP | 3 hr | 10/20 | 79 | 4 | ok | yes | 170 min |
| Muse Glimmer 30B | 90 min | 12/20 | 40 | 0 | ok | **no — 500** | 78 min |
| Qwen3.8 27B MTP | 90 min | 5/20 | 42 | 1 | ok | yes | 90 min |

- Stop reading at "cards" and "tests" and Muse Glimmer is the best local model by a mile.
- Add the "runs?" column and it's last.

## Every card, in order

![Per-card outcome strips for the three headline runs](/assets/images/local-models-build-an-app/chart-cards.svg)

- **Sol**: 20 cards, zero retries, 51 minutes. Nothing needed a second attempt.
- **Muse**: 20 cards, zero retries, 136 minutes. Also nothing needed a second attempt.
- **Qwen3.8**: 10 cards, 4 retries, 170 minutes — and its retries were expensive:
  - `06-feed-page` — 3 attempts, 38 min
  - `09-signup` — 3 attempts, 35 min
  - `01-db-schema` — 2 attempts, 34 min
  - **Those three cards ate 67% of the entire three-hour feature budget.**
  - The other seven averaged under 7 minutes each.

## What GPT-5.6 Sol built

![The Chirp home feed built by GPT-5.6 Sol](/assets/images/local-models-build-an-app/sol-feed.jpg)

I signed up through the UI rather than trusting the screenshots:

![The signup form](/assets/images/local-models-build-an-app/sol-signup.jpg)

- Designed form: labels, hint text per field, real focus ring.

![The composer with a live character counter](/assets/images/local-models-build-an-app/sol-composer.jpg)

- Composer with a live character counter, disabled submit on empty input.

![A posted chirp with the like button filled, showing a count of 1](/assets/images/local-models-build-an-app/sol-liked.png)

- Posting works. Liking works — heart fills, count increments.

![The Your Likes page](/assets/images/local-models-build-an-app/sol-likes.jpg)
![A reply threaded under its parent chirp](/assets/images/local-models-build-an-app/sol-thread.jpg)
![Search results grouped into People and Tweets](/assets/images/local-models-build-an-app/sol-search.jpg)

**Can:** read feed · sign up · log in/out · post · permalink · follow/unfollow · Following tab · like · your likes · reply · replies to you · search — all 12.

**Can't:** the header nav overlaps itself at 1456px wide ("Replies", "Log out" and "Likes" collide). No test caught it, because tests assert controls *exist*, not that they don't sit on top of each other.

## What Muse Glimmer built

*(Screenshots below are **after** a fix. Before it, none of these pages loaded.)*

![The Chirp feed built by Muse Glimmer](/assets/images/local-models-build-an-app/muse-feed.jpg)
![Muse Glimmer's search results](/assets/images/local-models-build-an-app/muse-search.jpg)

**Can:** on paper, the same 12 features — every route and API endpoint exists, and anonymous browsing works.

**Can't:**

- Serve a single page as delivered — `500` on `/`, `/search`, `/tweet/[id]`.
- Stay up once anyone logs in (see below).
- Seed itself: `npm run seed` dies with *"unable to open database file"* if `data/` doesn't exist. Sol's creates it.

## What Qwen3.8 built

![Qwen3.8's feed](/assets/images/local-models-build-an-app/qwen-feed.jpg)

**Can:** read feed · sign up · log in. That's the whole surface — 3 pages, 2 API endpoints.

**Can't:** everything from card 11 on — no posting, follows, likes, replies or search.

Its 90-minute run got 5 cards: a read-only feed, no auth at all.

![Qwen3.8's 90-minute feed](/assets/images/local-models-build-an-app/qwen-90min-feed.jpg)

## The bug tests cannot catch

- The spec forbids `next/headers` **in bold**. Reason: tests import route handlers directly, and `cookies()` throws outside a real request scope.
- Muse imported it anyway — in **five files** in the 3-hour run, both files in the 90-minute run.

```
Error: Route "/" used `cookies().get`. `cookies()` returns a Promise and
must be unwrapped with `await` or `React.use()` before accessing its properties.
```

- Two siblings rode along:
  - `params` read synchronously in the permalink route → hard 500.
  - `searchParams` read synchronously in the feed and search pages → **doesn't throw**. Silently yields `undefined`. Search returned nothing; the Following tab never engaged. A test asserting "the page renders" passes happily.
- **79 tests passed and `next build` succeeded over an app that 500s on its home page.** The tests never import the route modules; the failure only exists at request time.
- Qwen3.8 avoided this in both runs. Smaller apps — but they start.

## How long the fix took

- **2 minutes 49 seconds**, measured from first edit to commit.
- 3-hour repo: **19 insertions, 19 deletions, 6 files**. 90-minute repo: **2 lines**.
- Entirely mechanical: add `await` before `cookies()`, `params`, `searchParams`; make three helpers `async`.
- No restructuring, no design decisions, nothing a linter couldn't flag.
- Muse produced ~4,900 lines of coherent application in 136 minutes and lost all of it to a 3-minute fix it had been explicitly warned about.

## Then it got worse

![Next.js runtime error: only plain objects can be passed to Client Components](/assets/images/local-models-build-an-app/muse-crash.jpg)

- With pages finally serving, I signed up through Muse's UI. The account is created — `id: 8, handle: "scott"` is visible in the error — then rendering explodes.
- Cause: `node:sqlite` returns rows with a **null prototype**, passed straight from a Server Component into a Client Component.
- The app works right up until someone logs in.
- I'd added a runtime smoke check to the harness for exactly this class of bug — boot the server, fetch every route, fail on 5xx. **It passed Muse's app**, because every route it checks is anonymous. The crash needs a session.
- My "does it actually work" check had the same blind spot as the model's tests, one layer further out.
- Left unfixed. It's evidence.

## The numbers

![Stacked bar chart of application, test and CSS lines per run](/assets/images/local-models-build-an-app/chart-loc.svg)

| model / run | files | app | tests | css | total | commits | LOC/commit | test:app |
|---|---|---|---|---|---|---|---|---|
| Sol, 90 min | 64 | 2,072 | 1,811 | 1,194 | **5,119** | 22 | 233 | 0.87 |
| Muse, 3 hr | 66 | 1,689 | 1,571 | 1,553 | 4,851 | 22 | 220 | 0.93 |
| Qwen3.8, 3 hr | 38 | 1,117 | 1,386 | 804 | 3,323 | 12 | 277 | **1.24** |
| Muse, 90 min | 38 | 860 | 709 | 618 | 2,206 | 15 | 147 | 0.82 |
| Qwen3.8, 90 min | 25 | 464 | 765 | 502 | 1,747 | 7 | 250 | **1.65** |

![Bar chart of lines of code per minute](/assets/images/local-models-build-an-app/chart-throughput.svg)

- **Throughput spans 5×**: Sol ~100 LOC/min, Muse ~36, Qwen3.8 ~20. Same task, same machine, same harness.
- **Qwen3.8 writes more test code than application code** — 1.24 and 1.65 ratios. It's the most cautious of the three, and the only local model whose apps run. Two runs isn't causation, but it's consistent.
- **Muse writes the most CSS of anyone** — 1,553 lines, more than Sol's 1,194, on fewer lines of app code. It takes the design bar seriously. The apps look fine. They don't work.
- **Commit size is remarkably stable**: 220–277 LOC/commit across every run but one. A card really is ~250 lines of code plus tests, whoever writes it.

![Bar chart of wall-clock elapsed time per run](/assets/images/local-models-build-an-app/chart-time.svg)

## Conclusions

- **The two local models fail in opposite directions.**
  - Muse Glimmer: fast, complete, disciplined, zero retries across 32 cards — **and ships broken code**. Tripling the budget produced 4× the output and the identical defect. That's a property, not variance.
  - Qwen3.8: slow, narrow, half the cards, a third of the throughput — **and what it ships runs**.
- **Which local model is "better" depends entirely on whether you intend to run what it writes.**
- **Self-graded tests are not evidence that software works.** Every app here passed its own suite. Two were dead on arrival. The model writes code and tests in one pass, with the same misconceptions in both — so the tests are blind to exactly the errors that model is prone to.
- A build check catches a bit more. A runtime check catches more still. Mine still missed a crash that only happens once you're logged in.
- **The gap between "all tests pass" and "a person can use this" was the entire result.**

---

*Harness, spec and all twenty cards live in my `muse` benchmark repo. Each app is preserved with one git commit per card, so you can read the history in build order.*
