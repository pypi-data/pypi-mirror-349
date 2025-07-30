from pymongo.monitoring import CommandListener
import json
from collections import defaultdict, deque
from bson import Binary, ObjectId, json_util

class MongoJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder for MongoDB types."""
    def default(self, obj):
        if isinstance(obj, Binary):
            return obj.hex()  # Convert Binary to a hex string
        if isinstance(obj, ObjectId):
            return str(obj)  # Convert ObjectId to a string
        return super().default(obj)
class QueryCounter(CommandListener):
    """A MongoDB CommandListener to count and log database queries."""

    def __init__(self):
        self.reset()
        self.last_ten_requests = deque(maxlen=10)  # Store the last 10 requests

    def reset(self):
        """Resets the query count and details."""
        self._queries = defaultdict(int)
        self._commands = []  # Store the actual commands executed

    def started(self, event):
        """Called when a command starts."""
        try:
            query_str = json.dumps(
                {"command_name": event.command_name, "command": event.command},
                sort_keys=True,
                cls=MongoJSONEncoder,  # Use the custom encoder
            )
            command_dict = {
                "command_name": event.command_name,
                "command": json_util.loads(json_util.dumps(event.command)),  # Deserialize for readability
            }
            self._commands.append(command_dict)
            self._queries[query_str] += 1
        except Exception as e:
            print("Error in started method:", e)

    def succeeded(self, event):
        """Called when a command succeeds."""
        pass

    def failed(self, event):
        """Called when a command fails."""
        pass

    @property
    def total_queries(self):
        """Returns the total number of queries."""
        return sum(self._queries.values())

    @property
    def repeated_queries(self):
        """Returns queries that were executed more than once."""
        return {k: v for k, v in self._queries.items() if v > 1}

    @property
    def commands(self):
        """Returns the list of commands executed."""
        return self._commands

    def summary(self):
        """Returns a summary of the queries."""
        return {
            "total_queries": self.total_queries,
            "repeated_query_count": sum(v for v in self.repeated_queries.values()),
            "repeated_queries": self.repeated_queries,
            "commands": self.commands,  # Include commands in the summary
        }

    def add_request_summary(self, request_url, request_method, query_summary):
        """Adds a request summary to the last_ten_requests."""
        self.last_ten_requests.append({
            "url": request_url,
            "method": request_method,
            "query_summary": query_summary,
        })
        # Reset the query counter if the deque reaches its maximum length
        if len(self.last_ten_requests) == self.last_ten_requests.maxlen:
            self.reset()

    def get_last_ten_requests(self):
        """Returns the last ten request summaries in reverse order (most recent first)."""
        return list(reversed(self.last_ten_requests))
    