# TCI Calculator

A lightweight Python tool to compute the Topographic Control Index (TCI) from a DEM, following Huang et al. (2019).

## Install

```bash
pip install TCI_tool
```

## Quick Start

```python
from TCI_tool import full_workflow
import rasterio

tci = full_workflow(fp_dem, fp_aoi)
# save or analyze `tci`
```

## License

MIT
