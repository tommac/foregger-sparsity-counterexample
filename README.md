# Sparsity is not enough: Foregger's inequality fails for fully indecomposable matrices

**Tom Maciejewski** · Preprint, 2026 · [Read the paper (PDF)](paper.pdf) · [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24543258.svg)](https://doi.org/10.5281/zenodo.24543258)

## Abstract

A nearly decomposable matrix of order $n\ge3$ has at most $3n-3$ nonzero entries, and if it is doubly stochastic then its permanent is at least $2^{1-n}$. This is Foregger's inequality, proved by Lavi in 2026. Is it the sparsity of these matrices that matters, or their minimality? We show that sparsity is not enough. There is a fully indecomposable doubly stochastic $6\times6$ matrix with $15=3n-3$ positive entries, all equal to $\frac14$, $\frac38$ or $\frac12$, whose permanent is $\frac{15}{512}<\frac{16}{512}$; checking this takes three lines, and no smaller order allows it. The threshold is exact: a fully indecomposable doubly stochastic matrix with at most $2n+2$ positive entries satisfies the inequality, and in every order $n\ge3$ the same construction gives one with $2n+3$ positive entries that does not. Chaining the construction gives matrices within the $3n-3$ budget whose permanents fall below $2^{1-n}$ by a factor that is exponentially small in $n$.

## Contents

| File | What it is |
|---|---|
| [`paper.pdf`](paper.pdf) | The paper (5 pages) |
| [`paper.tex`](paper.tex) | Its LaTeX source |
| [`anc/verify.py`](anc/verify.py) | Exact check of the theorems and constants in the paper. Python standard library only; a few seconds. |
| [`anc/verification-output.txt`](anc/verification-output.txt) | What the scripts printed when this version was built |

## Checking the computations

```bash
python3 anc/verify.py
```

## Citing this paper

```bibtex
@misc{maciejewski2026sparsity,
  author = {Maciejewski, Tom},
  title  = {Sparsity is not enough: {Foregger}'s inequality fails for fully indecomposable matrices},
  year   = {2026},
  note   = {Preprint},
  doi    = {10.5281/zenodo.24543258},
}
```

## Status

This is a preprint and has not been peer reviewed. If you find an error, please open an issue.

## License

The paper is licensed under [CC BY 4.0](LICENSE). The code in `anc/` is under the [MIT License](LICENSE-CODE).
