"""Vector schematic of adsorption-induced membrane swelling; no experimental data."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

def make_graphic(root=None):
    root=Path(root) if root is not None else Path(__file__).resolve().parents[1]
    fig,ax=plt.subplots(figsize=(3.5,2.8))
    fig.subplots_adjust(left=.01,right=.99,bottom=.02,top=.98)
    ax.set(xlim=(0,10),ylim=(0,7));ax.axis('off')
    blue='#287E9C';tail='#78969B';gold='#C87728';ink='#253846'
    def bilayer(x,mid):
        for xx in np.linspace(x-1.3,x+1.3,12):
            for side in [-1,1]:
                yy=mid+side*.34
                ax.plot([xx-.025,xx-.025],[yy-side*.06,mid],lw=.75,color=tail)
                ax.plot([xx+.025,xx+.025],[yy-side*.06,mid],lw=.75,color=tail)
                ax.add_patch(Circle((xx,yy),.072,facecolor=blue,edgecolor='none'))
    for y in [2.5,3.9]:bilayer(2.1,y)
    for y in [1.7,4.8]:bilayer(7.3,y)
    ax.text(2.1,5.8,'Compact stack',ha='center',fontsize=8.7,color=ink)
    ax.text(7.3,5.8,'Swollen stack',ha='center',fontsize=8.7,color=ink)
    for x,y in [(6.5,2.19),(7.6,2.18),(6.8,4.32),(7.9,4.33),(8.6,3.4),(5.6,3.9)]:
        ax.add_patch(Circle((x,y),.14,facecolor=gold,edgecolor='none'))
        ax.text(x,y,'+',ha='center',va='center',fontsize=8,color='white')
    ax.annotate('',xy=(5.3,3.2),xytext=(3.8,3.2),arrowprops=dict(arrowstyle='->',color=gold,lw=1.4))
    ax.text(4.5,3.68,'Ion\nadsorption',ha='center',va='bottom',fontsize=8,color=ink)
    ax.annotate('',xy=(9.1,4.8),xytext=(9.1,1.7),arrowprops=dict(arrowstyle='<->',color=ink,lw=.85))
    ax.text(9.35,3.25,'D',fontsize=11,style='italic',color=ink,va='center')
    ax.text(5,.58,'Membrane charging and electrostatic swelling',ha='center',fontsize=7.8,color=ink)
    ax.text(5,.03,'Schematic',ha='center',fontsize=6.8,color='#687783')
    for ext in ['pdf','svg','png']:
        fig.savefig(root/f'figures/graphical-abstract.{ext}',dpi=300,transparent=True)
    plt.close(fig)

if __name__=='__main__':make_graphic()
