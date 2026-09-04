from pathlib import Path

from pcc_cross_game.architecture_falsification import build_architecture_falsification, write_outputs

ROOT = Path(__file__).resolve().parents[1]


def test_all_five_games_are_evaluable_and_universal_claim_fails():
    r = build_architecture_falsification(ROOT)
    rows = {x["game"]: x for x in r["games"]}
    assert all(rows[g]["status"] == "evaluated" for g in rows)
    assert r["summary"]["evaluated_games"] == 5
    assert r["summary"]["status"] == "failed"
    assert r["summary"]["cross_game_architecture_confirmed"] is False
    assert r["summary"]["games_passing_game_native_control_modulation_test"] == 2


def test_pooled_control_improvement_fails_frozen_threshold():
    r = build_architecture_falsification(ROOT)
    pooled = r["pooled_analysis"]["macro_mean_control_relative_improvement"]
    assert 0.039 < pooled < 0.0405
    assert r["criteria"]["pooled_control_improvement_at_least_5pct"]["status"] == "fail"
    assert r["criteria"]["control_improvement_in_at_least_4_of_5_games"]["status"] == "fail"


def test_interaction_discriminants_show_substrate_dependence():
    r = build_architecture_falsification(ROOT)
    rows = {x["game"]: x for x in r["games"]}
    assert rows["poker"]["architecture_result"]["strongest_interaction_axis"] == "pressure"
    assert rows["liars-dice"]["architecture_result"]["strongest_interaction_axis"] == "chaos"
    assert rows["rps"]["architecture_result"]["strongest_interaction_axis"] == "chaos"
    assert rows["micro-fighter"]["architecture_result"]["strongest_interaction_axis"] == "pressure"
    assert rows["colonel-blotto"]["architecture_result"]["interaction_discriminants_complete"] is False
    assert r["criteria"]["control_interaction_disproportionate_in_majority"]["status"] == "fail"


def test_leave_one_game_out_falsification_is_robust():
    r = build_architecture_falsification(ROOT)
    assert len(r["leave_one_game_out"]) == 5
    assert all(not fold["universal_control_architecture_survives"] for fold in r["leave_one_game_out"])
    crit = r["criteria"]["leave_one_game_out_qualitative_architecture"]
    assert crit["status"] == "fail"
    assert crit["falsification_robust_in_all_folds"] is True


def test_rank_stability_criterion_remains_explicitly_unresolved():
    r = build_architecture_falsification(ROOT)
    assert r["criteria"]["pressure_chaos_rank_stability_exceeds_control_in_majority"]["status"] == "not-evaluable-from-current-exports"


def test_outputs_write_final_report_without_stale_required_exports(tmp_path):
    r = build_architecture_falsification(ROOT)
    write_outputs(r, tmp_path)
    md = (tmp_path / "CROSS_GAME_ARCHITECTURE.md").read_text()
    assert "5/5 games are evaluable" in md
    assert "substrate-dependent PCC architecture" in md
    assert "## Required next exports" not in md
    assert (tmp_path / "cross-game-architecture.json").exists()
    assert (tmp_path / "cross-game-architecture.csv").exists()
