# Boolean Network GUI Tool

This tool is a python solver that uses NuXmv in order to solve boolean networks and experiments on them.

## Requirements

- Python ver. 3.x
### Required Python libraries
fonttools
matplotlib
networkx
numpy
pandas
pillow

- `NuXmv` (download separately)

## Setup
After downloading NuXmv run ~Main.py and specify the directory of the NuXmv tool. 

## Creating Boolean networks
## 1. Component Section
Defines network nodes and their values.
- **Syntax**: `<name> <range>` (`A 0-17`, `B 1,3,5`)

**Example**:
```
component {
    A 0-17
    B 0-17
    F 0,1,3
    res 0
}
```

## 2. Interaction Section
Defines how components influence each other.
- **Syntax**: `<source> <target> <type> <strength> <optional>`
- **Fields**:
  - `<type>`: `positive` or `negative`
  - `<strength>`: `weak1`, `weak2`, or `strong`
  - `<optional>`: `True` (optional) or `False` (definite)

**Example**:
```
interaction {
    A A positive weak1 False
    A res positive weak1 True
}
```

## 3. Condition Section
- **Syntax**: `<component_states> <expression_label>`

**Example**:
```
condition {
    A=0 and B=0 and F=1 and res=0 expression3
}
```

## 4. Experiment Section
- **Syntax**: `<start_time> <expression_label> <end_time> <expression_label>`

**Example**:
```
experiment {
    0 expression3 10 expression4
}
```

## 5. End Marker
`end` marks the end.


