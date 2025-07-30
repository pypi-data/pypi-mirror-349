"""
.. _SKDH IO:

File Reading (:mod:`skdh.io`)
====================================

.. currentmodule:: skdh.io

Device Specific IO
------------------

These processes are designed to quickly read in data from various different
wearable devices from their default binary file format.

.. autosummary::
    :toctree: generated/

    ReadCwa
    ReadBin
    ReadApdmH5
    ReadEmpaticaAvro

General Data IO
---------------

These processes are generic and not limited to a specific device/manufacturer's format.

.. autosummary::
    :toctree: generated/

    ReadNumpyFile
    ReadCSV

Multiple File IO
----------------

Support for reading multiple files in at once

.. autosummary::
    :toctree: generated/

    MultiReader
"""

from skdh.io.axivity import ReadCwa
from skdh.io import axivity
from skdh.io.geneactiv import ReadBin
from skdh.io import geneactiv
from skdh.io.apdm import ReadApdmH5
from skdh.io import apdm
from skdh.io.numpy_compressed import ReadNumpyFile
from skdh.io import numpy_compressed
from skdh.io.csv import ReadCSV
from skdh.io import csv
from skdh.io.empatica import ReadEmpaticaAvro
from skdh.io import empatica
from skdh.io import multireader
from skdh.io.multireader import MultiReader

__all__ = (
    "ReadCwa",
    "ReadBin",
    "ReadApdmH5",
    "ReadNumpyFile",
    "ReadCSV",
    "ReadEmpaticaAvro",
    "MultiReader",
    "axivity",
    "geneactiv",
    "apdm",
    "empatica",
    "numpy_compressed",
    "csv",
    "multireader",
)
