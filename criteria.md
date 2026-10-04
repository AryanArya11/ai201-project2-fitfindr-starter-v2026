# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**
I really want a matching query to make it through all three tools and return a fit card. Since two tools call the model, a failed request could stop the process. I feel like 4 of 5 tries sets a strong target while allowing one run to fail.

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:**

Personally, I feel like the agent should stop every time it finds no listings instead of trying to build an outfit with nothing. This branch only checks an empty list and doesn't rely on the model, so I expect it to work in 5 of 5 tries.

---

## 3. Each run keeps its item and outfit connected

Across five pairs of different matching queries, each run passes its selected
search result to `suggest_outfit`. It then passes the same item and the exact
outfit suggestion to `create_fit_card`. The second run does not carry over
the first run's item or outfit. This should work in 5 of 5 pairs.


**Why this target:** Personally, I really want the outfit and caption to match what the user is
currently asking for. Since the code stores and passes this information
between tools, I feel like it should work every time without mixing in
results from a previous run.


---

## 4. Fit cards are distinct, short, and specific to the find

Across five runs using five different items, at least 4 of 5 fit cards
have an opening sentence that no other card shares, contain 2 to 4
sentences, and mention the correct item, price, and platform at least once each.


**Why this target:** I really want each caption to feel specific to the find instead of repeating the same
opening for different items. It should also include the details someone would
care about without getting too long. Since the model writes the captions,
I allow one miss while expecting four cards to meet all these requirements.


---

## 5. Search stays within budget and responds quickly

Across five searches with a price limit, every returned listing stays at or
below the budget and each search finishes within one second.
At least three searches must return matches so empty results alone cannot pass.

**Why this target:**
I want users to find listings they can afford without having to wait long.
Since this tool realy only searches 40 local listings and doesn't call the model,
I feel like both the budget filter and a quick response should work every time.



---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
