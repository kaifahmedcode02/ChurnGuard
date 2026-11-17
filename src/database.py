"""
ChurnGuard — Dual-Portal SQLite Database Layer
Stores customer accounts, live support tickets from the Customer Portal, and rescue offers sent by Client Admin.
Author: Mohammed Kaif Ahmed (https://kaifcode.com)
"""
import os
import sqlite3
from datetime import datetime
from typing import List, Dict, Any
from ml_engine import ChurnGuardEngine

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "churnguard.db")

SEED_CUSTOMERS = [
    {"account_id": "CUST-101", "company_name": "NovaCloud Systems", "contact_name": "Arjun Mehta", "email": "arjun@novacloud.io", "monthly_bill": 110.0, "tenure_months": 6, "days_since_last_login": 18, "monthly_active_days": 9, "open_support_tickets": 3, "avg_ticket_wait_hours": 38.0, "feature_adoption_pct": 34.0, "contract_type": "Month-to-Month", "payment_failures": 0, "satisfaction_score": 2.0, "active_offer": "Priority 24h Support Fix + $15 Service Credit", "offer_status": "Pending Customer Acceptance"},
    {"account_id": "CUST-102", "company_name": "Apex FinTech Labs", "contact_name": "Sarah Jenkins", "email": "sarah@apexfintech.com", "monthly_bill": 95.0, "tenure_months": 32, "days_since_last_login": 1, "monthly_active_days": 27, "open_support_tickets": 0, "avg_ticket_wait_hours": 4.0, "feature_adoption_pct": 88.0, "contract_type": "One Year", "payment_failures": 0, "satisfaction_score": 4.8, "active_offer": "None (Safe & Loyal)", "offer_status": "Healthy"},
    {"account_id": "CUST-103", "company_name": "Velocity Logistics", "contact_name": "Rohan Deshmukh", "email": "rohan@velocitylog.in", "monthly_bill": 85.0, "tenure_months": 5, "days_since_last_login": 14, "monthly_active_days": 11, "open_support_tickets": 1, "avg_ticket_wait_hours": 16.0, "feature_adoption_pct": 30.0, "contract_type": "Month-to-Month", "payment_failures": 1, "satisfaction_score": 2.8, "active_offer": "1-Click Auto-Pay Recovery & 14-Day Grace Period", "offer_status": "Pending Customer Acceptance"},
    {"account_id": "CUST-104", "company_name": "Luminary Health AI", "contact_name": "Dr. Priya Nair", "email": "priya@luminaryhealth.org", "monthly_bill": 105.0, "tenure_months": 14, "days_since_last_login": 10, "monthly_active_days": 15, "open_support_tickets": 3, "avg_ticket_wait_hours": 42.0, "feature_adoption_pct": 62.0, "contract_type": "Month-to-Month", "payment_failures": 0, "satisfaction_score": 2.2, "active_offer": "Priority 24h Support Fix + $15 Service Credit", "offer_status": "Pending Customer Acceptance"},
    {"account_id": "CUST-105", "company_name": "BluePeak Retail", "contact_name": "Marcus Vance", "email": "marcus@bluepeak.co", "monthly_bill": 65.0, "tenure_months": 21, "days_since_last_login": 15, "monthly_active_days": 12, "open_support_tickets": 0, "avg_ticket_wait_hours": 5.0, "feature_adoption_pct": 58.0, "contract_type": "Month-to-Month", "payment_failures": 0, "satisfaction_score": 3.8, "active_offer": "None (Do Not Disturb)", "offer_status": "Quiet User"},
    {"account_id": "CUST-106", "company_name": "Zenith CyberSec", "contact_name": "Vikram Rao", "email": "vikram@zenithsec.io", "monthly_bill": 118.0, "tenure_months": 40, "days_since_last_login": 2, "monthly_active_days": 26, "open_support_tickets": 0, "avg_ticket_wait_hours": 5.0, "feature_adoption_pct": 90.0, "contract_type": "Two Year", "payment_failures": 0, "satisfaction_score": 4.9, "active_offer": "None (Safe & Loyal)", "offer_status": "Healthy"},
    {"account_id": "CUST-107", "company_name": "PixelCraft Studio", "contact_name": "Elena Rostova", "email": "elena@pixelcraft.design", "monthly_bill": 45.0, "tenure_months": 2, "days_since_last_login": 36, "monthly_active_days": 2, "open_support_tickets": 3, "avg_ticket_wait_hours": 60.0, "feature_adoption_pct": 12.0, "contract_type": "Month-to-Month", "payment_failures": 2, "satisfaction_score": 1.2, "active_offer": "None (Unlikely to Stay)", "offer_status": "Low ROI"},
    {"account_id": "CUST-108", "company_name": "Stellar EdTech", "contact_name": "Ananya Sharma", "email": "ananya@stellared.in", "monthly_bill": 92.0, "tenure_months": 9, "days_since_last_login": 9, "monthly_active_days": 16, "open_support_tickets": 2, "avg_ticket_wait_hours": 28.0, "feature_adoption_pct": 48.0, "contract_type": "Month-to-Month", "payment_failures": 0, "satisfaction_score": 2.6, "active_offer": "15% Loyalty Discount on 1-Year Plan Upgrade", "offer_status": "Pending Customer Acceptance"},
    {"account_id": "CUST-109", "company_name": "Vortex Media Group", "contact_name": "Kabir Malhotra", "email": "kabir@vortexmedia.io", "monthly_bill": 42.0, "tenure_months": 2, "days_since_last_login": 39, "monthly_active_days": 1, "open_support_tickets": 4, "avg_ticket_wait_hours": 64.0, "feature_adoption_pct": 10.0, "contract_type": "Month-to-Month", "payment_failures": 2, "satisfaction_score": 1.0, "active_offer": "None (Unlikely to Stay)", "offer_status": "Low ROI"},
    {"account_id": "CUST-110", "company_name": "EchoGrid Freelance", "contact_name": "Nadia Al-Mansoor", "email": "nadia@echogrid.co", "monthly_bill": 38.0, "tenure_months": 1, "days_since_last_login": 42, "monthly_active_days": 1, "open_support_tickets": 3, "avg_ticket_wait_hours": 58.0, "feature_adoption_pct": 8.0, "contract_type": "Month-to-Month", "payment_failures": 3, "satisfaction_score": 1.0, "active_offer": "None (Unlikely to Stay)", "offer_status": "Low ROI"}
]


class ChurnGuardDatabase:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.engine = ChurnGuardEngine()
        self._init_schema()

    def _get_conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_schema(self):
        with self._get_conn() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS customers (
                    account_id TEXT PRIMARY KEY,
                    company_name TEXT NOT NULL,
                    contact_name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    monthly_bill REAL NOT NULL,
                    tenure_months INTEGER NOT NULL,
                    days_since_last_login INTEGER NOT NULL,
                    monthly_active_days INTEGER NOT NULL,
                    open_support_tickets INTEGER NOT NULL,
                    avg_ticket_wait_hours REAL NOT NULL,
                    feature_adoption_pct REAL NOT NULL,
                    contract_type TEXT NOT NULL,
                    payment_failures INTEGER NOT NULL,
                    satisfaction_score REAL NOT NULL,
                    leaving_risk_pct REAL NOT NULL,
                    estimated_days_left INTEGER NOT NULL,
                    customer_group_name TEXT NOT NULL,
                    customer_group_code TEXT NOT NULL,
                    recommended_action_name TEXT NOT NULL,
                    expected_net_profit_saved REAL NOT NULL,
                    active_offer TEXT NOT NULL,
                    offer_status TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS rescue_events_log (
                    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    portal_source TEXT NOT NULL,
                    account_id TEXT NOT NULL,
                    company_name TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    details TEXT NOT NULL,
                    net_profit_impact REAL NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)
            count = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
            if count == 0:
                for c in SEED_CUSTOMERS:
                    self.upsert_customer(c, conn=conn)

    def upsert_customer(self, data: Dict[str, Any], conn=None) -> Dict[str, Any]:
        pred = self.engine.predict_customer(data)
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        rec = {
            "account_id": str(data.get("account_id", "CUST-101")),
            "company_name": str(data.get("company_name", "Custom Account")),
            "contact_name": str(data.get("contact_name", "Customer User")),
            "email": str(data.get("email", "user@company.com")),
            "monthly_bill": float(data.get("monthly_bill", 85.0)),
            "tenure_months": int(data.get("tenure_months", 12)),
            "days_since_last_login": int(data.get("days_since_last_login", 5)),
            "monthly_active_days": int(data.get("monthly_active_days", 18)),
            "open_support_tickets": int(data.get("open_support_tickets", 0)),
            "avg_ticket_wait_hours": float(data.get("avg_ticket_wait_hours", 8.0)),
            "feature_adoption_pct": float(data.get("feature_adoption_pct", 65.0)),
            "contract_type": str(data.get("contract_type", "Month-to-Month")),
            "payment_failures": int(data.get("payment_failures", 0)),
            "satisfaction_score": float(data.get("satisfaction_score", 3.5)),
            "leaving_risk_pct": pred["leaving_risk_pct"],
            "estimated_days_left": pred["estimated_days_left"],
            "customer_group_name": pred["customer_group"]["name"],
            "customer_group_code": pred["customer_group"]["code"],
            "recommended_action_name": pred["recommended_action"]["name"],
            "expected_net_profit_saved": pred["financial_impact"]["expected_net_profit_saved"],
            "active_offer": str(data.get("active_offer", pred["recommended_action"]["name"])),
            "offer_status": str(data.get("offer_status", "Ready to Send")),
            "updated_at": now
        }
        own = False
        if conn is None:
            conn = self._get_conn()
            own = True
        try:
            conn.execute("""
                INSERT INTO customers VALUES (
                    :account_id, :company_name, :contact_name, :email, :monthly_bill,
                    :tenure_months, :days_since_last_login, :monthly_active_days,
                    :open_support_tickets, :avg_ticket_wait_hours, :feature_adoption_pct,
                    :contract_type, :payment_failures, :satisfaction_score,
                    :leaving_risk_pct, :estimated_days_left, :customer_group_name,
                    :customer_group_code, :recommended_action_name, :expected_net_profit_saved,
                    :active_offer, :offer_status, :updated_at
                )
                ON CONFLICT(account_id) DO UPDATE SET
                    monthly_bill=excluded.monthly_bill,
                    tenure_months=excluded.tenure_months,
                    days_since_last_login=excluded.days_since_last_login,
                    monthly_active_days=excluded.monthly_active_days,
                    open_support_tickets=excluded.open_support_tickets,
                    avg_ticket_wait_hours=excluded.avg_ticket_wait_hours,
                    feature_adoption_pct=excluded.feature_adoption_pct,
                    contract_type=excluded.contract_type,
                    payment_failures=excluded.payment_failures,
                    satisfaction_score=excluded.satisfaction_score,
                    leaving_risk_pct=excluded.leaving_risk_pct,
                    estimated_days_left=excluded.estimated_days_left,
                    customer_group_name=excluded.customer_group_name,
                    customer_group_code=excluded.customer_group_code,
                    recommended_action_name=excluded.recommended_action_name,
                    expected_net_profit_saved=excluded.expected_net_profit_saved,
                    active_offer=excluded.active_offer,
                    offer_status=excluded.offer_status,
                    updated_at=excluded.updated_at
            """, rec)
            if own:
                conn.commit()
        finally:
            if own:
                conn.close()
        return {**rec, "prediction": pred}

    def list_customers(self) -> List[Dict[str, Any]]:
        with self._get_conn() as conn:
            rows = conn.execute("SELECT * FROM customers ORDER BY leaving_risk_pct DESC").fetchall()
            return [dict(r) for r in rows]

    def log_portal_event(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        entry = {
            "portal_source": str(payload.get("portal_source", "Client Admin")),
            "account_id": str(payload.get("account_id", "CUST-101")),
            "company_name": str(payload.get("company_name", "NovaCloud Systems")),
            "event_type": str(payload.get("event_type", "Rescue Offer Sent")),
            "details": str(payload.get("details", "Dispatched rescue offer to customer portal")),
            "net_profit_impact": float(payload.get("net_profit_impact", 0.0)),
            "created_at": now
        }
        with self._get_conn() as conn:
            cur = conn.execute("""
                INSERT INTO rescue_events_log (
                    portal_source, account_id, company_name, event_type, details, net_profit_impact, created_at
                ) VALUES (
                    :portal_source, :account_id, :company_name, :event_type, :details, :net_profit_impact, :created_at
                )
            """, entry)
            conn.commit()
            entry["event_id"] = cur.lastrowid
        return entry
