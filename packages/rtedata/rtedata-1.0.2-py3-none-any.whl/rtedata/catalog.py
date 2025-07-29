from dataclasses import dataclass, field
from typing import Dict

@dataclass
class Catalog:
    _structure: Dict[str, list[str]] = field(init=False, repr=False)

    def __post_init__(self):
      self.request_base_url = "https://digital.iservices.rte-france.com/open_api"
      self.docs_base_url = "https://data.rte-france.com/catalog/-/api/doc/user-guide"
      self.catalog_base_url = "https://data.rte-france.com/catalog/-/api"
      
      self._meta_mapping = {
        f"{self.request_base_url}/actual_generation/v1/" : {
            "keys": ["actual_generations_per_production_type", "actual_generations_per_unit"],
            "docs_url": f"{self.docs_base_url}/Actual+Generation/1.1",
            "catalog_url": f"{self.catalog_base_url}/generation/Actual-Generation/v1.1",
            "category": "generation"
        },
        f"{self.request_base_url}/generation_installed_capacities/v1/" : {
            "keys": ["capacities_cpc", "capacities_per_production_type", "capacities_per_production_unit"],
            "docs_url": f"{self.docs_base_url}/Generation+Installed+Capacities/1.1",
            "catalog_url": f"{self.catalog_base_url}/generation/Generation-Installed-Capacities/v1.1",
            "category": "generation"
        },
        f"{self.request_base_url}/unavailability_additional_information/v6/" : {
            "keys": ["other_market_information", "transmission_network_unavailabilities", "generation_unavailabilities_versions", "transmission_network_unavailabilities_versions", "generation_unavailabilities", "other_market_information_versions"],
            "docs_url": f"{self.docs_base_url}/Unavailability+Additional+Information/6.0",
            "catalog_url": f"{self.catalog_base_url}/generation/Unavailability-Additional-Information/v6.0",
            "category": "generation"
        },
        f"{self.request_base_url}/balancing_energy/v4/" : {
            "keys": ["volumes_per_energy_type", "prices", "imbalance_data", "standard_rr_data", "lead_times", "afrr_marginal_price", "volumes_per_entity_price", "tso_offers", "standard_afrr_data", "volumes_per_reasons"],
            "docs_url": f"{self.docs_base_url}/Balancing+Energy/4.0",
            "catalog_url": f"{self.catalog_base_url}/market/Balancing-Energy/v4.0",
            "category": "market"
            }
        }
      
      self._requests = {
            key: {
                "request_url": f"{base_url}{key}",
                "catalog_url": info["catalog_url"],
                "docs_url": info["docs_url"],
                "category": info["category"]
            }
            for base_url, info in self._meta_mapping.items()
            for key in info["keys"]
        }

    @property
    def keys(self) -> str:
        return list(self._requests.keys())
    
    def get_key_content(self, key: str) -> tuple[str]:
        key_content = self._requests.get(key, None)
        if key_content is None:
            raise KeyError(f"Request key '{key}' not in requests catalog")
        request_url = key_content.get("request_url")
        catalog_url = key_content.get("catalog_url")
        docs_url = key_content.get("docs_url", None)
        category = key_content.get("category")
        return request_url, catalog_url, docs_url, category
      
    def to_markdown(self) -> str:
        md = []
        md.append("| *data_type* | Catalog URL | Documentation URL | Category |")
        md.append("|-------------------|-----|-----|-----|")
        for key in self._requests:
            request_url, catalog_url, docs_url, category = self.get_key_content(key)
            docs_url = docs_url if docs_url is not None else "X"
            md.append(f"| `{key}` | *[Link]({catalog_url})* | *[Link]({docs_url})*| {category} |")
        return "".join(md)

    def __repr__(self):
        _repr = "rtedata Catalog : \n"
        for i, key in enumerate(self._requests):
            request_url, catalog_url, docs_url, category = self.get_key_content(key)
            _repr += f"{i} - {key} : \n"
            _repr += f"~> catalog url : {catalog_url} \n"
            if docs_url is not None:
                _repr += f"~> docs url : {docs_url} \n"
        return _repr
        
