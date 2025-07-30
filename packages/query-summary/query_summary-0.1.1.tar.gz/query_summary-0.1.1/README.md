# Query Summary

Query Summary is a Flask middleware designed to track MongoDB queries and provide a summary of query statistics. It includes a web interface to display the last 10 requests and their associated query details.

## Usage
Here's an example of how to use the package:

```python
# Import the package
from query_summary import QuerySummaryMiddleware
from pymongo import MongoClient

# Initialize the Flask app
app = Flask(__name__)

# Initialize the QuerySummaryMiddleware
query_summary_middleware = QuerySummaryMiddleware(app)

# Use the same MongoClient instance with the QuerySummaryMiddleware
client = MongoClient("mongodb://host:port", event_listeners=[query_summary_middleware.query_counter])

# Example MongoDB operation
db = client["example_database"]
db["example_collection"].insert_one({"name": "Test Document"})
```

### Notes:
- If you are using `mongoengine`, it internally creates its own `MongoClient` instance unless you explicitly pass one to it. To ensure compatibility.

```python
import mongoengine as me

# Use the same MongoClient instance with mongoengine
me.connect(alias="example_database", host=client)
```

- The `QuerySummaryMiddleware` automatically tracks MongoDB commands executed by the `MongoClient` instance it is registered with.
- go to /query_summary to see statistics
<img width="1280" alt="Screenshot 2025-05-22 at 15 32 54" src="https://github.com/user-attachments/assets/17547730-c330-478c-a1a6-b5d3601dd917" />
