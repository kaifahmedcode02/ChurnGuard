import unittest
from database import ChurnGuardDatabase

class TestChurnGuardDualPortal(unittest.TestCase):
    def setUp(self):
        self.db = ChurnGuardDatabase()

    def test_dual_portal_sync(self):
        customers = self.db.list_customers()
        self.assertGreaterEqual(len(customers), 8)
        pred = self.db.engine.predict_customer(customers[0])
        self.assertIn("leaving_risk_pct", pred)
        self.assertIn("recommended_action", pred)
        ev = self.db.log_portal_event({
            "portal_source": "Customer Portal",
            "account_id": "CUST-101",
            "company_name": "NovaCloud Systems",
            "event_type": "Accepted Rescue Offer",
            "details": "Accepted 15% Loyalty Offer",
            "net_profit_impact": 420.0
        })
        self.assertIn("event_id", ev)

if __name__ == "__main__":
    unittest.main()
