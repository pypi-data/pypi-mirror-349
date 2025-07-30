from flask import request, g, Blueprint, render_template
from pymongo import MongoClient, monitoring
from .counter import QueryCounter
from bson import json_util

class QuerySummaryMiddleware:
    """Middleware to integrate query summary into Flask."""

    def __init__(self, app=None):
        self.query_counter = QueryCounter()
        monitoring.register(self.query_counter)
        self.blueprint = Blueprint(
            "query_summary", __name__, template_folder="templates"
        )
        self.blueprint.add_url_rule(
            "/query_summary", "query_summary", self.query_summary_view
        )
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initializes the middleware with the Flask app."""
        app.before_request(self.before_request)
        app.after_request(self.after_request)
        app.register_blueprint(self.blueprint)

    def before_request(self):
        """Hook into Flask's request lifecycle before the request is processed."""
        g.query_counter = self.query_counter
        self.query_counter.reset()

    def after_request(self, response):
        """Hook into Flask's request lifecycle after the request is processed."""
        query_summary = self.query_counter.summary()
        self.query_counter.add_request_summary(
            request_url=request.url,
            request_method=request.method,
            query_summary=query_summary,
        )
        return response

    def query_summary_view(self):
        """View to display the last ten requests."""
        last_ten_requests = [
            {
                "url": request["url"],
                "method": request["method"],
                "query_summary": {
                    "total_queries": request["query_summary"]["total_queries"],
                    "repeated_query_count": request["query_summary"]["repeated_query_count"],
                    "commands": [json_util.dumps(cmd) for cmd in request["query_summary"]["commands"]],
                },
            }
            for request in self.query_counter.get_last_ten_requests()
        ]
        return render_template("query_summary.html", last_ten_requests=last_ten_requests)