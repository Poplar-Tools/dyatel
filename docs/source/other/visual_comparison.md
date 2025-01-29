# Visual Comparison 

## Overview

```{attention}
Supported for [allure](https://pypi.org/project/allure-pytest/) and [pytest](https://pypi.org/project/pytest/) frameworks.
- `allure` for reporting;
- `pytest` for sreenshot name definition.
```

The `VisualComparison` class is designed to facilitate visual regression testing by comparing screenshots of UI 
elements across different runs. It supports screenshot capturing, comparison, and visual difference highlighting. 
The class also handles dynamic thresholds, image comparison metrics, and can generate visual references for testing purposes.

<br>

## Interface

```{eval-rst}  
.. autoclass:: mops.visual_comparison.VisualComparison 
   :exclude-members: calculate_threshold 
   :members: assert_screenshot
   :undoc-members:
   :inherited-members:
```

<br>

## Usage

Usage
The `assert_screenshot` method of the `VisualComparison` class is utilized indirectly through the `assert_screenshot`
and `soft_assert_screenshot` methods provided by the `Group`, `Element`, and `DriverWrapper` classes. 
These methods are designed to take screenshots of elements or pages and compare them against a reference image to 
validate visual consistency across tests.

<br>

## Allure Integration
If the Allure framework is available in the project, the results of the visual comparison will be automatically 
attached to the Allure report as part of the test case. This includes:

**Actual Screenshot:**
   - The screenshot taken during the test.

**Expected Screenshot:**
   - The reference image used for comparison.

**Difference Screenshot:**
   - An image highlighting any differences found between the actual and expected screenshots.
