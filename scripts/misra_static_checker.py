#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
🛡️ Emniyet-Kritik Sistemler - MISRA C:2012 Statik Kural Denetleyicisi
Static Code Compliance Checker for DO-178C DAL A & ISO 26262 ASIL D Flight Code
Traceability: [SYS-TOOL-001] -> [HLR-TOOL-010] -> [UTEST-TOOL-030]
=============================================================================
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple

# Denetlenecek MISRA C:2012 Kuralları (Uçuş kaynak ve başlık dosyaları için)
MISRA_RULES = [
    (
        "MISRA C:2012 Rule 21.3",
        "Dinamik bellek tahsisi (malloc/calloc/realloc/free) kesinlikle yasaktır.",
        re.compile(r"\b(malloc|calloc|realloc|free)\s*\("),
    ),
    (
        "MISRA C:2012 Rule 15.1",
        "'goto' deyimi kontrol akışı determinizmini bozduğu için yasaktır.",
        re.compile(r"\bgoto\b"),
    ),
    (
        "MISRA C:2012 Rule 21.6",
        "Uçuş kodunda standart G/Ç (<stdio.h>, printf, scanf) kullanımı yasaktır.",
        re.compile(r"(#include\s*<stdio\.h>|\bprintf\s*\(|\bscanf\s*\()"),
    ),
    (
        "MISRA C:2012 Dir 4.6",
        "Boyutsuzluk riski taşıyan ham 'int/long/short' yerine <stdint.h> tipleri kullanılmalıdır.",
        re.compile(r"\b(unsigned\s+int|signed\s+int|unsigned\s+long|long\s+long|short\s+int)\b"),
    ),
    (
        "MISRA C:2012 Rule 14.4",
        "Sınırsız sonsuz döngü (while(1) / for(;;)) donanım kilitlenmesine yol açabilir.",
        re.compile(r"(while\s*\(\s*1\s*\)|while\s*\(\s*true\s*\)|for\s*\(\s*;\s*;\s*\))"),
    ),
]


def strip_c_comments(source: str) -> str:
    """Yorum satırlarını temizler ancak satır numaralarını korur."""
    def replacer(match: re.Match) -> str:
        text = match.group(0)
        return "\n" * text.count("\n")

    pattern = re.compile(r"//.*?$|/\*.*?\*/", re.DOTALL | re.MULTILINE)
    return pattern.sub(replacer, source)


def audit_c_file(file_path: Path) -> Tuple[List[str], bool]:
    """Bir C kaynak veya başlık dosyasını MISRA C:2012 ve DO-178C izlenebilirlik açısından denetler."""
    raw_content = file_path.read_text(encoding="utf-8", errors="ignore")
    clean_content = strip_c_comments(raw_content)
    clean_lines = clean_content.splitlines()

    violations: List[str] = []

    # 1. DO-178C İzlenebilirlik Etiketi Kontrolü (Yorumlar dahil)
    has_trace_tag = bool(
        re.search(r"\[(HAZ|SYS|HLR|LLR|HWR)-[A-Za-z0-9_-]+\]", raw_content)
    )
    if not has_trace_tag:
        violations.append(
            f"{file_path}:1 -> [DO-178C Traceability] Dosyada hiçbir izlenebilirlik etiketi ([LLR-xxx] / [SYS-xxx]) bulunamadı!"
        )

    # 2. MISRA C:2012 Kural Kontrolleri (Yalnızca aktif kod satırlarında)
    for line_no, line in enumerate(clean_lines, start=1):
        for rule_id, rule_desc, regex in MISRA_RULES:
            if regex.search(line):
                violations.append(
                    f"{file_path}:{line_no} -> [{rule_id}] {rule_desc} | Kod: {line.strip()}"
                )

    return violations, has_trace_tag


def main() -> int:
    root = Path(".")
    examples_dir = root / "examples"

    print("\n" + "=" * 76)
    print(" 🛡️  MISRA C:2012 & DO-178C STATİK KOD UYUM DENETLEYİCİSİ (STATIC LINTER)")
    print("=" * 76)

    # Uçuş kodu dizinlerindeki (src/ ve include/) tüm .c ve .h dosyalarını tara
    flight_files: List[Path] = []
    if examples_dir.exists():
        for p in sorted(examples_dir.rglob("*")):
            if p.is_file() and p.suffix in {".c", ".h"}:
                if "src" in p.parts or "include" in p.parts:
                    flight_files.append(p)

    all_violations: List[str] = []
    for fpath in flight_files:
        rel = fpath.as_posix()
        violations, has_trace = audit_c_file(fpath)
        all_violations.extend(violations)
        status = "[GEÇTİ - %100 UYUMLU]" if not violations else f"[İHLAL: {len(violations)}]"
        trace_str = "İzlenebilirlik: OK" if has_trace else "İzlenebilirlik: EKSİK"
        print(f"[*] {rel:<52} | {trace_str} | {status}")

    print("-" * 76)
    if all_violations:
        print(f"[!] Toplam {len(all_violations)} MISRA / DO-178C İhlali Tespit Edildi:")
        for v in all_violations:
            print(f"    - {v}")
        print("=" * 76 + "\n")
        return 1

    print(
        f"[+] Denetlenen {len(flight_files)} uçuş yazılımı modülünde 0 MISRA C:2012 ihlali bulundu."
    )
    print("=" * 76 + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
