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
