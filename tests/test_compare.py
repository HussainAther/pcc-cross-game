from pathlib import Path
from pcc_cross_game.compare import build_comparison, render_markdown, render_csv

ROOT = Path(__file__).resolve().parents[1]
POKER = ROOT / "sources" / "pcc-poker-v0.8.0"
LIARS = ROOT / "sources" / "pcc-liars-dice-v0.4.0"


def test_current_frozen_sources_preserve_cross_game_axis_asymmetry():
    report = build_comparison(POKER, LIARS)
    games = {g["game"]: g for g in report["games"]}
    assert games["poker"]["balance"]["status"] == "confirmed"
    assert games["liars-dice"]["balance"]["status"] == "failed"
    assert games["poker"]["axis_evidence"]["pressure"]["status"] == "confirmed"
    assert games["poker"]["axis_evidence"]["control"]["status"] == "unresolved"
    assert games["poker"]["axis_evidence"]["chaos"]["status"] == "unresolved"
    assert games["liars-dice"]["axis_evidence"]["pressure"]["status"] == "partial"
    assert games["liars-dice"]["axis_evidence"]["control"]["status"] == "failed"
    assert games["liars-dice"]["axis_evidence"]["chaos"]["status"] == "confirmed"


def test_liars_construct_status_is_derived_from_all_prespecified_family_checks():
    report = build_comparison(POKER, LIARS)
    liars = next(g for g in report["games"] if g["game"] == "liars-dice")
    assert liars["construct_recovery"]["all_axes_confirmed"] is False
    assert liars["axis_evidence"]["pressure"]["family_pass"] == {"family-a": True, "family-b": False}
    assert liars["axis_evidence"]["control"]["family_pass"] == {"family-a": False, "family-b": False}
    assert liars["axis_evidence"]["chaos"]["family_pass"] == {"family-a": True, "family-b": True}


def test_liars_mechanism_replication_remains_separate_from_construct_recovery():
    report = build_comparison(POKER, LIARS)
    liars = next(g for g in report["games"] if g["game"] == "liars-dice")
    mechanisms = {m["name"]: m for m in liars["mechanisms"]}
    assert mechanisms["Control-vs-Chaos challenge timing"]["status"] == "confirmed"
    assert mechanisms["Chaos bid-plausibility cost"]["status"] == "confirmed"
    assert mechanisms["history dependence"]["status"] == "partial"
    assert liars["axis_evidence"]["control"]["status"] == "failed"


def test_cross_game_findings_name_pressure_chaos_asymmetry_and_control_difficulty():
    report = build_comparison(POKER, LIARS)
    names = {x["finding"] for x in report["cross_game_findings"]}
    assert "Pressure evidence is currently stronger in poker" in names
    assert "Chaos evidence is currently stronger in Liar's Dice" in names
    assert "Control remains the hardest invariant observational axis" in names


def test_renderers_include_both_games_and_new_construct_statuses():
    report = build_comparison(POKER, LIARS)
    md = render_markdown(report)
    csv = render_csv(report)
    assert "Poker" in md and "Liar's Dice" in md
    assert "Chaos observational construct" in md and "confirmed" in md
    assert "poker" in csv and "liars-dice" in csv
