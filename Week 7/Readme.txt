| File Type             | Filename Pattern                   | Target Table    | Additional Columns | Notes                                       |
| --------------------- | ---------------------------------- | --------------- | ------------------ | ------------------------------------------- |
| CUST\_MSTR            | `CUST_MSTR_YYYYMMDD.csv`           | `CUST_MSTR`     | `Date`             | Extract `YYYY-MM-DD` from filename          |
| master\_child\_export | `master_child_export-YYYYMMDD.csv` | `master_child`  | `Date`, `DateKey`  | `Date`: `YYYY-MM-DD`, `DateKey`: `YYYYMMDD` |
| H\_ECOM\_ORDER        | `H_ECOM_ORDER.csv` (no date)       | `H_ECOM_Orders` | None               | Direct load                                 |
