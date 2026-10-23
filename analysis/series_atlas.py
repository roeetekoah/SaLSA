"""Browse representative curve candidates without inferring their spacing or phase."""
from pathlib import Path
import csv, math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]

def main():
    rows=list(csv.DictReader((ROOT/'data/series-inputs.csv').open(encoding='utf-8')))
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':7,'svg.fonttype':'none','pdf.fonttype':42,
                         'axes.spines.top':False,'axes.spines.right':False})
    for ion,col in zip(['Cu','Co','Ni','Mn','Fe'],['#007C83','#C66326','#5D68A7','#7A8B32','#A44B6C']):
        selected=[r for r in rows if r['ion']==ion]
        nrow=math.ceil(len(selected)/3)
        fig,axs=plt.subplots(nrow,3,figsize=(10,nrow*2.15+1),squeeze=False)
        for ax,r in zip(axs.flat,selected):
            a=np.loadtxt(ROOT/r['curated_file'],delimiter=',',skiprows=1)
            mask=a[:,0]>0
            ax.plot(a[mask,0],a[mask,1],color=col,lw=.6)
            ax.set_yscale('symlog',linthresh=1);ax.grid(axis='y',alpha=.15)
            ax.set_title(f'{r["observation_id"].replace("-Sheet1-","/")} | {r["nominal_concentration_mM"]} mM',loc='left',fontsize=8,fontweight='bold')
            kind='No Cycling' if r['scope']=='no_cycling_section' else 'main summary'
            stage=r['signal_processing_stage'].replace('_named_export','').replace('_',' ')
            ax.text(.98,.96,kind+' | '+stage,fontsize=6,ha='right',va='top',transform=ax.transAxes)
            ax.set_xlabel(r'$q$ (nm$^{-1}$)');ax.set_ylabel('Intensity (a.u.)')
        for ax in list(axs.flat)[len(selected):]:ax.axis('off')
        fig.suptitle(f'{ion} salt series | representative archived curve candidates',fontsize=13,fontweight='bold',x=.07,ha='left',y=.99)
        fig.text(.07,.955,'Source associations, not verified fit-to-row links. Different processing/treatments; no absolute intensity comparison.',fontsize=8,color='#566570')
        fig.text(.07,.015,'Symmetric log retains nonpositive intensities. Nonpositive q padding, if present, is omitted only from display and retained in CSV.',fontsize=7,color='#566570')
        fig.subplots_adjust(left=.07,right=.99,bottom=.06,top=.91,wspace=.3,hspace=.55)
        for ext in ['png','svg']:
            fig.savefig(ROOT/f'figures/series-atlas-{ion.lower()}.{ext}',dpi=150,facecolor='white')
        plt.close(fig)
    print(f'Generated five curve-atlas images from {len(rows)} representative row candidates; water control remains in input table.')

if __name__=='__main__':main()
