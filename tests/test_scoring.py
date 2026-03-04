"""Tests for the shared scoring module — the most critical business logic."""

from ai_shopping.scoring import (
    compute_phrase_bonus,
    compute_word_score,
    expand_synonyms,
    get_synonyms_for_word,
    has_budget_intent,
    has_type_conflict,
    matches_brand,
    score_item,
)

# --- expand_synonyms ---


def test_expand_synonyms_adds_pushchair_variants():
    expanded = expand_synonyms(["pushchair"])
    assert "stroller" in expanded
    assert "pram" in expanded
    assert "buggy" in expanded


def test_expand_synonyms_preserves_original():
    expanded = expand_synonyms(["pushchair"])
    assert "pushchair" in expanded


def test_expand_synonyms_no_match_returns_original():
    expanded = expand_synonyms(["laptop"])
    assert "laptop" in expanded
    assert "notebook" in expanded


def test_expand_synonyms_unknown_word_unchanged():
    expanded = expand_synonyms(["xyznonexistent"])
    assert expanded == ["xyznonexistent"]


# --- get_synonyms_for_word ---


def test_get_synonyms_excludes_self():
    syns = get_synonyms_for_word("pushchair")
    assert "pushchair" not in syns
    assert "stroller" in syns


def test_get_synonyms_unknown_word_empty():
    assert get_synonyms_for_word("flibbertigibbet") == []


# --- matches_brand ---


def test_matches_brand_in_attrs():
    assert matches_brand("Sony", "some random title", "sony") is True


def test_matches_brand_in_title():
    assert matches_brand("", "Sony WH-1000XM5 Headphones", "sony") is True


def test_matches_brand_no_match():
    assert matches_brand("Bose", "Bose QuietComfort", "sony") is False


# --- has_type_conflict ---


def test_earbuds_query_rejects_headphones():
    assert has_type_conflict(["earbuds"], "Noise Cancelling Headphones") is True


def test_earbuds_query_accepts_earbuds():
    assert has_type_conflict(["earbuds"], "Wireless Earbuds") is False


def test_headphones_query_rejects_earbuds():
    assert has_type_conflict(["headphones"], "Wireless Earbuds") is True


def test_speaker_query_rejects_headphones():
    assert has_type_conflict(["speaker"], "Noise Cancelling Headphones") is True


def test_no_conflict_for_unrelated_type():
    assert has_type_conflict(["vacuum"], "Robot Vacuum") is False


# --- compute_word_score ---


def test_word_in_title_scores_2():
    score, matched = compute_word_score(
        "speaker", {"bluetooth", "speaker"}, set(),
    )
    assert score == 2.0
    assert matched is True


def test_word_in_attrs_scores_1():
    score, matched = compute_word_score(
        "bluetooth", set(), {"bluetooth", "5.3"},
    )
    assert score == 1.0
    assert matched is True


def test_word_not_found_scores_0():
    score, matched = compute_word_score(
        "xyznonexistent", {"foo", "bar"}, {"baz"},
    )
    assert score == 0.0
    assert matched is False


def test_prefix_matching_works():
    score, matched = compute_word_score(
        "headphone", {"headphones", "wireless"}, set(),
    )
    assert matched is True


# --- compute_phrase_bonus ---


def test_phrase_bonus_for_consecutive_words():
    bonus = compute_phrase_bonus(
        ["bluetooth", "speaker"], "jbl bluetooth speaker black",
    )
    assert bonus == 3.0


def test_no_phrase_bonus_when_words_not_consecutive():
    bonus = compute_phrase_bonus(
        ["bluetooth", "speaker"], "jbl speaker with bluetooth",
    )
    assert bonus == 0.0


def test_no_phrase_bonus_for_single_word():
    bonus = compute_phrase_bonus(["speaker"], "bluetooth speaker")
    assert bonus == 0.0


# --- score_item (integration of all scoring components) ---


def test_score_item_relevant_item_positive():
    item = {
        "title": "JBL Flip 7 Bluetooth Speaker - Black",
        "attrs": {"brand": "JBL", "type": "Bluetooth Speaker"},
    }
    score = score_item(item, ["bluetooth", "speaker"])
    assert score > 0


def test_score_item_irrelevant_item_zero():
    item = {
        "title": "Nike Air Max 90 Running Shoes",
        "attrs": {"brand": "Nike", "type": "Running Shoes"},
    }
    score = score_item(item, ["bluetooth", "speaker"])
    assert score == 0.0


def test_score_item_brand_filter_rejects_wrong_brand():
    item = {
        "title": "Bose QuietComfort Headphones",
        "attrs": {"brand": "Bose", "type": "Headphones"},
    }
    score = score_item(item, ["headphones"], brand="sony")
    assert score == 0.0


def test_score_item_brand_filter_accepts_correct_brand():
    item = {
        "title": "Sony WH-1000XM6 Headphones",
        "attrs": {"brand": "Sony", "type": "Headphones"},
    }
    score = score_item(item, ["headphones"], brand="sony")
    assert score > 0


def test_score_item_type_conflict_rejects():
    item = {
        "title": "Sony WH-1000XM6 Headphones",
        "attrs": {"brand": "Sony", "type": "Noise Cancelling Headphones"},
    }
    score = score_item(item, ["earbuds"])
    assert score == 0.0


def test_score_item_synonym_matching_pushchair():
    item = {
        "title": "Silver Cross Reef Pushchair - Black",
        "attrs": {"brand": "Silver Cross", "type": "Pushchair"},
    }
    score = score_item(item, ["stroller"])
    assert score > 0


def test_score_item_colour_bonus():
    item = {
        "title": "JBL Speaker Black",
        "attrs": {"brand": "JBL", "colour": "Black", "type": "Speaker"},
    }
    score_no_colour = score_item(item, ["speaker"])
    score_with_colour = score_item(item, ["speaker"], colour="black")
    assert score_with_colour > score_no_colour


def test_score_item_condition_bonus():
    item = {
        "title": "JBL Speaker",
        "attrs": {"brand": "JBL", "type": "Speaker", "condition": "Used"},
    }
    score_no_cond = score_item(item, ["speaker"])
    score_with_cond = score_item(item, ["speaker"], condition="used")
    assert score_with_cond > score_no_cond


def test_score_item_short_query_needs_high_match():
    """Two-word query needs >= 60% match ratio."""
    item = {
        "title": "Some Random Bluetooth Thing",
        "attrs": {"connectivity": "Bluetooth"},
    }
    score = score_item(item, ["bluetooth", "speaker"])
    assert score == 0.0


# --- has_budget_intent ---


def test_budget_intent_detected():
    assert has_budget_intent(["cheap", "protein", "powder"]) is True
    assert has_budget_intent(["electric", "scooter", "budget"]) is True
    assert has_budget_intent(["affordable", "laptop"]) is True


def test_no_budget_intent():
    assert has_budget_intent(["bluetooth", "speaker"]) is False
    assert has_budget_intent(["sony", "headphones"]) is False


def test_filler_words_dont_break_scoring():
    """Words like 'aesthetic' and 'uni' shouldn't prevent matches."""
    item = {
        "title": "TaoTronics LED Desk Lamp - Silver",
        "attrs": {"type": "Desk Lamp"},
    }
    score = score_item(item, ["aesthetic", "desk", "lamp"])
    assert score > 0


def test_filler_only_query_falls_back():
    """If ALL words are filler, use them for matching."""
    item = {
        "title": "Budget Travel Backpack - Black",
        "attrs": {"type": "Backpack"},
    }
    score = score_item(item, ["budget", "travel"])
    assert score > 0
