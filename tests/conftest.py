import pytest
import os
from duneanalytics import DuneAnalytics


@pytest.fixture(scope="session")
def dune():
    print("===============Start=======================")
    yield DuneAnalytics(
        username=os.getenv("DUNE_USER"), password=os.getenv("DUNE_PASS")
    )
    print("===============End=======================")
