from pathlib import Path

from pcc_cross_game.chaos_benchmark import build_chaos_benchmark, render_markdown

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "sources/pcc-poker-v0.8.0"
L = ROOT / "sources/pcc-liars-dice-v0.4.0"
R = ROOT / "sources/pcc-rps-v0.2.0"


def report():
    return build_chaos_benchmark(P, L, R)


def test_randomness_alone_is_rejected_as_portable_chaos_measure():
    x = report()
    assert x["portable_requirements"]["high_randomness_alone_is_sufficient"] is False
    assert x["games"]["rps"]["raw_unpredictability_signal"]["status"] == "failed"


def test_value_guardrail_is_supported_but_single_scalar_is_not():
    x = report()
    assert x["portable_requirements"]["effective_unpredictability_times_adequacy_template_supported"] is True
    assert x["portable_requirements"]["value_or_performance_guardrail_required"] is True
    assert x["portable_requirements"]["single_scalar_chaos_measure_confirmed_across_all_games"] is False
    assert x["games"]["poker"]["value_or_performance_guardrail"]["status"] == "confirmed"
    assert x["games"]["liars-dice"]["value_or_performance_guardrail"]["status"] == "confirmed"
    assert x["games"]["rps"]["value_or_performance_guardrail"]["status"] == "confirmed"


def test_rps_exposes_action_only_identifiability_limit():
    x = report()
    assert x["games"]["rps"]["latent_intent_identifiability"]["status"] == "not-identifiable"
    assert x["games"]["rps"]["cross_family_construct_recovery"]["status"] == "failed"


def test_liars_dice_retains_confirmed_chaos_recovery():
    x = report()
    assert x["games"]["liars-dice"]["cross_family_construct_recovery"]["status"] == "confirmed"


def test_markdown_names_all_three_games():
    md = render_markdown(report())
    assert "Poker" in md and "Liar's Dice" in md and "Repeated RPS" in md
