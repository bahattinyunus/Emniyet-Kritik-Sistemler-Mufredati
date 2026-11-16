/**
 * ============================================================================
 * @file    fcc_pitch_monitor.c
 * @brief   Implementation of Pitch Runaway Safety Protection
 * 
 * Traceability:
 * [LLR-ELEV-204] <- [HLR-ELEV-101] <- [SYS-FCC-043] <- [HAZ-FCC-01]
 * Standards: RTCA DO-178C DAL A | MISRA C:2012 Compliant
 * ============================================================================
 */

#include "../include/fcc_pitch_monitor.h"

/* Statik yardımcı fonksiyon: Mutlak değer hesabı (Standart kütüphane bağımsız) */
static float FCC_AbsFloat(const float value)
{
    float result = value;
    if (result < 0.0f) {
        result = -result;
    }
    return result;
}

/* İlklendirme Fonksiyonu */
FccStatus_t FCC_PitchMonitor_Init(FccPitchSafetyMonitor_t * const monitor)
{
    /* [LLR-INIT-001] Parametre geçerlilik denetimi */
    if (monitor == (void *)0) {
        return FCC_STATUS_INVALID_PARAM;
    }

    monitor->command_channel_deg = 0.0f;
    monitor->monitor_channel_deg = 0.0f;
    monitor->fault_cycle_counter = 0U;
    monitor->actuator_disengaged = false;
    monitor->current_status      = FCC_STATUS_OK;

    return FCC_STATUS_OK;
}

/* Periyodik Emniyet Karar Fonksiyonu (10 ms döngüde çağrılır) */
FccStatus_t FCC_EvaluatePitchDiscrepancy(FccPitchSafetyMonitor_t * const monitor)
{
    /* [LLR-ELEV-204] 1. Savunmacı Programlama (Defensive Programming) */
    if (monitor == (void *)0) {
        return FCC_STATUS_INVALID_PARAM;
    }

    /* Eğer aktüatör zaten devreden çıkarılmışsa (Bypass/Latched state), kilitli kal */
    if (monitor->actuator_disengaged) {
        monitor->current_status = FCC_STATUS_TRIPPED;
        return FCC_STATUS_TRIPPED;
    }

    /* 2. COM ve MON kanalları arasındaki mutlak fark hesabı */
    const float raw_diff = monitor->command_channel_deg - monitor->monitor_channel_deg;
    const float abs_diff = FCC_AbsFloat(raw_diff);

    /* 3. Eşik değeri denetimi ve ardışık döngü filtreleme */
    if (abs_diff > FCC_PITCH_DISCREPANCY_LIMIT_DEG) {
        monitor->fault_cycle_counter++;

        if (monitor->fault_cycle_counter >= FCC_MAX_CONSECUTIVE_FAULT_CYCLES) {
            /* [SYS-FCC-043] Emniyet bariyeri tetiklendi: Aktüatörü izole et */
            monitor->actuator_disengaged = true;
            monitor->current_status      = FCC_STATUS_TRIPPED;
        } else {
            /* Henüz ardışık eşik aşılmadı (Gürültü filtreleme aşaması) */
            monitor->current_status      = FCC_STATUS_WARNING;
        }
    } else {
        /* Fark normal sınırlar içinde: Hata sayacını sıfırla */
        monitor->fault_cycle_counter = 0U;
        monitor->current_status      = FCC_STATUS_OK;
    }

    return monitor->current_status;
}
