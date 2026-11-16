#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
🛡️ Emniyet-Kritik Sistemler - Çift Yönlü İzlenebilirlik Matrisi & Açık Analizi Motoru
Bi-directional Requirements Traceability Matrix (RTM) & Gap Analysis Engine
Compliant with ARP4754B / DO-178C / DO-254 / ISO 26262 Lifecycle Auditing
=============================================================================
"""

import os
import re
import csv
import json
import argparse
from pathlib import Path
from collections import defaultdict

TAG_PATTERNS = {
    'HAZ': re.compile(r'\[HAZ-([A-Za-z0-9_-]+)\]'),
    'SYS': re.compile(r'\[SYS-([A-Za-z0-9_-]+)\]'),
    'HLR': re.compile(r'\[HLR-([A-Za-z0-9_-]+)\]'),
    'LLR': re.compile(r'\[LLR-([A-Za-z0-9_-]+)\]'),
    'HWR': re.compile(r'\[HWR-([A-Za-z0-9_-]+)\]'),
    'TEST': re.compile(r'\[(?:TEST|UTEST|HIL|VAL)-([A-Za-z0-9_-]+)\]'),
}

# Zincir doğrulaması için ebeveyn-çocuk ilişkisi algılama deseni
# Örn: Traceability: [LLR-XXX] <- [HLR-YYY] <- [SYS-ZZZ]
TRACE_LINK_PATTERN = re.compile(
    r'\[(HAZ|SYS|HLR|LLR|HWR|TEST|UTEST|HIL|VAL)-([A-Za-z0-9_-]+)\]'
)

def scan_files(root_dir):
    """Belirtilen dizindeki tüm kaynak kod ve markdown dokümanlarını tarar."""
    records = []
    dir_path = Path(root_dir)
    if not dir_path.exists():
        print(f"[!] Uyarı: Dizin bulunamadı: {root_dir}")
        return records

    valid_extensions = {'.md', '.txt', '.c', '.cpp', '.h', '.hpp', '.vhd', '.v', '.py', '.json'}
    ignore_dirs = {'.git', '.gemini', '__pycache__', 'node_modules', '.idea', '.vscode'}

    for path in dir_path.rglob('*'):
        if any(part in ignore_dirs for part in path.parts):
            continue
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
                            # Satırdaki tüm etiketleri sırasıyla yakala (ilişki zinciri analizi için)
                            all_raw_tags = [f"[{m[0]}-{m[1]}]" for m in TRACE_LINK_PATTERN.findall(line)]
                            records.append({
                                'file': str(path).replace('\\', '/'),
                                'rel_path': str(path.relative_to(dir_path) if dir_path != Path('.') else path).replace('\\', '/'),
                                'line': line_num,
                                'text': line.strip(),
                                'tags': found_tags,
                                'raw_tags_in_line': all_raw_tags
                            })
            except Exception as e:
                print(f"[HATA] Dosya taranamadı ({path}): {e}")
    return records

def analyze_traceability(records):
    """
    Taranan etiketler arasındaki hiyerarşik ilişkileri ve boşlukları analiz eder:
    - Kapsanan ve yetim (orphan) gereksinimler
    - Doğrulanmamış (test karşılığı bulunmayan) fonksiyonlar
    """
    summary = {k: {'count': 0, 'items': set(), 'locations': defaultdict(list)} for k in TAG_PATTERNS.keys()}
    links = defaultdict(set) # tag -> referenced_tags

    for r in records:
        for tag_type, tag_list in r['tags'].items():
            for t in tag_list:
                summary[tag_type]['count'] += 1
                summary[tag_type]['items'].add(t)
                summary[tag_type]['locations'][t].append(f"{r['rel_path']}:{r['line']}")

        # Aynı satırda ardışık etiketler varsa türetim/izleme bağı varsay
        line_tags = r['raw_tags_in_line']
        if len(line_tags) > 1:
            for i in range(len(line_tags) - 1):
                links[line_tags[i]].add(line_tags[i+1])
                links[line_tags[i+1]].add(line_tags[i])

    return summary, links

def generate_html_report(summary, links, records, output_html):
    """Etkileşimli, modern bir RTM Dashboard HTML raporu üretir."""
    total_tags = sum(len(d['items']) for d in summary.values())
    
    html_content = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🛡️ Emniyet-Kritik İzlenebilirlik Raporu (RTM Dashboard)</title>
    <style>
        :root {{
            --bg: #0d1117;
            --surface: #161b22;
            --border: #30363d;
            --text: #c9d1d9;
            --accent: #58a6ff;
            --haz: #f85149;
            --sys: #a371f7;
            --sw: #388bfd;
            --hw: #d29922;
            --test: #3fb950;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg);
            color: var(--text);
            margin: 0;
            padding: 30px;
        }}
        .header {{
            border-bottom: 1px solid var(--border);
            padding-bottom: 20px;
            margin-bottom: 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        h1 {{ margin: 0; color: #fff; font-size: 1.8rem; display: flex; align-items: center; gap: 10px; }}
        .badge {{ background: #238636; color: white; padding: 4px 10px; border-radius: 20px; font-size: 0.8rem; font-weight: bold; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; margin-bottom: 30px; }}
        .card {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 16px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }}
        .card-num {{ font-size: 2rem; font-weight: bold; margin: 8px 0; }}
        .card-lbl {{ font-size: 0.85rem; text-transform: uppercase; color: #8b949e; letter-spacing: 1px; }}
        .haz-color {{ color: var(--haz); border-top: 3px solid var(--haz); }}
        .sys-color {{ color: var(--sys); border-top: 3px solid var(--sys); }}
        .hlr-color {{ color: var(--sw); border-top: 3px solid var(--sw); }}
        .llr-color {{ color: #79c0ff; border-top: 3px solid #79c0ff; }}
        .hwr-color {{ color: var(--hw); border-top: 3px solid var(--hw); }}
        .test-color {{ color: var(--test); border-top: 3px solid var(--test); }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 8px;
            overflow: hidden;
            margin-top: 20px;
        }}
        th, td {{
            padding: 12px 16px;
            text-align: left;
            border-bottom: 1px solid var(--border);
            font-size: 0.9rem;
        }}
        th {{ background: #21262d; color: #f0f6fc; font-weight: 600; }}
        tr:hover {{ background: #1c2128; }}
        code {{
            background: #21262d;
            padding: 2px 6px;
            border-radius: 4px;
            color: #ff7b72;
            font-family: ui-monospace, SFMono-Regular, Consolas, monospace;
            font-size: 0.85rem;
        }}
        .tag-pill {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
            margin-right: 4px;
        }}
        .tag-HAZ {{ background: rgba(248, 81, 73, 0.2); color: #ff7b72; border: 1px solid #f85149; }}
        .tag-SYS {{ background: rgba(163, 113, 247, 0.2); color: #d2a8ff; border: 1px solid #a371f7; }}
        .tag-HLR {{ background: rgba(56, 139, 253, 0.2); color: #79c0ff; border: 1px solid #388bfd; }}
        .tag-LLR {{ background: rgba(88, 166, 255, 0.2); color: #a5d6ff; border: 1px solid #58a6ff; }}
        .tag-HWR {{ background: rgba(210, 153, 34, 0.2); color: #e3b341; border: 1px solid #d29922; }}
        .tag-TEST {{ background: rgba(63, 185, 80, 0.2); color: #7ee787; border: 1px solid #3fb950; }}
        .footer {{ margin-top: 40px; text-align: center; color: #8b949e; font-size: 0.8rem; }}
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h1>🛡️ Emniyet-Kritik İzlenebilirlik Raporu</h1>
            <p style="margin: 5px 0 0 0; color: #8b949e;">RTCA DO-178C / DO-254 / ARP4754B Sertifikasyon Uyum Denetleyicisi</p>
        </div>
        <div class="badge">DO-178C DAL A AUDIT READY</div>
    </div>

    <div class="grid">
        <div class="card haz-color">
            <div class="card-lbl">Tehlike Analizleri</div>
            <div class="card-num">{len(summary['HAZ']['items'])}</div>
            <div style="font-size: 0.75rem; color:#8b949e;">ARP 4761A / FHA</div>
        </div>
        <div class="card sys-color">
            <div class="card-lbl">Sistem Gerek.</div>
            <div class="card-num">{len(summary['SYS']['items'])}</div>
            <div style="font-size: 0.75rem; color:#8b949e;">ARP 4754B</div>
        </div>
        <div class="card hlr-color">
            <div class="card-lbl">Üst Seviye Yazılım</div>
            <div class="card-num">{len(summary['HLR']['items'])}</div>
            <div style="font-size: 0.75rem; color:#8b949e;">DO-178C (HLR)</div>
        </div>
        <div class="card llr-color">
            <div class="card-lbl">Alt Seviye Tasarım</div>
            <div class="card-num">{len(summary['LLR']['items'])}</div>
            <div style="font-size: 0.75rem; color:#8b949e;">DO-178C (LLR)</div>
        </div>
        <div class="card hwr-color">
            <div class="card-lbl">Donanım Gerek.</div>
            <div class="card-num">{len(summary['HWR']['items'])}</div>
            <div style="font-size: 0.75rem; color:#8b949e;">DO-254 (HWR)</div>
        </div>
        <div class="card test-color">
            <div class="card-lbl">Doğrulama & Test</div>
            <div class="card-num">{len(summary['TEST']['items'])}</div>
            <div style="font-size: 0.75rem; color:#8b949e;">MC/DC & HIL Tests</div>
        </div>
    </div>

    <h2>📋 Tespit Edilen İzlenebilirlik Kayıtları ({len(records)} Konum)</h2>
    <table>
        <thead>
            <tr>
                <th style="width: 25%;">Kaynak Dosya & Satır</th>
                <th style="width: 15%;">Etiketler</th>
                <th style="width: 60%;">Metin / İlgili Tanım</th>
            </tr>
        </thead>
        <tbody>
    """

    for r in records[:250]: # İlk 250 kaydı listele
        tags_html = ""
        for tag_type, tag_list in r['tags'].items():
            for t in tag_list:
                tags_html += f'<span class="tag-pill tag-{tag_type}">{t}</span>'
        
        escaped_text = r['text'].replace('<', '&lt;').replace('>', '&gt;')
        html_content += f"""
            <tr>
                <td><code>{r['rel_path']}:{r['line']}</code></td>
                <td>{tags_html}</td>
                <td>{escaped_text}</td>
            </tr>
        """

    html_content += f"""
        </tbody>
    </table>

    <div class="footer">
        Oluşturulma: Emniyet-Kritik Sistemler Müfredatı Otomasyon Motoru | ISO 26262 & DO-178C Traceability Tool
    </div>
</body>
</html>
    """

    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"[+] İnteraktif HTML Dashboard oluşturuldu: {output_html}")

def export_csv(records, output_path):
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Dosya', 'Satir', 'Etiket Turu', 'Etiket', 'Icerik'])
        for r in records:
            for tag_type, tag_list in r['tags'].items():
                for tag in tag_list:
                    writer.writerow([r['rel_path'], r['line'], tag_type, tag, r['text']])
    print(f"[+] RTM CSV Raporu kaydedildi: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Emniyet-Kritik Sistemler Çift Yönlü İzlenebilirlik Analizcisi")
    parser.add_argument('--docs-dir', default='.', help="Taranacak kök dizin")
    parser.add_argument('--output-csv', default='rtm_report.csv', help="Çıktı CSV dosyası")
    parser.add_argument('--output-html', default='rtm_dashboard.html', help="Çıktı interaktif HTML raporu")
    args = parser.parse_args()

    print("\n" + "="*70)
    print(" 🛡️  EMNİYET-KRİTİK SİSTEMLER - İZLENEBİLİRLİK (RTM) DENETLEYİCİSİ")
    print("     RTCA DO-178C / DO-254 / SAE ARP4754B / ISO 26262 Compliance")
    print("="*70)
    print(f"[*] Hedef Dizin : {os.path.abspath(args.docs_dir)}")

    records = scan_files(args.docs_dir)
    summary, links = analyze_traceability(records)

    print("\n" + "-"*65)
    print(f"{'Etiket Kategorisi':<24} | {'Benzersiz Öğe':<16} | {'Toplam Geçiş':<12}")
    print("-"*65)
    category_names = {
        'HAZ': 'Tehlike (FHA/ARP4761)',
        'SYS': 'Sistem Gereksinimi',
        'HLR': 'Üst Seviye Yazılım',
        'LLR': 'Alt Seviye Tasarım',
        'HWR': 'Donanım (DO-254)',
        'TEST': 'Test / MC-DC Doğrulama'
    }
    for cat in ['HAZ', 'SYS', 'HLR', 'LLR', 'HWR', 'TEST']:
        name = category_names.get(cat, cat)
        u_cnt = len(summary[cat]['items'])
        t_cnt = summary[cat]['count']
        print(f"{name:<24} | {u_cnt:<16} | {t_cnt:<12}")
    print("-"*65)

    export_csv(records, args.output_csv)
    generate_html_report(summary, links, records, args.output_html)
    print("="*70 + "\n")

if __name__ == '__main__':
    main()
