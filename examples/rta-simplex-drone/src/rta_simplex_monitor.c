/**
 * ============================================================================
 * @file    rta_simplex_monitor.c
 * @brief   ASTM F3269 Run-Time Assurance (RTA) Simplex Monitor Implementation
 *
 * Traceability:
 * [LLR-RTA-010] <- [HLR-RTA-001] <- [SYS-RTA-01], [SYS-RTA-02] <- [HAZ-RTA-01]
 * Standards: ASTM F3269-21 | RTCA DO-178C DAL A | MISRA C:2012 Compliant
 * ============================================================================
 */

#include "../include/rta_simplex_monitor.h"

/* Statik yardımcı fonksiyon: Standart kütüphane bağımsız mutlak değer */
static float RTA_AbsFloat(const float val)
{
    float res = val;
    if (res < 0.0f) {
        res = -res;
    }
    return res;
}

/* [LLR-RTA-009] RTA Simplex Durum Bloğu İlklendirme */
RtaActiveSource_t RTA_Simplex_Init(RtaSimplexContext_t * const ctx)
{
    if (ctx == (void *)0) {
        return RTA_SOURCE_INVALID_ERROR;
    }

    ctx->active_source         = RTA_SOURCE_COMPLEX_AI;
    ctx->trip_reason           = RTA_REASON_NONE;
    ctx->selected_elevator_deg = 0.0f;
    ctx->intervention_count    = 0U;
    ctx->recovery_latched      = false;

    return ctx->active_source;
}

/* [LLR-RTA-010] 5 ms Periyotlu Emniyet Zarfı Denetimi ve Simplex Anahtarlama */
RtaActiveSource_t RTA_EvaluateSafetyEnvelope(
    RtaSimplexContext_t * const ctx,
    const RtaFlightState_t * const state)
{
    /* 1. Savunmacı Programlama: NULL İşaretçi Kontrolü */
    if ((ctx == (void *)0) || (state == (void *)0)) {
        return RTA_SOURCE_INVALID_ERROR;
    }

    /* 2. Latched (Kilitli) Kurtarma Durumu Kontrolü [SYS-RTA-02] */
    if (ctx->recovery_latched) {
        ctx->active_source         = RTA_SOURCE_SAFETY_RECOVERY;
        ctx->selected_elevator_deg = state->safe_elevator_cmd_deg;
        return RTA_SOURCE_SAFETY_RECOVERY;
    }

    /* 3. Çok Boyutlu Emniyet Zarfı (Safety Envelope) Koşullarının Hesaplanması */
    const float abs_roll = RTA_AbsFloat(state->current_roll_deg);
    const float abs_cmd  = RTA_AbsFloat(state->ai_elevator_cmd_deg);

    const bool aoa_violated  = (state->current_aoa_deg > RTA_MAX_AOA_DEG);
    const bool roll_violated = (abs_roll > RTA_MAX_ROLL_ANGLE_DEG);
    const bool alt_violated  = (state->altitude_agl_m < RTA_MIN_ALTITUDE_AGL_M);
    const bool ai_faulted    = (!state->ai_heartbeat_valid) || (abs_cmd > RTA_MAX_CMD_SLEW_DEG);

    /* 4. Birleşik Karar İfadesi (MC/DC Hedef Kararı: A || B || C || D) */
    if (aoa_violated || roll_violated || alt_violated || ai_faulted) {
        /* [SYS-RTA-01] & [SYS-RTA-02] Zarf İhlali: DAL A Emniyet Kontrolcüsüne Geç! */
        ctx->active_source         = RTA_SOURCE_SAFETY_RECOVERY;
        ctx->selected_elevator_deg = state->safe_elevator_cmd_deg;
        ctx->recovery_latched      = true;
        ctx->intervention_count++;

        if (aoa_violated) {
            ctx->trip_reason = RTA_REASON_AOA_STALL_RISK;
        } else if (roll_violated) {
            ctx->trip_reason = RTA_REASON_EXCESSIVE_ROLL;
        } else if (alt_violated) {
            ctx->trip_reason = RTA_REASON_ALTITUDE_FLOOR;
        } else {
            ctx->trip_reason = RTA_REASON_AI_UNHEALTHY_OR_CMD;
        }
    } else {
        /* Tüm emniyet zarfı koşulları sağlandı: AI komutunu aktüatöre ilet */
        ctx->active_source         = RTA_SOURCE_COMPLEX_AI;
        ctx->trip_reason           = RTA_REASON_NONE;
        ctx->selected_elevator_deg = state->ai_elevator_cmd_deg;
    }

    return ctx->active_source;
}
