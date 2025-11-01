import os, io, datetime as dt, sys, re
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import boto3
import argparse

# --------- CONFIG ---------
parser = argparse.ArgumentParser()
parser.add_argument("--excel-file", required=False, default=os.getenv("EXCEL_FILE"))
parser.add_argument("--lake-bucket", required=False, default=os.getenv("LAKE_BUCKET"))
parser.add_argument("--region", required=False, default=os.getenv("AWS_REGION","us-west-2"))
parser.add_argument("--only", help="Comma-separated sheet keys from SHEET_TABLE_MAP to upload")
args = parser.parse_args()

EXCEL_FILE  = args.excel_file
LAKE_BUCKET = args.lake_bucket
AWS_REGION  = args.region
ONLY        = set([s.strip() for s in args.only.split(",")]) if args.only else None

# Map workbook sheets -> target table names (snake_case)
SHEET_TABLE_MAP = {
    "win_history":               "win_history",
    "regular_season":           "regular_season",
    "matchup_data":              "matchup_data",
    "lineup_efficiency_weekly":  "lineup_efficiency_weekly",
    "player_details_by_team":    "player_details_by_team",
    "player_total_points":       "player_total_points",
    "playoffs_legacy":           "playoffs_legacy",
    "auction_drafts":            "auction_drafts",
    "member":                    "member"
}

# Define expected columns for each table to drop extras
TABLE_COLUMN_WHITELIST = {
    "win_history": [
        "championship_year",
        "place",
        "member_id", 
        "member",
        "money_won"
    ],
    # Add other tables as needed
}
# --------------------------

def to_snake(s: str) -> str:
    s = re.sub(r"[^\w]+", "_", s)
    s = re.sub(r"_{2,}", "_", s)
    return s.strip("_").lower()

def write_parquet_to_s3(df: pd.DataFrame, bucket: str, key: str, s3):
    """Write DataFrame to S3 as Parquet"""
    table = pa.Table.from_pandas(df, preserve_index=False)
    buf = io.BytesIO()
    pq.write_table(table, buf, compression="snappy")
    s3.put_object(Bucket=bucket, Key=key, Body=buf.getvalue())

def normalize_df(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names and types"""
    df = df.copy()

    def to_snake(s: str) -> str:
        s = re.sub(r"[^\w]+", "_", s or "")
        s = re.sub(r"_{2,}", "_", s)
        return s.strip("_").lower() or "col"

    # snake_case all columns
    cols = [to_snake(str(c)) for c in df.columns]

    # enforce uniqueness by appending __2, __3, ...
    seen = {}
    new_cols = []
    for c in cols:
        base = c or "col"
        name = base
        i = 2
        while name in seen:
            name = f"{base}__{i}"
            i += 1
        seen[name] = True
        new_cols.append(name)
    df.columns = new_cols

    # light type coercions
    for c in ["season","week","points","points_for","points_against","margin","price","round","pick","year"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    return df

def clean_dataframe(df: pd.DataFrame, table_name: str) -> pd.DataFrame:
    """Apply table-specific cleaning rules"""
    
    # First normalize columns
    df = normalize_df(df)
    
    # Check if this table has a whitelist
    if table_name in TABLE_COLUMN_WHITELIST:
        whitelist = TABLE_COLUMN_WHITELIST[table_name]
        
        # Find columns that match the whitelist (case-insensitive)
        whitelist_lower = [c.lower() for c in whitelist]
        keep_cols = [c for c in df.columns if c.lower() in whitelist_lower]
        
        # Filter to only keep whitelisted columns
        df = df[keep_cols]
        
        print(f"    ℹ Applied column whitelist - kept {len(keep_cols)}/{len(df.columns)} columns")
    
    # Remove columns that look like Excel artifacts
    df = df.loc[:, ~df.columns.str.contains('^unnamed', case=False, na=False)]
    
    # Remove completely empty columns
    df = df.dropna(axis=1, how='all')
    
    # Remove duplicate columns (keep first occurrence)
    df = df.loc[:, ~df.columns.duplicated()]
    
    return df


def main():
    if not EXCEL_FILE or not LAKE_BUCKET:
        print("Set EXCEL_FILE and LAKE_BUCKET environment variables.", file=sys.stderr)
        sys.exit(1)

    s3 = boto3.client("s3", region_name=AWS_REGION)
    today = dt.date.today().isoformat()

    xl = pd.ExcelFile(EXCEL_FILE)
    available = {s.lower(): s for s in xl.sheet_names}

    uploaded = []
    skipped = []

    for sheet_req, table_name in SHEET_TABLE_MAP.items():
        if ONLY and sheet_req not in ONLY:
            continue
            
        # resolve case-insensitive sheet name
        sheet_real = available.get(sheet_req.lower())
        if not sheet_real:
            # try loose match (ignore underscores)
            norm_req = sheet_req.replace("_","").lower()
            candidates = [s for s in xl.sheet_names if norm_req in s.replace("_","").lower()]
            sheet_real = candidates[0] if candidates else None

        if not sheet_real:
            skipped.append((sheet_req, "sheet not found"))
            continue

        print(f"Processing sheet: {sheet_real}")
        df = xl.parse(sheet_real)
        
        if df.empty:
            skipped.append((sheet_real, "empty sheet"))
            continue

        # Apply cleaning
        df = clean_dataframe(df, table_name)
        
        # Add metadata columns
        df["source_system"] = "excel_legacy"
        
        # DO NOT add imported_on as a column (used for partitioning only)
        
        print(f"    Final schema: {len(df)} rows × {len(df.columns)} columns")
        print(f"    Columns: {list(df.columns)}")

        # Write to S3 with partition path
        prefix = f"staging/legacy_excel/{to_snake(table_name)}/imported_on={today}"
        key    = f"{prefix}/part-0000.parquet"
        
        write_parquet_to_s3(df, LAKE_BUCKET, key, s3)
        uploaded.append((sheet_real, key, len(df)))

    print("\n" + "="*70)
    print("Uploaded:")
    for s, k, n in uploaded:
        print(f"  sheet='{s}' -> s3://{LAKE_BUCKET}/{k}  rows={n}")

    if skipped:
        print("\nSkipped:")
        for s, why in skipped:
            print(f"  sheet='{s}' reason={why}")
    
    print("\n" + "="*70)
    print("Next steps:")
    print("1. Run: aws glue start-crawler --name ff-data-project-staging-legacy-excel")
    print("2. Wait for crawler to complete (2-5 minutes)")
    print("3. Test in Athena: SELECT * FROM ff-data-project_raw.stg_win_history LIMIT 10")
    print("="*70)

if __name__ == "__main__":
    main()