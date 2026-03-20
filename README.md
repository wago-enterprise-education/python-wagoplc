# Python WAGO PLC Library

This library provides a simple interface to interact with WAGO PLCs using Python. It allows you to read and write data to the PLC, making it easier to integrate WAGO PLCs into your Python applications. The libraries main focus for now is to support multiple controllers with the [VS Code Extension WAGO CC100](https://marketplace.visualstudio.com/items?itemName=WAGO-education.vscode-wago-cc100). At the point the supported controllers are only the Wago Compact Controller 751-9301,751-9401 and 751-9403
without support for the serial interfaces and DALI.

> [!CAUTION]
> **This repository is a development repository that was created as part of a student project and is not regularly maintained. It is neither a stable version nor an official repository of WAGO GmbH & Co. KG.**

## Development setup

This module uses [uv](https://uv.pypa.io/en/stable/) as the build system. To set up the development environment, follow these steps:

```bash
uv sync
```

The Library intergrates the all the basic function block from Codesys seamlessly into Python-.
The functionblocks include 
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

```python 

def porta_westfalica(
        oTorsteuerung_FB: Torsteuerung, xEndlageS1: bool,
        xEndlageS2: bool, xS1: bool, xS2: bool):
    oTorsteuerung_FB(xS1, xS2, xEndlageS1, xEndlageS2)
    print(oTorsteuerung_FB.tor_auf, oTorsteuerung_FB.tor_zu)

    return dict(oTorsteuerung_FB=oTorsteuerung_FB)
```
