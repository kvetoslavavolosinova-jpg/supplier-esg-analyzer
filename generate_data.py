import pandas as pd
import os

def generate_raw_data():
    print("=== GENERATING RAW AUTOMOTIVE LOGISTICS DATA ===")
    
    # Uisti sa, že priečinok data existuje
    os.makedirs("data", exist_ok=True)

    # 1. SUPPLIER MASTER DATA (Kmeňové dáta s chybami v DUNS a názvoch)
    master_data = {
        "Supplier_ID": [101, 102, 103, 104, 105, 106, 107, 108],
        "Supplier_Name": [
            " Continental AG ",      # Medzery na začiatku a konci
            "Bosch GmbH", 
            "Steel-Plast s.r.o.", 
            " Continental AG",       # Duplicitný zápis s inou medzerou
            "Kautex Textron ", 
            "ZF Group", 
            "Benteler Automotive", 
            "Hella Slovakia"
        ],
        "DUNS_Number": [
            "12-345-6789", 
            "987654321", 
            None,                    # Chýbajúce DUNS
            "12-345-6789",           # Duplicitné DUNS
            "45678",                 # Príliš krátke DUNS (neúplné)
            "88-999-1111", 
            "22-333-4444", 
            "55-666-7777"
        ],
        "Country": ["Germany", "Germany", "Slovakia", "Germany", "Czechia", "Germany", "Czechia", "Slovakia"],
        "Registration_Status": ["Complete", "Complete", "Incomplete", "Complete", "Incomplete", "Complete", None, "Complete"]
    }
    df_master = pd.DataFrame(master_data)
    df_master.to_csv("data/supplier_master_data.csv", index=False)
    print("✔ 'data/supplier_master_data.csv' created.")


    # 2. SUPPLIER ESG RATINGS (S-Rating tabuľka)
    esg_data = {
        "Supplier_ID": [101, 102, 103, 105, 106, 107, 108], # Schválne chýba ID 104 (Continental duplicita)
        "S_Rating_Score": [4.2, 4.8, 2.1, 1.8, 4.0, 3.9, 4.5], # 2.1 a 1.8 sú rizikové pod 3.0
        "ISO_14001_Certified": ["Yes", "Yes", "No", "No", "Yes", "Yes", "Yes"]
    }
    df_esg = pd.DataFrame(esg_data)
    df_esg.to_csv("data/supplier_esg_ratings.csv", index=False)
    print("✔ 'data/supplier_esg_ratings.csv' created.")


    # 3. SHIPMENT DELIVERIES (Transakčné dodávky dielov)
    shipments = {
        "Order_ID": [5001, 5002, 5003, 5004, 5005, 5006, 5007, 5008, 5009, 5010],
        "Supplier_ID": [101, 102, 103, 104, 105, 106, 107, 108, 101, 102],
        "Order_Date": [
            "2026-08-01", "2026-08-02", "2026-08-03", "2026-08-05", "2026-08-06", 
            "2026-08-10", "2026-08-12", "2026-08-14", "2026-08-15", "2026-08-16"
        ],
        "Delivery_Date": [
            "2026-08-04", "2026-08-14", "2026-08-05", "2026-08-07", "2026-08-20", 
            "2026-08-12", "2026-08-15", "2026-08-18", "2026-08-19", "2026-08-28"
        ],
        "Ordered_Qty": [1000, 2000, 500, 1200, 800, 1500, 3000, 1000, 1500, 2000],
        "Defective_Qty": [15, 22, 0, 45, 12, 5, 150, 8, 30, 10]
    }
    df_shipments = pd.DataFrame(shipments)
    df_shipments.to_csv("data/shipment_deliveries.csv", index=False)
    print("✔ 'data/shipment_deliveries.csv' created.")
    print("================================================")
    print("All datasets generated successfully!")

if __name__ == "__main__":
    generate_raw_data()