# mystery-⚙️-matic

mystery-o-matic is a Python program used to produce the content of [mystery-o-matic.com](https://mystery-o-matic.com). It produces a random [murdery mystery](https://en.wikipedia.org/wiki/Murder_mystery) to solve using [fuzzing testing](https://en.wikipedia.org/wiki/Fuzzing). Once a mystery is generated, it produces a static html file which contains all the clues (and the solution to verify it).

## Installation

Make sure all the requirements are installed. If you are using Ubuntu:

```
$ sudo apt-get install libsecp256k1-0 graphviz
```

Solidity 0.8.x is needed, so we can install `solc-select` for that:

```
pip install solc-select
solc-select install 0.8.17
solc-select use 0.8.17
```

Finally, install the tool from this repository:

```
$ pip install .
```

## Usage

To generate a new mystery in the default scenario:

```
$ MysteryOMatic scenarios/simple.template.sol static out
```

The tool will produce a static `index.html` file stored in the `out` directory which contains the description of the case, some clues as well as the solution.

## Scenarios

The tool provides a single scenario for creating a random murder mystery, where the rules are encoded in the `scenarios/simple.template.sol` file, but others could be added. In order to add a new scenario:

* Create a Solidity smart contract called `StoryModel`
* Encode the rules to advance every step of the story. Clues are generated using events such as `SawWhenLeaving` and `SawWhenArriving` but others can be added as well.
* Add an Echidna boolean property should be added `mystery_not_solved` (which returns false when all the steps to complete a mystery are done)