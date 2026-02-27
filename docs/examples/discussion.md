# Discussion of the implementation proposals

## Arduino-style

### Pros

* simple, well-structured code
* intuitive for Arduino users

### Cons

* awkward for PLC programmers
* no descriptive names for I/O interfaces
* does not correspond with structure of cyclic program
* autocompletion not possible

## Variables

### Pros

* clearly structured
* descriptive names
* interface-variable mapping and program code in one file
* ST-like, but with Python syntax

### Cons

* much boilerplate code
* task variables need to be added as parameters
* not applicable for larger systems (e.g. PFC200)

## Variables with mapping in config file

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

To be done.
