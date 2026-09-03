from pathlib import Path
from pcc_cross_game.architecture_falsification import build_architecture_falsification, write_outputs

ROOT = Path(__file__).resolve().parents[1]


def test_blotto_is_evaluable_but_cross_game_claim_remains_pending():
    r = build_architecture_falsification(ROOT)
    rows = {x['game']: x for x in r['games']}
    assert rows['colonel-blotto']['status'] == 'evaluated'
    assert rows['colonel-blotto']['architecture_result']['primary_pass'] is True
    assert rows['colonel-blotto']['architecture_result']['relative_improvement'] > 0.15
    assert r['summary']['evaluated_games'] == 1
    assert r['summary']['status'] == 'pending'
    assert r['summary']['cross_game_architecture_confirmed'] is False


def test_missing_game_exports_are_pending_not_failed():
    r = build_architecture_falsification(ROOT)
    rows = {x['game']: x for x in r['games']}
    for game in ('poker','liars-dice','rps','micro-fighter'):
        assert rows[game]['status'] == 'pending-trajectory-export'


def test_outputs_write(tmp_path):
    r = build_architecture_falsification(ROOT)
    write_outputs(r, tmp_path)
    assert (tmp_path/'CROSS_GAME_ARCHITECTURE.md').exists()
    assert (tmp_path/'cross-game-architecture.json').exists()
    assert (tmp_path/'cross-game-architecture.csv').exists()
