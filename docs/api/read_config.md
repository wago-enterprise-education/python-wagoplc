<!-- markdownlint-disable -->

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/read_config.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `read_config`
wagoplc.read_config 

Read the configuration file. 

Functions: 


- read_config: read and validate the configuration 
- validate_task: validate schema of tasks section to ensure all parameters are present. 

**Global Variables**
---------------
- **YAML_CONFIG**
- **INPUT**
- **OUTPUT**
- **LOG_FILE**

---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/read_config.py#L33"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_controller`

```python
get_controller(controller_id: str) → Controller
```

Get controller object by item number. 

controller_id: item number 


---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/read_config.py#L56"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `read_config`

```python
read_config(
    tasks_obj: Tasks | None = None
) → tuple[list[Task], dict[str, Any], Controller]
```

Read the configuration file. 

:param tasks_obj: Optional Tasks object from the application script :return: The tasks, the variable mapping and the controller object. :raise FileNotFoundError: If the configuration file does not exist. :raise exceptions.InvalidConfigError: if the configuration does not include the itemNumber field, a function block or a task entry point do not exist, or if there are duplicates in the variable mapping. 


---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/read_config.py#L173"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `validate_task`

```python
validate_task(config) → None
```

Validate task schema. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
