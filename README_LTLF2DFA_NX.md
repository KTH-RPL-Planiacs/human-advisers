# LTLf2DFA_NX

Translates LTLf formulae into deterministic finite automata as a networkx DiGraph.

## LTLf Syntax

Propositonal Symbols:

- true, false
- any lowercase string

Boolean Operators:

- !     (negation)
- ->    (implication)
- <->   (equivalence)
- &&    (and)
- ||    (or)

Temporal Operators (uppercase):

- G     (always)
- F     (eventually)
- U     (until)
- V     (release)
- X     (next)
- WX    (weak next)

## Additional Setup

Install MONA. On ubuntu, simply:

```shell
sudo apt install mona
```

## Usage

```python
from ltlf2dfa_nx.parse_ltlf import to_mona
from ltlf2dfa_nx.mona2nx import to_nxgraph

mona = to_mona("G a && F b")
ba = to_nxgraph(mona)
```
