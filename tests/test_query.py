from __future__ import annotations

import unittest

import pandas as pd

from services.datasets import table_name_for_dataset
from services.query import generate_sql, run_query


class QueryServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.frame = pd.DataFrame(
            {
                "Region": ["East", "West", "East"],
                "Total_Sales": [100.0, 250.0, 50.0],
                "Product_Name": ["A", "B", "C"],
                "Profit": [20.0, 60.0, 10.0],
            }
        )
        self.table_name = table_name_for_dataset("sales-data.csv")

    def test_generates_grouped_sales_query(self) -> None:
        sql = generate_sql("total sales by region", list(self.frame.columns), self.table_name)
        result, truncated = run_query(self.frame, self.table_name, sql)
        self.assertFalse(truncated)
        self.assertEqual(result["Region"].tolist(), ["West", "East"])
        self.assertEqual(result["value"].tolist(), [250.0, 150.0])

    def test_generates_top_n_query(self) -> None:
        sql = generate_sql("top 1 products by profit", list(self.frame.columns), self.table_name)
        result, _ = run_query(self.frame, self.table_name, sql)
        self.assertEqual(result.iloc[0]["Product_Name"], "B")

    def test_rejects_mutating_queries(self) -> None:
        with self.assertRaisesRegex(ValueError, "Only read-only"):
            run_query(self.frame, self.table_name, "DELETE FROM sales_data")

    def test_authorizer_blocks_writes_inside_with_query(self) -> None:
        sql = f"WITH sample AS (SELECT 1) DELETE FROM {self.table_name}"
        with self.assertRaisesRegex(ValueError, "not allowed"):
            run_query(self.frame, self.table_name, sql)

    def test_rejects_multiple_statements(self) -> None:
        sql = f"SELECT * FROM {self.table_name}; SELECT 1"
        with self.assertRaisesRegex(ValueError, "one statement|not allowed|SQL query"):
            run_query(self.frame, self.table_name, sql)

    def test_workspace_starts_without_a_dataset(self) -> None:
        from unittest.mock import patch

        from UI import workspace

        class FakeSessionState(dict):
            def __getattr__(self, key: str):
                try:
                    return self[key]
                except KeyError as error:
                    raise AttributeError(key) from error

            def __setattr__(self, key: str, value: object) -> None:
                self[key] = value

        state = FakeSessionState()
        with patch.object(workspace.st, "session_state", state):
            workspace._initialize_workspace({"id": 1, "name": "Jane Doe", "email": "jane@example.com"})

        self.assertEqual(state["qg_datasets"], {})
        self.assertIsNone(state["qg_selected_dataset"])


if __name__ == "__main__":
    unittest.main()
