## HoloBench
### Benchmarking Discrete Sequence Optimization Algorithms

### Installation

```bash
python -m pip install pytorch-holo
```

### Usage

```bash
python scripts/benchmark_optimizer.py
```


### Example
```python
import torch
from holo.test_functions.closed_form import Ehrlich
from holo.optim import DiscreteEvolution

test_fn = Ehrlich(negate=True)
print(f"Desired motif: {test_fn.motifs[0]}")
print(f"Desired motif spacing: {test_fn.spacings[0]}")
print(f"Optimal value: {test_fn.optimal_value}")
initial_solution = test_fn.initial_solution()
vocab = list(range(test_fn.num_states))

params = [
    torch.nn.Parameter(
        initial_solution.float(),
    )
]

optimizer = DiscreteEvolution(
    params,
    vocab,
    mutation_prob=1/test_fn.dim,
    recombine_prob=1/test_fn.dim,
    num_particles=1024,
    survival_quantile=0.01
)

print(f"\nInitial solution: {params[0].data}")
print("\nOptimizing...")
for _ in range(4):
    loss = optimizer.step(lambda x: test_fn(x[0]))
    print(f"loss: {loss}")
print(f"\nFinal solution: {params[0].data}")
```

## Contributing

Contributions are welcome!

### Install dev requirements and pre-commit hooks

```bash
python -m pip install -r requirements-dev.in
pre-commit install
```

### Testing

```bash
python -m pytest -v --cov-report term-missing --cov=./holo ./tests
```

### Reproducing

The Weights & Biases dashboard for the experiments in "Closed-Form Test Functions for Biophysical Optimization Algorithms" can be found [here](https://wandb.ai/samuelstanton/holo).

### Citation

If you use HoloBench in your research, please cite the following paper:

```
@inproceedings{stanton2024closed,
  title={Closed-Form Test Functions for Biophysical Sequence Optimization Algorithms},
  author={Stanton, Samuel and Alberstein, Robert and Frey, Nathan and Watkins, Andrew and Cho, Kyunghyun},
  booktitle={1st Machine Learning for Life and Material Sciences Workshop at ICML},
  year={2024},
  url={https://arxiv.org/abs/2407.00236}
}
```
