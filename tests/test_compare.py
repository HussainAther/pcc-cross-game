from pathlib import Path
from pcc_cross_game.compare import build_comparison, render_markdown, render_csv

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'sources/pcc-poker-v0.8.0'; L=ROOT/'sources/pcc-liars-dice-v0.5.0'; R=ROOT/'sources/pcc-rps-v0.2.0'; M=ROOT/'sources/pcc-micro-fighter-v1.0.0'; B=ROOT/'sources/pcc-colonel-blotto-v1.1.0'
def report(): return build_comparison(P,L,R,M,B)

def test_five_games_preserve_construct_boundaries():
    g={x['game']:x for x in report()['games']}
    assert g['poker']['axis_evidence']['pressure']['status']=='confirmed'
    assert g['liars-dice']['axis_evidence']['chaos']['status']=='confirmed'
    assert g['rps']['axis_evidence']['pressure']['status']=='absent-by-design'
    assert all(g['micro-fighter']['axis_evidence'][a]['status']=='unresolved' for a in ('pressure','control','chaos'))
    assert g['colonel-blotto']['axis_evidence']['pressure']['status']=='confirmed'
    assert g['colonel-blotto']['axis_evidence']['control']['status']=='partial'
    assert g['colonel-blotto']['axis_evidence']['chaos']['status']=='confirmed'

def test_micro_mechanistic_evidence_is_separate_from_construct_recovery():
    m=next(x for x in report()['games'] if x['game']=='micro-fighter')
    mechs={x['name']:x for x in m['mechanisms']}
    assert mechs['spatial Pressure threat generation']['status']=='confirmed'
    assert mechs['Control defense-to-counter conversion']['status']=='partial'
    assert mechs['deterministic spatial retreat as Control']['status']=='failed'
    assert mechs['retreat-backfire decomposition']['status']=='confirmed'
    assert mechs['effective Chaos resistance to calibrated exploitation']['status']=='confirmed'
    assert mechs['Chaos is not randomness']['status']=='confirmed'
    assert m['balance']['status']=='failed'

def test_cross_game_findings_include_spatial_generalization():
    names={x['finding'] for x in report()['cross_game_findings']}
    assert 'PCC mechanisms can be probed in a spatial non-card environment' in names
    assert 'spatial Control is not equivalent to maximizing distance' in names
    assert 'mechanistic support can precede construct recovery' in names
    assert 'Chaos is not randomness in spatial combat' in names

def test_renderers_include_micro_fighter_and_blotto():
    md=render_markdown(report()); csv=render_csv(report())
    assert 'Micro-Fighter' in md and 'micro-fighter' in csv
    assert 'Colonel Blotto' in md and 'colonel-blotto' in csv

def test_bundled_source_provenance_hashes_match():
    import hashlib,json
    provenance=json.loads((ROOT/'sources/PROVENANCE.json').read_text())
    assert provenance['schema_version']==9
    for entry in provenance['files']:
        path=ROOT/entry['path']; assert path.is_file(); assert path.stat().st_size==entry['bytes']; assert hashlib.sha256(path.read_bytes()).hexdigest()==entry['sha256']
