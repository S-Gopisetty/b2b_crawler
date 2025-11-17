import csv
import json
from dataclasses import asdict

from config import CONFIG
from crawler import IndiaMartCategoryCrawler


def save_outputs(records):
    CONFIG.output_dir.mkdir(exist_ok=True)

    jsonl_path = CONFIG.output_dir / "products.jsonl"
    with jsonl_path.open("w", encoding="utf-8") as jf:
        for r in records:
            jf.write(json.dumps(asdict(r), ensure_ascii=False) + "\n")

    if not records:
        print("[WARN] No records to write to CSV.")
        return
    csv_path = CONFIG.output_dir / "products.csv"
    dict_records = []
    for r in records:
        d = asdict(r)
        d["specs"] = json.dumps(d["specs"], ensure_ascii=False)
        dict_records.append(d)

    fieldnames = list(dict_records[0].keys())
    with csv_path.open("w", newline="", encoding="utf-8") as cf:
        writer = csv.DictWriter(cf, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dict_records)

    print(f"[INFO] JSONL -> {jsonl_path}")
    print(f"[INFO] CSV   -> {csv_path}")


def main():
    crawler = IndiaMartCategoryCrawler()
    records = crawler.crawl()
    save_outputs(records)


if __name__ == "__main__":
    main()
