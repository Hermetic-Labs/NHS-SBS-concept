import pandas as pd
import json
import os
import datetime

# Paths
EXCEL_PATH = r"d:\Minimax\docs\Bidder_Copy_Clarification_Qs_Healthcare_AI_SBS10525_BATCH 2_03_06_26.xlsx"
OUTPUT_PATH = r"d:\Minimax\nhs_sbs_cq_portal\data\cq_index.json"

def ingest_excel():
    print(f"Reading {EXCEL_PATH}...")
    try:
        # Read the Excel file. We might need to skip rows if the header isn't row 0.
        # Assuming the first row is headers for now.
        df = pd.read_excel(EXCEL_PATH)
        
        # Clean column names
        df.columns = [str(c).strip().replace('\n', ' ').replace('\r', '') for c in df.columns]
        
        # We don't know the exact column names, but we expect something like "Question", "Answer", "Category", "Sub-category", "Supplier ID"
        # We will convert the entire dataframe into a list of dictionaries, preserving all columns.
        
        records = df.to_dict(orient="records")
        
        cleaned_records = []
        for i, row in enumerate(records):
            # Only keep rows that have some value in at least one column
            if any(pd.notna(v) and str(v).strip() != "" for v in row.values()):
                clean_row = {}
                for k, v in row.items():
                    if pd.notna(v):
                        if isinstance(v, (pd.Timestamp, datetime.datetime, datetime.date)):
                            clean_row[k] = v.isoformat()
                        else:
                            clean_row[k] = v
                    else:
                        clean_row[k] = None
                # Add an internal ID
                clean_row["_id"] = f"CQ-B2-{i+1:04d}"
                cleaned_records.append(clean_row)
        
        print(f"Processed {len(cleaned_records)} valid clarification questions.")
        
        # Save to JSON
        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            json.dump(cleaned_records, f, indent=2, ensure_ascii=False)
            
        print(f"Index successfully written to {OUTPUT_PATH}")
        
    except Exception as e:
        print(f"Error during ingestion: {e}")

if __name__ == "__main__":
    ingest_excel()
