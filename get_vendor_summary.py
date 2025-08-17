import pandas as pd
import sqlite3
import logging
from ingestion_db import ingest_db

logging.basicConfig(
    filename='logs/get_vendor_summary.log',
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

def create_vendor_summary(conn):
    """This function will add different tables  get overall summary and adding new columns in the resultant data"""
    vendor_sales_summary = pd.read_sql(""" WITH FreightSummary AS
(SELECT
VendorNumber,
SUM(Freight) AS "FreightCost" 
FROM vendor_invoice
GROUP BY "VendorNumber"),

PurchaseSummary AS (
SELECT 
    p.VendorName,
    p.VendorNumber,
    p.Brand,
    p.Description,
    p.PurchasePrice,
    pp.Volume,
    pp.Price AS "ActualPrice",
    SUM(p.Quantity) AS TotalPurchaseQuantity,
    SUM(p.Dollars) AS TotalPurchaseDollars
FROM purchases p
JOIN purchase_prices pp
    ON p.Brand = pp.Brand
WHERE p.PurchasePrice > 0
GROUP BY p.VendorName, p.VendorNumber, p.Brand,p.Description,p.PurchasePrice,pp.Volume,pp.Price
),

SalesSummary AS (
SELECT
VendorNo,
Brand,
SUM(SalesDollars) as TotalSalesDollars,
SUM(SalesPrice) as TotalSalesPrice,
SUM(ExciseTax) as TotalExciseTax,
SUM(SalesQuantity) as TotalSalesQuantity
FROM Sales
Group BY VendorNo, Brand
)

SELECT 
ps.VendorNumber,
ps.VendorName,
ps.Brand,
ps.Description,
ps.PurchasePrice,
ps.ActualPrice,
ps.Volume,
ps.TotalPurchaseQuantity,
ps.TotalPurchaseDollars,
ss.TotalSalesQuantity,
ss.TotalSalesDollars,
ss.TotalSalesPrice,
ss.TotalExciseTax,
fs.FreightCost
FROM PurchaseSummary ps
LEFT JOIN SalesSummary ss
ON ps.VendorNumber = ss.VendorNo
AND ps.Brand = ss.Brand
LEFT JOIN FreightSummary fs
ON ps.VendorNumber = fs.VendorNumber
ORDER BY TotalPurchaseDollars DESC
""",conn)
    
    return vendor_sales_summary

def clean_data(df):
    # It will clear inconsistencies 
 
    # Change the dtype of Volume 
    vendor_sales_summary['Volume'] = vendor_sales_summary['Volume'].astype('float64')
    # Removing wide spaces from Vendor Name and Description
    vendor_sales_summary['VendorName'].str.strip()
    vendor_sales_summary['Description'].str.strip()
    # Replace the null values with 0
    vendor_sales_summary.fillna(0, inplace = True)
    
    # Creating some new columns
    vendor_sales_summary['Gross Profit'] = vendor_sales_summary['TotalSalesDollars'] - vendor_sales_summary['TotalPurchaseDollars']
    vendor_sales_summary['Profit Margin'] = (vendor_sales_summary['Gross Profit']/vendor_sales_summary['TotalSalesDollars'])*100
    vendor_sales_summary['Stock TurnOver'] = vendor_sales_summary['TotalSalesQuantity']/vendor_sales_summary['TotalPurchaseQuantity']
    vendor_sales_summary['Sales PurchaseRatio']=vendor_sales_summary['TotalSalesDollars']/vendor_sales_summary['TotalPurchaseDollars']
    
    return df

if __name__ == '__main__':
    # creating database connection
    conn = sqlite3.connect('inventory.db')
    
    logging.info('Creating Vendor Summary Table....')
    summary_df = create_vendor_summary(conn)
    logging.info(summary_df.head())
    
    logging.info("Cleaning Data...")
    clean_df = clean_data(summary_df)
    logging.info(clean_df.head())
    
    logging.info('ingesting Data...')
    ingest_db(clean_df,'vendor_sales_summary',conn)
    logging.info("Completed")
    
    
    
    
    