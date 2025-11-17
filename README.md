# **B2B Product Crawler – IndiaMART Category Scraper**

This project is a modular Python-based web crawler designed to extract structured product data from **IndiaMART** category listings.

It automatically:

1. Fetches a **category (listing) page**
2. Extracts all **product detail URLs**
3. Opens each product URL
4. Scrapes full product information
5. Saves the data into **JSONL** and **CSV** formats

This implementation is ideal for academic submissions, data engineering practice, and B2B marketplace data extraction demonstrations.

---

## 🚀 Features

### ✔ Category → Product Link Extraction  
Automatically collects product detail links from:

https://dir.indiamart.com/impcat/paper-cup-making-machine.html


### ✔ Product Page Parsing  
Extracts structured product details including:

- Product name  
- Price (text + numeric value)  
- Currency  
- City & full address (best-effort match)  
- Specification table (key–value pairs)  
- Product description  
- Company name  
- Company website  
- Contact person  
- GST number  
- Timestamp (`scraped_at`)

### ✔ Multiple Output Formats  
Crawler saves results to:

- `output/products.jsonl`
- `output/products.csv`

### ✔ Resilient HTTPS Fetcher  
Includes retry logic, backoff timing, and browser-like headers to avoid blocking.

---

## 📁 Project Structure

B2B_CRAWLER/
│
├── config.py
├── fetcher.py
├── parser_base.py
├── parser_indiamart.py
├── crawler.py
├── main.py
├── test_extract_links.py # (optional debugging tool)
├── requirements.txt
├── output/
└── README.md


---

## 🛠 Installation

### 1. Navigate to project directory
```bash
cd B2B_CRAWLER

pip install -r requirements.txt
python --version

python main.py


## Summary Insights (for Report)

- **Price Distribution**:  
  Most paper cup machines cluster between certain price bands (see histogram).  
  A few very high-priced machines form a long right tail → these may be high-end, fully automatic machines.

- **Supplier Geography**:  
  Top contributing cities and states include known industrial hubs.  
  This suggests manufacturing clusters for packaging/printing machinery.

- **Product Naming Patterns**:  
  Frequent keywords include *"automatic"*, *"semi"*, *"cup"*, *"machine"*, *"making"*, and numeric capacities.  
  This indicates buyers likely compare **automation level** and **throughput**.

- **Specification Patterns**:  
  Most common technical attributes: *Automation Grade*, *Phase*, *Capacity*, *Power*, *Voltage*, etc.  
  These are critical decision variables in B2B buying.

- **Data Quality Issues**:  
  - Some products have missing or non-numeric prices.  
  - Location fields are sometimes incomplete or inconsistently formatted.  
  - Specs are unevenly filled — some products list rich details, others very few.  

These observations can be used to propose **data cleaning steps**, **standardization of attributes**, and further **price benchmarking** or **market segmentation**.
