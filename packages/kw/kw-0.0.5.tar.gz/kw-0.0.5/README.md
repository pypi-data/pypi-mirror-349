# kw
Utils to work with storage

To install:	```pip install kw```

## Overview

The `kw` package provides a comprehensive set of utilities designed to facilitate the manipulation, storage, and retrieval of data, particularly using HDF5 storage format with Pandas. It includes functionality for serializing and deserializing objects, handling large datasets efficiently, and performing complex data operations within stores. The package is particularly useful for scenarios involving large-scale data analysis and storage optimization in Python.

## Features

- **Serialization and Compression**: Functions for serializing objects with optional compression using gzip, allowing efficient storage of large Python objects.
- **Data Store Manipulation**: Extensive support for manipulating HDF5 stores, including querying, appending, replacing, and managing data in a structured format.
- **Data Retrieval and Transformation**: Utilities to fetch and transform data based on specific conditions and criteria.
- **Store Information Retrieval**: Functions to extract detailed metadata and structure information from data stores.

## Installation

To install the package, run the following command:

```bash
pip install kw
```

## Usage Examples

### Serializing Objects

#### Saving an Object with Compression

```python
from kw import gz_pickle_dump

my_object = {'key': 'value'}
filename = 'data.pkl.gz'
gz_pickle_dump(my_object, filename)
```

#### Loading a Compressed Object

```python
from kw import gz_pickle_load

loaded_object = gz_pickle_load('data.pkl.gz')
```

### Working with HDFStores

#### Creating a Custom Store Class

```python
from kw import MyStore

store = MyStore('my_data.h5')
```

#### Adding Data to the Store

```python
import pandas as pd

df = pd.DataFrame({'A': [1, 2, 3]})
store.put('my_key', df)
```

#### Retrieving Data from the Store

```python
retrieved_data = store.select('my_key')
```

### Advanced Data Manipulation

#### Copying Data Between Stores

```python
from kw import copy_data

copy_data('source_store.h5', 'target_store.h5', ['dataset1', 'dataset2'], overwrite=True)
```

#### Filtering and Selecting Data

```python
from kw import StoreSelector

selector = StoreSelector('my_store.h5', 'my_key', 'A')
selected_data = selector.get_table(selection='value1')
```

## Documentation

Each function and class in the `kw` package is documented with docstrings, providing a detailed description of its purpose, parameters, and usage examples. This documentation can be accessed through standard Python help functions, such as `help()` or by reading the source code directly.

## Contributing

Contributions to the package are welcome. Please ensure that any pull requests or issues are submitted through the package's GitHub repository.

## License

The `kw` package is open-sourced under the MIT license, which allows for liberal reuse and modification.