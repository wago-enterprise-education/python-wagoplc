<!-- markdownlint-disable -->

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/fb.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `fb`
Standard library. This module holds function blocks defined by the PLC programming norm DIN EN 61131-3. They can be imported and used in a PLC program. 


- CTU: up-counter 
- CTD: down-counter 
- CTUD: up- and down-counter 
- TP: impulse giver 
- TON: switch-on-timer 
- TOF: switch-off-timer 
- RS: RS latch 
- SR: SR latch 
- R_TRIG: trigger on rising flank 
- F_TRIG: trigger on falling flank 



---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/fb.py#L28"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `FB`
Generic superclass for a function block. 

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/fb.py#L31"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__()
```

Configure any initial settings. 





---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/fb.py#L40"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `CTU`
An up-counter function block. 

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/fb.py#L43"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(pv: int = 0)
```

pv: when this limit is reached by cv, q is set to True (default 0) 





---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/fb.py#L72"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `CTD`
A down-counter function block. 

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/fb.py#L75"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(pv: int = 0)
```

pv: if a rising edge is registered for ld, cv is set to this value (default 0) 





---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/fb.py#L103"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `CTUD`
An up- and down-counter function block. 

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/fb.py#L106"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(pv: int = 0)
```

pv: when this limit is reached by cv, q is set to True 





---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/fb.py#L151"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `TP`
Create an impulse. 

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/fb.py#L154"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(pt: float = 0.0)
```

pt: the impulse time 





---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/fb.py#L190"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `TON`
Create a delay in switching on. 

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/fb.py#L193"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(pt: float = 0.0)
```

pt: the delay time 





---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/fb.py#L226"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `TOF`
Create a delay in switching off. 

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/fb.py#L229"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(pt: float = 0.0)
```

pt: the delay time 





---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/fb.py#L263"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `RS`
A RS latch (reset dominance). 

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/fb.py#L266"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__()
```









---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/fb.py#L286"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `SR`
A SR latch (set dominance). 

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/fb.py#L289"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__()
```









---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/fb.py#L305"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `R_TRIG`
Trigger on a rising flank. 

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/fb.py#L308"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__()
```









---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/fb.py#L323"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `F_TRIG`
Trigger on a falling flank. 

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/fb.py#L326"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__()
```











---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
