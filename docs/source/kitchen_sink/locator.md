# Locator dataclass

## Overview

The `Locator` class is designed to provide a flexible mechanism for managing locators in a unified way.
This class supports different locator types for various platforms and devices, including `desktop`, `mobile`, and `tablet` environments. 
The `Locator` class is particularly useful in automation frameworks where locators need to be adapted based on the specific driver 
and capabilities being used.

This object and its usage aim to reduce the redundancy of creating multiple attributes for different platforms. 
By centralizing locators in a single `Locator` object, it simplifies the codebase and enhances maintainability.

<br>

## Interface

```{eval-rst}  
.. autoclass:: mops.mixins.objects.locator.Locator
   :undoc-members:
   :inherited-members:
```

<br>

## Usage

The `Locator` class is designed to be flexible and adaptive, making it suitable for various automation scenarios. 
Here’s how the attributes work together:

- **`loc_type`** is optional. If not specified, the system will attempt to automatically select the appropriate locator type based on the provided locator.
- **`default`** will be used if no specific locator is provided for the current platform or device.

<br>

### Example

```python
# Providing string parameter instead of Locator object
button = Element('.button', name='button')

search_button = Element(Locator(desktop='.search', mobile='.mobile.search'), name='search button')
```
