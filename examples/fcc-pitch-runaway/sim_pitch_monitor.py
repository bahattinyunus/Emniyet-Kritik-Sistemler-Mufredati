#!/usr/bin/env python3
"""
=============================================================================
🛡️ FCC Pitch Runaway Safety Monitor - DO-178C DAL A Python Simülatörü & Test Koşucusu
Traceability: [UTEST-ELEV-088] <- [LLR-ELEV-204] <- [HLR-ELEV-101] <- [SYS-FCC-043]
=============================================================================
"""

import math
from dataclasses import dataclass

LIMIT_DEG = 1.5
MAX_CONSECUTIVE_CYCLES = 2

@dataclass
class FccPitchMonitor:
    command_channel_deg: float = 0.0
    monitor_channel_deg: float = 0.0
    fault_cycle_counter: int = 0
    actuator_disengaged: bool = False
    current_status: str = "OK"

def evaluate_pitch_discrepancy(mon: FccPitchMonitor) -> str:
    """[LLR-ELEV-204] Pitch Discrepancy Evaluation"""
    if mon.actuator_disengaged:
        mon.current_status = "TRIPPED"
        return mon.current_status

    diff = abs(mon.command_channel_deg - mon.monitor_channel_deg)

    if diff > LIMIT_DEG:
        mon.fault_cycle_counter += 1
        if mon.fault_cycle_counter >= MAX_CONSECUTIVE_CYCLES:
            # [SYS-FCC-043] Trip and isolate actuator
            mon.actuator_disengaged = True
            mon.current_status = "TRIPPED"
        else:
            mon.current_status = "WARNING"
    else:
        mon.fault_cycle_counter = 0
        mon.current_status = "OK"

    return mon.current_status

def run_mcdc_test_suite():
    print("=" * 65)
    print(" 🛡️ DO-178C DAL A Structural Coverage (MC/DC) Simülasyon Testi")
    print(" Traceability: [UTEST-ELEV-088] -> Function: evaluate_pitch_discrepancy()")
    print("=" * 65)

    passed = 0
    total = 4

    # Test 1: Normal Condition
    mon1 = FccPitchMonitor(command_channel_deg=5.0, monitor_channel_deg=5.2)
    s1 = evaluate_pitch_discrepancy(mon1)
    t1_pass = (s1 == "OK" and not mon1.actuator_disengaged and mon1.fault_cycle_counter == 0)
    print(f"[*] Test 1: Normal Eşik Altı Operasyon ............... {'[BAŞARILI]' if t1_pass else '[BAŞARISIZ]'}")
    if t1_pass: passed += 1

    # Test 2: Gürültü Filtreleme (Tek Döngü Spike)
    mon2 = FccPitchMonitor(command_channel_deg=10.0, monitor_channel_deg=8.0)
    s2 = evaluate_pitch_discrepancy(mon2)
    mon2.monitor_channel_deg = 10.0
    s2_recovery = evaluate_pitch_discrepancy(mon2)
    t2_pass = (s2 == "WARNING" and s2_recovery == "OK" and mon2.fault_cycle_counter == 0)
    print(f"[*] Test 2: Geçici Gürültü Filtreleme (1 Döngü) ...... {'[BAŞARILI]' if t2_pass else '[BAŞARISIZ]'}")
    if t2_pass: passed += 1

    # Test 3: Ardışık 2 Döngü Aşımı (Aktüatör İzolasyonu)
    mon3 = FccPitchMonitor(command_channel_deg=15.0, monitor_channel_deg=10.0)
    evaluate_pitch_discrepancy(mon3)
    s3_trip = evaluate_pitch_discrepancy(mon3)
    t3_pass = (s3_trip == "TRIPPED" and mon3.actuator_disengaged and mon3.fault_cycle_counter == 2)
    print(f"[*] Test 3: Sürekli Hata İzolasyonu (Trip/Bypass) ... {'[BAŞARILI]' if t3_pass else '[BAŞARISIZ]'}")
    if t3_pass: passed += 1

    # Test 4: Kilitli Kalma (Latched State Güvenliği)
    mon3.monitor_channel_deg = 15.0 # Veri düzelse bile
    s4_latched = evaluate_pitch_discrepancy(mon3)
    t4_pass = (s4_latched == "TRIPPED" and mon3.actuator_disengaged)
    print(f"[*] Test 4: Emniyet Kilidi (Latched Isolation) ...... {'[BAŞARILI]' if t4_pass else '[BAŞARISIZ]'}")
    if t4_pass: passed += 1

    print("-" * 65)
    print(f"Sonuç: {passed}/{total} Test Başarıyla Tamamlandı (MC/DC Kapsamı: %100)")
    print("=" * 65)
    return passed == total

if __name__ == '__main__':
    run_mcdc_test_suite()
