![logo](https://raw.githubusercontent.com/henriupton99/rtedata/main/misc/rtedata_logo.png)

<p align="center">
  <img src="https://img.shields.io/pypi/v/rtedata?color=blue" alt="PyPI version" />
  <img src="https://img.shields.io/pypi/pyversions/rtedata" alt="Python versions" />
  <img src="https://github.com/henriupton99/rtedata/actions/workflows/tests.yml/badge.svg" alt="Tests" />
  <img src="https://img.shields.io/pypi/dm/rtedata.svg?label=PyPI%20downloads" alt="Downloads per month" />
  <img src="https://img.shields.io/github/license/henriupton99/rtedata" alt="License" />
  <img src="https://img.shields.io/codecov/c/github/henriupton99/rtedata" alt="Coverage" />
</p>

Python wrapper for [RTE API](https://data.rte-france.com/) requests. 

## 1. Usage

```python
pip install rtedata
```

#### 1.1. Get RTE API credentials

You need to follow these first steps in order to setup your wrapper :  

* [create an account](https://data.rte-france.com/create_account) on the RTE platform
* [create an application](https://data.rte-france.com/group/guest/apps) associated to your account (the name and description of the app is not relevant)
* collect your app IDs (**ID Client** and **ID Secret**) available in your application dashboard
* **subscribe** to the relevant APIs regarding the "*data_type*" you request (please refer to the table in the last section to get the associated links)

#### 1.2. Generate a data retrieval

To retrieve data using the wrapper, follow this pipeline :

```python
from rtedata import Client
client = Client(client_id="XXX", client_secret="XXX")
dfs = client.retrieve_data(start_date="2024-01-01 00:00:00", end_date="2024-01-02 23:59:00", data_type="actual_generations_per_unit", output_dir="./output")
```

where :
* **start_date** is the first date of the data retrieval (format *YYYY-MM-DD HH:MM:SS*)
* **end_date** is the last date of the data retrieval (format *YYYY-MM-DD HH:MM:SS*)
* **data_type** is the desired data to collect (a keyword list is given in the next section). It can be a single keyword *"XXX"* or a list of keyword separated by a comma *"XXX,YYY,ZZZ"*
* **output_dir** (*optionnal*): the output directory to store the results

The generic output format is a pandas dataframe / **.csv** file containing the data for all dates between **start_date** and **end_date**. It will generate one file per desired **data_type** and will store all of them in a **./results** folder with the generic name *"<data_type>_<start_date>_<end_date>.csv"*.

## 2. Available *data_type* options

It is possible to see the full options catalog using the client attribute **catalog** :

```python
from rtedata import Client
client = Client(client_id="XXX", client_secret="XXX")
client.catalog
```

The following table is an exhaustive list of all possible (currently handled) options for the **data_type** argument for the retrieval, and the description of the associated data :

| *data_type* | Catalog URL | Documentation URL | Category |
|-------------------|-----|-----|-----|
| `actual_generations_per_production_type` | *[Link](https://data.rte-france.com/catalog/-/api/generation/Actual-Generation/v1.1)* | *[Link](https://data.rte-france.com/catalog/-/api/doc/user-guide/Actual+Generation/1.1)*| generation |
| `actual_generations_per_unit` | *[Link](https://data.rte-france.com/catalog/-/api/generation/Actual-Generation/v1.1)* | *[Link](https://data.rte-france.com/catalog/-/api/doc/user-guide/Actual+Generation/1.1)*| generation |
| `capacities_cpc` | *[Link](https://data.rte-france.com/catalog/-/api/generation/Generation-Installed-Capacities/v1.1)* | *[Link](https://data.rte-france.com/catalog/-/api/doc/user-guide/Generation+Installed+Capacities/1.1)*| generation |
| `capacities_per_production_type` | *[Link](https://data.rte-france.com/catalog/-/api/generation/Generation-Installed-Capacities/v1.1)* | *[Link](https://data.rte-france.com/catalog/-/api/doc/user-guide/Generation+Installed+Capacities/1.1)*| generation |
| `capacities_per_production_unit` | *[Link](https://data.rte-france.com/catalog/-/api/generation/Generation-Installed-Capacities/v1.1)* | *[Link](https://data.rte-france.com/catalog/-/api/doc/user-guide/Generation+Installed+Capacities/1.1)*| generation |
| `other_market_information` | *[Link](https://data.rte-france.com/catalog/-/api/generation/Unavailability-Additional-Information/v6.0)* | *[Link](https://data.rte-france.com/catalog/-/api/doc/user-guide/Unavailability+Additional+Information/6.0)*| generation |
| `transmission_network_unavailabilities` | *[Link](https://data.rte-france.com/catalog/-/api/generation/Unavailability-Additional-Information/v6.0)* | *[Link](https://data.rte-france.com/catalog/-/api/doc/user-guide/Unavailability+Additional+Information/6.0)*| generation |
| `generation_unavailabilities_versions` | *[Link](https://data.rte-france.com/catalog/-/api/generation/Unavailability-Additional-Information/v6.0)* | *[Link](https://data.rte-france.com/catalog/-/api/doc/user-guide/Unavailability+Additional+Information/6.0)*| generation |
| `transmission_network_unavailabilities_versions` | *[Link](https://data.rte-france.com/catalog/-/api/generation/Unavailability-Additional-Information/v6.0)* | *[Link](https://data.rte-france.com/catalog/-/api/doc/user-guide/Unavailability+Additional+Information/6.0)*| generation |
| `generation_unavailabilities` | *[Link](https://data.rte-france.com/catalog/-/api/generation/Unavailability-Additional-Information/v6.0)* | *[Link](https://data.rte-france.com/catalog/-/api/doc/user-guide/Unavailability+Additional+Information/6.0)*| generation |
| `other_market_information_versions` | *[Link](https://data.rte-france.com/catalog/-/api/generation/Unavailability-Additional-Information/v6.0)* | *[Link](https://data.rte-france.com/catalog/-/api/doc/user-guide/Unavailability+Additional+Information/6.0)*| generation |
| `volumes_per_energy_type` | *[Link](https://data.rte-france.com/catalog/-/api/market/Balancing-Energy/v4.0)* | *[Link](https://data.rte-france.com/catalog/-/api/doc/user-guide/Balancing+Energy/4.0)*| market |
| `prices` | *[Link](https://data.rte-france.com/catalog/-/api/market/Balancing-Energy/v4.0)* | *[Link](https://data.rte-france.com/catalog/-/api/doc/user-guide/Balancing+Energy/4.0)*| market |
| `imbalance_data` | *[Link](https://data.rte-france.com/catalog/-/api/market/Balancing-Energy/v4.0)* | *[Link](https://data.rte-france.com/catalog/-/api/doc/user-guide/Balancing+Energy/4.0)*| market |
| `standard_rr_data` | *[Link](https://data.rte-france.com/catalog/-/api/market/Balancing-Energy/v4.0)* | *[Link](https://data.rte-france.com/catalog/-/api/doc/user-guide/Balancing+Energy/4.0)*| market |
| `lead_times` | *[Link](https://data.rte-france.com/catalog/-/api/market/Balancing-Energy/v4.0)* | *[Link](https://data.rte-france.com/catalog/-/api/doc/user-guide/Balancing+Energy/4.0)*| market |
| `afrr_marginal_price` | *[Link](https://data.rte-france.com/catalog/-/api/market/Balancing-Energy/v4.0)* | *[Link](https://data.rte-france.com/catalog/-/api/doc/user-guide/Balancing+Energy/4.0)*| market |
| `volumes_per_entity_price` | *[Link](https://data.rte-france.com/catalog/-/api/market/Balancing-Energy/v4.0)* | *[Link](https://data.rte-france.com/catalog/-/api/doc/user-guide/Balancing+Energy/4.0)*| market |
| `tso_offers` | *[Link](https://data.rte-france.com/catalog/-/api/market/Balancing-Energy/v4.0)* | *[Link](https://data.rte-france.com/catalog/-/api/doc/user-guide/Balancing+Energy/4.0)*| market |
| `standard_afrr_data` | *[Link](https://data.rte-france.com/catalog/-/api/market/Balancing-Energy/v4.0)* | *[Link](https://data.rte-france.com/catalog/-/api/doc/user-guide/Balancing+Energy/4.0)*| market |
| `volumes_per_reasons` | *[Link](https://data.rte-france.com/catalog/-/api/market/Balancing-Energy/v4.0)* | *[Link](https://data.rte-france.com/catalog/-/api/doc/user-guide/Balancing+Energy/4.0)*| market |'
