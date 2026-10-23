# Evidence decisions

The immutable source-row transcription is `data/observations.csv`. New interpretation belongs in `data/curation-decisions.csv` and `data/evidence-links.csv`. Source filenames identify archive records; they do not independently establish vial identity, treatment or experimental replication. The source table carries a condition-wide Co conflict flag; the curation table identifies the demonstrated export conflict as RE9 and explicitly records that no separate RE12 identity conflict was established.

The evidence-link table has one representative source pointer per registry row, 32 matching active-peak Phase_a records and separate sample/background operands. All 72 representative sample DC headers were associated with raw logs after checking the actual subtraction expression; this does not establish which candidate generated an ambiguous spacing assignment. Nineteen expressions use a background-first variable order. The table identifies sample and background operands from the subtraction expression. Candidate alternatives and incomplete nested background definitions remain visible.

| Issue | Current disposition |
|---|---|
| Co 0.1 mM representative paper export | Exactly matches Cu RE3, not genuine Co RE9. Exclude the old signal/model pair; do not silently relabel the paired model. |
| Cu 1 mM contradiction | RE2/RE5 saved five-peak fits and curves support finite distances near 6.34 nm. Correct the old pure-form-factor statement. |
| Fe 30 mM export | Matches a contiguous crop of a DC-subtracted source. Not used as a matched solution-background-subtracted overlay. |
| Intermediate-concentration WB3 | Byte-identical to a Strong Centrifuge workbook. Some sample/INI links recovered; do not assign treatment to every row from the workbook name. |
| Mn 30 mM fit edition | Updated Mn67 edition matches 15.788546 nm; other copies store Ni50's value. Preserve the conflict rather than choosing an entire archive branch as canonical. |
| Cu 30/40/50 N/A | Processed curves exist. N/A means a missing assignment in the chosen table, not no acquisition. |
| Weak, ambiguous or single peaks | Visible tentative markers; no unqualified harmonic-series claim. |
| Alternative and second-try fits | Separate markers; no averaging or sample multiplication. |
| Blanks and No Picks | Different statuses. A blank is not a form-factor-only observation. |
| Historical Error values | Preserved; no plotted error bars until definition and relation to preparation variability are recovered. |
| Nominal concentrations | Preparation labels, not free-ion activities. Fe and divalent chlorides have different ideal ionic strengths at equal molarity. |
| Measurement temperature | Zero log fields with oven-off notes do not establish 0°C. No thermal phase assigned. |
| Replication | Source rows and RE/RT/Roee labels do not establish independent preparations. |

The current concentration figure authenticates recorded assignments. It does not independently validate every fit or constitute a phase diagram. The water reference is retained as recorded, with identity unresolved; it must not support a precise adsorption comparison until checked.

Run-specific measurement temperature, some preparation links and some fit-session assignments remain unresolved. These limits should be considered when comparing conditions or interpreting individual source assignments.
