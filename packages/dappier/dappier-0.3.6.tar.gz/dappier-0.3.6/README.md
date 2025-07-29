# Dappier Python SDK

The Dappier Python SDK provides an easy-to-use interface for interacting with the Dappier API.

---

## Installation

Install the SDK using pip:

```bash
pip install dappier
```

---

## Initialization

Below is an example of how to use the Dappier SDK:

```python
import os
from dappier import Dappier

# Set your API key as an environment variable
os.environ["DAPPIER_API_KEY"] = "<YOUR_API_KEY>"

# Initialize the Dappier SDK
app = Dappier()
```

Replace `<YOUR_API_KEY>` with actual Dappier API key which you can get from your [Dappier account](https://platform.dappier.com/home).

---

## Real-Time Search

You can perform a real-time search by providing a query. This will search for real-time data related to your query. You can pick a specific aimodel from [marketplace](https://marketplace.dappier.com/).

```python
response = app.search_real_time_data(query="What is the stock price of Apple ?", ai_model_id="am_01j06ytn18ejftedz6dyhz2b15")
```

---

## AI Recommendations

The AI Recommendations feature allows you to query for articles and other content using a specific data model. You can pick a specific datamodel from [marketplace](https://marketplace.dappier.com/).

```python
response = app.get_ai_recommendations(
    query="latest tech news",
    data_model_id="dm_02hr75e8ate6adr15hjrf3ikol",
    similarity_top_k=5,
    ref="techcrunch.com",
    num_articles_ref=2,
    search_algorithm="most_recent"
)
```

For detailed documentation and advanced features, refer to the official [Dappier documentation](https://docs.dappier.com/quickstart).
