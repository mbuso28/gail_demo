import streamlit as st
import pandas as pd
import plotly.express as px
import os
from fpdf import FPDF
from datetime import datetime
import numpy as np

st.set_page_config(page_title="GAIL Demo", layout="wide")
st.title("📡 GAIL Demo Dashboard – Lost Asset Prediction")

df = pd.read_csv("assets.csv")

# --- SIDEBAR FILTERS ---
with st.sidebar:
    st.header("🔍 Filter Assets")
    site_filter = st.multiselect("Last Seen Site", options=df["Last_Seen_Site"].unique(), default=df["Last_Seen_Site"].unique())
    status_filter = st.multiselect("Status", options=df["Status"].unique(), default=df["Status"].unique())
    prediction_filter = st.multiselect("Predicted Location", options=df["Predicted_Location"].dropna().unique(), default=df["Predicted_Location"].dropna().unique())

filtered_df = df[
    (df["Last_Seen_Site"].isin(site_filter)) &
    (df["Status"].isin(status_filter)) &
    (df["Predicted_Location"].isin(prediction_filter))
].copy()

# --- RISK SCORE SIMULATION ---
def generate_risk_score(row):
    site_risk = {"Tower A": 0.6, "Tower B": 0.4, "Tower C": 0.3, "Tower D": 0.7, "Tower E": 0.5}
    return round(site_risk.get(row["Last_Seen_Site"], 0.4) + (0.1 if row["Status"] == "Missing" else -0.2), 2)

filtered_df.loc[:, "Predicted_Risk_Score"] = filtered_df.apply(generate_risk_score, axis=1)

# --- TABLE OF FILTERED RESULTS ---
st.subheader("📋 Filtered Antennas")
st.dataframe(filtered_df, use_container_width=True)

# --- ASSET PROFILE & FILE UPLOAD ---
st.subheader("🧾 Asset Profile Viewer")
asset_id = st.selectbox("Select Antenna", df["Antenna_ID"].unique())
selected_asset = df[df["Antenna_ID"] == asset_id].iloc[0]

st.markdown(f"""
**Antenna ID:** {selected_asset['Antenna_ID']}  
**Asset Type:** {selected_asset['Asset_Type']}  
**Technician:** {selected_asset['Technician']}  
**Last Seen:** {selected_asset['Date_Last_Seen']} at {selected_asset['Last_Seen_Site']}  
**Status:** {selected_asset['Status']}  
**Predicted Location:** {selected_asset['Predicted_Location']}  
**Risk Score:** {generate_risk_score(selected_asset)}
""")

# --- MOCK ASSET MOVEMENT HISTORY ---
st.markdown("### 📑 Movement History (Simulated)")
movement_data = pd.DataFrame([
    {"Date": "2024-11-03", "Location": "Tower A", "Action": "Installed"},
    {"Date": "2025-01-18", "Location": "Tower B", "Action": "Serviced"},
    {"Date": "2025-04-25", "Location": "Tower B", "Action": "Marked as Missing"},
])
st.table(movement_data)

# --- FILE UPLOAD ---
upload = st.file_uploader("Upload Document (e.g. test cert, collection form):", type=["pdf", "jpg", "png", "jpeg"])
if upload:
    os.makedirs("uploads", exist_ok=True)
    save_path = os.path.join("uploads", f"{asset_id}_{upload.name}")
    with open(save_path, "wb") as f:
        f.write(upload.read())
    st.success(f"Uploaded to: {save_path}")

# --- REFURBISHMENT SIMULATION ---
with st.expander("🛠️ Simulate Asset Flow"):
    flow_stage = st.radio("Select current stage:", ["Missing", "Collected", "Refurbished", "Tested"])
    st.success(f"{asset_id} is currently at **{flow_stage}** stage.")

# --- MAP VISUALIZATION ---
st.subheader("🗺️ Map of Filtered Antennas")

filtered_df.loc[:, "Size"] = np.where(filtered_df["Status"] == "Missing", 30, 10)
filtered_df.loc[:, "Legend_Label"] = np.where(filtered_df["Status"] == "Missing", "Missing (Red)", "Found (Blue)")
color_map = {"Missing (Red)": "red", "Found (Blue)": "blue"}

if not filtered_df.empty:
    fig = px.scatter_mapbox(
        filtered_df,
        lat="Last_Seen_Lat",
        lon="Last_Seen_Lon",
        hover_name="Antenna_ID",
        size="Size",
        color="Legend_Label",
        color_discrete_map=color_map,
        zoom=12,
        height=500,
        mapbox_style="open-street-map"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data matches your filters.")

# --- EXPORT TO PDF ---
st.subheader("📤 Export Filtered Data to PDF")

def export_pdf(data):
    def safe_text(text):
        return str(text).encode("latin-1", "replace").decode("latin-1")

    pdf = FPDF()
    pdf.add_page()
    logo_path = "static/vikela_logo.png"
    if os.path.exists(logo_path):
        pdf.image(logo_path, x=150, y=10, w=40)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, safe_text("Filtered Antenna Report - GAIL Demo"), ln=True)
    pdf.set_font("Arial", size=10)
    pdf.ln(10)

    # Column Headings
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(40, 8, "Antenna ID")
    pdf.cell(40, 8, "Last Seen")
    pdf.cell(40, 8, "Status")
    pdf.cell(40, 8, "Predicted")
    pdf.cell(20, 8, "Risk", ln=True)

    # Table Rows
    pdf.set_font("Arial", size=10)
    for index, row in data.iterrows():
        pdf.cell(40, 8, safe_text(row['Antenna_ID']))
        pdf.cell(40, 8, safe_text(row['Last_Seen_Site']))
        pdf.cell(40, 8, safe_text(row['Status']))
        pdf.cell(40, 8, safe_text(row['Predicted_Location']))
        pdf.cell(20, 8, str(row['Predicted_Risk_Score']), ln=True)

    filename = f"gail_filtered_report_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    path = os.path.join("exports", filename)
    os.makedirs("exports", exist_ok=True)
    pdf.output(path)
    return path

if st.button("Download PDF"):
    if not filtered_df.empty:
        pdf_path = export_pdf(filtered_df)
        with open(pdf_path, "rb") as f:
            st.download_button("Click to Download", f, file_name=os.path.basename(pdf_path))
    else:
        st.warning("No data to export.")
