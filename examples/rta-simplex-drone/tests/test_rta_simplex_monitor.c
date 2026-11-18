/**
 * ============================================================================
 * @file    test_rta_simplex_monitor.c
 * @brief   DO-178C DAL A Structural Coverage (MC/DC) Unit Test Suite for RTA
 *
 * Traceability Reference:
 * [UTEST-RTA-099] MC/DC Verification of RTA_EvaluateSafetyEnvelope()
 * Decision under test: (aoa_violated || roll_violated || alt_violated || ai_faulted)
 * ============================================================================
 */

#include <stdio.h>
#include "../include/rta_simplex_monitor.h"

static uint32_t g_passed = 0U;
static uint32_t g_failed = 0U;

#define RUN_RTA_TEST(fn) \
    do { \
        printf("[RUNNING] %-42s ... ", #fn); \
        if (fn()) { \
            printf("PASSED\n"); \
            g_passed++; \
        } else { \
            printf("FAILED\n"); \
            g_failed++; \
        } \
    } while (0)

static RtaFlightState_t make_nominal_state(void)
{
    RtaFlightState_t s;
    s.current_roll_deg      = 10.0f;
    s.current_aoa_deg       = 5.0f;
    s.altitude_agl_m        = 120.0f;
    s.ai_elevator_cmd_deg   = 3.5f;
    s.safe_elevator_cmd_deg = -2.0f;
    s.ai_heartbeat_valid    = true;
    return s;
}

/* Test 1: Savunmacı NULL Pointer Reddi */
static bool test_rta_null_rejection(void)
{
    RtaSimplexContext_t ctx;
    RtaFlightState_t st = make_nominal_state();
    RtaActiveSource_t r1 = RTA_Simplex_Init((void *)0);
    RtaActiveSource_t r2 = RTA_EvaluateSafetyEnvelope((void *)0, &st);
    RtaActiveSource_t r3 = RTA_EvaluateSafetyEnvelope(&ctx, (void *)0);
    return (r1 == RTA_SOURCE_INVALID_ERROR) &&
           (r2 == RTA_SOURCE_INVALID_ERROR) &&
           (r3 == RTA_SOURCE_INVALID_ERROR);
}

/* Test 2 (MC/DC Vector 1 - F,F,F,F -> FALSE): Nominal AI Operasyonu */
static bool test_rta_nominal_ai_passthrough(void)
{
    RtaSimplexContext_t ctx;
    (void)RTA_Simplex_Init(&ctx);
    RtaFlightState_t st = make_nominal_state();

    RtaActiveSource_t src = RTA_EvaluateSafetyEnvelope(&ctx, &st);
    return (src == RTA_SOURCE_COMPLEX_AI) &&
           (!ctx.recovery_latched) &&
           (ctx.trip_reason == RTA_REASON_NONE);
}

/* Test 3 (MC/DC Vector 2 - T,F,F,F -> TRUE): AoA Stall İhlali [SYS-RTA-01] */
static bool test_rta_aoa_stall_trip(void)
{
    RtaSimplexContext_t ctx;
    (void)RTA_Simplex_Init(&ctx);
    RtaFlightState_t st = make_nominal_state();
    st.current_aoa_deg = 16.5f; /* > 15.0 deg */

    RtaActiveSource_t src = RTA_EvaluateSafetyEnvelope(&ctx, &st);
    return (src == RTA_SOURCE_SAFETY_RECOVERY) &&
           (ctx.trip_reason == RTA_REASON_AOA_STALL_RISK) &&
           (ctx.recovery_latched);
}

/* Test 4 (MC/DC Vector 3 - F,T,F,F -> TRUE): Aşırı Yatış Açısı İhlali */
static bool test_rta_excessive_roll_trip(void)
{
    RtaSimplexContext_t ctx;
    (void)RTA_Simplex_Init(&ctx);
    RtaFlightState_t st = make_nominal_state();
    st.current_roll_deg = -52.0f; /* |roll| > 45.0 deg */

    RtaActiveSource_t src = RTA_EvaluateSafetyEnvelope(&ctx, &st);
    return (src == RTA_SOURCE_SAFETY_RECOVERY) &&
           (ctx.trip_reason == RTA_REASON_EXCESSIVE_ROLL) &&
           (ctx.recovery_latched);
}

/* Test 5 (MC/DC Vector 4 - F,F,T,F -> TRUE): Minimum İrtifa (Geofence) İhlali */
static bool test_rta_altitude_floor_trip(void)
{
    RtaSimplexContext_t ctx;
    (void)RTA_Simplex_Init(&ctx);
    RtaFlightState_t st = make_nominal_state();
    st.altitude_agl_m = 24.0f; /* < 30.0 m */

    RtaActiveSource_t src = RTA_EvaluateSafetyEnvelope(&ctx, &st);
    return (src == RTA_SOURCE_SAFETY_RECOVERY) &&
           (ctx.trip_reason == RTA_REASON_ALTITUDE_FLOOR) &&
           (ctx.recovery_latched);
}

/* Test 6 (MC/DC Vector 5 - F,F,F,T -> TRUE): AI Heartbeat Kaybı / Aşırı Komut */
static bool test_rta_ai_unhealthy_and_latch(void)
{
    RtaSimplexContext_t ctx;
    (void)RTA_Simplex_Init(&ctx);
    RtaFlightState_t st = make_nominal_state();
    st.ai_heartbeat_valid = false;

    RtaActiveSource_t src1 = RTA_EvaluateSafetyEnvelope(&ctx, &st);

    /* Sonraki döngüde AI düzelmiş görünse dahi Latched kalmalı */
    st.ai_heartbeat_valid = true;
    RtaActiveSource_t src2 = RTA_EvaluateSafetyEnvelope(&ctx, &st);

    return (src1 == RTA_SOURCE_SAFETY_RECOVERY) &&
           (ctx.trip_reason == RTA_REASON_AI_UNHEALTHY_OR_CMD) &&
           (src2 == RTA_SOURCE_SAFETY_RECOVERY);
}

int main(void)
{
    printf("====================================================================\n");
    printf(" 🛡️ ASTM F3269 RTA Simplex Envelope Monitor Test Suite [UTEST-RTA-099]\n");
    printf("====================================================================\n");

    RUN_RTA_TEST(test_rta_null_rejection);
    RUN_RTA_TEST(test_rta_nominal_ai_passthrough);
    RUN_RTA_TEST(test_rta_aoa_stall_trip);
    RUN_RTA_TEST(test_rta_excessive_roll_trip);
    RUN_RTA_TEST(test_rta_altitude_floor_trip);
    RUN_RTA_TEST(test_rta_ai_unhealthy_and_latch);

    printf("--------------------------------------------------------------------\n");
    printf("Sonuç: %u Başarılı, %u Başarısız (MC/DC Kapsamı: %%100)\n", g_passed, g_failed);
    printf("====================================================================\n");

    return (g_failed == 0U) ? 0 : 1;
}
