"""Check integrity and scientific invariants of the curated processed-data route."""
from pathlib import Path
import csv, hashlib, json
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(name):return list(csv.DictReader((ROOT/name).open(encoding='utf-8-sig')))

def main():
    provenance=json.loads((ROOT/'data/provenance.json').read_text())
    for p in provenance:assert sha(ROOT/p['curated_file'])==p['curated_sha256'],p['curated_file']
    registry=rows('data/observations.csv');lookup={r['observation_id']:r for r in registry}
    assert len(registry)==len(lookup)==72
    assert sum(r['scope']=='no_cycling_section' for r in registry)==6
    pts=rows('results/spacing-points.csv')
    assert len(pts)==48
    for p in pts:
        src=lookup[p['observation_id']]
        assert src['scope']=='main_summary' and src['ion']!='control'
        assert p['ion']==src['ion'] and float(p['nominal_concentration_mM'])==float(src['concentration_mM_nominal'])
        if p['record_kind']=='second_try_fit':assert float(p['spacing_nm'])==float(src['second_try_spacing_raw'])
        elif p['record_kind']!='mixed_cell_value':assert float(p['spacing_nm'])==float(src['spacing_nm_recorded'])
    mixed={(p['ion'],float(p['nominal_concentration_mM']),float(p['spacing_nm'])) for p in pts if p['record_kind']=='mixed_cell_value'}
    assert mixed=={('Fe',50,11.279192),('Fe',50,11.784526),('Co',30,13.89),('Co',30,14.097209)}
    # Explicit source anchors prevent the old Cu contradiction and missing-cell conversion.
    assert [lookup[k]['spacing_nm_recorded'] for k in ['WB1-Sheet1-R3','WB1-Sheet1-R6']]==['6.337113','6.34724']
    assert all(lookup[k]['observation_status']=='no_peaks_recorded' for k in ['WB1-Sheet1-R2','WB1-Sheet1-R5'])
    assert lookup['WB2-Sheet1-R20']['observation_status']=='blank_spacing_entry'
    curation={r['observation_id']:r for r in rows('data/curation-decisions.csv')}
    assert 'no_RE12_identity_conflict_established' in curation['WB1-Sheet1-R13']['effective_flags']
    coverage=rows('results/condition-summary.csv');assert len(coverage)==40
    assert sum(int(r['source_rows']) for r in coverage)==65
    examples=[]
    for s in json.loads((ROOT/'data/curve-inputs.json').read_text()):
        dat={k:np.loadtxt(ROOT/v,delimiter=',',skiprows=1) for k,v in s['paths'].items()}
        a=dat['signal'];m=dat['model'];assert len(a)==1621 and np.array_equal(a,dat['subtracted'])
        assert np.array_equal(a[:,0],m[:,0]) and np.all(np.diff(a[:,0])>0)
        out=rows(f'results/{s["ion"].lower()}-overlay-values.csv')
        values=np.array([[float(r[k]) for k in ['q_nm_inverse','processed_intensity_au','archived_model_au','data_minus_model_au']] for r in out])
        assert np.array_equal(values[:,:2],a) and np.array_equal(values[:,2],m[:,1])
        assert np.array_equal(values[:,3],a[:,1]-m[:,1])
        examples.append({'sample':s['sample'],'all_export_rows_verified':len(a),'nonpositive_values_retained':int(sum(a[:,1]<=0))})
    # Independent divided-difference interpolation, avoiding the plotting code's polyfit routine.
    ni=next(s for s in json.loads((ROOT/'data/curve-inputs.json').read_text()) if s['ion']=='Ni')
    sig=np.loadtxt(ROOT/ni['paths']['signal'],delimiter=',',skiprows=1)
    dc=np.loadtxt(ROOT/ni['paths']['sample_dc'],delimiter=',',skiprows=1)
    bg=np.loadtxt(ROOT/ni['paths']['background_dc'],delimiter=',',skiprows=1)
    q=sig[:,0];a=np.interp(q,dc[:,0],dc[:,1]);b=np.interp(q,bg[:,0],bg[:,1])
    for r in rows('results/background-sensitivity.csv'):
        y=a-float(r['factor'])*b;centers=[]
        for lo,hi in [(.63,.85),(1.36,1.58)]:
            mask=(q>=lo)&(q<=hi);x=q[mask];v=y[mask];j=int(np.argmax(v))
            x0,x1,x2=x[j-1:j+2];y0,y1,y2=v[j-1:j+2]
            s01=(y1-y0)/(x1-x0);s12=(y2-y1)/(x2-x1);quad=(s12-s01)/(x2-x0)
            center=(x0+x1)/2-s01/(2*quad);assert x0<=center<=x2;centers.append(center)
        estimate=2*np.pi/((centers[0]+2*centers[1])/5)
        assert abs(estimate-float(r['two_order_D_nm']))<1e-10
    parameters=json.loads((ROOT/'data/ni-active-parameters.json').read_text())
    assert int(parameters['peaks'])==len(parameters['active_centers_nm_inverse'])==2
    centers=np.array(parameters['active_centers_nm_inverse']);orders=np.array([1,2])
    stored_D=float(2*np.pi/(orders@centers/(orders@orders)))
    assert abs(stored_D-8.520042)<.0000005
    # Candidate source links preserve row IDs and keep sample/background operands distinct.
    links=rows('data/evidence-links.csv');series=rows('data/series-inputs.csv')
    assert len(links)==len(series)==72 and {r['observation_id'] for r in links}==set(lookup)
    for r in links:
        assert 'BACKGROUND' not in r['acquisition_relative_path'].upper()
        assert r['independent_preparation_id']=='unresolved'
    total=0
    for r in series:
        assert sha(ROOT/r['curated_file'])==r['curated_sha256']
        a=np.loadtxt(ROOT/r['curated_file'],delimiter=',',skiprows=1)
        assert len(a)==int(r['numeric_rows']) and np.isfinite(a).all()
        assert sum(a[:,1]<=0)==int(r['nonpositive_intensity_rows'])
        total+=len(a)
    assert total==128511
    report={'passed':True,'source_rows':len(registry),'spacing_values_checked':len(pts),
            'curated_input_hashes_checked':len(provenance),'examples':examples,
            'independent_sensitivity_derivation_passed':True,
            'stored_active_center_D_nm':stored_D,'series_candidates_checked':len(series),
            'series_numerical_rows_checked':total,
            'scope':'Processed-data tables and arithmetic only; no nonlinear historical fit or raw-detector reconstruction.'}
    (ROOT/'results/verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
