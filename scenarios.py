"""
The runs your test needs. ← UNIT 4, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
the empty-search branch needs an impossible query. One about the fit card needs
the same item run more than once. Working that out is Milestone 3's first step,
and this file is where you write it down.

`run_eval.py` runs everything here five times and writes the run log — five
because your criteria are written out of five.

Three scenarios are filled in to show the shape. Add or change whatever your
own criteria need — these are a starting point, not a fixed set.
"""

SCENARIOS = [
    {
        # A query the data can match. Criterion 1.
        "name": "matching query completes",
        "query": "vintage graphic tee under $30",
        "wardrobe": "example",
        "criterion": 1,
    },
    {
        # A query nothing can match. Criterion 2 — the branch.
        "name": "impossible query stops early",
        "query": "designer ballgown size XXS under $5",
        "wardrobe": "example",
        "criterion": 2,
    },
    {
        # A user with nothing saved. One of unit 4's three failure modes.
        "name": "empty wardrobe",
        "query": "denim jacket under $50",
        "wardrobe": "empty",
        "criterion": None,
    },
    # TODO: add what your criteria 3, 4 and 5 need.
    #
    # Set "criterion" to the number in criteria.md that the scenario tests.
    # "criterion": None means a diagnostic run — useful to have, but it isn't
    # one of your five, and run_eval.py marks it as such in the table.
    #
    # For a state criterion, any normal query works — what you're checking is
    # what ends up in the session, not what the user typed.
    #
    # For a fit-card criterion, you probably want the SAME query listed more
    # than once, or several different items, depending on what your criterion
    # actually says.

    {
        "name": "item and outfit stay connected",
        "query": "vintage graphic tee under $30, size M",
        "second_query": "90s track Jacket in size M",
        "wardrobe": "example",
        "criterion": 3,
    },
    {
    "name": "fit card for graphic tee",
    "query": "vintage graphic tee under $30, size M",
    "wardrobe": "example",
    "criterion": 4,
    },
    {
        "name": "fit card for track jacket",
        "query": "90s track jacket in size M",
        "wardrobe": "example",
        "criterion": 4,
    },
    {
        "name": "fit card for slip dress",
        "query": "silk slip dress in midi length under $40",
        "wardrobe": "example",
        "criterion": 4,
    },
    {
        "name": "fit card for sneakers",
        "query": "platform sneakers size 8",
        "wardrobe": "example",
        "criterion": 4,
    },
    {
        "name": "fit card for denim jacket",
        "query": "denim jacket under $50",
        "wardrobe": "example",
        "criterion": 4,
    },
    {
        "name": "budget search for tee",
        "query": "graphic tee under $30",
        "wardrobe": "example",
        "criterion": 5,
        "search_only": True,
        "search_inputs": {"description": "graphic tee", "max_price": 30},
    },
    {
        "name": "budget search for jacket",
        "query": "track jacket under $50",
        "wardrobe": "example",
        "criterion": 5,
        "search_only": True,
        "search_inputs": {"description": "track jacket", "max_price": 50},
    },
    {
        "name": "budget search for dress",
        "query": "silk slip dress under $40",
        "wardrobe": "example",
        "criterion": 5,
        "search_only": True,
        "search_inputs": {"description": "silk slip dress", "max_price": 40},
    },
    {
        "name": "budget search for sneakers",
        "query": "platform sneakers under $50",
        "wardrobe": "example",
        "criterion": 5,
        "search_only": True,
        "search_inputs": {"description": "platform sneakers", "max_price": 50},
    },
    {
        "name": "budget search with no affordable match",
        "query": "designer ballgown under $5",
        "wardrobe": "example",
        "criterion": 5,
        "search_only": True,
        "search_inputs": {"description": "designer ballgown", "max_price": 5},
    },
]

WARDROBES = ("example", "empty")


def validate() -> list[str]:
    """Complain about anything malformed, before a long run rather than during."""
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("query", "").strip():
            problems.append(f"scenario {i} has no query")
        if scenario.get("wardrobe") not in WARDROBES:
            problems.append(
                f"scenario {i} has wardrobe {scenario.get('wardrobe')!r} — "
                f"it should be one of {WARDROBES}"
            )
    return problems
