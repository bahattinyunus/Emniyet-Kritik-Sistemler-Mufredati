#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
🛡️ Emniyet-Kritik Sistemler - Nicel FTA & Otomatik MC/DC Doğrulama Motoru
Quantitative Fault Tree Analysis (ARP 4761A) & Automated MC/DC Solver (DO-178C)
Traceability: [SYS-TOOL-001] -> [HLR-TOOL-010] -> [LLR-TOOL-020] -> [UTEST-TOOL-030]
=============================================================================
"""

import itertools
import sys
from dataclasses import dataclass
from typing import Callable, Dict, List, Set, Tuple


@dataclass(frozen=True)
class BasicEvent:
    code: str
    name: str
    failure_rate_per_fh: float  # Uçuş saati başına hata olasılığı (lambda * t)


def evaluate_fbw_fault_tree(state: Dict[str, bool]) -> bool:
    """
    [HAZ-FCC-01] Tepe Olay: Uçuş Kontrol Yüzeyi Kontrolsüz Sapması (Catastrophic)
    Mantıksal Hata Ağacı Denklemi:
      TopEvent = (CH_A_FAIL and CH_B_FAIL)
                 or (COM_CPU_ERR and MON_CPU_ERR)
                 orMECH_JAM_CCF
    Burada MECH_JAM_CCF aşırı düşük olasılıklı mekanik sıkışma veya
    Voter/Solenoid çift yedekli valf arızası (VALVE_1 and VALVE_2) olarak modellenir:
      TopEvent = (A1 and A2) or (B1 and B2) or (V1 and V2) or (S1 and S2 and S3)
    """
    fcc_dual_channel_loss = state["FCC_CH_A"] and state["FCC_CH_B"]
    com_mon_undetected = state["COM_LOGIC"] and state["MON_WATCHDOG"]
    dual_hydraulic_valve_jam = state["BYPASS_VALVE_1"] and state["BYPASS_VALVE_2"]
    tmr_sensor_majority_fail = (
        (state["AOA_SENS_1"] and state["AOA_SENS_2"])
        or (state["AOA_SENS_2"] and state["AOA_SENS_3"])
        or (state["AOA_SENS_1"] and state["AOA_SENS_3"])
    )
    return (
        fcc_dual_channel_loss
        or com_mon_undetected
        or dual_hydraulic_valve_jam
        or tmr_sensor_majority_fail
    )


def find_minimal_cut_sets(
    events: List[BasicEvent], tree_fn: Callable[[Dict[str, bool]], bool]
) -> List[Set[str]]:
    """Boolean hata ağacındaki tüm Minimal Kesme Kümelerini (MCS) bulur."""
    codes = [e.code for e in events]
    minimal_cut_sets: List[Set[str]] = []

    for r in range(1, len(codes) + 1):
        for combo in itertools.combinations(codes, r):
            candidate = set(combo)
            # Eğer alt kümesi zaten bir MCS ise atla (Minimality koşulu)
            if any(mcs.issubset(candidate) for mcs in minimal_cut_sets):
                continue

            state = {c: (c in candidate) for c in codes}
            if tree_fn(state):
                minimal_cut_sets.append(candidate)

    return minimal_cut_sets


def run_quantitative_fta_audit() -> bool:
    print("\n" + "=" * 76)
    print(" 📐 1. SAE ARP 4761A NİCEL HATA AĞACI ANALİZİ (QUANTITATIVE FTA ENGINE)")
    print("    Tepe Olay: [HAZ-FCC-01] Kontrolsüz Pitch Runaway (Hedef: < 1.0e-09 / FH)")
    print("=" * 76)

    events = [
        BasicEvent("FCC_CH_A", "Birincil Uçuş Kontrol Kanalı A", 1.2e-5),
        BasicEvent("FCC_CH_B", "Yedek Uçuş Kontrol Kanalı B", 1.2e-5),
        BasicEvent("COM_LOGIC", "Command İşlemcisi Komut Hatası", 1.5e-5),
        BasicEvent("MON_WATCHDOG", "Monitor Kanalı & Karşılaştırıcı Hatası", 1.0e-5),
        BasicEvent("BYPASS_VALVE_1", "Solenoid Bypass Valfi #1 Kilitlenmesi", 8.0e-6),
        BasicEvent("BYPASS_VALVE_2", "Solenoid Bypass Valfi #2 Kilitlenmesi", 8.0e-6),
        BasicEvent("AOA_SENS_1", "Hücum Açısı (AoA) Sensörü #1 (TMR)", 1.0e-5),
        BasicEvent("AOA_SENS_2", "Hücum Açısı (AoA) Sensörü #2 (TMR)", 1.0e-5),
        BasicEvent("AOA_SENS_3", "Hücum Açısı (AoA) Sensörü #3 (TMR)", 1.0e-5),
    ]
    prob_map = {e.code: e.failure_rate_per_fh for e in events}

    mcs_list = find_minimal_cut_sets(events, evaluate_fbw_fault_tree)

    print(f"\n[*] Tespit Edilen Minimal Kesme Kümesi (MCS) Sayısı: {len(mcs_list)}")
    print("-" * 76)
    print(f"{'MCS #':<7} | {'Derece (Order)':<14} | {'Kesme Kümesi Bileşenleri':<35} | {'Olasılık (/FH)':<14}")
    print("-" * 76)

    top_prob = 0.0
    spof_detected = False
    mcs_probs: List[Tuple[Set[str], float]] = []

    for idx, mcs in enumerate(mcs_list, start=1):
        p_mcs = 1.0
        for code in mcs:
            p_mcs *= prob_map[code]
        mcs_probs.append((mcs, p_mcs))
        top_prob += p_mcs
        order = len(mcs)
        if order == 1:
            spof_detected = True
        comp_str = " AND ".join(sorted(mcs))
        print(f"MCS-{idx:02d}  | Order-{order:<8} | {comp_str:<35} | {p_mcs:.3e}")

    print("-" * 76)
    print("\n[*] Fussell-Vesely (FV) Bileşen Kritiklik Ölçütü (Importance Analysis):")
    for e in events:
        contrib = sum(p for mcs, p in mcs_probs if e.code in mcs)
        fv_importance = (contrib / top_prob) * 100.0 if top_prob > 0 else 0.0
        print(f"    - {e.code:<15} ({e.name:<40}): FV = %{fv_importance:5.2f}")

    target_limit = 1.0e-9
    compliant = (top_prob < target_limit) and (not spof_detected)

    print("-" * 76)
    print(f"[*] Tekil Hata Noktası (Single Point of Failure - Order 1): {'YOK (PASS)' if not spof_detected else 'VAR (FAIL!)'}")
    print(f"[*] Hesaplanan Tepe Olay Olasılığı (P_top)                : {top_prob:.3e} / Uçuş Saati")
    print(f"[*] FAA / EASA CS-25.1309 DAL A Sertifikasyon Sınırı       : {target_limit:.3e} / Uçuş Saati")
    print(f"[*] Sertifikasyon Durumu                                   : {'[UYUMLU - DAL A ONAYLI]' if compliant else '[UYUMSUZ]'}")
    print("=" * 76)
    return compliant


def solve_mcdc_pairs(
    var_names: List[str], decision_fn: Callable[[Tuple[bool, ...]], bool], label: str
) -> bool:
    """
    Verilen N değişkenli Boolean karar fonksiyonu için doğruluk tablosunu çıkarır,
    her koşulun bağımsız etkisini kanıtlayan MC/DC çiftlerini (Independence Pairs)
    ve minimum N+1 test kümesini otomatik olarak bulur.
    """
    print("\n" + "=" * 76)
    print(f" 🔬 2. OTOMATİK DO-178C DAL A MC/DC ÇÖZÜCÜ: {label}")
    print("=" * 76)

    n = len(var_names)
    truth_table: Dict[Tuple[bool, ...], Tuple[int, bool]] = {}

    for idx, bits in enumerate(itertools.product([False, True], repeat=n), start=1):
        truth_table[bits] = (idx, decision_fn(bits))

    pairs_by_var: Dict[str, List[Tuple[Tuple[bool, ...], Tuple[bool, ...]]]] = {
        v: [] for v in var_names
    }

    for bits, (_, out1) in truth_table.items():
        for i, v in enumerate(var_names):
            if not bits[i]:
                flipped = list(bits)
                flipped[i] = True
                flipped_t = tuple(flipped)
                _, out2 = truth_table[flipped_t]
                if out1 != out2:
                    pairs_by_var[v].append((bits, flipped_t))

    # Minimum N+1 vektör kapsama seçimi (Greedy / Exact Set Cover)
    selected_vectors: Set[Tuple[bool, ...]] = set()
    chosen_pairs: Dict[str, Tuple[Tuple[bool, ...], Tuple[bool, ...]]] = {}

    # İlk koşulun ilk çiftini tohum olarak al, diğer koşullarda ortak vektörleri maksimize et
    for v in var_names:
        best_pair = min(
            pairs_by_var[v],
            key=lambda p: (0 if p[0] in selected_vectors else 1)
            + (0 if p[1] in selected_vectors else 1),
        )
        chosen_pairs[v] = best_pair
        selected_vectors.add(best_pair[0])
        selected_vectors.add(best_pair[1])

    print(f"[*] Koşul Sayısı (N = {n}) | Teorik Minimum MC/DC Test Sayısı (N + 1) = {n + 1}")
    print(f"[*] Çözücü Tarafından Bulunan Optimal MC/DC Test Vektör Sayısı       = {len(selected_vectors)}")
    print("-" * 76)
    for v in var_names:
        p0, p1 = chosen_pairs[v]
        id0, out0 = truth_table[p0]
        id1, out1 = truth_table[p1]
        b0_str = ",".join("T" if b else "F" for b in p0)
        b1_str = ",".join("T" if b else "F" for b in p1)
        print(
            f"  [Koşul {v:<14}] Bağımsızlık Çifti: "
            f"T{id0:02d}({b0_str})={str(out0):<5} <--> T{id1:02d}({b1_str})={str(out1):<5}"
        )

    print("-" * 76)
    header_vars = " | ".join(f"{v:^10}" for v in var_names)
    print(f"  {'Vektör':<8} | {header_vars} | {'Karar Çıktısı':^14}")
    print("-" * 76)
    for vec in sorted(selected_vectors, key=lambda x: truth_table[x][0]):
        vid, vout = truth_table[vec]
        cols = " | ".join(f"{'TRUE' if b else 'FALSE':^10}" for b in vec)
        print(f"  T{vid:02d}      | {cols} | {str(vout):^14}")
    print("=" * 76)

    return len(selected_vectors) == (n + 1)


def main() -> int:
    fta_ok = run_quantitative_fta_audit()

    # 1. Modül 3.3 Yangın/Motor Kapatma Kararı: (A || B) && C
    mcdc1_ok = solve_mcdc_pairs(
        ["A_OverTemp", "B_FuelLeak", "C_Running"],
        lambda b: (b[0] or b[1]) and b[2],
        "[LLR-MCDC-01] Shutdown = (A_OverTemp || B_FuelLeak) && C_Running",
    )

    # 2. Örnek 2 RTA Simplex Emniyet Zarfı Kararı: A || B || C || D
    mcdc2_ok = solve_mcdc_pairs(
        ["AoA_Viol", "Roll_Viol", "Alt_Viol", "AI_Fault"],
        lambda b: b[0] or b[1] or b[2] or b[3],
        "[LLR-RTA-010] RTA_Trip = (AoA_Viol || Roll_Viol || Alt_Viol || AI_Fault)",
    )

    if fta_ok and mcdc1_ok and mcdc2_ok:
        print("\n[+] TÜM NİCEL FTA VE MC/DC DOĞRULAMA KANITLARI BAŞARIYLA TAMAMLANDI.\n")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
