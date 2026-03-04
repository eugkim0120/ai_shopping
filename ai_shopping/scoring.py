"""Relevance scoring — single source of truth for search relevance logic.

Extracted from web_data.py and demo.py to eliminate duplication. All scoring
decisions are made here and independently testable.
"""

STOP_WORDS = {
    "the", "a", "an", "and", "or", "for", "with", "on", "in",
    "to", "of", "is", "it",
}

# Filler/adjective words that signal preference but shouldn't be required to match
FILLER_WORDS = {
    "aesthetic", "cheap", "budget", "best", "good", "nice", "cool",
    "great", "amazing", "top", "quality", "premium", "basic",
    "affordable", "expensive", "popular", "trending", "viral",
    "uni", "school", "work", "home", "travel", "gym",
}

MIN_MATCH_RATIO = 0.5

SYNONYMS = [
    {"pushchair", "stroller", "pram", "buggy", "pushchairs",
     "strollers", "prams", "buggies"},
    {"headphones", "headphone"},
    {"earbuds", "earbud", "buds"},
    {"trainers", "sneakers", "shoes", "dunks"},
    {"laptop", "notebook", "macbook"},
    {"mobile", "phone", "smartphone"},
    {"tv", "television"},
    {"fridge", "refrigerator"},
    {"sofa", "couch"},
    {"secondhand", "used", "preloved", "pre-owned"},
    {"vintage", "retro", "classic"},
    {"tumbler", "cup", "flask", "bottle"},
    {"leggings", "tights", "yoga pants"},
    {"jacket", "coat"},
]

# Words that imply preference for lower prices
BUDGET_WORDS = {"cheap", "budget", "affordable"}

TYPE_CONFLICTS: dict[str, set[str]] = {
    "earbuds": {"noise cancelling headphones", "headphones"},
    "headphones": {"wireless earbuds", "bluetooth speaker"},
    "speaker": {"wireless earbuds", "noise cancelling headphones", "headphones"},
}


def expand_synonyms(words: list[str]) -> list[str]:
    """Expand query words with their synonyms."""
    expanded = list(words)
    for word in words:
        for group in SYNONYMS:
            if word in group:
                for syn in group:
                    if syn not in expanded:
                        expanded.append(syn)
    return expanded


def get_synonyms_for_word(word: str) -> list[str]:
    """Return all synonyms for a single word (excluding itself)."""
    result = []
    for group in SYNONYMS:
        if word in group:
            for syn in group:
                if syn != word:
                    result.append(syn)
    return result


def matches_brand(item_brand: str, item_title: str, brand: str) -> bool:
    """Check whether an item matches the required brand."""
    brand_lower = brand.lower()
    return brand_lower in item_brand.lower() or brand_lower in item_title.lower()


def has_type_conflict(query_words: list[str], item_type: str) -> bool:
    """Check if the item's type conflicts with the query's intended product type."""
    item_type_lower = item_type.lower()
    for type_word, conflicting_types in TYPE_CONFLICTS.items():
        if type_word in query_words and item_type_lower in conflicting_types:
            return True
    return False


def compute_word_score(
    word: str, title_words: set[str], attrs_words: set[str],
) -> tuple[float, bool]:
    """Score a single query word against title and attribute words.

    Returns (score, matched).
    """
    title_match = any(
        w.startswith(word) or word.startswith(w)
        for w in title_words if len(w) > 2
    )
    if title_match:
        return 2.0, True

    attrs_match = any(
        w.startswith(word) or word.startswith(w)
        for w in attrs_words if len(w) > 2
    )
    if attrs_match:
        return 1.0, True

    return 0.0, False


def compute_phrase_bonus(meaningful_words: list[str], title_lower: str) -> float:
    """Bonus for consecutive query words appearing as a phrase in the title."""
    bonus = 0.0
    if len(meaningful_words) >= 2:
        for i in range(len(meaningful_words) - 1):
            phrase = f"{meaningful_words[i]} {meaningful_words[i + 1]}"
            if phrase in title_lower:
                bonus += 3.0
    return bonus


def score_item(
    item: dict,
    query_words: list[str],
    colour: str | None = None,
    condition: str | None = None,
    brand: str | None = None,
) -> float:
    """Score how well an item matches the search query.

    Returns 0.0 for irrelevant items.
    """
    title_lower = item["title"].lower()
    title_words = set(title_lower.split())
    attrs = item.get("attrs", {})
    attrs_text = " ".join(attrs.values()).lower()
    attrs_words = set(attrs_text.split())

    # Hard brand filter
    if brand and not matches_brand(attrs.get("brand", ""), title_lower, brand):
        return 0.0

    # Split query words into meaningful (must match) and filler (preference only)
    all_non_stop = [w for w in query_words if w not in STOP_WORDS]
    meaningful_words = [w for w in all_non_stop if w not in FILLER_WORDS]

    # If ALL words are filler (e.g. "cheap nice"), fall back to all
    if not meaningful_words:
        meaningful_words = all_non_stop
    if not meaningful_words:
        return 0.0

    # Type conflict check
    item_type = attrs.get("type", "")
    if item_type and has_type_conflict(meaningful_words, item_type):
        return 0.0

    # Score each word, expanding synonyms per-word
    score = 0.0
    matches = 0
    for word in meaningful_words:
        words_to_check = [word] + [
            syn for syn in get_synonyms_for_word(word)
            if syn not in meaningful_words
        ]

        for w_check in words_to_check:
            word_score, matched = compute_word_score(w_check, title_words, attrs_words)
            if matched:
                score += word_score
                matches += 1
                break

    # Phrase bonus
    score += compute_phrase_bonus(meaningful_words, title_lower)

    # Minimum match ratio — stricter for short queries
    match_ratio = matches / len(meaningful_words) if meaningful_words else 0
    min_ratio = MIN_MATCH_RATIO if len(meaningful_words) > 2 else 0.6
    if match_ratio < min_ratio:
        return 0.0

    # Type boost
    if item_type:
        item_type_lower = item_type.lower()
        for word in meaningful_words:
            if word in item_type_lower:
                score += 2.0

    # Colour and condition bonuses
    if colour and colour.lower() in attrs_text:
        score += 1.0
    if condition:
        item_cond = attrs.get("condition", "").lower()
        if condition.lower() in item_cond:
            score += 1.0

    return score


def has_budget_intent(query_words: list[str]) -> bool:
    """Check if the query expresses a preference for cheaper items."""
    all_non_stop = [w for w in query_words if w not in STOP_WORDS]
    return bool(BUDGET_WORDS & set(all_non_stop))
