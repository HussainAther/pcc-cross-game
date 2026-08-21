from pathlib import Path
from pcc_cross_game.control_benchmark import build_control_benchmark, render_markdown

ROOT = Path(__file__).resolve().parents[1]
P = ROOT/'sources/pcc-poker-v0.8.0'
L = ROOT/'sources/pcc-liars-dice-v0.5.0'
R = ROOT/'sources/pcc-rps-v0.2.0'

def report(): return build_control_benchmark(P,L,R)

def test_benchmark_does_not_claim_single_portable_control_observable():
    x=report(); assert x['conclusion']['control_is_single_portable_observable'] is False

def test_poker_timing_intervention_is_confirmed_but_context_is_partial():
    x=report()['games']['poker']; assert x['timing_or_intervention_sensitivity']['status']=='confirmed'; assert x['history_or_context_use']['status']=='partial'

def test_liars_history_is_partial_and_timing_is_confirmed():
    x=report()['games']['liars-dice']; assert x['history_or_context_use']['status']=='partial'; assert x['timing_or_intervention_sensitivity']['status']=='confirmed'

def test_rps_predictive_gain_fails_cross_family_and_timing_is_not_applicable():
    x=report()['games']['rps']; assert x['predictive_gain']['status']=='partial'; assert x['timing_or_intervention_sensitivity']['status']=='not-applicable'

def test_markdown_preserves_unresolved_and_not_applicable():
    md=render_markdown(report()); assert 'unresolved' in md and 'not-applicable' in md
