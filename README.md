# Theoretical Analysis of Internet Architectures

## Project Overview
This project contains the source code for a theoretical analysis of different Internet architectures. Architectures examined include the current BGP network, based on [CAIDA](https://www.caida.org) data, a hypothetical SCION topology, and synthetic expander graphs.

## Requirements

- Python >= 3.11
- Installing python dependencies:
```
 pip install -r requirements.txt
```

## Commands

To evaluate the data, run:

```bash
python3 -m scripts.evaluate_border_breadth
```

```bash
python3 -m scripts.evaluate_metrics_comparison
```

```bash
python3 -m scripts.evaluate_downsampling
````


To produce the figures, run:

```bash
python3 -m plots.plot_border_breadth
```

```bash
python3 -m plots.plot_metrics_comparison
```

```bash
python3 -m plots.plot_downsampling
```

