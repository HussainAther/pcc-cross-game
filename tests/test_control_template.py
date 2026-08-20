from pathlib import Path
from pcc_cross_game.control_template import build_control_template_benchmark, render_markdown

ROOT = Path(__file__).resolve().parents[1]
P = ROOT/'sources/pcc-poker-v0.8.0'
L = ROOT/'sources/pcc-liars-dice-v0.4.0'
R = ROOT/'sources/pcc-rps-v0.2.0'

def report(): return build_control_template_benchmark(P,L,R)

def test_no_universal_scalar_is_claimed():
    assert report()['conclusion']['single_scalar_control_supported'] is False

def test_poker_has_full_three_stage_support():
    x=report()['games']['poker']
    assert x['information_uptake']['status']=='confirmed'
    assert x['context_alignment']['status']=='confirmed'
    assert x['value_sensitive_intervention']['status']=='confirmed'

def test_liars_value_intervention_confirms_but_information_is_partial():
    x=report()['games']['liars-dice']
    assert x['information_uptake']['status']=='partial'
    assert x['context_alignment']['status']=='partial'
    assert x['value_sensitive_intervention']['status']=='confirmed'

def test_rps_preserves_structural_non_applicability():
    x=report()['games']['rps']
    assert x['context_alignment']['status']=='unresolved'
    assert x['value_sensitive_intervention']['status']=='not-applicable'

def test_markdown_names_three_stage_template():
    md=render_markdown(report())
    assert 'Information Uptake' in md and 'Context Alignment' in md and 'Value Sensitive Intervention' in md
