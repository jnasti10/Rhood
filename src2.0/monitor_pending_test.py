import unittest
from unittest.mock import patch
from monitor_pending import main
from utils.trade_data import Trade_data
import json

# Mock data for testing
mock_executed_string = """{
    "id": "valid_executed_order",
    "chain_symbol": "UPRO",
    "strategy": "long_condor_call",
    "pending_quantity": "0",
    "quantity": "1",
    "created_at": "2024-11-20",
    "premium": "99.00000000",
    "legs": []
}"""

mock_pending_string = """{
    "id": "valid_pending_order",
    "chain_symbol": "UPRO",
    "strategy": "long_condor_call",
    "pending_quantity": "1",
    "quantity": "1",
    "created_at": "2024-11-20",
    "premium": "99.00000000",
    "legs": []
}"""

class TestMonitorPending(unittest.TestCase):
    def setUp(self):
        """Set up mock trade data."""
        self.mock_data = Trade_data(1, "MOCK_trade_data.obj")
        self.mock_data.pending_positions = {
            "UPRO": [
                {"id": "valid_executed_order"},
                {"id": "valid_pending_order"}
            ]
        }
        self.mock_data.active_positions = {"UPRO": []}
        self.mock_data.save()

    def mock_getOrderByID(order_id):
        """Simulated responses for getOrderByID."""
        mock_responses = {
            "valid_executed_order": json.loads(mock_executed_string),
            "valid_pending_order": json.loads(mock_pending_string),
        }
        return mock_responses.get(order_id, {"state": "not_found"})

    def mock_get_data(self):
        """Override get_data() to return mock trade data."""
        return self.mock_data

    @patch("monitor_pending.getOrderByID", side_effect=mock_getOrderByID)
    @patch("monitor_pending.get_data", side_effect=mock_get_data)
    def test_monitor_pending(self, mock_get_data, mock_get_order):
        """Run the main function and verify behavior."""
        main(self.mock_data)  # Call the actual main() function

        # Reload mock data to check changes
        self.mock_data.load()

        # Assertions
        self.assertEqual(len(self.mock_data.pending_positions["UPRO"]), 1)  # Only the pending order should remain
        self.assertEqual(len(self.mock_data.active_positions["UPRO"]), 1)  # One executed order should be added

        # Verify the executed order is correct
        executed_order = self.mock_data.active_positions["UPRO"][0]
        self.assertEqual(executed_order["id"], "valid_executed_order")
        self.assertEqual(executed_order["pending_quantity"], "0")

if __name__ == "__main__":
    unittest.main()
