# Discussion of the implementation proposals

## #1: Arduino-style

### Pros

* simple, well-structured code
* intuitive for Arduino users

### Cons

* awkward for PLC programmers
* no descriptive names for I/O interfaces
* does not correspond with structure of cyclic program
* autocompletion not possible

## #2: Variables

### Pros

* clearly structured
* descriptive names
* interface-variable mapping and program code in one file
* ST-like, but with Python syntax

### Cons

* much boilerplate code
* task variables need to be added as parameters
* not applicable for larger systems (e.g. PFC200)

## #3: Variables with mapping in config file

### Pros

* can be auto-generated (good for larger projects)
* overhead can be avoided by defining tasks and other settings in config file
* overview of all possible interfaces
* portable configuration, can be used by extension

### Cons

* extra file and dependency
* function signatures still need to be amended manually
* increasingly hard to grasp

# Design decision

Implement support for design #2 and basic support for design #3 (to be extended in the future).
Variables defined directly in the Python script should take precedence over variables in the
configuration file.