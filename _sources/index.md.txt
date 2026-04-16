# Python WAGO PLC Library Documentation

The `python-wagoplc` library was designed to enable programmers to build PLC applications with ease,
and is currently usable for rather simple, standard automation tasks. It is open-source, Python-based and without the
overhead of a complex graphical interface like the *Controller Development System* (CoDeSys). Given the lower entry hurdle, it could be used for educational purposes and hobby projects.

As of this writing (March 2026), it supports the older WAGO CC100 generation (since 751-9301). Advanced functionality like bus systems or communication protocols are at the time not supported, but all onboard I/O elements can be accessed programmatically. It is planned to support both the newer CC100 generation and the PFC controllers (750 series) in the future. While the former have a static set of features on board, and are therefore suited for smaller projects, the latter can be fully customized with a large set of more than 500 modules.

`python-wagoplc` is intended to be used together with the [VS Code Extension WAGO CC100](https://marketplace.visualstudio.com/items?itemName=WAGO-education.vscode-wago-cc100), which provides a graphical interface for communicating with the controller as well as a Docker-based runtime environment.

```{toctree}
:maxdepth: 2
user-guide.md
development.md
reference.md
```