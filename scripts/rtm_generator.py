#!/usr/bin/env python3
"""
Emniyet-Kritik Sistemler Icin Cift Yonlu Izlenebilirlik Matrisi (RTM) Uretici
Traceability Matrix Generator for Safety-Critical Systems
"""

import os
import re
import csv
import argparse
from pathlib import Path
from collections import defaultdict

TAG_PATTERNS = {
    'HAZ': re.compile(r'\[HAZ-([A-Za-z0-9_-]+)\]'),
    'SYS': re.compile(r'\[SYS-([A-Za-z0-9_-]+)\]'),
    'HLR': re.compile(r'\[HLR-([A-Za-z0-9_-]+)\]'),
    'LLR': re.compile(r'\[LLR-([A-Za-z0-9_-]+)\]'),
    'HWR': re.compile(r'\[HWR-([A-Za-z0-9_-]+)\]'),
    'TEST': re.compile(r'\[(?:TEST|UTEST)-([A-Za-z0-9_-]+)\]'),
}

def scan_files(directory):
    records = []
    dir_path = Path(directory)
    if not dir_path.exists():
        print(f"[UYARI] Dizin bulunamadi: {directory}")
        return records

    valid_extensions = {'.md', '.txt', '.c', '.cpp', '.h', '.hpp', '.vhd', '.v', '.py'}
    
    for path in dir_path.rglob('*'):
        if path.is_file() and path.suffix.lower() in valid_extensions:
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line_num, line in enumerate(f, start=1):
                        found_tags = {}
                        for tag_type, pattern in TAG_PATTERNS.items():
                            matches = pattern.findall(line)
                            if matches:
                                found_tags[tag_type] = [f"[{tag_type}-{m}]" for m in matches]
                        
                        if found_tags:
                            records.append({
                                'file': str(path),
                                'line': line_num,
                                'text': line.strip(),
                                'tags': found_tags
                            })
            except Exception as e:
                print(f"[HATA] Dosya okunamadi {path}: {e}")
    return records

def build_rtm(records):
    summary = defaultdict(lambda: {'count': 0, 'items': set()})
    for r in records:
        for tag_type, tag_list in r['tags'].items():
            summary[tag_type]['count'] += len(tag_list)
            summary[tag_type]['items'].update(tag_list)
    return summary

def export_csv(records, output_path):
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Dosya', 'Satir', 'Etiket Turu', 'Etiket', 'Icerik'])
        for r in records:
            for tag_type, tag_list in r['tags'].items():
                for tag in tag_list:
                    writer.writerow([r['file'], r['line'], tag_type, tag, r['text']])
    print(f"[BASARILI] RTM Raporu kaydedildi: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Emniyet-Kritik Izlenebilirlik Matrisi Uretici")
    parser.add_argument('--docs-dir', default='./modules', help="Taranacak dokuman/kod dizini")
    parser.add_argument('--output', default='rtm_report.csv', help="Cikti CSV dosyasi")
    args = parser.parse_args()

    print("=" * 65)
    print(" 🛡️ Emniyet-Kritik Sistemler - Izlenebilirlik (RTM) Denetleyicisi")
    print("=" * 65)
    print(f"Hedef Dizin : {args.docs_dir}")
    print(f"Cikti       : {args.output}\n")

    records = scan_files(args.docs_dir)
    # Eger modules bos veya yoksa README.md'yi de tarayalim
    readme_records = scan_files('.')
    combined = records + [r for r in readme_records if 'README.md' in r['file']]

    summary = build_rtm(combined)
    print(f"{'Etiket Kategorisi':<20} | {'Benzersiz Oge':<15} | {'Toplam Gecis':<12}")
    print("-" * 55)
    for cat in ['HAZ', 'SYS', 'HLR', 'LLR', 'HWR', 'TEST']:
        unique_cnt = len(summary[cat]['items'])
        total_cnt = summary[cat]['count']
        print(f"{cat:<20} | {unique_cnt:<15} | {total_cnt:<12}")
    print("-" * 55)

    export_csv(combined, args.output)

if __name__ == '__main__':
    main()
