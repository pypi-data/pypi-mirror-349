# Gene panel builder datamodels

A collection of useful Pydantic datamodels for the Gene Panel Builder

## Installation

`pip install gpb-models`

## Usage

With a gene panel exported from the Gene Panel Builder in a folder `MyGenePanel`, load the panel like this:

```
from pathlib import Path
from gpb_models import GenePanel

json_file = next(Path("MyGenePanel").glob("*.json))
with json_file.open() as f:
    panel = GenePanel.model_validate_json(f.read())

print(panel)
```