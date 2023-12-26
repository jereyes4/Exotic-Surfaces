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

## List of examples used in the article

### Genus $0$: Exotic $\mathbb{CP}^2\char"0023 4\overline{\mathbb{CP}^2}$

In order of appearance in the paper, we extracted the following examples:

1. $K^2 = 5$ with two chains $(3,1)$ and $(700,257)$. From `4422_v1.jsonl`, index `14074`.
2. $K^2 = 5$ with two chains $(700,257)$ and $(493,181)$. From `4422_v1.jsonl`, index `14075`.
3. $K^2 = 5$ with two chains $(700,257)$ and $(700,257)$. From `4422_v1.jsonl`, index `14076`.
4. $K^2 = 5$ with two chains $(256,75)$ and $(17,5)$. From `4422_v1.jsonl`, index `14073`.
5. $K^2 = 5$ with two chains $(82,25)$ and $(59,18)$. From `4422_v1.jsonl`, index `14068`.
6. $K^2 = 5$ with two chains $(89,34)$ and $(26,11)$. From `4422_v1.jsonl`, index `14069`.
7. $K^2 = 5$ with two chains $(89,34)$ and $(37,11)$. From `4422_v1.jsonl`, index `14070`.
8. $K^2 = 5$ with two chains $(111,31)$ and $(26,11)$. From `4422_v1.jsonl`, index `14071`.

### Genus $1$: Exotic $3\mathbb{CP}^2\char"0023 9\overline{\mathbb{CP}^2}$

9. $K^2 = 10$ with two chains $(19843,5873)$ and $(571,169)$. From `K3_2I82I1I2I4.jsonl`, index `3`.
10. $K^2 = 10$ with two chains $(513,212)$ and $(121,50)$. From `K3_2I82I1I2I4.jsonl`, index `1`.
11. $K^2 = 10$ with two chains $(139,41)$ and $(19309,5695)$. From `K3_2I82I1I2I4.jsonl`, index `2`.

### Genus $1$: Exotic $3\mathbb{CP}^2\char"0023 8\overline{\mathbb{CP}^2}$

12. $K^2 = 11$ with two chains $(58441,21457)$ and $(42249,15512)$. From `K3_2I82I1I2I4.jsonl`, index `4`.
13. $K^2 = 11$ with two chains $(88889,33952)$ and $(51584,19703)$. From `K3_2I82I1I2I4.jsonl`, index `5`.

### Genus $1$: Exotic $3\mathbb{CP}^2\char"0023 7\overline{\mathbb{CP}^2}$

14. $K^2 = 11$ with two chains $(2687,795)$ and $(436,129)$. From `K3_2I82I1I2I4.jsonl`, index `6`.
15. $K^2 = 11$ with two chains $(263303,77905)$ and $(436,129)$. From `K3_2I82I1I2I4.jsonl`, index `9`.
16. $K^2 = 11$ with two chains $(266348,78757)$ and $(487,144)$. From `K3_2I82I1I2I4.jsonl`, index `10`.
17. $K^2 = 11$ with two chains $(4,1)$ and $(267721,78962)$. From `K3_2I82I1I2I4.jsonl`, index `11`.
