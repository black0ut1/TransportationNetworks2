# Transportation Networks 2

A fork of [Transportation Networks](https://github.com/bstabler/TransportationNetworks) with better TNTP format:
- Easier to parse
- Numbering of nodes start with 0 (and not 1)
- Removed redundant zeros from some OD tables

---
## Format
There are four types of TNTP files in this repo:
- Network file (`.net.tntp`)
- Origin-destination matrix/table file (`.odm.tntp`)
- Edge flow file (`.flow.tntp`)
- Node file (`.node.tntp`)

`<Text>` in angle brackets in format snippets denotes
some value that is explained below the snippet.

### Network file
Describes structure of the oriented graph representing transportation network.
```
NODES:<nodes>
ZONES:<zones>
EDGES:<edges>
END
<start> <end> <capacity> <freeFlow> <length> <speed> <toll> <b> <power> <type>
<start> <end> <capacity> <freeFlow> <length> <speed> <toll> <b> <power> <type>
<start> <end> <capacity> <freeFlow> <length> <speed> <toll> <b> <power> <type>
...
```
The file starts with header:
- `<nodes>` - Number of nodes in network. The set of nodes is then represented by the
numbers 0..(nodes-1).
- `<zones>` - Number of zones in network. Zones are special nodes, they are the sources and
sinks of traffic flow in the network (see OD matrix). The set of zones is a subset of set of
nodes and is represented by number 0..(zones-1).
- `<edges>` - Number of edges in network. Also the number of lines after header.

The header ends with `END` line, after which start lines describing each edge:

- `<start>` - Node from which this edge originates.
- `<end>` - Node to which this edge points.
- `<capacity>` - Practical capacity of traffic link represented by this edge.
- `<freeFlow>` - Free flow time of traffic link represented by this edge. The time one car would
take to cross this link if the link would be otherwise empty.
- `<length>` - Irrelevant for STA algorithms.
- `<speed>` - Irrelevant for STA algorithms.
- `<toll>` - Irrelevant for STA algorithms.
- `<b>` - Parameter of BPR function. Might aswell be always 0.15.
- `<power>` - Parameter of BPR function. Might aswell be always 4.
- `<type>` - Irrelevant for STA algorithms.

### OD matrix file
Describes the origin-destination matrix/table in form of a sparse matrix. In this matrix, the
element in position `(i, j)` represents traffic flow originating in zone `i` going to
zone `j`. The matrix is thus a square matrix of rank equal to number of zones.
```
ZONES:<zones>
FLOW:<flow>
END
<i> <j>:<flow> <j>:<flow> <j>:<flow> ...
<i> <j>:<flow> <j>:<flow> <j>:<flow> ...
<i> <j>:<flow> <j>:<flow> <j>:<flow> ...
...
```
The file starts with header:
- `<zones>` - Rank of the matrix.
- `<flow>` - Total flow in the OD matrix. Sum of all its elements.

The header ends with `END` line, after which start the sparse matrix. Each line 
start with matrix row number `<i>` followed by pairs of column numbers `<j>` and
according flows `<flow>`. Pairs where flow is zero are not present.


