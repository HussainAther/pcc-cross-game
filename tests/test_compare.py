from pathlib import Path
from pcc_cross_game.compare import build_comparison, render_markdown, render_csv

ROOT = Path(__file__).resolve().parents[1]
POKER = ROOT / "sources" / "pcc-poker-v0.8.0"
LIARS = ROOT / "sources" / "pcc-liars-dice-v0.4.0"
RPS = ROOT / "sources" / "pcc-rps-v0.2.0"


def current_report():
    return build_comparison(POKER, LIARS, RPS)


def test_current_frozen_sources_preserve_three_game_axis_asymmetry():
    report = current_report()
    games = {g["game"]: g for g in report["games"]}
    assert games["poker"]["axis_evidence"]["pressure"]["status"] == "confirmed"
    assert games["poker"]["axis_evidence"]["control"]["status"] == "unresolved"
    assert games["poker"]["axis_evidence"]["chaos"]["status"] == "unresolved"
    assert games["liars-dice"]["axis_evidence"]["pressure"]["status"] == "partial"
    assert games["liars-dice"]["axis_evidence"]["control"]["status"] == "failed"
    assert games["liars-dice"]["axis_evidence"]["chaos"]["status"] == "confirmed"
    assert games["rps"]["axis_evidence"]["pressure"]["status"] == "absent-by-design"
    assert games["rps"]["axis_evidence"]["control"]["status"] == "failed"
    assert games["rps"]["axis_evidence"]["chaos"]["status"] == "failed"


def test_rps_pressure_negative_control_passes_in_both_families():
    report = current_report()
    rps = next(g for g in report["games"] if g["game"] == "rps")
    assert rps["axis_evidence"]["pressure"]["family_pass"] == {"A": True, "B": True}
    mechanisms = {m["name"]: m for m in rps["mechanisms"]}
    assert mechanisms["Pressure absence negative control"]["status"] == "confirmed"
    assert rps["negative_controls"]["status"] == "confirmed"


def test_rps_failed_aggregate_flag_does_not_erase_pressure_negative_control():
    report = current_report()
    rps = next(g for g in report["games"] if g["game"] == "rps")
    assert rps["frozen_result"]["negative_control_confirmed"] is False
    assert rps["negative_controls"]["status"] == "confirmed"
    assert rps["axis_evidence"]["control"]["family_pass"] == {"A": False, "B": True}
    assert rps["axis_evidence"]["chaos"]["family_pass"] == {"A": False, "B": False}


def test_liars_construct_status_is_derived_from_all_prespecified_family_checks():
    report = current_report()
    liars = next(g for g in report["games"] if g["game"] == "liars-dice")
    assert liars["construct_recovery"]["all_axes_confirmed"] is False
    assert liars["axis_evidence"]["pressure"]["family_pass"] == {"family-a": True, "family-b": False}
    assert liars["axis_evidence"]["control"]["family_pass"] == {"family-a": False, "family-b": False}
    assert liars["axis_evidence"]["chaos"]["family_pass"] == {"family-a": True, "family-b": True}


def test_cross_game_findings_include_negative_control_and_entropy_failure():
    report = current_report()
    names = {x["finding"] for x in report["cross_game_findings"]}
    assert "Pressure evidence is currently stronger in poker" in names
    assert "Chaos evidence is currently stronger in Liar's Dice" in names
    assert "Control remains the hardest invariant observational axis" in names
    assert "Pressure absence is recoverable as a negative control" in names
    assert "naive entropy is not a portable Chaos observable" in names
    assert "the cross-game framework can represent an absent axis" in names


def test_renderers_include_all_three_games_and_absent_axis():
    report = current_report()
    md = render_markdown(report)
    csv = render_csv(report)
    assert "Poker" in md and "Liar's Dice" in md and "Repeated RPS" in md
    assert "absent-by-design" in md
    assert "poker" in csv and "liars-dice" in csv and "rps" in csv


def test_bundled_source_provenance_hashes_match():
    import hashlib, json
    provenance = json.loads((ROOT / "sources" / "PROVENANCE.json").read_text())
    assert provenance["schema_version"] == 4
    for entry in provenance["files"]:
        path = ROOT / entry["path"]
        assert path.is_file()
        assert path.stat().st_size == entry["bytes"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == entry["sha256"]
