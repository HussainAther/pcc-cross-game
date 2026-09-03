from pathlib import Path
from pcc_cross_game.theory_status import build_theory_status, write_outputs

ROOT = Path(__file__).resolve().parents[1]


def report():
    return build_theory_status(ROOT)


def test_five_games_are_in_canonical_status():
    assert report()["games"] == ["poker", "liars-dice", "rps", "micro-fighter", "colonel-blotto"]


def test_axis_status_is_not_overclaimed():
    r = report()["axis_status"]
    assert r["poker"] == {"pressure": "confirmed", "control": "unresolved", "chaos": "unresolved"}
    assert r["liars-dice"] == {"pressure": "partial", "control": "failed", "chaos": "confirmed"}
    assert r["rps"]["pressure"] == "absent-by-design"
    assert r["micro-fighter"] == {"pressure": "unresolved", "control": "unresolved", "chaos": "unresolved"}
    assert r["colonel-blotto"] == {"pressure": "confirmed", "control": "partial", "chaos": "confirmed"}


def test_core_falsifications_are_retained():
    findings = {x["claim"]: x["status"] for x in report()["portable_findings"]}
    assert findings["The poker-specific Pressure-Chaos-Control dominance cycle is universal across competitive games."] == "failed"
    assert findings["Randomness alone is sufficient evidence of Chaos."] == "failed"
    assert findings["Creating distance is sufficient evidence of spatial Control."] == "failed"


def test_theory_report_does_not_change_poker_human_boundary():
    assert any("PCC Poker v0.8.0 remains scientifically frozen" in x for x in report()["current_boundaries"])


def test_outputs_write(tmp_path):
    write_outputs(report(), tmp_path)
    assert (tmp_path / "THEORY_STATUS.md").exists()
    assert (tmp_path / "THEORY_STATUS.json").exists()
    assert (tmp_path / "theory-status.csv").exists()
