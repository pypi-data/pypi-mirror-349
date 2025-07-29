# Scientific Microservices Python Wrapper

This Python module provides a simple interface to the APIs offered by [Scientific Microservices](https://scientificmicroservices.com/how-it-works). These APIs deliver lightweight, cloud-hosted scientific models designed for rapid data analysis and preprocessing.

## Features

- **Simple Interface** – Invoke scientific models with minimal code.
- **Fast Responses** – Get results in milliseconds.
- **Chainable APIs** – Combine multiple APIs for advanced workflows.
- **Stateless Operations** – Each call is independent.
- **Secure Communication** – All data is transmitted over secure protocols.

## Installation

Install the package using pip:

```bash
pip install ScientificMicroservices
```

Usage
Here's a basic example of how to use the wrapper:

```python
from ScientificMicroservices import DetectOutliers
# Initialize the API client
api_key = os.environ("api_key")
# Define the input data
input_data = [1, 2, 4, 5, 40, 3, 5, 6]

# Call the API
outliers = DetectOutliers(input_data, api_key)

# Process the response
print(response)
Replace ModelAPI with the specific model you wish to use and adjust the input_data accordingly.

Documentation
For detailed information on available models and their parameters, please refer to the Scientific Microservices API documentation.

Contributing
Contributions are welcome! If you'd like to improve this wrapper or add support for additional models, please fork the repository and submit a pull request.
Read the Docs

License
This project is licensed under the MIT License - see the LICENSE file for details.
