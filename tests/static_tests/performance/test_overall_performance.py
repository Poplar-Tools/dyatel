import cProfile
import pstats
import sys
import tracemalloc
import time

import pytest

from mops.base.element import Element
from mops.base.group import Group
from mops.base.page import Page


section_sub_elements_count = 5000


class AnotherSection1(Group):

    def __init__(self):
        super().__init__('AnotherSection')


class AnotherSection(Group):

    def __init__(self):
        super().__init__('AnotherSection')

    another_some_element = Element('AnotherSection_another_some_element')


class SomeSection(Group):

    def __init__(self, locator):
        super().__init__(locator)

    AnotherSection = AnotherSection()


class SomePage(Page):

    def __init__(self, driver_wrapper = None):
        super().__init__('SomePage', driver_wrapper=driver_wrapper)



@pytest.fixture(scope='module')
def set_elements_class_var_objects():
    for _i in range(section_sub_elements_count):
        _element = Element(f'{_i}_element')
        setattr(AnotherSection1, _element.name, _element)


@pytest.mark.parametrize('case', range(5))
def test_performance_element_initialisation(mocked_selenium_driver, case, set_elements_class_var_objects):
    tracemalloc.start()
    start_cpu = time.process_time()

    with cProfile.Profile() as pr:
        section = AnotherSection1()

    end_cpu = time.process_time()
    cpu_time = end_cpu - start_cpu  # CPU time used

    peak_mem = tracemalloc.get_traced_memory()[1] / 1024**2
    tracemalloc.stop()

    stats: pstats.Stats = pstats.Stats(pr)
    stats.strip_dirs().sort_stats("time").print_stats(20)

    print('stats.total_tt=', stats.total_tt)
    print('peak_mem=', peak_mem)
    print('cpu_time=', cpu_time)

    expected_peak_mem = 5.3
    expected_init_duration = 0.6

    if sys.version_info >= (3, 9):
        expected_peak_mem = 5.3
        expected_init_duration = 0.65
    if sys.version_info >= (3, 10):
        expected_peak_mem = 5.3
        expected_init_duration = 0.7
    if sys.version_info >= (3, 11):
        expected_peak_mem = 4.6
        expected_init_duration = 1.0
    if sys.version_info >= (3, 12):
        expected_peak_mem = 4.4
        expected_init_duration = 1.2

    assert expected_init_duration -0.5 < stats.total_tt < expected_init_duration,\
        f"Execution time too high: {stats.total_tt:.3f} sec"
    assert expected_peak_mem -1 < peak_mem < expected_peak_mem,\
        f"Peak memory usage too high: {peak_mem:.2f} MB"
    assert len(section.sub_elements) == section_sub_elements_count, \
        f"Expected {section_sub_elements_count} elements, got {len(section.sub_elements)}"
    assert cpu_time < expected_init_duration, f"CPU execution time too high: {cpu_time:.3f} sec"


@pytest.fixture(scope='module')
def set_groups_class_var_objects():
    for _i in range(20):
        _element = Element(f'AnotherSection_another_some_element_{_i}')
        setattr(AnotherSection, _element.name, _element)

    for _i in range(50):
        _element = Element(f'SomeSection_some_element_{_i}')
        setattr(SomeSection, _element.name, _element)

    for _i in range(50):
        _section = SomeSection(f'{_i}_SomeSection')
        setattr(SomePage, _section.name, _section)


@pytest.mark.parametrize('case', range(5))
def test_performance_group_initialisation(mocked_selenium_driver, case, set_groups_class_var_objects):

    tracemalloc.start()
    start_cpu = time.process_time()

    with cProfile.Profile() as pr:
        page = SomePage()

    end_cpu = time.process_time()
    cpu_time = end_cpu - start_cpu  # CPU time used

    peak_mem = tracemalloc.get_traced_memory()[1] / 1024**2
    tracemalloc.stop()

    stats: pstats.Stats = pstats.Stats(pr)
    stats.strip_dirs().sort_stats("time").print_stats(20)

    count = len(page.sub_elements)
    for page_object in page.sub_elements.values():
        count += len(page_object.sub_elements)
        for sub_element in page_object.sub_elements.values():
            count += len(sub_element.sub_elements)

    print('stats.total_tt=', stats.total_tt)
    print('peak_mem=', peak_mem)
    print('cpu_time=', cpu_time)

    expected_peak_mem = 3.9
    expected_init_duration = 0.7

    if sys.version_info >= (3, 9):
        expected_peak_mem = 3.9
        expected_init_duration = 1.0

    if sys.version_info >= (3, 10):
        expected_peak_mem = 3.9
        expected_init_duration = 1.1

    if sys.version_info >= (3, 11):
        expected_peak_mem = 3.3
        expected_init_duration = 1.45

    if sys.version_info >= (3, 12):
        expected_peak_mem = 3.1
        expected_init_duration = 1.75

    assert expected_init_duration -0.5 < stats.total_tt < expected_init_duration, \
        f"Execution time too high: {stats.total_tt:.3f} sec"
    assert expected_peak_mem -1 < peak_mem < expected_peak_mem, \
        f"Peak memory usage too high: {peak_mem:.2f} MB"
    assert cpu_time < expected_init_duration, f"CPU execution time too high: {cpu_time:.3f} sec"
    assert count > 3600, f"Expected 3600 elements, got {count}"