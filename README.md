# Theoretical Analysis of Internet Architectures

## Project Overview
This project contains the source code for a theoretical analysis of different Internet architectures. Architectures examined include the current BGP network, based on [CAIDA](https://www.caida.org) data, a hypothetical SCION tology and synthetic expander graphs.


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

