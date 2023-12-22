# Exotic-Surfaces

This repository contains a selection of inputs and outputs for the "Wahl_Chains" program found [here](https://github.com/jereyes4/Wahl_Chains/).

Among these results, we, Javier Reyes and Giancarlo Urzúa, picked some interesting examples to put in the (preprint) "Exotic Surfaces" ([arXiv:2211.13163](https://arxiv.org/abs/2211.13163)).

To run these examples, one must compile the "Wahl_Chains" program, place the executable at the root of this folder and run the shell scripts `TestAll.sh` in folders `Genus0` and `Genus1`. Shell scripts are meant to be run on a Unix-like system, such as Linux or macOS, though one can always run the program with all test files manually, as specified in the "Wahl_Chains" repository.

The output of the program is already included in the repository, as a `.jsonl` file in the `data` folders, and a `.tex` file in the `tables` folders. Furthermore, a compiled `.pdf` file with the tables is also provided.

## Extras

The program `MakeMeASection.py` was used in while writing the article. It is a command-line program with a graphical output, that takes indices of various `.jsonl` files and exports those examples in a compact way.

The graphical program `Display.py` found in the repository "Wahl_Chains" is used to see in detail each particular example, including how an original configuration is blown-up, resulting chains and discrepancies.

## Note

Although the "Wahl_Chains" program performs checks to determine whether examples satisfy certain criteria (in our case, nef-ness and effectiveness of the canonical divisor and obstruction), they do not work in all cases as when $p_g = 1$, and may also give false negatives. Either way, all examples in the article were checked by hand for all the required properties.