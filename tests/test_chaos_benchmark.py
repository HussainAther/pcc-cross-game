from pathlib import Path
from pcc_cross_game.chaos_benchmark import build_chaos_benchmark, render_markdown
ROOT=Path(__file__).resolve().parents[1]; P=ROOT/'sources/pcc-poker-v0.8.0'; L=ROOT/'sources/pcc-liars-dice-v0.5.0'; R=ROOT/'sources/pcc-rps-v0.2.0'; M=ROOT/'sources/pcc-micro-fighter-v1.0.0'
def report(): return build_chaos_benchmark(P,L,R,M)
def test_value_guardrail_supported_in_original_three_labs():
    x=report()['games']; assert x['poker']['value_or_performance_guardrail']['status']=='confirmed'; assert x['liars-dice']['value_or_performance_guardrail']['status']=='confirmed'; assert x['rps']['value_or_performance_guardrail']['status']=='confirmed'
def test_micro_chaos_mechanism_is_strong_but_construct_stays_unresolved():
    m=report()['games']['micro-fighter']
    assert m['raw_unpredictability_signal']['status']=='confirmed'
    assert m['value_or_performance_guardrail']['status']=='confirmed'
    assert m['exploitability_or_plausibility_guardrail']['status']=='confirmed'
    assert m['cross_family_construct_recovery']['status']=='unresolved'
def test_single_scalar_not_claimed(): assert report()['portable_requirements']['single_scalar_chaos_measure_confirmed_across_all_games'] is False
def test_markdown_includes_micro(): assert 'Micro-Fighter' in render_markdown(report())
