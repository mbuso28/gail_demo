
# GAIL Demo – Asset Prediction Dashboard

![Vikela SA Logo](static/vikela_logo.png)

## 📡 Overview

**GAIL (Geo-Asset Intelligence Locator)** is a Streamlit-powered dashboard designed to assist Vikela SA in predicting the location of lost telecom assets like antennas. This demo illustrates how AI can be used to visualize, analyze, and simulate asset tracking based on location, status, and historical data.

---

## 🔍 Features

- 📍 Interactive map showing last known and predicted locations
- 🧾 Asset profile viewer with historical movement simulation
- 📤 PDF export of filtered asset data
- 🗃️ Upload supporting documents (e.g. test certs, collection forms)
- 🔄 Simulated flow of asset recovery and refurbishment
- 📊 Risk scoring for intelligent prioritization

---

## 📁 Folder Structure

```
gail_demo/
├── app.py                  # Streamlit dashboard app
├── assets.csv              # Sample asset data
├── requirements.txt        # Required Python libraries
├── static/
│   └── vikela_logo.png     # Vikela SA logo
├── uploads/                # Folder created for uploaded files
└── exports/                # Folder created for exported PDFs
```

---

## 🚀 How to Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/gail-demo.git
cd gail-demo

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

---

## 📦 Deployment

This app is optimized for deployment using **[Streamlit Cloud](https://streamlit.io/cloud)**. After uploading the files to GitHub:
1. Sign in at [streamlit.io/cloud](https://streamlit.io/cloud)
2. Connect your GitHub repo
3. Set `app.py` as the main file
4. Click **Deploy**

---

## 📬 Contact

Developed by **Mbuso Ndlovu** for **Vikela SA**  
📧 info@vikela-sa.co.za | 📞 +27 655 2903  
🏢 Regus Business Park, Southdowns, Centurion  
🌐 [www.vikela-sa.co.za](http://www.vikela-sa.co.za)

---

## 🛠️ License

This demo is for internal and client-facing presentations only.
