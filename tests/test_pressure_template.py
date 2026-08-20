from pathlib import Path
from pcc_cross_game.pressure_template import build_pressure_template_benchmark
ROOT=Path(__file__).resolve().parents[1]
def report(): return build_pressure_template_benchmark(ROOT/'sources/pcc-poker-v0.8.0',ROOT/'sources/pcc-liars-dice-v0.4.0',ROOT/'sources/pcc-rps-v0.2.0')
def test_rps_pressure_absent_by_design():
    r=report(); assert r['games']['rps']['commitment_exposure']['status']=='absent-by-design'; assert r['games']['rps']['commitment_exposure']['negative_control']=='confirmed'
def test_commitment_transfers_between_sequential_games():
    r=report(); assert r['games']['poker']['commitment_exposure']['status']=='confirmed'; assert r['games']['liars-dice']['commitment_exposure']['status']=='confirmed'
def test_liars_response_constriction_not_invented(): assert report()['games']['liars-dice']['response_constriction']['status']=='unresolved'
def test_full_template_not_overclaimed(): assert report()['conclusion']['full_three_stage_template_confirmed_cross_game'] is False
