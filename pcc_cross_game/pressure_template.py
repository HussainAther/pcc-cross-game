from __future__ import annotations
import csv, io, json
from pathlib import Path
from typing import Any

STAGES=("commitment_exposure","response_constriction","strategic_consequence")

def _load(p: Path)->dict[str,Any]: return json.loads(p.read_text())
def _family_status(vals: dict[str,bool])->str:
    v=list(vals.values())
    return "confirmed" if v and all(v) else "partial" if any(v) else "failed" if v else "unresolved"

def build_pressure_template_benchmark(poker_root,liars_root,rps_root,micro_root=None):
    p,l,r=map(Path,(poker_root,liars_root,rps_root)); m=Path(micro_root) if micro_root is not None else None
    panel=_load(p/'validation/family-invariant-panel.json')
    suppression=_load(p/'validation/pressure-surprise-decomposition.json')
    mechanism=_load(p/'validation/control-pressure-mechanism.json')
    lc=_load(l/'validation/construct-recovery.json')
    constriction=_load(l/'validation/pressure-response-constriction.json')
    rn=_load(r/'validation/negative-control.json')

    pcand=panel['candidates']
    p_exposure={f: bool(d['target_correlation']>=panel['thresholds']['minimum_target_correlation'] and d['discriminant_margin']>=panel['thresholds']['minimum_discriminant_margin']) for f,d in pcand['pressure_exposure']['families'].items()}
    p_response={f: bool(d['target_correlation']>=panel['thresholds']['minimum_target_correlation'] and d['discriminant_margin']>=panel['thresholds']['minimum_discriminant_margin']) for f,d in pcand['predicted_fold_probability']['families'].items()}
    p_consequence={f: bool(suppression['prespecified_checks'][f'{f}_pressure_exposure_tracks_pressure'] and suppression['prespecified_checks'][f'{f}_pressure_correlation_reduced_by_0_20']) for f in ('independent','score')}

    lpressure={fam: all(ch.values()) for fam,ch in ((fam,d['axis_checks']['pressure']) for fam,d in lc['families'].items())}
    l_effects={fam:d['effects']['pressure'] for fam,d in lc['families'].items()}
    l_commit={fam: bool(x['matching_effect']>=lc['prespecified_thresholds']['minimum_matching_standardized_effect']) for fam,x in l_effects.items()}
    l_consequence={fam: bool(x['matching_effect']>x['shuffled_matching_effect_95th_percentile']) for fam,x in l_effects.items()}
    l_response={
        'family-a': bool(constriction['prespecified_checks']['family_a_response_constriction']),
        'family-b': bool(constriction['prespecified_checks']['family_b_response_constriction']),
    }

    r_abs={fam: all(d['checks'][k] for k in ('pressure_absent_neutral','pressure_absent_control','pressure_absent_chaos')) for fam,d in rn['families'].items()}

    games={
      'poker':{
       'commitment_exposure':{'status':_family_status(p_exposure),'family_checks':p_exposure,'basis':'label-free public pressure exposure is positive and discriminant in both frozen policy families'},
       'response_constriction':{'status':_family_status(p_response),'family_checks':p_response,'basis':'predicted opponent fold probability is a family-invariant Pressure observable, consistent with constrained opponent response'},
       'strategic_consequence':{'status':_family_status(p_consequence),'family_checks':p_consequence,'basis':'pressure exposure explains a substantial Pressure-linked surprisal suppression in both families; the stronger Chaos-margin claim remains only partial'},
      },
      'liars-dice':{
       'commitment_exposure':{'status':_family_status(l_commit),'family_checks':l_commit,'basis':'the prespecified public commitment/escalation score responds strongly to assigned Pressure in both families'},
       'response_constriction':{'status':_family_status(l_response),'family_checks':l_response,'basis':'the frozen matched-state replay finds response constriction in Family B but not Family A at closely matched truth probability'},
       'strategic_consequence':{'status':_family_status(l_consequence),'family_checks':l_consequence,'basis':'Pressure commitment signal beats shuffled-label expectation in both families, although Family B fails discriminant recovery because Chaos also drives commitment'},
      },
      'rps':{
       'commitment_exposure':{'status':'absent-by-design','negative_control':_family_status(r_abs),'basis':'simultaneous fixed-cost RPS has no escalating commitment channel; the frozen Pressure candidate is exactly zero across all policies'},
       'response_constriction':{'status':'not-applicable','basis':'each RPS round always leaves the opponent the same three actions; no escalating action narrows the legal response set'},
       'strategic_consequence':{'status':'not-applicable','basis':'without a Pressure channel there is no Pressure-specific strategic consequence to test'},
      }
    }
    if m is not None:
      mp=_load(m/'validation/pressure-dominance-decomposition.json')
      mr=mp['replicated_diagnostics']
      games['micro-fighter']={
       'commitment_exposure':{'status':'confirmed' if mr['space_capture']['replicated_expected_direction'] and mr['attack_opportunity_generation']['replicated_expected_direction'] else 'partial','basis':'Pressure consistently converts forward spatial commitment into space compression and in-range attack opportunities across frozen matchups'},
       'response_constriction':{'status':'confirmed' if mr['defensive_response_forcing']['replicated_expected_direction'] else 'failed','basis':'Pressure induces more next-tick defensive/retreat responses across all frozen Pressure matchups, providing a spatial response-constriction analogue'},
       'strategic_consequence':{'status':'partial' if not mr['damage_conversion']['replicated_expected_direction'] else 'confirmed','basis':'Pressure threat volume has strategic consequences but damage conversion does not replicate universally; Family A Control wins despite being spatially constrained'},
      }

    portable=[s for s in STAGES if sum(games[g][s]['status']=='confirmed' for g in games)>=2]
    return {'schema_version':1,'benchmark':'cross-game-pressure-structural-template','template':list(STAGES),'purpose':'Test a portable structural template for Pressure without forcing Pressure into games that lack escalating commitment.','games':games,'portable_confirmed_stages':portable,'conclusion':{'single_scalar_pressure_supported':False,'full_three_stage_template_confirmed_cross_game':False,'status':'partial-structural-support','basis':'Commitment/threat exposure and response constriction now have direct support in Poker and Micro-Fighter, with commitment also supported in Liar’s Dice and absent in RPS. Strategic consequence is not universal in Micro-Fighter because threat generation does not always convert into damage, so the full Pressure mechanism remains only partially portable.'},'guardrails':['No source policy, threshold, or frozen result is modified.','Absent-by-design and not-applicable are structural statements, not failed Pressure recovery.','Liar’s Dice Pressure recovery remains partial overall; the new response-constriction intervention is also family-specific and is not relabeled as a universal mechanism.','This benchmark does not alter PCC Poker v0.8.0 or its human-data measurement contract.']}

def render_markdown(r):
    lines=['# Cross-Game Pressure Structural Template','','Proposed portable structure: **commitment exposure → response constriction → strategic consequence**.','','| Stage | Poker | Liar\'s Dice | Repeated RPS | Micro-Fighter |','|---|---|---|---|---|']
    for s in STAGES: lines.append('| '+s.replace('_',' ').title()+' | '+' | '.join(r['games'][g][s]['status'] for g in ('poker','liars-dice','rps','micro-fighter') if g in r['games'])+' |')
    lines += ['', '## Interpretation','',f"- **Overall status:** {r['conclusion']['status']}.",f"- {r['conclusion']['basis']}",'','## Guardrails','']+[f'- {x}' for x in r['guardrails']]
    return '\n'.join(lines)+'\n'
def render_csv(r):
    out=io.StringIO(); w=csv.writer(out); w.writerow(['game','stage','status','basis'])
    for g,stages in r['games'].items():
      for s,x in stages.items(): w.writerow([g,s,x['status'],x['basis']])
    return out.getvalue()
def write_outputs(r,output_dir):
    o=Path(output_dir); o.mkdir(parents=True,exist_ok=True)
    (o/'pressure-structural-template.json').write_text(json.dumps(r,indent=2)+'\n')
    (o/'PRESSURE_STRUCTURAL_TEMPLATE.md').write_text(render_markdown(r))
    (o/'pressure-structural-template.csv').write_text(render_csv(r))
