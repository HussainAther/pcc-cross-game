from pathlib import Path
from pcc_cross_game.pressure_template import build_pressure_template_benchmark
ROOT=Path(__file__).resolve().parents[1]
def report(): return build_pressure_template_benchmark(ROOT/'sources/pcc-poker-v0.8.0',ROOT/'sources/pcc-liars-dice-v0.5.0',ROOT/'sources/pcc-rps-v0.2.0',ROOT/'sources/pcc-micro-fighter-v0.8.0')
def test_rps_pressure_absent_by_design(): assert report()['games']['rps']['commitment_exposure']['status']=='absent-by-design'
def test_micro_pressure_spatial_constriction_is_confirmed():
    x=report()['games']['micro-fighter']; assert x['commitment_exposure']['status']=='confirmed'; assert x['response_constriction']['status']=='confirmed'; assert x['strategic_consequence']['status']=='partial'
def test_liars_response_constriction_stays_partial(): assert report()['games']['liars-dice']['response_constriction']['status']=='partial'
def test_full_template_not_overclaimed(): assert report()['conclusion']['full_three_stage_template_confirmed_cross_game'] is False
