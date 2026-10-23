<picture>
<source media="(max-width: 520px) and (prefers-color-scheme: dark)" srcset="assets/hero-mobile-dark.svg">
<source media="(max-width: 520px)" srcset="assets/hero-mobile-light.svg">
<source media="(prefers-color-scheme: dark)" srcset="assets/hero-dark.svg">
<img src="assets/hero-light.svg" width="100%" alt="SaLSA — Salt–Lipid Scattering Analysis. Ion-dependent organization of DPPC membranes.">
</picture>

How do metal ions change the organization of lipid membranes? SaLSA uses small-angle X-ray scattering (SAXS) to compare DPPC in CuCl₂, CoCl₂, NiCl₂, MnCl₂ and FeCl₃ solutions across salt concentrations of 0.1–100 mM.

**Roee Tekoah, Eitan Eisenthal Berkovitz, Lea Fink, Asaf Shemesh and Uri Raviv**<br>
<sub>Raviv Group · Hebrew University of Jerusalem · Research conducted in 2017–2018</sub>

## ↗ Read the work

<table width="100%">
<tr><td width="84" align="center" valign="middle"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/paper-dark.svg"><img src="assets/paper-light.svg" width="64" alt=""></picture></td><td valign="middle"><p><strong>The paper</strong><br>Ion-dependent lamellar organization of DPPC membranes: a SAXS study. Experimental methods, results, interpretation and supporting information.</p><p><a href="output/pdf/main.pdf">Read the paper · 9 pages ↗</a></p></td></tr>
<tr><td width="84" align="center" valign="middle"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/curves-dark.svg"><img src="assets/curves-light.svg" width="64" alt=""></picture></td><td valign="middle"><p><strong>The measurements</strong><br>Processed scattering curves across five salt series, with recorded lamellar spacings and source links.</p><p><a href="docs/curve-atlas.md">Browse the curves ↗</a> &nbsp;·&nbsp; <a href="results/spacing-points.csv">Spacing data ↗</a></p></td></tr>
<tr><td width="84" align="center" valign="middle"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/workflow-dark.svg"><img src="assets/workflow-light.svg" width="64" alt=""></picture></td><td valign="middle"><p><strong>The experiment</strong><br>Sample preparation, SAXS measurements, background subtraction and structural analysis with X+.</p><p><a href="docs/workflow.md">Experimental workflow ↗</a> &nbsp;·&nbsp; <a href="docs/evidence.md">Data documentation ↗</a></p></td></tr>
</table>

## ◈ Membrane organization across the salt series

The concentration series compares lamellar repeat distances and their dependence on ion identity. The paper interprets the swelling and contraction in terms of adsorption, membrane charging and electrostatic screening.

<a href="output/pdf/main.pdf#page=4"><img src="figures/concentration-response.png" width="100%" alt="Recorded lamellar repeat distances versus nominal added salt for nickel, cobalt, iron, manganese and copper. Symbols distinguish primary, tentative and alternative assignments."></a>

<sub>Recorded spacing assignments; tentative and alternative values are shown separately. [Figure and interpretation →](output/pdf/main.pdf#page=4)</sub>

## ⌘ Data and analysis

[Processed curves](data/series-inputs.csv), [spacing tables](results/spacing-points.csv), [source associations](data/evidence-links.csv) and [figures](figures/) accompany the manuscript. The [analysis scripts](analysis/) regenerate plots and numerical summaries from the processed inputs; the original detector integration and nonlinear X+ fits are separate steps.

**[Run the analysis →](environment/README.md)** &nbsp;·&nbsp; [Understand the data →](docs/evidence-links.md)

## ↗ Related research

The study builds on the Raviv Group’s work on ion adsorption and interactions between lipid membranes, including [Szekely et al. (2011)](https://doi.org/10.1021/la200264s) and [Fink et al. (2017)](https://doi.org/10.1021/acs.langmuir.7b00596).

**[Research context and references →](docs/research-context.md)**

---

<sub>[Cite SaLSA](CITATION.cff) · [Authors and contributions](docs/contributors.md) · Code: [MIT](LICENSES/MIT.txt) · Manuscript, figures and data: [CC BY 4.0](LICENSES/CC-BY-4.0.txt) · [License scope](LICENSE.md)</sub>
