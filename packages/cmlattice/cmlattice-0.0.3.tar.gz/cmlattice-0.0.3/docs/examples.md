

For more in-depth examples on using cml for your projects check out the notebooks folder of our git [repo](https://github.com/mskmay66/cml/tree/main/notebooks). But below is a simple example of using a `RulkovLattice` in python and bash.

## Python

```python
# initialize the lattice object
lattice = RulkovLattice(n=10, r=4, mu=0, sigma=1)

# run a hundred step simulation
STEPS = 100
sim_gen = lattice.simulate(STEPS)

# unpack the generator
sim = list(sim_gen)

# finally, vizualize your simulation
viz = Visualization(lattice)
v = viz.animate()
```

## bash

```bash
cml simulate -k rulkov -n 10 -r 4 -e 1 -m 0 -s 1 -t 100
```

The Result:

![A blinking rulkov](assets/blinking_rulkov.gif)
