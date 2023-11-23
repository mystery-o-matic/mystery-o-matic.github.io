# mystery-⚙️-matic

mystery-o-matic is a Python program used to produce the content of [mystery-o-matic.com](https://mystery-o-matic.com). It produces a random [murdery mystery](https://en.wikipedia.org/wiki/Murder_mystery) to solve using [fuzzing testing](https://en.wikipedia.org/wiki/Fuzzing). Once a mystery is generated, it produces a static html file which contains all the clues (and the solution to verify it).

## Installation

Make sure all the requirements are installed. If you are using Ubuntu:

```bash
sudo apt-get install libsecp256k1-0 graphviz graphviz-dev
```

Solidity 0.8.x is needed, so we can install `solc-select` for that:

```bash
pip install solc-select
solc-select install 0.8.17
solc-select use 0.8.17
```

Finally, install the tool from this repository:

```bash
pip install .
```

mystery-o-matic requires the usage of [echidna](https://github.com/crytic/echidna/) for obtaining a random mystery prompt and its solution, but uses [a specific PR](https://github.com/crytic/echidna/pull/1075) that was not merged yet. For convenience, there is a precompiled binary provided in the `bin` folder. Otherwise, [it can be compiled from source code using `stack` or `nix`](https://github.com/crytic/echidna#building-using-stack).

## Usage

mystery-o-matic will always generate a fresh mystery to solve, but depending on the output mode (`--mode`) will produce different results:

* `html`: it will generate a local copy of mystery-o-matic.com which contains the description of the case, some clues as well as the solution.
* `text`: it will start an interactive version of murder mystery to solve by command It can also start a Telegram bot if an API key is provided.

By default it will use the `html` output to generate a new mystery in the default scenario:

```bash
mystery-o-matic scenarios/simple.template.sol static out
```

The tool will produce a static `index.html` file stored in the `out` directory.

## Scenarios

The tool provides a single scenario for creating a random murder mystery, where the rules are encoded in the `scenarios/simple.template.sol` file, but others could be added. In order to add a new scenario:

* Create a Solidity smart contract called `StoryModel`
* Encode the rules to advance every step of the story. Clues are generated using events such as `SawWhenLeaving` and `SawWhenArriving` but others can be added as well.
* Add an Echidna boolean property should be added `mystery_not_solved` (which returns false when all the steps to complete a mystery are done)
