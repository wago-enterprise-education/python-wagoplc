# Roadmap

This is the roadmap of the `python-wagoplc` library. 

- Publish wagoplc 0.1
- Build and publish first version of `wagoplc` Docker image
- Support for newer CC100 versions (9401, 9403, 9402)
- Extensive testing
- Event-based and periodic tasks
- Support for serial interface
- Support for bus systems (CAN, DALI)

## Notes on CC100 versions awaiting support

### 751-9401

* Awaiting firmware update re-adding system files for analog inputs
* CAN Bus support

### 751-9403

* DALI support

### 751-9402

* Multi-I/O handling
* Set configuration and outputs via WDx

### 751-9412

* Yocto-based -> config-tools removed; control OMS via WDx