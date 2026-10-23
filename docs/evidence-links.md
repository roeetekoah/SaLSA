# Portable evidence links

`evidence-links.csv` has exactly one row for each of the 72 `observation_id` values in the source table, in the original order. It indexes source associations; the rows do not establish 72 independent samples.

## Portable paths and joining

Join the table to `data/observations.csv` by `observation_id`. The source workbook, row, original scope, original sample ID and original condition are preserved. IDs such as `RE 9`, `RT56`, `Roee_57` and `Roee_56low` remain distinct historical strings; no global prefix substitution was performed.

Resolve paths against two user-supplied archive roots:

| Alias | Expected archive directory |
|---|---|
| `DPPC_PAPER` | `DPPC Paper` |
| `DPPC_PROJECT` | `DPPC_Project` |

All path cells use forward-slash relative paths, with no drive letters or absolute local paths. The CSV contains the hashes of selected signals, sample DC inputs, and INIs. `additional_candidates_json` is a JSON array within a properly quoted CSV cell; each item has its own role, archive alias, relative path, SHA-256, and link status. The CSV preserves UTF-8 source text. `background_links_json` records subtracted-background inputs and their acquisition links separately; these must never be treated as sample runs.

## Interpret the confidence fields separately

- `signal_link_status=identifier_and_condition_candidate_only` means the selected source has the expected acquisition identifier and condition in the archive. This does not independently prove vial identity or prove that the curve generated the exact workbook value. The selected path is a useful representative pointer, not a resolution of every ambiguous row.
- `ini_link_status=phase_a_matches_active_peaks` means a named INI's stored `Phase_a` equals the relevant worksheet value within 10^-6 nm and its active `peaks` count is greater than zero. There are **32** such row links. This is parameter provenance, not a refitted result, goodness-of-fit validation, or proof that all stored centers belong to the selected signal.
- `same_identifier_candidate_only` means an INI was recovered by acquisition identifier but no relevant matching active-peak spacing was established. This includes form-factor-only or blank-spacing rows, for which a surviving `Phase_a` may be stale and meaningless.
- `not_recovered` means this bounded search did not recover a matching named parameter candidate; it is not proof that none exists outside the inventoried locations.
- `acquisition_link_status=sample_operand_id_and_dc_header_match_raw_log` applies to 57 BG-subtracted selected curves. The positive first operand of the recorded subtraction expression is traced to a named sample DC file; its acquisition identifier and No Cycling variant are checked against the selected signal. Its header sample identifier is then checked again, all background-named headers are rejected as sample links, and the first five lines are compared with the raw acquisition log. Those lines are the internal detector path, shutter-open time, shutter-close time, exposure-time field, and beam-stop counts.
- `acquisition_link_status=selected_dc_sample_id_and_header_match_raw_log` applies to the 15 selected WB3 DC curves. Their sample identifiers and treatment variants are checked against their own acquisition headers, followed by the same five-line log comparison. All **72 representative row links** now pass the full sample-role, identifier, and header checks. This supplies a source association; it does not verify detector integration, preparation count, accurate exposure-field interpretation, or which acquisition generated an ambiguous summary entry.
- `paper_export_identity_status` reports numerical q/intensity equality separately. Three rows have exact numerical subset matches to correctly named paper exports (Ni RE45, Mn RE50, Fe Roee52). Cu RE3 matches the conflicted Co-labeled paper export; that status explicitly retains the label conflict. Other rows were not compared to paper exports in this pass.

The No Cycling entries have their own signal and raw-log paths and remain separate rows. The main-series entries are not automatically assigned a cycling treatment. Every `independent_preparation_id` remains `unresolved`.

### Sample and background operands

Sample identity follows the positive operand in the recorded subtraction expression. The letters `A` and `B` do not have fixed sample/background roles. Nineteen expressions use `B − scaled A`, where `A` is the background.

For example, Cu RE1 has `B-(A*0.84)`, with `B=RE_1_7200sec_DC_Sub`; Cu RE3 has `B-(A*0.92)`, with `B=RE_3_7200sec_DC_Sub`. Their sample logs are `Series1/Raw Data/20170123/RE_1_7200sec.log` and `Series1/Raw Data/20170122_2/RE_3_7200sec.log`. Background logs are retained separately in `background_links_json`.

Three BG headers (Co RE7, RE8 and RE9) specify the sample operand but omit a nested variable definition for the background. Their sample runs follow the explicit sample operand; missing background definitions are marked `header_definition_incomplete`.

## Selection and unresolved cases

For WB1/WB2, condition-folder signals were preferred over aggregate copies. Alternative copies were compared by SHA-256 and labeled byte-identical or different editions. A matching active-peak INI was preferred when available; this is why Co RE9's selected INI comes from the aggregate `All BG SUB Signals Series 1` folder rather than the condition folder.

For WB3, the selected signal paths are named acquisition candidates from the same condition. When a row can refer to multiple acquisitions or treatments, the remaining curves are retained in `additional_candidates_json` and `issues` marks the ambiguity. In particular:

- Fe40 can refer to Roee54, Roee55 or the later Roee55low strong-centrifuge acquisition. The representative pointer to Roee55low does not resolve this choice.
- Fe50 explicitly contains RT56 and RT57 values. Its representative signal is Roee57's strong-centrifuge curve, with both 56 and 57 alternatives retained. The unrelated/stale zero-peak INI named for 56 is retained only as an additional candidate, not paired with the selected 57 signal.
- Cu30/40/50 N/A cells have signal candidates because their acquisitions exist. N/A remains “no spacing assigned in the summary.”
- Mn30 uses the updated `MembraneExp updated to 19.9.17` INI because its stored `Phase_a` matches the summary. The conflicting Paper-archive INI remains an explicit alternative.
- Co30's matching INI supports the three-peak value 14.097209. The 13.89 value is an alternate analysis and must not be counted as another preparation.

Second Try values in WB2 have separate Series3 parameter and curve leads in the JSON candidate field, where recoverable. These are not automatically new preparations or equivalent processing stages. The selected primary fields continue to refer to the main-summary acquisition.

Other informative mismatches remain visible in `issues`: the selected INIs for Co RE8, Fe RE25/27/28, Fe RE34, Cu RE39, and Ni RE47 do not match the primary workbook value. They must not be silently promoted to validated fits. The source table’s generic Co-example conflict flag on RE12 is retained verbatim, but the notes clarify that the exact Cu identity finding concerned the RE9-labeled paper export; no such identity conflict was established for the separate RE12 signal.

## Ni RE45: historical indexing recovered

The selected Ni RE45 INI declares two active peaks, with centers q1=0.728879 and q2=1.479209 nm^-1. The origin-constrained relation q_h=h·b, for h=1,2, gives:

`b = (1 × 0.728879 + 2 × 1.479209) / (1² + 2²) = 0.7374594 nm^-1`

`D = 2π / b = 8.520042333421456 nm`

This agrees with the stored/workbook D=8.520042 nm to its printed precision (difference 3.33 × 10^-7 nm). The leftover `Center3=2.191709` key is inactive; including it would instead produce 8.571522118021456 nm. Active peak count must therefore govern the calculation.

An independent descriptive check of the processed measured intensity used windows [0.65,0.82] and [1.35,1.58] nm^-1, located each sampled maximum, and interpolated its three neighboring values with a quadratic. The sampled maxima were 0.73485 and 1.4681 nm^-1; the interpolated maxima were 0.7362188606687952 and 1.46720372938368 nm^-1. Applying the same two-order indexing relation to those maxima gives **8.55873733851604 nm**, reproducing the previously quoted approximate 8.55874 nm.

These calculations use **different center estimators**: serialized profile-model peak centers versus maxima of the total measured intensity. They need not coincide, especially for broad peaks superposed on a varying form factor/background or other model components. This distinction explains why the numerical procedures yield different D values; it does not by itself establish that the historical model was correct or identify the physical origin of the difference. No profile fit was rerun. The worksheet's 0.00848 nm error remains undefined.

The active-center inputs are supplied in [the Ni parameter record](../data/ni-active-parameters.json). The archived Ni100 mM parameters recover the indexed spacing of 8.520 nm from the two active peak centers; direct local intensity maxima give a different descriptive estimate. The latter is a sensitivity check, not a replacement for the recorded fit result.

## Verification

The corrected CSV has 72 unique IDs matching the source table exactly; all preserved identifier/condition fields match their source rows. All 506 path/hash checks pass. No absolute local paths occur in the CSV. The 57 positive sample operands and 15 directly selected sample DC curves were checked against acquisition identifiers, treatment variants and raw-log headers; background headers are explicitly rejected from sample-link columns. Four paper-export numerical subset matches, 32 active-peak Phase_a matches, and the Ni indexing calculations remain checked. None of these checks supplies an independent-preparation count or validates the unresolved historical uncertainty definitions. The sample/background association fields, hashes and unresolved cases are supplied in [the evidence-link table](../data/evidence-links.csv).
