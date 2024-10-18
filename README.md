# mystery-⚙️-matic

mystery-o-matic is a Python program used to produce the content of [mystery-o-matic.com](https://mystery-o-matic.com). It produces a random [murder mystery](https://en.wikipedia.org/wiki/Murder_mystery) to solve using [fuzzing testing](https://en.wikipedia.org/wiki/Fuzzing). Once a mystery is generated, it produces a static html file that contains all the clues (and the solution to verify it).

mystery-o-matic supports the following languages:

* [English](https://mystery-o-matic.com/en)
* [Spanish](https://mystery-o-matic.com/es)

## Installation

Make sure all the requirements are met. If you are using Ubuntu:

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

mystery-o-matic requires the usage of [echidna](https://github.com/crytic/echidna/) for obtaining a random mystery prompt and its solution but uses [a specific PR](https://github.com/crytic/echidna/pull/1075) that has not been merged yet. For convenience, there is a precompiled binary provided in the `bin` folder. Otherwise, [it can be compiled from source code using `stack` or `nix`](https://github.com/crytic/echidna#building-using-stack).

## Usage

mystery-o-matic will always generate a fresh mystery to solve, but depending on the output mode (`--mode`) will produce different results:

* `html`: it will generate a local copy of mystery-o-matic.com which contains the description of the case, some clues and the solution.
* `text`: it will start an interactive version of a murder mystery to solve by specific commands. It can also start a Telegram bot if an API key is provided.

By default, it will use the `html` output to generate a new mystery in the default scenario:

```bash
mystery-o-matic scenarios/simple.template.sol static out
```

The tool will produce a static `index.html` file stored in the `out` directory.

## Integrations

While the code is open-source, I'm aware of the difficulties of using or integrating other people's code. If you don't know or don't want to run this code directly, but you are still interested in using the output of this tool in your work of fiction (e.g. novel, game, film), please feel free to [contact me](https://forms.gle/dvA4Wr8LiuHFmDZN7) so I can do that for you. The generated mystery will look like this:

```
Characters:
  * CHAR1 is bob
  * CHAR2 is carol
  * CHAR3 is eddie

Final Locations:
  * ROOM3 is kitchen
  * ROOM2 is dining room
  * ROOM0 is bedroom
  * ROOM1 is bathroom

Solution:
 Initial Locations:
  * CHAR1 was in the ROOM1
  * CHAR2 was in the ROOM2
  * CHAR3 was in the ROOM3

Actions:
1. takesWeapon($CHAR3)
2. move($CHAR3, $ROOM0)
3. move($CHAR2, $ROOM1)
4. move($CHAR1, $ROOM0)
5. kills($CHAR3, $CHAR1)
6. move($CHAR3, $ROOM1)
```

## Scenarios

The mystery generation involves using a Solidity smart contract. This was used because of the nature of blockchain transactions as operations, but everything is simulated so no cryptocurrency is involved. Instead, every transaction represents a possible state change in the murder mystery (e.g. Alice walks from the kitchen to the bathroom). If the state change breaks any rule (e.g. no more than two characters can be in the same room), then the transaction reverts and the fuzzing tool keeps exploring.

The tool provides a single scenario for creating a random murder mystery, where the rules are encoded in the `scenarios/simple.template.sol` file, but others could be added. To add a new scenario:

* Create a Solidity smart contract called `StoryModel`
* Encode the rules to advance every step of the story. Clues are generated using events such as `SawWhenLeaving` and `SawWhenArriving` but others can be added as well.
* Add an Echidna boolean property should be added `mystery_not_solved` (which returns false when all the steps to complete a mystery are done)

## Donations

If you want to support the development, you can donate using crypto to 0xd0FD96CD73762Fd081cf2269D79F359e4314629b (ETH, BSC, etc)
