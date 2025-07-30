"""
CO2 emissions catalog factory
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2019 - 2025 Concordia CERC group
Project Coder Koa Wells kekoa.wells@concordia.ca
"""

from pathlib import Path
from typing import TypeVar

from hub.catalog_factories.co2_emissions.nrcan_catalog import NrcanCatalog

Catalog = TypeVar('Catalog')


class Co2EmissionsCatalogFactory:
  """
  Co2EmissionsCatalogFactory class
  """
  def __init__(self, file_type, base_path=None):
    if base_path is None:
      base_path = Path(Path(__file__).parent.parent / 'data/co2_emissions')
    self._catalog_type = '_' + file_type.lower()
    self._path = base_path
    print(self._path)

  @property
  def _nrcan_co2_catalog(self):
    """
    Retrieve NRCAN Embodied CO2 Emissions catalog
    """
    return NrcanCatalog(self._path)

  @property
  def catalog(self) -> Catalog:
    """
    Return a cost catalog
    :return: CostCatalog
    """
    return getattr(self, self._catalog_type, lambda: None)
