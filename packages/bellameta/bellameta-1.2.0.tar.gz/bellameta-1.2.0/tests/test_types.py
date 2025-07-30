import os

from bellameta.types import Cohort, Task

def test_cohort():
    assert Cohort.list() == ['Example']

def test_task():
    assert Task.list() == ['Subtyping']


