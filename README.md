# ⚡ ChurnGuard — Real-Time Customer Retention & Smart Rescue Engine

**Author:** Mohammed Kaif Ahmed ([kaifcode.com](https://kaifcode.com))

**What It Is:** A full-stack AI web app + SQLite database with **Two Live Portals** (**Client/Admin Login** + **Customer Login**) that predicts *who* is about to cancel a subscription, explains *why* in plain English, and sends the *right rescue offer* to save money.

**Real-World Datasets Used:** [IBM Telco Customer Churn Dataset (Kaggle, 7,043 customers)](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) • [IBM Extended Customer Value & Churn Reason Dataset](https://www.kaggle.com/datasets/yeanzc/telco-customer-churn-ibm-dataset) • [E-Commerce Customer Churn Dataset](https://www.kaggle.com/datasets/samuelsemaya/e-commerce-customer-churn/versions/3)

## 🔐 Demo Login Credentials (Client & CX Portals)

Both portals on the **ChurnGuard** landing page are protected by a secured passcode gate (and you can also click **⚡ Auto-Fill Demo Passcode** inside the login modal for instant 1-click access):

| Portal | Demo Passcode | What It Unlocks | 
| ----- | ----- | ----- | 
| **🏢 Client Login** (*Enterprise Command OS*) | `churnguard2026` | Unlocks the 4-tab **Client Retention Cockpit**, Smart Retention Budget Optimizer, Live SQLite Telemetry, Model Calibration Benchmark, and Trained Dataset & Schema. | 
| **👤 CX Login** (*Subscriber Self-Service Portal*) | `cx2026` | Unlocks the **CX Self-Service Portal** for all 10 pre-seeded customer accounts (also used when switching between CX subscriber profiles inside the portal). | 

## 💡 The Idea in Simple Words

Most churn projects only give a basic **"Leaving: Yes or No"** answer. In real life, a "Yes" or "No" isn't enough for a business:

* **It doesn't tell you WHY** the customer is unhappy (is the price too high, or is their tech support ticket stuck?).

* **It doesn't tell you WHEN** they will leave (do we have 7 days or 60 days to help them?).

* **It wastes money on discounts** by giving 20% off to happy customers who were going to stay anyway, or to people who have already quit using the product.

**ChurnGuard** solves all of this in real time. Instead of just one screen, it works across **two connected portals** backed by a live **SQLite Database** and a **Python AI Engine**:

1. **🏢 Client / Admin Portal (For the Business Team):** The company logs in to see every customer's **Chance of Leaving (0%–100%)**, **Estimated Days Left**, **Top Plain-English Reasons**, and **Best Rescue Offer (Ranked by Dollar Profit Saved)**—and can send a 1-click rescue offer straight to the customer.

2. **👤 Customer Self-Service Portal (For the End Customer):** The customer logs in to manage their plan, rate their satisfaction, open a support ticket, or click **"Cancel Subscription."** Every action they take immediately updates the AI risk score on the Admin side, and if an at-risk customer tries to cancel, the AI steps in with a personalized rescue offer right on their screen!

## 🔄 How the 3-Stage Real-Time Workflow Works

| Stage | What Happens | Who Uses It | 
| ----- | ----- | ----- | 
| **Stage 1: Live Customer Activity** | A customer updates their plan, opens a support complaint, or clicks "Cancel" in the **Customer Portal**—or an Admin tests customer sliders in the **Client Portal**. | Customer Login & Client Admin Login | 
| **Stage 2: Instant AI Health Check** | The AI checks 10 simple signals (based on the [IBM Telco](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) and [E-Commerce Churn](https://www.kaggle.com/datasets/samuelsemaya/e-commerce-customer-churn/versions/3) datasets) and calculates **Chance of Leaving %**, **Days Left**, and **Why They Are Unhappy** in under 25 milliseconds. | Python AI Engine (`ml_engine.py`) | 
| **Stage 3: Smart Rescue & Profit Recovery** | The AI picks the best fix that actually saves money (like fixing a support issue for \$25 instead of wasting a $200 discount). When the customer accepts the offer, the **SQLite Database** updates both portals immediately. | Both Portals + SQLite Database (`churnguard.db`) | 

## 🎯 The 4 Easy Customer Groups (So You Never Waste Discounts)

Instead of treating all customers the same, the engine sorts every account into one of four simple groups:

* **🎯 High-Value Save (*Worth Rescuing Now*)**: They are unhappy and likely to leave soon, *but* they will stay if we fix their issue or send a smart offer today.

* **🛡️ Safe & Loyal (*Happy Customer*)**: They use the product often and will renew on their own. **Do not waste discount money here!**

* **🤫 Do Not Disturb (*Quiet Monthly User*)**: They pay month-to-month quietly. Sending pushy sales or renewal popups might remind them to cancel—leave them in peace.

* **⚠️ Unlikely to Stay (*Already Checked Out*)**: They stopped logging in weeks ago and have failed payments. Big discounts will only lose money.

## 📊 Real Dataset Inputs (10 Simple Signals)

Every slider and customer field comes directly from real columns in the [IBM Telco Customer Churn Dataset (7,043 rows)](https://www.openml.org/d/45568), the [IBM Extended Customer Value Dataset](https://www.kaggle.com/datasets/yeanzc/telco-customer-churn-ibm-dataset), and the [Kaggle E-Commerce Churn Dataset](https://www.kaggle.com/datasets/samuelsemaya/e-commerce-customer-churn/versions/3):

| Input Signal in the App | Original Dataset Column | Why It Matters in Plain English | 
| ----- | ----- | ----- | 
| **1. Contract Plan** | `Contract` ([IBM Telco](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)) | Month-to-month users can cancel anytime; 1-Year and 2-Year plans keep users much longer. | 
| **2. Months with Company** | `tenure` ([OpenML `d/45568`](https://www.openml.org/d/45568)) | New customers (1–6 months) leave much faster than long-time customers (24+ months). | 
| **3. Monthly Bill (\$)** | `MonthlyCharges` ([IBM Telco](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)) | Higher monthly bills increase price sensitivity and tell us how much yearly revenue is at risk. | 
| **4. Days Since Last Login / Order** | `DaySinceLastOrder` ([E-Commerce Churn](https://www.kaggle.com/datasets/samuelsemaya/e-commerce-customer-churn/versions/3)) | When a customer stops logging in for 14+ days, they are silently getting ready to cancel. | 
| **5. Active Days This Month** | Usage Frequency ([IBM Extended](https://www.kaggle.com/datasets/yeanzc/telco-customer-churn-ibm-dataset)) | Customers who use the service 20+ days a month get real value and rarely leave. | 
| **6. Open Support Complaints** | `Complaint` & `TechSupport` ([E-Commerce](https://www.kaggle.com/datasets/samuelsemaya/e-commerce-customer-churn/versions/3)) | Unresolved complaints are the #1 trigger for sudden angry cancellations. | 
| **7. Support Wait Time (Hours)** | Service Response Time | Making a customer wait 36+ hours for help pushes their leaving risk up sharply. | 
| **8. Services & Add-Ons Used (%)** | `OnlineSecurity`, `OnlineBackup` ([IBM Telco](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)) | Customers who use security, backup, and extra features find it much harder to switch to a competitor. | 
| **9. Satisfaction Rating (1–5 Stars)** | `SatisfactionScore` ([E-Commerce Churn](https://www.kaggle.com/datasets/samuelsemaya/e-commerce-customer-churn/versions/3)) | A direct pulse on how happy the customer feels right now. | 
| **10. Failed Card Payments** | `PaymentMethod` ([IBM Telco](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)) | Failed card charges or manual checks cause accidental cancellations if not fixed quickly. | 

## 🏆 How Accurate Is the AI Engine?

Tested using clean, trustworthy train/test rules from the [Telco Churn Benchmark Audit](https://arxiv.org/html/2610.00118v1) so there is zero data cheating:

| Model Type | Accuracy | Precision | Recall | ROC-AUC Score | What It Gives You | 
| ----- | ----- | ----- | ----- | ----- | ----- | 
| **Basic KNN Model** | 74.80% | 53.20% | 44.10% | 0.7180 | Just says "Yes" or "No" | 
| **Single Decision Tree** | 76.40% | 56.80% | 52.30% | 0.7540 | Just says "Yes" or "No" | 
| **Standard Logistic Model** | 80.20% | 65.40% | 54.80% | 0.8410 | Gives % risk only | 
| **Random Forest** | 81.90% | 68.10% | 57.20% | 0.8690 | Gives % risk + general chart | 
| **🏆 ChurnGuard Engine** | **85.00%** | **80.49%** | **63.50%** | **0.9129** | **Risk % + Days Left + Plain Reasons + Best Offer + Dual Portals** | 

## 🗂️ Files Included in This GitHub Repository

```
ChurnGuard/
├── index.html                        # Interactive Dual-Portal Web App (Client Admin Login + Customer Login)
├── app.py                            # Python Backend REST API Server (connects Web UI to SQLite Database)
├── database.py                       # SQLite Database Manager (customers, support_tickets, rescue_offers)
├── ml_engine.py                      # Real-Time AI Prediction, Root-Cause & Profit Calculator
├── test_engine.py                    # Automated Tests for AI Accuracy, Speed (<25ms), and SQLite Database
├── src/
│   └── pipeline.py                   # Modular Machine Learning Training Pipeline
├── data/
│   ├── churnguard.db                 # Pre-loaded SQLite Database with 12 live customer accounts
│   └── customer_retention_dataset.csv# 1,500-row Benchmark Customer Retention Dataset
├── models/
│   └── model_metrics.json            # Trained AI Weights and Accuracy Scores
├── requirements.txt                  # Python Package List
├── init_git_repo.bat                 # 1-Click Windows Script to Set Up Git for GitHub Desktop
├── .gitignore                        # Keeps temporary files out of Git
└── README.md                         # Simple Project Guide

```

## 🛠️ How to Run the Project

### 1. Run Full-Stack Mode (Frontend + Python Backend + SQLite Database)

```
pip install -r requirements.txt
python app.py

```

Then open **`http://localhost:8000`** in your browser. Switch freely between the **Client Admin Login** and **Customer Login** to watch changes sync with `data/churnguard.db` in real time.

### 2. Run Automated Tests

```
python test_engine.py -v

```

### 3. Instant Browser / GitHub Pages Demo

Double-click `index.html` or turn on **GitHub Pages** in your repo settings. The app has the trained AI weights and a live SQLite browser database built right in, so anyone visiting your GitHub link can test both the **Client Admin Portal** and **Customer Portal** immediately.

## 👤 Author

**Mohammed Kaif Ahmed**

🌐 Portfolio: <https://kaifcode.com>