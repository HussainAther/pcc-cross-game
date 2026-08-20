from pathlib import Path
from pcc_cross_game.compare import build_comparison, render_markdown, render_csv

ROOT = Path(__file__).resolve().parents[1]
POKER = ROOT / "sources" / "pcc-poker-v0.8.0"
LIARS = ROOT / "sources" / "pcc-liars-dice-v0.3.0"


def test_current_frozen_sources_compare_without_promoting_missing_axes():
    report = build_comparison(POKER, LIARS)
    games = {g["game"]: g for g in report["games"]}
    assert games["poker"]["balance"]["status"] == "confirmed"
    assert games["liars-dice"]["balance"]["status"] == "failed"
    assert games["poker"]["axis_evidence"]["pressure"]["status"] == "confirmed"
    assert games["poker"]["axis_evidence"]["control"]["status"] == "unresolved"
    assert all(games["liars-dice"]["axis_evidence"][a]["status"] == "unresolved" for a in ("pressure", "control", "chaos"))


def test_liars_mechanism_replication_is_separate_from_construct_recovery():
    report = build_comparison(POKER, LIARS)
    liars = next(g for g in report["games"] if g["game"] == "liars-dice")
    mechanisms = {m["name"]: m for m in liars["mechanisms"]}
    assert mechanisms["Control-vs-Chaos challenge timing"]["status"] == "confirmed"
    assert mechanisms["Chaos bid-plausibility cost"]["status"] == "confirmed"
    assert mechanisms["history dependence"]["status"] == "partial"
    assert liars["axis_evidence"]["control"]["status"] == "unresolved"


def test_renderers_include_both_games():
    report = build_comparison(POKER, LIARS)
    md = render_markdown(report)
    csv = render_csv(report)
    assert "Poker" in md and "Liar's Dice" in md
    assert "poker" in csv and "liars-dice" in csv
