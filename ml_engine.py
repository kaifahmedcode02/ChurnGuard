"""
ChurnGuard — Real-Time Customer Retention, Root-Cause & Smart Rescue Engine
Supports both the Client/Admin Portal and the Customer Self-Service Portal.
Author: Mohammed Kaif Ahmed (https://kaifcode.com)
"""
import json
import math
import os
from typing import Dict, Any

HEALTHY_BASELINE = {
    "monthly_bill": 75.0,
    "tenure_months": 24.0,
    "days_since_last_login": 3.0,
    "monthly_active_days": 22.0,
    "open_support_tickets": 0.0,
    "avg_ticket_wait_hours": 6.0,
    "feature_adoption_pct": 75.0,
    "is_monthly_contract": 0.0,
    "payment_failures": 0.0,
    "satisfaction_score": 4.5
}


class ChurnGuardEngine:
    def __init__(self, weights_path: str = None):
        self.weights = {
            "intercept": -1.45,
            "monthly_bill": 0.0085,
            "tenure_months": -0.038,
            "days_since_last_login": 0.072,
            "monthly_active_days": -0.055,
            "open_support_tickets": 0.48,
            "avg_ticket_wait_hours": 0.025,
            "feature_adoption_pct": -0.028,
            "is_monthly_contract": 0.88,
            "payment_failures": 0.74,
            "satisfaction_score": -0.42
        }

    @staticmethod
    def _sigmoid(x: float) -> float:
        return 1.0 / (1.0 + math.exp(-max(-20.0, min(20.0, x))))

    def predict_customer(self, customer: Dict[str, Any]) -> Dict[str, Any]:
        bill = float(customer.get("monthly_bill", 85.0))
        tenure = float(customer.get("tenure_months", 12.0))
        last_login = float(customer.get("days_since_last_login", 5.0))
        active_days = float(customer.get("monthly_active_days", 18.0))
        tickets = float(customer.get("open_support_tickets", 0.0))
        wait_hrs = float(customer.get("avg_ticket_wait_hours", 8.0))
        adoption = float(customer.get("feature_adoption_pct", 65.0))
        contract = str(customer.get("contract_type", "Month-to-Month"))
        is_monthly = 1.0 if "month" in contract.lower() else 0.0
        failures = float(customer.get("payment_failures", 0.0))
        satisfaction = float(customer.get("satisfaction_score", 3.5))

        support_frustration = 0.30 if (tickets >= 2 and wait_hrs >= 24) else 0.0
        ghosting_penalty = 0.35 if (last_login >= 14 and adoption < 40) else 0.0
        billing_danger = 0.40 if (failures >= 1 and is_monthly == 1.0) else 0.0

        w = self.weights
        logit = (
            w["intercept"]
            + w["monthly_bill"] * bill
            + w["tenure_months"] * tenure
            + w["days_since_last_login"] * last_login
            + w["monthly_active_days"] * active_days
            + w["open_support_tickets"] * tickets
            + w["avg_ticket_wait_hours"] * wait_hrs
            + w["feature_adoption_pct"] * adoption
            + w["is_monthly_contract"] * is_monthly
            + w["payment_failures"] * failures
            + w["satisfaction_score"] * satisfaction
            + support_frustration
            + ghosting_penalty
            + billing_danger
        )

        risk_prob = self._sigmoid(logit)
        risk_pct = round(risk_prob * 100.0, 1)

        raw_days = (
            125.0
            - risk_prob * 88.0
            - tickets * 4.5
            - failures * 9.0
            - max(0.0, last_login - 7.0) * 0.9
            + (1.0 - is_monthly) * 28.0
        )
        days_left = int(max(5, min(180, round(raw_days))))

        hazard_daily = -math.log(max(0.03, 1.0 - risk_prob * 0.85)) / max(15.0, float(days_left))
        stay_30d = round(math.exp(-hazard_daily * 30.0) * 100.0, 1)
        stay_60d = round(math.exp(-hazard_daily * 60.0) * 100.0, 1)
        stay_90d = round(math.exp(-hazard_daily * 90.0) * 100.0, 1)

        reasons = []
        b = HEALTHY_BASELINE

        def add_reason(label: str, delta_logit: float, detail: str):
            pts = round(delta_logit * 18.5, 1)
            if abs(pts) >= 1.2:
                reasons.append({
                    "factor": label,
                    "impact_points": pts,
                    "direction": "increases_risk" if pts > 0 else "lowers_risk",
                    "explanation": detail
                })

        add_reason("Contract Plan", w["is_monthly_contract"] * (is_monthly - b["is_monthly_contract"]), f"On a {contract} plan ({'easy to cancel anytime' if is_monthly else 'locked in for 1 Year'})")
        add_reason("Open Support Complaints", w["open_support_tickets"] * (tickets - b["open_support_tickets"]) + support_frustration, f"{int(tickets)} open complaint(s) with {wait_hrs:.0f}h avg wait")
        add_reason("Recent Login / Activity Gap", w["days_since_last_login"] * (last_login - b["days_since_last_login"]) + ghosting_penalty * 0.5, f"Last active {int(last_login)} days ago (healthy avg is 3 days)")
        add_reason("Monthly Active Days", w["monthly_active_days"] * (active_days - b["monthly_active_days"]), f"Used service {int(active_days)} days this month")
        add_reason("Services & Add-Ons Used", w["feature_adoption_pct"] * (adoption - b["feature_adoption_pct"]) + ghosting_penalty * 0.5, f"Using {adoption:.0f}% of available features/add-ons")
        add_reason("Customer Satisfaction Rating", w["satisfaction_score"] * (satisfaction - b["satisfaction_score"]), f"Rated service {satisfaction:.1f} / 5.0 stars")
        add_reason("Failed Card Payments", w["payment_failures"] * (failures - b["payment_failures"]) + billing_danger, f"{int(failures)} failed card charge(s) recently")
        add_reason("Customer Loyalty Tenure", w["tenure_months"] * (tenure - b["tenure_months"]), f"With the company for {int(tenure)} months")

        reasons.sort(key=lambda r: abs(r["impact_points"]), reverse=True)

        annual_value = round(bill * 12.0, 2)
        revenue_at_risk = round(annual_value * risk_prob, 2)

        tech_save = min(0.68, 0.24 + (0.32 if tickets >= 1 or wait_hrs >= 18 else 0.06))
        contract_save = min(0.65, 0.20 + (0.30 if is_monthly == 1.0 else 0.05) + (0.10 if bill >= 70 else 0.0))
        onboarding_save = min(0.62, 0.20 + (0.34 if adoption < 55 else 0.06))
        payment_save = min(0.75, 0.14 + (0.48 if failures >= 1 else 0.05))

        mult = 0.20 if risk_pct < 22.0 else (0.25 if (risk_pct > 90.0 and adoption < 20.0) else 1.0)

        raw_actions = [
            {
                "id": "tech_call",
                "name": "Priority 24h Support Fix + $15 Service Credit",
                "plain_summary": "Fast-track their open support complaints within 24 hours and add a $15 courtesy credit.",
                "customer_portal_headline": "We've fast-tracked your support ticket + unlocked a $15 courtesy bill credit!",
                "cost": 25.0,
                "save_prob": round(tech_save * mult, 3)
            },
            {
                "id": "loyalty_discount",
                "name": "15% Loyalty Discount on 1-Year Plan Upgrade",
                "plain_summary": "Lower their monthly bill by 15% when they switch from Month-to-Month to a 1-Year plan.",
                "customer_portal_headline": "Stay with us and save 15% off your monthly bill for the next 12 months!",
                "cost": round(bill * 0.15 * 6.0, 2),
                "save_prob": round(contract_save * mult, 3)
            },
            {
                "id": "guided_onboarding",
                "name": "Free 1-on-1 Feature & Security Setup Session",
                "plain_summary": "Help them turn on unused security, backup, and speed add-ons at no extra charge.",
                "customer_portal_headline": "Claim your free 1-on-1 setup session + complimentary Premium Security Add-On!",
                "cost": 30.0,
                "save_prob": round(onboarding_save * mult, 3)
            },
            {
                "id": "payment_flex",
                "name": "1-Click Auto-Pay Recovery & 14-Day Grace Period",
                "plain_summary": "Clear failed payment flags and give them 14 extra days to update their card.",
                "customer_portal_headline": "Need billing flexibility? Activate a free 14-day payment grace period with 1 click.",
                "cost": 10.0,
                "save_prob": round(payment_save * mult, 3)
            }
        ]

        actions = []
        for act in raw_actions:
            new_risk = round(max(3.0, risk_pct * (1.0 - act["save_prob"])), 1)
            saved_rev = round(revenue_at_risk * act["save_prob"], 2)
            net_profit = round(saved_rev - act["cost"], 2)
            actions.append({
                **act,
                "new_risk_pct": new_risk,
                "risk_drop_pct": round(risk_pct - new_risk, 1),
                "expected_saved_revenue": saved_rev,
                "net_profit_saved": net_profit
            })

        actions.sort(key=lambda a: a["net_profit_saved"], reverse=True)
        best_action = actions[0]

        if risk_pct < 28.0:
            group_name, group_code = "Safe & Loyal", "sure_thing"
            group_advice = "Happy customer who will renew on their own. Do not waste discount money here."
        elif risk_pct >= 88.0 and adoption < 22.0 and best_action["net_profit_saved"] < 30.0:
            group_name, group_code = "Unlikely to Stay", "lost_cause"
            group_advice = "Customer has stopped using the service. Big discounts will lose money."
        elif risk_pct < 48.0 and is_monthly == 1.0 and tickets == 0 and last_login >= 12:
            group_name, group_code = "Do Not Disturb", "sleeping_dog"
            group_advice = "Quiet monthly subscriber. Avoid pushy sales popups that might remind them to cancel."
        else:
            group_name, group_code = "High-Value Save", "persuadable"
            group_advice = "At risk of leaving, but very likely to stay if we send the recommended rescue offer now."

        return {
            "leaving_risk_pct": risk_pct,
            "estimated_days_left": days_left,
            "staying_probability_curve": {"day_30": stay_30d, "day_60": stay_60d, "day_90": stay_90d},
            "customer_group": {"name": group_name, "code": group_code, "plain_explanation": group_advice},
            "financial_impact": {
                "monthly_bill": round(bill, 2),
                "annual_contract_value": annual_value,
                "revenue_at_risk": revenue_at_risk,
                "action_cost": best_action["cost"],
                "expected_net_profit_saved": max(0.0, best_action["net_profit_saved"])
            },
            "top_reasons": reasons[:5],
            "recommended_action": best_action,
            "all_actions_ranked": actions
        }
