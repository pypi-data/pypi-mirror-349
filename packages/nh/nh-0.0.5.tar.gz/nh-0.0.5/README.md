# nh
framework for data flow

To install:	```pip install nh```

## Overview
The `nh` package provides a robust framework designed to facilitate the management and pipelining of data processes in Python applications. At its core, the package includes the `DataFlow` class, which allows for the definition, dependency management, and execution of data retrieval and storage operations in a structured manner.

## Features
- **Data Dependency Management**: Automatically handles the dependencies between different pieces of data within the application.
- **Dynamic Data Handling**: Supports dynamic creation of data handlers if specific data-making functions are not provided.
- **Verbose Progress Reporting**: Includes capabilities to report on the progress of data operations, which can be adjusted by setting the verbosity level.

## Key Components
### `DataFlow` Class
The `DataFlow` class is central to the `nh` framework, enabling the pipelining and management of data processes. It allows developers to define how data should be fetched, processed, and stored.

#### Constructor
The constructor accepts any number of keyword arguments to set initial properties. It sets up data dependencies, makers, and storers, and initializes the data flow process.

#### Methods
- **`mk_data_flow()`**: Sets up the data flow based on dependencies and available data makers.
- **`put_in_store(name, data)`**: Stores data in a predefined storage system.
- **`put_in_attr(name, data)`**: Stores data as an attribute of the `DataFlow` instance.
- **`put_in_data_dict(name, data)`**: Stores data in a dictionary attribute `data_dict` of the `DataFlow` instance.
- **`get_data(data_name, **kwargs)`**: Retrieves data based on the name and optional parameters. Handles dependencies and uses data makers if necessary.
- **`get_data_lite_and_broad(data_name, **kwargs)`**: A variant of `get_data` that is optimized for broader and lighter data fetching scenarios.
- **`print_progress(min_level, msg='', verbose_level=None)`**: Utility method for printing progress messages based on the verbosity level.

## Usage Examples

### Setting Up a Data Flow
```python
from nh import DataFlow

class MyDataFlow(DataFlow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_dependencies = {
            'summary_data': ['raw_data']
        }
        self.data_makers = {
            'raw_data': self.fetch_raw_data
        }

    def fetch_raw_data(self):
        # Implement fetching raw data
        return "Raw data"

    def process_data(self, raw_data):
        # Implement data processing
        return f"Processed {raw_data}"

# Create instance of MyDataFlow
data_flow = MyDataFlow(verbose_level=2)

# Fetch and process data
processed_data = data_flow.get_data('summary_data')
print(processed_data)
```

### Storing and Retrieving Data
```python
# Assuming `data_flow` is an instance of MyDataFlow
data_flow.put_in_attr('processed_data', processed_data)
retrieved_data = data_flow.get_data('processed_data')
print(retrieved_data)
```

This enhanced documentation provides a clearer understanding of the functionalities provided by the `nh` package, along with examples to help users integrate it into their projects effectively.