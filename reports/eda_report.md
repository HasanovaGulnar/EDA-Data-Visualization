# Exploratory Data Analysis Report

## 1. Dataset overview
- Rows: 9994
- Columns: 21
- Duplicate rows: 0

## 2. Column data types
Row ID             int64
Order ID             str
Order Date           str
Ship Date            str
Ship Mode            str
Customer ID          str
Customer Name        str
Segment              str
Country              str
City                 str
State                str
Postal Code        int64
Region               str
Product ID           str
Category             str
Sub-Category         str
Product Name         str
Sales            float64
Quantity           int64
Discount         float64
Profit           float64

## 3. Missing values
Row ID           0
Order ID         0
Order Date       0
Ship Date        0
Ship Mode        0
Customer ID      0
Customer Name    0
Segment          0
Country          0
City             0
State            0
Postal Code      0
Region           0
Product ID       0
Category         0
Sub-Category     0
Product Name     0
Sales            0
Quantity         0
Discount         0
Profit           0

## 4. Descriptive statistics
            Row ID   Postal Code         Sales     Quantity     Discount       Profit
count  9994.000000   9994.000000   9994.000000  9994.000000  9994.000000  9994.000000
mean   4997.500000  55190.379428    229.858001     3.789574     0.156203    28.656896
std    2885.163629  32063.693350    623.245101     2.225110     0.206452   234.260108
min       1.000000   1040.000000      0.444000     1.000000     0.000000 -6599.978000
25%    2499.250000  23223.000000     17.280000     2.000000     0.000000     1.728750
50%    4997.500000  56430.500000     54.490000     3.000000     0.200000     8.666500
75%    7495.750000  90008.000000    209.940000     5.000000     0.200000    29.364000
max    9994.000000  99301.000000  22638.480000    14.000000     0.800000  8399.976000

## 5. Potential outliers (IQR method)
- Row ID: 0 potential outliers (0.00%)
- Postal Code: 0 potential outliers (0.00%)
- Sales: 1167 potential outliers (11.68%)
- Quantity: 170 potential outliers (1.70%)
- Discount: 856 potential outliers (8.57%)
- Profit: 1881 potential outliers (18.82%)

## 6. Correlation matrix
               Row ID  Postal Code     Sales  Quantity  Discount    Profit
Row ID       1.000000     0.009671 -0.001359 -0.004016  0.013480  0.012497
Postal Code  0.009671     1.000000 -0.023854  0.012761  0.058443 -0.029961
Sales       -0.001359    -0.023854  1.000000  0.200795 -0.028190  0.479064
Quantity    -0.004016     0.012761  0.200795  1.000000  0.008623  0.066253
Discount     0.013480     0.058443 -0.028190  0.008623  1.000000 -0.219487
Profit       0.012497    -0.029961  0.479064  0.066253 -0.219487  1.000000

Correlation is not evidence of causation.

## Hypothesis testing
Hipotez testi teyin edilmeyib.
Datasetin meqsedine uygun hipotez evvelceden secilmelidir.

## Further investigation
- Examine missing-value mechanisms.
- Investigate potential outliers before removing them.
- Check whether duplicates are legitimate transactions.
- Consider sampling bias and data leakage.
- Interpret results in the dataset's business context.