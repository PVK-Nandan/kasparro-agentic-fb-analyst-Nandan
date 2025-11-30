# Data Directory

## Expected Data Format

The system expects a tab-separated CSV file with the following columns:

### Required Columns

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| campaign_name | string | Campaign identifier | "Men ComfortMax Launch" |
| adset_name | string | Ad set identifier | "Adset-1 Retarget" |
| date | string | Performance date | "01-01-2025" (DD-MM-YYYY) |
| spend | float | Ad spend amount | 640.09 |
| impressions | int | Number of impressions | 235597 |
| clicks | int | Number of clicks | 4313 |
| ctr | float | Click-through rate | 0.0183 |
| purchases | int | Number of purchases | 80 |
| revenue | float | Revenue generated | 1514.28 |
| roas | float | Return on ad spend | 2.37 |
| creative_type | string | Creative format | "Image", "Video", "UGC", "Carousel" |
| creative_message | string | Ad copy text | "Breathable organic cotton..." |
| audience_type | string | Audience segment | "Broad", "Lookalike", "Retargeting" |
| platform | string | Ad platform | "Facebook", "Instagram" |
| country | string | Target country | "US", "UK", "IN" |

## Data Setup Options

### Option 1: Use Sample Data (Default)

A sample dataset is included in this directory. To use it:

```bash
# Already configured in config/config.yaml
use_sample_data: true
data_path: "data/sample_fb_ads.csv"
```

### Option 2: Use Full Dataset

Place your full dataset file and configure the path:

```bash
# Via environment variable (recommended)
export DATA_CSV=/path/to/your/synthetic_fb_ads_undergarments.csv

# Or edit config/config.yaml
use_sample_data: false
data_path: "/path/to/your/data.csv"
```

## Data Quality Notes

### Missing Values
The system handles missing values gracefully:
- Missing `spend`: Row excluded from spend-based calculations
- Missing `clicks`: CTR calculation skipped
- Missing `revenue`: ROAS calculation skipped

### Data Validation
The system performs these validations:
- Date parsing and conversion
- Numeric type conversion with error handling
- Minimum spend threshold filtering ($50 default)
- Outlier detection for key metrics

### Sample Size
- Minimum recommended: 1000 rows
- Date range: At least 14 days for trend analysis
- Minimum campaigns: 3+

## File Format

- **Separator**: Tab (`\t`)
- **Encoding**: UTF-8
- **Date Format**: DD-MM-YYYY
- **Decimal Separator**: Period (.)
- **No header row issues**: First row must be column names

## Testing Your Data

To verify your data loads correctly:

```python
import pandas as pd

df = pd.read_csv('your_file.csv', sep='\t')
print(f"Rows: {len(df)}")
print(f"Columns: {df.columns.tolist()}")
print(df.head())
```

Expected output should show all 15 columns with proper data types.