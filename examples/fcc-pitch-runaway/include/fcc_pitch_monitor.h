/**
 * ============================================================================
 * @file    fcc_pitch_monitor.h
 * @brief   Flight Control Computer (FCC) Pitch Runaway Safety Monitor
 * @details RTCA DO-178C DAL A | MISRA C:2012 Compliant Architecture
 * 
 * Traceability Reference:
 * [SYS-FCC-042] Dual Channel COM/MON Architecture
 * [SYS-FCC-043] Elevator Runaway Isolation Barrier
 * [HLR-ELEV-101] Discrepancy Monitoring Functionality
 * [LLR-ELEV-204] Consecutive Cycle Threshold Evaluation
 * ============================================================================
 */

#ifndef FCC_PITCH_MONITOR_H
#define FCC_PITCH_MONITOR_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Emniyet Kısıtları (Safety Parameters) */
#define FCC_PITCH_DISCREPANCY_LIMIT_DEG     (1.5f)
#define FCC_MAX_CONSECUTIVE_FAULT_CYCLES    (2U)

/**
 * @brief Hata Durum Kodları (DO-178C Deterministik Hata Yönetimi)
 */
typedef enum {
    FCC_STATUS_OK             = 0x00U,
    FCC_STATUS_WARNING        = 0x01U,
    FCC_STATUS_TRIPPED        = 0x02U,
    FCC_STATUS_INVALID_PARAM  = 0xFFU
} FccStatus_t;

/**
 * @brief Pitch Emniyet İzleme Durum Yapısı
 */
typedef struct {
    float       command_channel_deg;  /*!< Command (COM) kanalı pitch komutu (derece) */
    float       monitor_channel_deg;  /*!< Monitor (MON) kanalı pitch komutu (derece) */
    uint32_t    fault_cycle_counter;  /*!< Ardışık hata sayacı */
    bool        actuator_disengaged;  /*!< Aktüatör emniyetli bypass bayrağı */
    FccStatus_t current_status;       /*!< Anlık emniyet durumu */
} FccPitchSafetyMonitor_t;

/**
 * @brief   Emniyet monitörü durumunu ilklendirir.
 * @param   monitor Monitör veri yapısı işaretçisi
 * @return  FCC_STATUS_OK veya FCC_STATUS_INVALID_PARAM
 */
FccStatus_t FCC_PitchMonitor_Init(FccPitchSafetyMonitor_t * const monitor);

/**
 * @brief   COM ve MON kanalları arasındaki pitch komut farkını değerlendirir.
 * @details [LLR-ELEV-204] Fark limiti ardışık döngüler boyunca aşılırsa aktüatörü izole eder.
 * @param   monitor Monitör veri yapısı işaretçisi
 * @return  FccStatus_t Güncel emniyet durumu
 */
FccStatus_t FCC_EvaluatePitchDiscrepancy(FccPitchSafetyMonitor_t * const monitor);

#ifdef __cplusplus
}
#endif

#endif /* FCC_PITCH_MONITOR_H */
