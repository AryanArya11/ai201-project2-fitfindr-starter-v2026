# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->

FitFindr can help someone find the thrift listings based on what they want, their size, and their budget. You can simply ask, and it will suggest an outfit using clothes from their wardrobe and write a short caption for the look. 
If FitFindr sees no listings match your description, it will communicate that to you and stop.



---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:** This tool searches for listings by description, specifically keywords and phrases; the other paramters are sizing and budget which are relevant to narrowing down for a precise search, but are not required.
- **Inputs:** `description` (str), `size` (str or None), `max_price` (float or None). Size matching ignores case: M matches S/M, but L does not match XL. The price limit is inclusive. None skips that filter.
- **Returns:** A list of matching listing dictionaries is returned by the function containing: id, title, description, category, style_tags, size, condition, price, colors, brand, and platform. Brands can also be None. Results are ranked by keyword overlap and capped at `config.SEARCH_RESULT_LIMIT`.
- **When it has nothing:** Simply returns an empty list `[]` if a listing isn't found.

### `suggest_outfit`

- **What it does:** This tool creates one or two suggestions for outfits by using the thrifted item selected from the search results and the user's current wardrobe. Based off of that, the model will generate an outfit suggestion.
- **Inputs:** `new_item` (dict containing a listing), `wardrobe` (dict with an `items` key containing a list of wardrobe items).
- **Returns:** A non-empty string describing outfit combinations and naming the wardrobe pieces used. 
- **When it has nothing:** When the `wardrobe['items']` is empty, the model will generate some general styling ideas for the thrifted/new item.

### `create_fit_card`

- **What it does:** This tool calls the model to write a short, postable caption (roughly two-to-four setnences) based off the outfit suggestion and the new item.
- **Inputs:** `outfit` (str from `suggest_outfit`), `new_item` (dict containing a listing).
- **Returns:** A two-to-four sentence caption that mentions the item, its price, and its platform once each and describes the outfit's vibe.
- **When it has nothing:** If the `outfit` parameter is empty or contains only whitespace, a guardrail will trigger and return "Cannot create a fit card without an outfit suggestion."


### `compare_price`

- **What it does:** Compares the selected item's price with other listings in the same category that share at least two style tags.
- **Inputs:** `new_item` (listing dict).
- **Returns:** A dict with `comparable_ids` (list of listing IDs), `median_price` (float or None), and `relationship` (str).
- **When it has nothing:** If fewer than two similar listings exist, returns None for the median and "insufficient_data" for the relationship.

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:** If `search_listings()` returns an empty list, then the agent saves a message explaining what the user could change and stops. Otherwise, it selects the first result, suggests an outfit, and creats a fit card.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** I used regex to pull the size and maximum price
out of the query. The remaining description becomes the keywords for searching.

**What moves through the session:** 
The way this works is that each query gets its own session so results from previous runs don't get mixed in. The agent saves the search inputs in `parsed` and the matching listings in `search_results`. It stores the first match in `selected_item` and passes it with the wardrobe to `suggest_outfit`. Then it passes the returned `outfit_suggestion` and that same item to `create_fit_card`, saving the caption in `fit_card`. If nothing matches, it saves a message in `error` and stops.

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask 'vintage graphic tee under $30, size M'

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   Here are two outfit ideas featuring the **Y2K Baby Tee — Butterfly Print**:

### Outfit 1: Y2K Streetwear Contrast
* **New Item:** Y2K Baby Tee — Butterfly Print
* **Wardrobe Pieces Used:** 
  * Baggy straight-leg jeans, dark wash (w_001)
  * Vintage black denim jacket (w_006)
  * Chunky white sneakers (w_007)
  * Black crossbody bag (w_010)

**Why it works:** 
This look plays on classic early 2000s proportions by pairing the fitted, cropped silhouette of the baby tee with the relaxed, high-waisted fit of the dark wash baggy jeans. Throwing on the slightly cropped black denim jacket and chunky white sneakers ties the streetwear vibe together while letting the pink and purple butterfly graphic pop against the dark denim.

---

### Outfit 2: Casual Earth-Tone Mix
* **New Item:** Y2K Baby Tee — Butterfly Print
* **Wardrobe Pieces Used:** 
  * Wide-leg khaki trousers (w_002)
  * Black combat boots (w_008)
  * Brown leather belt (w_009)
  * Black crossbody bag (w_010)

**Why it works:**
This outfit balances casual Y2K nostalgia with a grounded, minimalist aesthetic. Tucking the fitted baby tee into the wide-leg khaki trousers (cinched with the brown leather belt) creates a flattering silhouette. Adding the black combat boots and black crossbody bag introduces an edgy contrast that keeps the look grounded and effortless.

  Fit card: Scored this Y2K butterfly print baby tee for just $18 on depop and it is honestly the cutest piece. I styled it with baggy denim and chunky sneakers to lean into that classic early 2000s streetwear vibe.

0 model calls this session, 2 served from cache

```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'description': 'Y2K era low-rise cargo pants. Lots of pockets. Khaki color, slightly distressed at the hems. Great for layering with a long tee.', 'category': 'bottoms', 'style_tags': ['y2k', 'cargo', '2000s', 'streetwear'], 'size': 'W29', 'condition': 'fair', 'price': 27.0, 'colors': ['khaki', 'tan'], 'brand': None, 'platform': 'poshmark'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}]
```

```text
$ python -c "from tools import search_listings; results = search_listings('graphic tee', size='M', max_price=30); print([(item['title'], item['size'], item['price']) for item in results])"
[('Y2K Baby Tee — Butterfly Print', 'S/M', 18.0), ('Mesh Long-Sleeve Top — Black', 'S/M', 15.0)]
```

```text
$ python -c "from tools import search_listings; print(search_listings('designer ballgown', size='XXS', max_price=5))"
[]
```


```
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"


Here are two outfits featuring the Vintage Levi's 501 Jeans and pieces from your saved wardrobe:

### Outfit 1: Effortless Casual Streetwear
* **Bottoms:** Vintage Levi's 501 Jeans (New Item)
* **Top:** White ribbed tank top (`w_003`)
* **Outerwear:** Oversized grey crewneck sweatshirt (`w_004`)
* **Shoes:** Chunky white sneakers (`w_007`)
* **Accessories:** Black crossbody bag (`w_010`)

**Why it works:** 
This look leans into a relaxed, everyday streetwear aesthetic. The fitted white ribbed tank top provides a clean, minimal base that balances the relaxed straight-leg fit of the 501s. Tossing the oversized grey crewneck over top creates a comfortable, textured silhouette, while the chunky white sneakers and black crossbody bag tie the casual, classic color palette together.

---

### Outfit 2: Edgy Vintage Mix
* **Bottoms:** Vintage Levi's 501 Jeans (New Item)
* **Top:** Black cropped zip hoodie (`w_005`)
* **Outerwear:** Vintage black denim jacket (`w_006`)
* **Shoes:** Black combat boots (`w_008`)
* **Accessories:** Brown leather belt (`w_009`)

**Why it works:**
This outfit plays with contrasting denim washes and textures for a sharper, grungier edge. The medium wash of the Levi's stands out sharply against the black outerwear, cropped hoodie, and combat boots. Adding the brown leather belt introduces a nice earth-tone accent that breaks upthe black-and-blue combination while highlighting the vintage character of the jeans.
```

```
python -c "from tools import suggest_outfit; from utils.data_loader import load_listings; print(suggest_outfit(load_listings()[0], {'items': []}))"
Here are two outfit ideas featuring the Vintage Levi's 501 Jeans, styled with pieces you could easily add to your wardrobe.

### Outfit 1: Casual Streetwear
*   **The Look:** Relaxed, effortless, and everyday-ready.
*   **Suggested Piece to Pair:** A crisp, oversized white graphic t-shirt (tucked in loosely) and a pair of classic canvas sneakers like white Converse Lows or Adidas Sambas.
*   **Why it works:** The medium wash of the Levi's pairs naturally with stark white for a clean contrast. The casual fit of a graphic tee complements the laid-back, vintage aesthetic of the 501s without trying too hard. 

### Outfit 2: Elevated Vintage
*   **The Look:** Smart-casual with a timeless, textural mix.
*   **Suggested Piece to Pair:** A black fitted ribbed tank top layered under an oversized black-and-white houndstooth blazer, finished with black leather loafers or chunky ankle boots.
*   **Why it works:** Pairing structured, slightly formal pieces like a blazer and leather shoes with the faded knees and relaxed straight-leg cut of the vintage denim creates a great high-low balance.
```

```
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"

Scored these classic vintage Levi's 501 jeans on depop for just $38. Pairing them with crisp white sneakers gives off the ultimate effortlessstreetwear vibe. It is safe to say these are going to be on heavy rotation from now on.
```

```
python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('   ', load_listings()[0]))"
Cannot create a fit card without an outfit suggestion.
```

---

## How I Used AI

**Moment 1**

- **What I asked for:** I asked Claude to help me understand how the three tools connected and how information moved between them.
- **What came back:** It gave me a top-down explanation of how the search finds an item, the outfit tool pairs it with wardrobe pieces, and the caption tool uses both to create a fit card.
- **What I changed:** I used that explanation to write the Tool Inventory in my own language and clarify what each tool receives and returns.

**Moment 2**

- **What I asked for:** I asked ChatGPT to help me understand what made the planning loop an agent instead of just three tool calls in a row.
- **What came back:** It explained how the search result decides what happens next. If nothing matches, the agent stops. If something matches, it passes the selected item to the next tool.
- **What I changed:** I used that explanation to write the branch rule in my README. I also tested both paths because I really wanted to see that the agent stopped when there was nothing to work with.

---

---
## Stretch Features

- **Fourth tool:** I want to add `compare_price` so users can see how the item's price compares to similar listings.
- **Second branch:** If there aren't enough similar listings, the agent will let the user know. Otherwise, it will show the price comparison. Either way, it will still suggest an outfit and create a caption.
- **Style memory:** I really want users to be able to save their wardrobe so they don't have to enter the same clothes every time they use FitFindr.


### What the price comparison changed

The agent now calls `compare_price` after selecting an item. It saves the
result in `price_comparison` and the explanation in `price_message`.

The second branch is in `agent.py::run_agent`. If the median is `None`,
the agent explains that there aren't enough similar listings. Otherwise,
it shows whether the price is below, above, or equal to the median.
Both paths continue to the outfit and caption.

This comparison uses the local dataset, so it isn't a live market valuation.

### Price comparison run

```text
$ python app.py ask 'vintage graphic tee under $30, size M'
  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Price (compare_price): This price is below the $24.00 median of 3 similar listings.

  Outfit:   Here are two outfit ideas featuring the **Y2K Baby Tee — Butterfly Print**:

### Outfit 1: Y2K Streetwear Contrast
* **New Item:** Y2K Baby Tee — Butterfly Print
* **Wardrobe Pieces Used:** 
  * Baggy straight-leg jeans, dark wash (w_001)
  * Vintage black denim jacket (w_006)
  * Chunky white sneakers (w_007)
  * Black crossbody bag (w_010)

**Why it works:** 
This look plays on classic early 2000s proportions by pairing the fitted, cropped silhouette of the baby tee with the relaxed, high-waisted fit of the dark wash baggy jeans. Throwing on the slightly cropped black denim jacket and chunky white sneakers ties the streetwear vibe together while letting the pink and purple butterfly graphic pop against the dark denim.

---

### Outfit 2: Casual Earth-Tone Mix
* **New Item:** Y2K Baby Tee — Butterfly Print
* **Wardrobe Pieces Used:** 
  * Wide-leg khaki trousers (w_002)
  * Black combat boots (w_008)
  * Brown leather belt (w_009)
  * Black crossbody bag (w_010)

**Why it works:**
This outfit balances casual Y2K nostalgia with a grounded, minimalist aesthetic. Tucking the fitted baby tee into the wide-leg khaki trousers(cinched with the brown leather belt) creates a flattering silhouette. Adding the black combat boots and black crossbody bag introduces an edgy contrast that keeps the look grounded and effortless.

  Fit card: Scored this Y2K butterfly print baby tee for just $18 on depop and it is honestly the cutest piece. I styled it with baggy denim and chunky sneakers to lean into that classic early 2000s streetwear vibe.

0 model calls this session, 2 served from cache
```

### Not enough similar listings

```text
$ python app.py ask 'platform sneakers size 8'
  Found:    Platform Sneakers — White Chunky Sole — $48.0 on poshmark

  Price (compare_price): Not enough similar listings to compare prices. At least two are needed.

  Outfit:   Here are two outfits using the **Platform Sneakers — White Chunky Sole** and pieces from your saved wardrobe:

### Outfit 1: Y2K Streetwear Casual
* **New Item:** Platform Sneakers — White Chunky Sole
* **Wardrobe Pieces:** 
  * Baggy straight-leg jeans, dark wash (w_001)
  * White ribbed tank top (w_003)
  * Black cropped zip hoodie (w_005)
  * Black crossbody bag (w_010)

**Why this works:** 
This look leans entirely into the late 90s/early 2000s streetwear aesthetic of the sneakers. Pairing the fitted white tank top with the baggydark-wash jeans creates a classic, balanced silhouette. Layering the black cropped zip hoodie on top keeps the proportions short at the waist, allowing the chunky platform sole and baggy hem to take center stage. Finished with the black crossbody bag, it’s an effortless, cohesive everyday fit.

---

### Outfit 2: Contrast Casual 
* **New Item:** Platform Sneakers — White Chunky Sole
* **Wardrobe Pieces:** 
  * Wide-leg khaki trousers (w_002)
  * Oversized grey crewneck sweatshirt (w_004)
  * Brown leather belt (w_009)
  * Black crossbody bag (w_010)

**Why this works:**
This outfit plays with a more relaxed, earth-toned palette while using the sneakers to add a crisp, sporty anchor to the bottom. Tucking the oversized grey crewneck into the wide-leg khaki trousers (accented by the brown leather belt) gives the look some intentional structure. The bright white platform sole ties in with the casual vibe, keeping the voluminous wide-leg trousers from looking weighed down.

  Fit card: Scored these chunky white platform sneakers with Velcro straps just in time to lean into a late 90s and early 2000s streetwear aesthetic. I found them on Poshmark for $48, and they add the ultimate retro edge to any casual fit.

0 model calls this session, 2 served from cache
```


### Style memory

I added wardrobe memory so users don't have to enter the same clothes every
time. `--wardrobe` loads a wardrobe file, and `--remember` saves it after a
successful run. Later runs automatically load the saved wardrobe.

In the first run, I saved a wardrobe containing only my red canvas sneakers.
In the second run, I asked for a different item without providing a wardrobe
file. The agent loaded the saved sneakers and used them in the new outfit.

The saved wardrobe stays in `.fitfindr/wardrobe.json`, which is ignored by Git.
Searching for an item does not automatically add it to the wardrobe.

```
$ python app.py ask 'vintage graphic tee under $30, size M' --wardrobe demo_wardrobe.json --remember
(loaded wardrobe from demo_wardrobe.json)

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Price (compare_price): This price is below the $24.00 median of 3 similar listings.

  Outfit:   Here is one outfit idea using the Y2K Baby Tee with the butterfly print and the available wardrobe item:

### Outfit: Casual Y2K Streetwear

* **Top:** Y2K Baby Tee — Butterfly Print
* **Shoes:** My red canvas sneakers

**Why this works:**
The fitted, cropped silhouette of the baby tee pairs naturally with casual everyday footwear. The red in the canvas sneakers creates a playful, high-contrast pop against the pink and purple tones in the butterfly graphic, leaning into a fun, effortless streetwear vibe.

  Fit card: Scored this adorable Y2K baby tee with the cutest butterfly graphic for just $18. I paired it with my red canvas sneakers to play off the pink and purple tones in the print. It gives off such a fun, effortless streetwear vibe that I am obsessed with, and I found the whole thing on Depop.

(saved wardrobe: 1 items)
2 model calls this session, 618 prompt + 177 output tokens
```
```
$ python app.py ask '90s track jacket in size M'
(loaded saved wardrobe: 1 items)

  Found:    90s Track Jacket — Navy/White Stripe — $45.0 on poshmark

  Price (compare_price): This price is above the $42.00 median of 3 similar listings.

  Outfit:   Here is an outfit idea using the new 90s track jacket and your saved wardrobe item:

### Outfit: Retro Streetwear Casual
* **Outerwear:** 90s Track Jacket — Navy/White Stripe
* **Shoes:** My red canvas sneakers

**Why these pieces work together:**
The track jacket's sporty, 90s streetwear aesthetic pairs naturally with your casual canvas sneakers. The navy and white colorway of the jacket provides a classic, neutral base that makes the red in your sneakers pop as a bold, complementary accent color.

  Fit card: Scored this navy and white 90s track jacket for just $45.00 on Poshmark. I paired it with my red canvas sneakers to lean into that retro streetwear casual vibe. It's the ultimate lightweight layer for running errands while still looking put together.

2 model calls this session, 612 prompt + 173 output tokens
```
---

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

### Milestone 1: Move one tool onto MCP

I registered `search_listings` in `mcp_server.py` and changed
`agent.py::run_agent` to use `mcp_client.call_tool` instead of calling the
search function directly. It still returns the same listing dictionaries,
so I didn't need to change how the rest of the loop uses them.

I checked that the server showed the tool and its inputs. Then I tried a
matching query, which returned a listing, outfit, and fit card. I also tried
an impossible query, and the agent stopped with suggestions on what to
change without making any model calls.

---


---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```

```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```

```

**Empty search**

```

```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
