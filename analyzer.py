import pandas as pd
import matplotlib.pyplot as plt
import os

# Nastavenie matplotlib pre bezpečné ukladanie na Macu
import matplotlib
matplotlib.use('Agg')

def load_and_merge_data():
    print("=== SUPPLIER COMPLIANCE & ESG ANALYZER ===")
    print("[INFO] Loading raw datasets...")
    try:
        df_master = pd.read_csv("data/supplier_master_data.csv")
        df_esg = pd.read_csv("data/supplier_esg_ratings.csv")
        df_shipments = pd.read_csv("data/shipment_deliveries.csv")
        print("✔ All datasets loaded successfully!")
        return pd.merge(pd.merge(df_shipments, df_master, on="Supplier_ID", how="left"), df_esg, on="Supplier_ID", how="left")
    except FileNotFoundError as e:
        print(f"❌ Error: Could not find data files. Details: {e}")
        return None


def clean_data(df):
    print("\n=== STEP 4: CLEANING & STANDARDIZING DATA ===")
    df["Supplier_Name"] = df["Supplier_Name"].str.strip()
    df["Registration_Status"] = df["Registration_Status"].fillna("Unknown")
    df["DUNS_Number"] = df["DUNS_Number"].astype(str).str.strip().replace("nan", None)
    print("✔ Data cleaning completed!")
    return df


def validate_duns(duns):
    if pd.isna(duns) or duns is None:
        return False
    clean_duns = str(duns).replace("-", "").replace(" ", "")
    return len(clean_duns) == 9 and clean_duns.isdigit()


def validate_data(df):
    print("\n=== STEP 5: VALIDATING DATA & CREATING QUALITY FLAGS ===")
    df["Is_DUNS_Valid"] = df["DUNS_Number"].apply(validate_duns)
    df["Is_Reg_Complete"] = df["Registration_Status"] == "Complete"
    df["Has_Data_Quality_Issue"] = ~(df["Is_DUNS_Valid"] & df["Is_Reg_Complete"])
    print("✔ Data validation completed!")
    return df


def calculate_kpis(df):
    print("\n=== STEP 6: CALCULATING LOGISTICS & QUALITY KPIs ===")
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    df["Delivery_Date"] = pd.to_datetime(df["Delivery_Date"])
    df["Actual_Lead_Time"] = (df["Delivery_Date"] - df["Order_Date"]).dt.days
    
    target_lead_time = 5
    df["Delay_Days"] = (df["Actual_Lead_Time"] - target_lead_time).clip(lower=0)
    df["Is_On_Time"] = df["Actual_Lead_Time"] <= target_lead_time
    
    supplier_kpi = df.groupby(["Supplier_ID", "Supplier_Name"]).agg(
        Total_Orders=("Order_ID", "count"),
        Avg_Lead_Time=("Actual_Lead_Time", "mean"),
        On_Time_Shipments=("Is_On_Time", "sum"),
        Total_Ordered_Qty=("Ordered_Qty", "sum"),
        Total_Defective_Qty=("Defective_Qty", "sum"),
        S_Rating_Score=("S_Rating_Score", "first"),
        ISO_14001_Certified=("ISO_14001_Certified", "first"),
        Has_Data_Quality_Issue=("Has_Data_Quality_Issue", "first"),
        Country=("Country", "first")
    ).reset_index()
    
    supplier_kpi["On_Time_Delivery_Pct"] = (supplier_kpi["On_Time_Shipments"] / supplier_kpi["Total_Orders"]) * 100
    supplier_kpi["Defect_Rate_Pct"] = (supplier_kpi["Total_Defective_Qty"] / supplier_kpi["Total_Ordered_Qty"]) * 100
    
    print("✔ Logistics & Quality KPIs calculated successfully!")
    return df, supplier_kpi


def evaluate_supplier_risk(row):
    if ((pd.notna(row["S_Rating_Score"]) and row["S_Rating_Score"] < 3.0) or 
        row["Defect_Rate_Pct"] > 4.0 or 
        row["On_Time_Delivery_Pct"] < 50.0):
        return "High Risk"
    
    elif (pd.isna(row["S_Rating_Score"]) or 
          row["S_Rating_Score"] < 4.0 or 
          row["Has_Data_Quality_Issue"] == True or 
          row["ISO_14001_Certified"] == "No"):
        return "Medium Risk"
    
    return "Low Risk"


def categorize_risk(kpi_df):
    print("\n=== STEP 7: EVALUATING S-RATING & SUPPLIER RISK CATEGORIES ===")
    kpi_df["Risk_Category"] = kpi_df.apply(evaluate_supplier_risk, axis=1)
    print("✔ Risk categorization completed!")
    return kpi_df


def generate_visualizations(kpi_df):
    print("\n=== STEP 8: GENERATING VISUALIZATIONS (Matplotlib) ===")
    os.makedirs("plots", exist_ok=True)
    
    plt.figure(figsize=(10, 6))
    valid_esg = kpi_df[kpi_df["S_Rating_Score"].notna()]
    
    colors = []
    for risk in valid_esg["Risk_Category"]:
        if risk == "High Risk":
            colors.append("#d9534f")
        elif risk == "Medium Risk":
            colors.append("#f0ad4e")
        else:
            colors.append("#5cb85c")
            
    plt.bar(valid_esg["Supplier_Name"], valid_esg["S_Rating_Score"], color=colors, edgecolor='black', alpha=0.85)
    plt.axhline(y=3.0, color='red', linestyle='--', linewidth=1.5, label='Min. Compliance Limit (3.0)')
    
    plt.title("Supplier ESG S-Rating Scores (Higher is Better)", fontsize=14, fontweight='bold', pad=15)
    plt.ylabel("S-Rating Score", fontsize=12)
    plt.xlabel("Supplier Name", fontsize=12)
    plt.xticks(rotation=30, ha='right')
    plt.ylim(0, 5.5)
    plt.grid(axis='y', linestyle=':', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    
    plot_path = "plots/supplier_s_rating_chart.png"
    plt.savefig(plot_path, dpi=150)
    plt.close()
    print(f"✔ Chart successfully saved to '{plot_path}'")


def export_and_report(kpi_df):
    print("\n=== STEP 9: EXPORTING DATA & GENERATING BUSINESS REPORT ===")
    
    # 1. Export vyčistených výsledkov do nového CSV pre budúce Power BI
    export_path = "data/supplier_compliance_report.csv"
    kpi_df.to_csv(export_path, index=False)
    print(f"✔ Cleaned compliance report exported to '{export_path}'")
    
    # 2. Generovanie štatistík pre biznis report
    total_suppliers = len(kpi_df)
    high_risk_count = len(kpi_df[kpi_df["Risk_Category"] == "High Risk"])
    med_risk_count = len(kpi_df[kpi_df["Risk_Category"] == "Medium Risk"])
    low_risk_count = len(kpi_df[kpi_df["Risk_Category"] == "Low Risk"])
    
    # Najhorší dodávatelia podľa logistiky a kvality
    worst_otd = kpi_df.sort_values(by="On_Time_Delivery_Pct").iloc[0]
    worst_quality = kpi_df.sort_values(by="Defect_Rate_Pct", ascending=False).iloc[0]

    # Výpis biznis správy do terminálu
    print("\n" + "="*50)
    print("     EXECUTIVE SUPPLY CHAIN COMPLIANCE REPORT     ")
    print("="*50)
    print(f"Total Suppliers Analyzed: {total_suppliers}")
    print(f"🔴 High Risk Partners:   {high_risk_count} (Immediate Action Required)")
    print(f"🟡 Medium Risk Partners: {med_risk_count} (Under Monitoring)")
    print(f"🟢 Low Risk Partners:    {low_risk_count} (Approved)")
    print("-"*50)
    print("KEY CRITICAL FINDINGS:")
    print(f"1. Logistics Bottleneck: '{worst_otd['Supplier_Name']}' has the worst On-Time Delivery rate ({worst_otd['On_Time_Delivery_Pct']}%).")
    print(f"2. Quality Issue:        '{worst_quality['Supplier_Name']}' has the highest Defect Rate ({worst_quality['Defect_Rate_Pct']:.2f}%).")
    
    high_risk_names = kpi_df[kpi_df["Risk_Category"] == "High Risk"]["Supplier_Name"].tolist()
    print(f"3. High Risk Action List: Escalate contract reviews for: {', '.join(high_risk_names)}")
    print("="*50)


if __name__ == "__main__":
    raw_df = load_and_merge_data()
    if raw_df is not None:
        cleaned_df = clean_data(raw_df)
        validated_df = validate_data(cleaned_df)
        final_df, kpi_df = calculate_kpis(validated_df)
        final_compliance_df = categorize_risk(kpi_df)
        generate_visualizations(final_compliance_df)
        export_and_report(final_compliance_df)