import os
from datetime import datetime
from typing import Any, List, Optional

import pandas as pd
import psycopg

from .span import Span
from .metric import Metric


class CVec:
    """
    CVec API Client
    """

    host: Optional[str]
    tenant: Optional[str]
    api_key: Optional[str]
    default_start_at: Optional[datetime]
    default_end_at: Optional[datetime]

    def __init__(
        self,
        host: Optional[str] = None,
        tenant: Optional[str] = None,
        api_key: Optional[str] = None,
        default_start_at: Optional[datetime] = None,
        default_end_at: Optional[datetime] = None,
    ) -> None:
        """
        Setup the SDK with the given host and API Key.
        The host and API key are loaded from environment variables CVEC_HOST,
        CVEC_TENANT, CVEC_API_KEY, if they are not given as arguments to the constructor.
        The default_start_at and default_end_at can provide a default query time interval for API methods.
        """
        self.host = host or os.environ.get("CVEC_HOST")
        self.tenant = tenant or os.environ.get("CVEC_TENANT")
        self.api_key = api_key or os.environ.get("CVEC_API_KEY")
        self.default_start_at = default_start_at
        self.default_end_at = default_end_at

        if not self.host:
            raise ValueError(
                "CVEC_HOST must be set either as an argument or environment variable"
            )
        if not self.tenant:
            raise ValueError(
                "CVEC_TENANT must be set either as an argument or environment variable"
            )
        if not self.api_key:
            raise ValueError(
                "CVEC_API_KEY must be set either as an argument or environment variable"
            )

    def _get_db_connection(self) -> psycopg.Connection:
        """Helper method to establish a database connection."""
        return psycopg.connect(
            user=self.tenant,
            password=self.api_key,
            host=self.host,
            dbname=self.tenant,
        )

    def get_spans(
        self,
        name: str,
        start_at: Optional[datetime] = None,
        end_at: Optional[datetime] = None,
        limit: Optional[int] = None,
    ) -> List[Span]:
        """
        Return time spans for a metric. Spans are generated from value changes
        that occur after `start_at` (if specified) and before `end_at` (if specified).
        If `start_at` is `None` (e.g., not provided via argument or class default),
        the query is unbounded at the start. If `end_at` is `None`, it's unbounded at the end.

        Each span represents a period where the metric's value is constant.
        - `value`: The metric's value during the span.
        - `name`: The name of the metric.
        - `raw_start_at`: The timestamp of the value change that initiated this span's value.
          This will be >= `_start_at` if `_start_at` was specified.
        - `raw_end_at`: The timestamp marking the end of this span's constant value.
          For the newest span, the value is `None`. For other spans, it's the raw_start_at of the immediately newer data point, which is next span in the list.
        - `id`: Currently `None`.
        - `metadata`: Currently `None`.

        Returns a list of Span objects, sorted in descending chronological order (newest span first).
        Each Span object has attributes corresponding to the fields listed above.
        If no relevant value changes are found, an empty list is returned.
        The `limit` parameter restricts the number of spans returned.
        """
        _start_at = start_at or self.default_start_at
        _end_at = end_at or self.default_end_at

        with self._get_db_connection() as conn:
            with conn.cursor() as cur:
                query_params = {
                    "metric": name,
                    "start_at": _start_at,
                    "end_at": _end_at,
                    # Fetch up to 'limit' points. If limit is None, then the `LIMIT NULL` clause
                    # has no effect (in PostgreSQL).
                    "limit": limit,
                }

                combined_query = """
                SELECT
                    time,
                    value_double,
                    value_string
                FROM metric_data
                WHERE metric = %(metric)s
                  AND (time >= %(start_at)s OR %(start_at)s IS NULL)
                  AND (time < %(end_at)s OR %(end_at)s IS NULL)
                ORDER BY time DESC
                LIMIT %(limit)s
                """
                cur.execute(combined_query, query_params)
                db_rows = cur.fetchall()
                spans = []

                # None indicates that the end time is not known; the span extends beyond
                # the query period.
                raw_end_at = None
                for time, value_double, value_string in db_rows:
                    raw_start_at = time
                    value = value_double if value_double is not None else value_string
                    spans.append(
                        Span(
                            id=None,
                            name=name,
                            value=value,
                            raw_start_at=raw_start_at,
                            raw_end_at=raw_end_at,
                            metadata=None,
                        )
                    )
                    raw_end_at = raw_start_at

                return spans

    def get_metric_data(
        self,
        names: Optional[List[str]] = None,
        start_at: Optional[datetime] = None,
        end_at: Optional[datetime] = None,
    ) -> pd.DataFrame:
        """
        Return all data-points within a given [start_at, end_at) interval,
        optionally selecting a given list of metric names.
        The return value is a Pandas DataFrame with four columns: name, time, value_double, value_string.
        One row is returned for each metric value transition.
        """
        _start_at = start_at or self.default_start_at
        _end_at = end_at or self.default_end_at

        params = {
            "start_at": _start_at,
            "end_at": _end_at,
            "tag_names_is_null": names is None,
            # Pass an empty tuple if names is None or empty, otherwise the tuple of names.
            # ANY(%(empty_tuple)s) will correctly result in no matches if names is empty.
            # If names is None, the tag_names_is_null condition handles it.
            "tag_names_list": names if names else [],
        }

        sql_query = """
            SELECT metric AS name, time, value_double, value_string
            FROM metric_data
            WHERE (time >= %(start_at)s OR %(start_at)s IS NULL)
              AND (time < %(end_at)s OR %(end_at)s IS NULL)
              AND (%(tag_names_is_null)s IS TRUE OR metric = ANY(%(tag_names_list)s))
            ORDER BY name, time ASC
        """

        with self._get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql_query, params)
                rows = cur.fetchall()

        if not rows:
            return pd.DataFrame(
                columns=["name", "time", "value_double", "value_string"]
            )

        # Create DataFrame from fetched rows
        df = pd.DataFrame(
            rows, columns=["name", "time", "value_double", "value_string"]
        )

        # Return the DataFrame with the required columns
        return df[["name", "time", "value_double", "value_string"]]

    def get_metrics(
        self, start_at: Optional[datetime] = None, end_at: Optional[datetime] = None
    ) -> List[Metric]:
        """
        Return a list of metrics that had at least one transition in the given [start_at, end_at) interval.
        All metrics are returned if no start_at and end_at are given.
        """
        sql_query: str
        params: Optional[dict[str, Any]]

        if start_at is None and end_at is None:
            # No time interval specified by arguments, return all tags
            sql_query = """
                SELECT id, normalized_name AS name, birth_at, death_at
                FROM tag_names
                ORDER BY name ASC;
            """
            params = None
        else:
            # Time interval specified, find tags with transitions in the interval
            _start_at = start_at or self.default_start_at
            _end_at = end_at or self.default_end_at

            params = {"start_at_param": _start_at, "end_at_param": _end_at}
            sql_query = f"""
                SELECT DISTINCT metric_id AS id, metric AS name, birth_at, death_at
                FROM {self.tenant}.metric_data
                WHERE (time >= %(start_at_param)s OR %(start_at_param)s IS NULL)
                  AND (time < %(end_at_param)s OR %(end_at_param)s IS NULL)
                ORDER BY name ASC;
            """

        with self._get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql_query, params)
                rows = cur.fetchall()

        # Format rows into list of Metric objects
        metrics_list = [
            Metric(
                id=row[0],
                name=row[1],
                birth_at=row[2],
                death_at=row[3],
            )
            for row in rows
        ]
        return metrics_list
