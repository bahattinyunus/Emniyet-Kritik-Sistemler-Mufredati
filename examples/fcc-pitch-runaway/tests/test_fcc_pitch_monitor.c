/**
 * ============================================================================
 * @file    test_fcc_pitch_monitor.c
 * @brief   DO-178C DAL A Structural Coverage (MC/DC) Unit Test Suite
 * 
 * Traceability Reference:
 * [UTEST-ELEV-088] MC/DC and Boundary Evaluation of Discrepancy Logic
 * Target Function: FCC_EvaluatePitchDiscrepancy()
 * ============================================================================
 */

#include <stdio.h>
#include <assert.h>
#include "../include/fcc_pitch_monitor.h"

static int g_tests_passed = 0;
static int g_tests_failed = 0;

#define RUN_TEST(test_func) \
    do { \
        printf("[RUNNING] %s ... ", #test_func); \
        if (test_func()) { \
            printf("PASSED\n"); \
            g_tests_passed++; \
        } else { \
            printf("FAILED\n"); \
            g_tests_failed++; \
        } \
    } while(0)

/* Test 1: NULL Pointer Savunma Testi */
static bool test_null_pointer_rejection(void)
{
    /* [UTEST-ELEV-088-01] NULL parametre geldiğinde geçersiz kod dönmeli */
    FccStatus_t status = FCC_EvaluatePitchDiscrepancy(NULL);
    return (status == FCC_STATUS_INVALID_PARAM);
}

/* Test 2: Normal Operasyon (Fark Eşik Altında) */
static bool test_normal_operation(void)
{
    /* [UTEST-ELEV-088-02] Fark <= LIMIT -> OK */
    FccPitchSafetyMonitor_t mon;
    (void)FCC_PitchMonitor_Init(&mon);

    mon.command_channel_deg = 5.0f;
    mon.monitor_channel_deg = 5.2f; /* Fark = 0.2 < 1.5 */

    FccStatus_t status = FCC_EvaluatePitchDiscrepancy(&mon);
    return (status == FCC_STATUS_OK) && (!mon.actuator_disengaged) && (mon.fault_cycle_counter == 0U);
}

/* Test 3: Tek Döngü Hata (Gürültü Filtreleme) */
static bool test_transient_spike_filtered(void)
{
    /* [UTEST-ELEV-088-03] 1. Döngü ihlal -> WARNING, Aktüatör açık kalmalı */
    FccPitchSafetyMonitor_t mon;
    (void)FCC_PitchMonitor_Init(&mon);

    mon.command_channel_deg = 10.0f;
    mon.monitor_channel_deg = 8.0f; /* Fark = 2.0 > 1.5 */

    FccStatus_t status = FCC_EvaluatePitchDiscrepancy(&mon);
    bool check1 = (status == FCC_STATUS_WARNING) && (!mon.actuator_disengaged) && (mon.fault_cycle_counter == 1U);

    /* Sonraki döngüde düzelirse sayacın sıfırlandığını doğrula */
    mon.monitor_channel_deg = 10.1f;
    status = FCC_EvaluatePitchDiscrepancy(&mon);
    bool check2 = (status == FCC_STATUS_OK) && (mon.fault_cycle_counter == 0U);

    return check1 && check2;
}

/* Test 4: İki Ardışık Döngü Hata (Trip / Bypass Tetikleme) */
static bool test_consecutive_fault_tripped(void)
{
    /* [UTEST-ELEV-088-04] 2 ardışık ihlal -> TRIPPED & Aktüatör izole edilmeli */
    FccPitchSafetyMonitor_t mon;
    (void)FCC_PitchMonitor_Init(&mon);

    mon.command_channel_deg = 15.0f;
    mon.monitor_channel_deg = 10.0f; /* Fark = 5.0 > 1.5 */

    /* Döngü 1: Uyarı */
    (void)FCC_EvaluatePitchDiscrepancy(&mon);

    /* Döngü 2: Kilitlenme (Trip) */
    FccStatus_t status = FCC_EvaluatePitchDiscrepancy(&mon);

    bool tripped = (status == FCC_STATUS_TRIPPED) && (mon.actuator_disengaged == true);

    /* Döngü 3: Değer düzelse dahi LATCHED (Kilitli) kalmalı */
    mon.monitor_channel_deg = 15.0f;
    FccStatus_t status_latched = FCC_EvaluatePitchDiscrepancy(&mon);

    return tripped && (status_latched == FCC_STATUS_TRIPPED);
}

int main(void)
{
    printf("================================================================\n");
    printf(" 🛡️ DO-178C DAL A Structural Coverage Test Suite [UTEST-ELEV-088]\n");
    printf(" Target: FCC Pitch Runaway Safety Monitor\n");
    printf("================================================================\n");

    RUN_TEST(test_null_pointer_rejection);
    RUN_TEST(test_normal_operation);
    RUN_TEST(test_transient_spike_filtered);
    RUN_TEST(test_consecutive_fault_tripped);

    printf("----------------------------------------------------------------\n");
    printf("Sonuç: %d Başarılı, %d Başarısız\n", g_tests_passed, g_tests_failed);
    printf("================================================================\n");

    return (g_tests_failed == 0) ? 0 : 1;
}
