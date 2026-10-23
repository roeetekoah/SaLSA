# Experimental and computational workflow

## Experiment

The DPPC dispersions were prepared from ethanol aliquots, lyophilized and hydrated with the corresponding salt solutions. The main preparation protocol included freeze–thaw cycling, incubation, transfer to capillaries and centrifugation before SAXS. Separate No Cycling records are identified in the data tables.

Detector images were radially integrated with FIT2D. Dark-current and salt-solution background corrections preceded structural analysis with X+. Lamellar peak positions were indexed to estimate repeat distances; bilayer models describe the scattering envelope. Full preparation and analysis details appear in the [paper](../output/pdf/main.pdf).

## Data and plotting

The repository provides processed numerical curves, sample and processing links, recorded spacing assignments and model exports. `analysis/rebuild.py` produces the manuscript figures and numerical summaries; `analysis/series_atlas.py` generates the salt-series curve atlas; `analysis/verify.py` checks input integrity and numerical relationships. See the [setup instructions](../environment/README.md).

The scripts begin with processed inputs. They do not re-integrate detector frames or rerun nonlinear X+ fits. Candidate source links, alternative assignments and differences in processing stage are described in the [data documentation](evidence.md).
