"""Rebuild the curated DPPC results and figures without laboratory software.

Inputs are processed historical curves and recorded summary cells, not detector
frames. Model exports are not refitted. Run from any directory with Python 3.13.
"""
from pathlib import Path
import csv, json, re
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyArrowPatch
from matplotlib.colors import ListedColormap

ROOT=Path(__file__).resolve().parents[1]
IONS=['Cu','Co','Ni','Mn','Fe']
CONCS=[.1,1,10,20,30,40,50,100]
COLORS=['#007C83','#C66326','#5D68A7','#7A8B32','#A44B6C']

def curve(path): return np.loadtxt(ROOT/path,delimiter=',',skiprows=1)
def write_csv(name,rows):
    with (ROOT/name).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def save(fig,name):
    for ext in ['png','svg','pdf']:
        fig.savefig(ROOT/f'figures/{name}.{ext}',dpi=200,facecolor='white',metadata=None)
    plt.close(fig)

def style():
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.titlesize':10,
        'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42,
        'svg.fonttype':'none','axes.linewidth':.7,'xtick.direction':'out','ytick.direction':'out'})

def schematic():
    fig=plt.figure(figsize=(8,3.5))
    ax=fig.add_axes([.02,.07,.47,.84]);ax.set(xlim=(0,10),ylim=(0,7));ax.axis('off')
    for mid in [1.5,4.7]:
        for x in np.linspace(.6,6.6,18):
            for side in [-1,1]:
                y=mid+side*.55
                ax.add_patch(Circle((x,y),.11,color='#007C83'))
                ax.plot([x-.04,x-.04],[y-side*.12,mid],color='#899F9F',lw=1)
                ax.plot([x+.04,x+.04],[y-side*.12,mid],color='#899F9F',lw=1)
    for x,y in [(1,3),(2.3,2.8),(4.2,3.5),(5.8,2.9),(2.9,6.3)]:
        ax.add_patch(Circle((x,y),.13,color='#C66326'));ax.text(x,y,'+',ha='center',va='center',color='white',fontsize=8)
    ax.annotate('',xy=(7.3,5.25),xytext=(7.3,2.05),arrowprops=dict(arrowstyle='<->',color='#182C3A'))
    ax.text(7.55,3.65,'D',fontsize=13,va='center')
    ax.text(.4,.15,'Lamellar repeat distance, not the water gap',color='#4D5965',fontsize=8.5)
    ax.text(.4,6.75,'a  Structural question',fontweight='bold',fontsize=11)
    ax.text(.4,5.65,'DPPC bilayers',fontsize=8.5)
    ax.text(3.5,6.2,'Added salt',fontsize=8.5,color='#C66326')
    bx=fig.add_axes([.53,.13,.45,.78]);bx.axis('off')
    bx.text(0,1,'b  Measurement and inference',fontweight='bold',fontsize=11,va='top')
    steps=[('SAXS patterns','Radial integration and corrections'),('Processed intensity I(q)','Correlation peaks and broad-lobe scattering'),('Assigned lamellar orders','D from qh = 2 pi h / D')]
    for y,(title,sub) in zip([.75,.43,.11],steps):
        bx.text(.02,y,title,fontsize=10,color='#182C3A',fontweight='bold')
        bx.text(.02,y-.1,sub,fontsize=8,color='#4D5965')
        if y>.2: bx.annotate('',xy=(.47,y-.22),xytext=(.47,y-.13),arrowprops=dict(arrowstyle='->',color='#8A969E'))
    save(fig,'system-and-workflow')

def points_from_registry(rows):
    points=[]
    for r in rows:
        if r['scope']!='main_summary' or r['ion']=='control': continue
        base={'observation_id':r['observation_id'],'ion':r['ion'],
              'nominal_concentration_mM':float(r['concentration_mM_nominal']),
              'source_column':'C','record_kind':'recorded_primary','sample_label':r['sample_id_as_recorded']}
        if r['spacing_nm_recorded']:
            kind='tentative_single_peak' if 'ambiguous_single_peak' in r['flags'] or 'zero_error' in r['flags'] else 'recorded_primary'
            points.append({**base,'record_kind':kind,'spacing_nm':float(r['spacing_nm_recorded'])})
        elif r['observation_status']=='multiple_or_alternative_spacing_values':
            # Explicit finite parsing rules, not an unrestricted extraction of all digits.
            text=r['spacing_cell_raw']
            if r['ion']=='Fe' and float(r['concentration_mM_nominal'])==50:
                matches=re.findall(r'(RT\d+):\s*([\d.]+)',text)
            elif r['ion']=='Co' and float(r['concentration_mM_nominal'])==30:
                matches=[('without third peak','13.89'),('with third peak','14.097209')]
            else: raise ValueError('Unreviewed mixed spacing cell')
            for label,value in matches:
                points.append({**base,'record_kind':'mixed_cell_value','sample_label':label,'spacing_nm':float(value)})
        if r['second_try_spacing_raw']:
            points.append({**base,'source_column':'F','record_kind':'second_try_fit',
                           'spacing_nm':float(r['second_try_spacing_raw'])})
    return points

def concentration(rows):
    points=points_from_registry(rows)
    write_csv('results/spacing-points.csv',points)
    fig,axs=plt.subplots(2,3,figsize=(9.2,6),layout='constrained',sharex=True,sharey=True)
    order=['Ni','Co','Fe','Mn','Cu']
    palette=dict(zip(IONS,COLORS))
    for ax,ion in zip(axs.flat,order):
        col=palette[ion]
        for p in [x for x in points if x['ion']==ion]:
            kind=p['record_kind']; marker='o' if kind=='recorded_primary' else 'D' if kind=='tentative_single_peak' else 'x'
            kwargs={'facecolors':'none'} if kind=='tentative_single_peak' else {}
            if marker=='x': ax.scatter(p['nominal_concentration_mM'],p['spacing_nm'],marker=marker,color=col,s=30,lw=1.3)
            else: ax.scatter(p['nominal_concentration_mM'],p['spacing_nm'],marker=marker,edgecolors=col,c=None if kwargs else col,s=27,lw=1,**kwargs)
        ax.axhline(6.323221,color='#9CA5AC',lw=.7,ls=':',zorder=0)
        ax.set_xscale('log');ax.set_ylim(5,28);ax.set_xlim(.07,145)
        ax.set_title(ion+('Cl$_3$' if ion=='Fe' else 'Cl$_2$'),loc='left',fontweight='bold',color=col)
        ax.set_xticks([.1,1,10,100],['0.1','1','10','100']);ax.grid(axis='y',color='#E0E5E8',lw=.5)
    for ax in [axs[0,0],axs[1,0]]: ax.set_ylabel('Recorded D (nm)')
    for ax in axs[1,:2]: ax.set_xlabel('Nominal added salt (mM)')
    legend=axs[1,2];legend.axis('off')
    legend.text(.03,.93,'Lamellar repeat distance',fontweight='bold',fontsize=10,transform=legend.transAxes)
    for y,marker,text in [(.77,'o','Primary spacing assignment'),(.61,'D','Tentative single-peak assignment'),(.45,'x','Mixed-cell or second-try value')]:
        legend.scatter(.06,y,marker=marker,s=30,color='#394552',facecolors='none' if marker=='D' else '#394552',transform=legend.transAxes)
        legend.text(.15,y,text,fontsize=8.2,va='center',transform=legend.transAxes)
    legend.text(.03,.25,'Dotted line: water reference\n\nAlternative assignments are retained\nseparately; values are not averaged.',fontsize=8,color='#4D5965',va='top',transform=legend.transAxes)
    save(fig,'concentration-response')
    return points

def coverage(rows):
    statuses=['spacing_recorded','no_peaks_recorded','blank_spacing_entry','multiple_or_alternative_spacing_values','not_available_in_summary']
    short=['D','NP','blank','alt','N/A'];table=[]
    fig,ax=plt.subplots(figsize=(8.6,3.8));ax.set_xlim(-.5,7.5);ax.set_ylim(4.5,-.5)
    for i,ion in enumerate(IONS):
        for j,c in enumerate(CONCS):
            selected=[r for r in rows if r['scope']=='main_summary' and r['ion']==ion and float(r['concentration_mM_nominal'])==c]
            counts={s:sum(r['observation_status']==s for r in selected) for s in statuses}
            actual=[s for s in statuses if counts[s]]
            text=' / '.join(short[statuses.index(s)]+(f'({counts[s]})' if counts[s]>1 else '') for s in actual)
            face='#E3EFF0' if actual==['spacing_recorded'] else '#F6ECD8' if 'no_peaks_recorded' in actual else '#EEF0F2'
            ax.add_patch(Rectangle((j-.48,i-.47),.96,.94,facecolor=face,edgecolor='white'))
            ax.text(j,i,text,ha='center',va='center',fontsize=9 if len(text)<12 else 8)
            table.append({'ion':ion,'nominal_concentration_mM':c,'source_rows':len(selected),
                **counts,'status_labels':text,'independent_samples':'unresolved'})
    ax.set_xticks(range(8),['0.1','1','10','20','30','40','50','100']);ax.set_yticks(range(5),IONS)
    ax.set_xlabel('Nominal added salt concentration (mM)');ax.tick_params(length=0)
    for s in ax.spines.values():s.set_visible(False)
    fig.subplots_adjust(left=.07,right=.99,top=.94,bottom=.28)
    fig.text(.07,.10,'D: numeric spacing cell   NP: "No Picks"   alt: mixed values   blank: empty spacing cell   N/A: recorded unavailable',fontsize=8)
    fig.text(.07,.045,'Parentheses count source rows, not samples. A blank is not a peak-free observation. No Cycling rows are excluded.',fontsize=8,color='#4D5965')
    save(fig,'observation-map');write_csv('results/condition-summary.csv',table)

def representative():
    specs=json.loads((ROOT/'data/curve-inputs.json').read_text())
    fig,axs=plt.subplots(2,2,figsize=(8,5.4),height_ratios=[2.6,1],layout='constrained')
    full,fa=plt.subplots(1,2,figsize=(8,3.4),layout='constrained')
    checks=[]
    for j,(s,col) in enumerate(zip(specs,['#007C83','#C66326'])):
        data={k:curve(v) for k,v in s['paths'].items()}
        q,y=data['signal'].T; qm,ym=data['model'].T
        assert np.array_equal(q,qm) and np.array_equal(data['signal'],data['subtracted'])
        aa,bb=data['sample_dc'],data['background_dc']
        assert q[0]>=max(aa[0,0],bb[0,0]) and q[-1]<=min(aa[-1,0],bb[-1,0])
        calc=np.interp(q,aa[:,0],aa[:,1])-s['background_factor']*np.interp(q,bb[:,0],bb[:,1])
        delta=y-calc;assert abs(delta).max()<5e-5
        mask=(q>=.2)&(q<=3);assert (y[mask]>0).all() and (ym[mask]>0).all()
        ax=axs[0,j];ar=axs[1,j]
        ax.plot(q[mask],y[mask],color='#46515B',lw=.65,label='Processed measurement')
        ax.plot(q[mask],ym[mask],color=col,lw=1.2,label='Archived model')
        ax.set_yscale('log');ax.set_title(f'{chr(97+j)}  {s["salt"]}, {s["concentration_mM"]} mM | {s["sample"]}',loc='left',fontweight='bold')
        ax.set_xlim(.2,3);ax.set_ylim(.35,230);ax.legend(fontsize=7,frameon=False)
        ar.axhline(0,color='#8C98A0',lw=.7);ar.plot(q[mask],(y-ym)[mask],color=col,lw=.65)
        ar.set_xlim(.2,3);ar.set_ylim(-60,60);assert np.max(abs((y-ym)[mask]))<60
        ar.set_xlabel(r'$q$ (nm$^{-1}$)')
        if j==0:ax.set_ylabel('Intensity (a.u.)');ar.set_ylabel('Data - model\n(a.u.)')
        for a in [ax,ar]:a.grid(axis='y',alpha=.2)
        a=fa[j];a.plot(q,y,color='#46515B',lw=.65,label='Processed measurement');a.plot(q,ym,color=col,lw=1.2,label='Archived model')
        a.set_yscale('symlog',linthresh=1);a.axvspan(q[0],.2,color='#F6ECD8');a.axvspan(3,q[-1],color='#EEF0F2')
        a.set_title(f'{s["salt"]} {s["concentration_mM"]} mM | {sum(y<=0)} nonpositive values',fontsize=9)
        a.set_xlabel(r'$q$ (nm$^{-1}$)');a.legend(fontsize=7,frameon=False);a.grid(axis='y',alpha=.2)
        if j==0:a.set_ylabel('Intensity (a.u.; symmetric log)')
        records=[dict(q_nm_inverse=x,processed_intensity_au=v,archived_model_au=m,data_minus_model_au=v-m) for x,v,m in zip(q,y,ym)]
        write_csv(f'results/{s["ion"].lower()}-overlay-values.csv',records)
        checks.append({'sample':s['sample'],'rows':len(q),'q_min':q[0],'q_max':q[-1],
            'subtraction_max_abs_difference_au':float(abs(delta).max()),'nonpositive_values':int(sum(y<=0)),
            'signal_matches_processed_source':True,'model_q_matches_signal':True,'model_refitted':False})
    save(fig,'representative-scattering');save(full,'full-range-diagnostic')
    return checks

def peak_center(q,y,window):
    mask=(q>=window[0])&(q<=window[1]);x=q[mask];v=y[mask]
    j=int(np.argmax(v));assert 0<j<len(x)-1
    local=x[j-1:j+2]-x[j];a,b,c=np.polyfit(local,v[j-1:j+2],2)
    shift=-b/(2*a);assert a<0 and local[0]<=shift<=local[-1]
    return float(x[j]+shift)

def sensitivity():
    # A deliberately bounded, descriptive stress test. These percentages are NOT an error model.
    s=next(s for s in json.loads((ROOT/'data/curve-inputs.json').read_text()) if s['ion']=='Ni')
    raw=curve(s['paths']['sample_dc']);bg=curve(s['paths']['background_dc']);observed=curve(s['paths']['signal'])
    q=observed[:,0];a=np.interp(q,raw[:,0],raw[:,1]);b=np.interp(q,bg[:,0],bg[:,1])
    windows=[(.63,.85),(1.36,1.58)];h=np.array([1,2]);reports=[]
    fig,axs=plt.subplots(1,2,figsize=(8,3.3),layout='constrained')
    for frac,col in zip([-.05,-.01,0,.01,.05],['#95A847','#007C83','#273A49','#C66326','#A44B6C']):
        factor=s['background_factor']*(1+frac);y=a-factor*b
        centers=np.array([peak_center(q,y,w) for w in windows]);slope=float(h@centers/(h@h));D=float(2*np.pi/slope)
        reports.append({'relative_factor_change':frac,'factor':factor,'q1_nm_inverse':centers[0],
                        'q2_nm_inverse':centers[1],'two_order_D_nm':D,
                        'q2_over_q1':centers[1]/centers[0]})
        for ax,w in zip(axs,windows):
            m=(q>=w[0])&(q<=w[1]);ax.plot(q[m],y[m],color=col,lw=1,label=f'{frac:+.0%}' if frac else 'Archived factor')
    for n,ax in enumerate(axs):
        ax.set_xlabel(r'$q$ (nm$^{-1}$)');ax.set_title(f'Ni RE45 | assigned order {n+1}',loc='left',fontsize=10);ax.grid(alpha=.2)
    axs[0].set_ylabel('Reconstructed intensity (a.u.)');axs[1].legend(fontsize=7,frameon=False)
    save(fig,'background-sensitivity');write_csv('results/background-sensitivity.csv',reports)
    report={'sample':'Ni RE45','nominal_salt_mM':100,'base_factor':s['background_factor'],
            'relative_factor_changes':[-.05,-.01,0,.01,.05],'peak_windows_nm_inverse':windows,
            'method':'Three-point quadratic interpolation at highest intensity in each fixed window; assign h=1,2; least-squares slope through origin; D=2*pi/slope.',
            'D_range_nm':[min(r['two_order_D_nm'] for r in reports),max(r['two_order_D_nm'] for r in reports)],
            'recorded_workbook_D_nm':8.520042,'uncertainty_estimated':False,
            'limits':'Illustrative perturbations, not calibrated factor uncertainty. Windows/orders selected by inspection of two visible peaks. Not the original X+ fit; no raw integration, order-selection, temperature or sample-variation test.'}
    (ROOT/'results/sensitivity-method.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    return report

def main():
    from graphical_abstract import make_graphic
    make_graphic(ROOT)
    for sub in ['figures','results']:(ROOT/sub).mkdir(exist_ok=True)
    style();rows=list(csv.DictReader((ROOT/'data/observations.csv').open(encoding='utf-8-sig')))
    schematic();points=concentration(rows);coverage(rows);checks=representative();sens=sensitivity()
    report={'source_rows':len(rows),'main_rows':sum(r['scope']=='main_summary' for r in rows),
        'no_cycling_rows':sum(r['scope']=='no_cycling_section' for r in rows),'displayed_spacing_values':len(points),
        'spacing_marker_counts':{k:sum(p['record_kind']==k for p in points) for k in sorted(set(p['record_kind'] for p in points))},
        'curve_checks':checks,'sensitivity':sens,'statistical_uncertainty_reported':False}
    (ROOT/'results/rebuild-summary.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
