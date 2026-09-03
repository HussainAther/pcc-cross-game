from pathlib import Path
from pcc_cross_game.control_template import build_control_template_benchmark, render_markdown
ROOT=Path(__file__).resolve().parents[1]; P=ROOT/'sources/pcc-poker-v0.8.0'; L=ROOT/'sources/pcc-liars-dice-v0.5.0'; R=ROOT/'sources/pcc-rps-v0.2.0'; M=ROOT/'sources/pcc-micro-fighter-v1.0.0'
def report(): return build_control_template_benchmark(P,L,R,M)
def test_no_universal_scalar_is_claimed(): assert report()['conclusion']['single_scalar_control_supported'] is False
def test_poker_has_full_three_stage_support(): assert all(report()['games']['poker'][s]['status']=='confirmed' for s in ('information_uptake','context_alignment','value_sensitive_intervention'))
def test_micro_fighter_value_sensitive_intervention_is_confirmed_but_context_is_partial():
    x=report()['games']['micro-fighter']; assert x['information_uptake']['status']=='partial'; assert x['context_alignment']['status']=='partial'; assert x['value_sensitive_intervention']['status']=='confirmed'
def test_rps_preserves_structural_non_applicability(): assert report()['games']['rps']['value_sensitive_intervention']['status']=='not-applicable'
def test_markdown_includes_micro_fighter(): assert 'Micro-Fighter' in render_markdown(report())
