/**
 * ============================================================================
 * @file    rta_simplex_monitor.h
 * @brief   ASTM F3269 Run-Time Assurance (RTA) Simplex Architecture Monitor
 * 
 * System Context:
 * Supervises an untrusted Complex/AI Flight Controller (DAL E / COTS) and
 * deterministically switches control authority to a certified Recovery Safety
 * Controller (DAL A) upon flight envelope violation or telemetry staleness.
 *
 * Traceability:
 * [HAZ-RTA-01] -> [SYS-RTA-01], [SYS-RTA-02] -> [HLR-RTA-001] -> [LLR-RTA-010]
 * Standards: ASTM F3269-21 | RTCA DO-178C DAL A | MISRA C:2012 Compliant
 * ============================================================================
 */

#ifndef RTA_SIMPLEX_MONITOR_H
#define RTA_SIMPLEX_MONITOR_H

#include <stdint.h>
#include <stdbool.h>

/* ========================================================================= */
/* EMNİYET ZARFI SABİTLERİ (SAFETY ENVELOPE THRESHOLDS)                      */
/* ========================================================================= */
#define RTA_MAX_ROLL_ANGLE_DEG       (45.0f)   /* Maksimum yatış açısı sınırı */
#define RTA_MAX_AOA_DEG              (15.0f)   /* Stall koruması hücum açısı [SYS-RTA-01] */
#define RTA_MIN_ALTITUDE_AGL_M       (30.0f)   /* Minimum yerden yükseklik (Geofence) */
#define RTA_MAX_CMD_SLEW_DEG         (12.0f)   /* Tek adımda izin verilen maks AI komutu */

/* Aktif Kontrol Kaynağı Durumu */
typedef enum {
    RTA_SOURCE_COMPLEX_AI = 0,     /* Normal: Karmaşık / AI Kontrolcü devrede */
    RTA_SOURCE_SAFETY_RECOVERY,    /* Korumalı: DAL A Emniyet Kontrolcüsü devraldı */
    RTA_SOURCE_INVALID_ERROR       /* Savunmacı: Parametre veya bellek hatası */
} RtaActiveSource_t;

/* Zarf İhlali Neden Kodu (Bitmask / Enum) */
typedef enum {
    RTA_REASON_NONE = 0,
    RTA_REASON_AOA_STALL_RISK,     /* Hücum açısı > 15.0 deg */
    RTA_REASON_EXCESSIVE_ROLL,     /* Yatış açısı > 45.0 deg */
    RTA_REASON_ALTITUDE_FLOOR,     /* İrtifa < 30.0 m */
    RTA_REASON_AI_UNHEALTHY_OR_CMD /* AI heartbeat dondu veya aşırı komut sıçraması */
} RtaTripReason_t;

/* Hava Aracı Anlık Durum ve Komut Yapısı */
typedef struct {
    float    current_roll_deg;     /* Mevcut yatış açısı (-180..+180) */
    float    current_aoa_deg;      /* Mevcut hücum açısı (Angle of Attack) */
    float    altitude_agl_m;       /* Yerden yükseklik (AGL metre) */
    float    ai_elevator_cmd_deg;  /* AI Kontrolcünün talep ettiği irtifa komutu */
    float    safe_elevator_cmd_deg;/* DAL A Emniyet Kontrolcüsünün kurtarma komutu */
    bool     ai_heartbeat_valid;   /* E2E Alive Counter / AI sağlık durumu */
} RtaFlightState_t;

/* RTA Simplex Denetleyici Durum Bloğu */
typedef struct {
    RtaActiveSource_t active_source;
    RtaTripReason_t   trip_reason;
    float             selected_elevator_deg;
    uint32_t          intervention_count;
    bool              recovery_latched;
} RtaSimplexContext_t;

/* Fonksiyon Prototipleri */
RtaActiveSource_t RTA_Simplex_Init(RtaSimplexContext_t * const ctx);

RtaActiveSource_t RTA_EvaluateSafetyEnvelope(
    RtaSimplexContext_t * const ctx,
    const RtaFlightState_t * const state
);

#endif /* RTA_SIMPLEX_MONITOR_H */
