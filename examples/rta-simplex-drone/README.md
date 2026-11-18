# 🛡️ Örnek Vaka 2: ASTM F3269 Run-Time Assurance (RTA) & Simplex Otonom İHA Zarf Koruması

Bu mühendislik uygulaması, **Modül 7.1 (EASA AI Roadmap)** ve **Modül 7.2 (ASTM F3269 Run-Time Assurance & Simplex Architecture)** kapsamında anlatılan teorik mimarinin **RTCA DO-178C DAL A** ve **MISRA C:2012** kurallarına uygun çalışan gerçeklemesidir.

---

## 1. Mimari Problem ve Emniyet Hedefi
Derin Öğrenme (DNN) veya Takviyeli Öğrenme (Reinforcement Learning) tabanlı bir otonom uçuş kontrolcüsü yüksek performanslı manevralar yapabilir ancak deterministik olarak sertifiye edilemez (**DAL E / Sertifikasız**).  
**ASTM F3269 Simplex Mimarisi** ile yapay zeka kontrolcüsünün önüne **DAL A seviyesinde sertifikalı bir Emniyet Monitörü (`RTA_EvaluateSafetyEnvelope`) ve Seçici Anahtar** yerleştirilir:

```mermaid
flowchart LR
    State["Uçuş Durumu<br/>(AoA, Roll, AGL, Heartbeat)"] --> Mon["DAL A Emniyet Monitörü<br/>[SYS-RTA-01]"]
    AI["Sertifikasız AI Kontrolcü<br/>(ai_elevator_cmd)"] --> Sw{"Simplex Anahtar<br/>[SYS-RTA-02]"}
    Safe["DAL A Kurtarma Kontrolcüsü<br/>(safe_elevator_cmd)"] --> Sw
    Mon -->|Zarf İhlali = TRUE<br/>(Latched Switch)| Sw
    Sw --> Act["İrtifa Dümeni (Elevator)<br/>Aktüatörü"]

    classDef dalA fill:#065f46,stroke:#34d399,stroke-width:2px,color:#fff;
    classDef cots fill:#7f1d1d,stroke:#f87171,stroke-width:2px,color:#fff;
    class Mon,Safe,Sw dalA;
    class AI cots;
```

---

## 2. Çift Yönlü İzlenebilirlik Zinciri (Bi-directional Traceability)

| Katman | Etiket ID | Tanım |
| :--- | :--- | :--- |
| **Tehlike (Hazard)** | `[HAZ-RTA-01]` | Yapay zeka uçuş kontrolcüsünün dağılım dışı (OOD) sensör verisiyle stall açısını aşan veya minimum irtifa altına inen komut üretmesi (Catastrophic). |
| **Sistem Gereksinimi 1** | `[SYS-RTA-01]` | Emniyet monitörü hücum açısını ($\text{AoA} \le 15^\circ$), yatış açısını ($|\text{Roll}| \le 45^\circ$) ve yerden yüksekliği ($\text{AGL} \ge 30\text{ m}$) 5 ms periyotla denetlemelidir. |
| **Sistem Gereksinimi 2** | `[SYS-RTA-02]` | Herhangi bir emniyet zarfı ihlalinde veya AI sağlık sayacı kaybında, Simplex anahtarı kontrolü kilitli (latched) olarak DAL A Emniyet Kontrolcüsüne devretmelidir. |
| **Üst Seviye Yazılım (HLR)** | `[HLR-RTA-001]` | Yazılım, 4 bağımsız zarf koşulunu değerlendirmeli ve ihlal nedenini (`RtaTripReason_t`) kaydetmelidir. |
| **Alt Seviye Tasarım (LLR)** | `[LLR-RTA-010]` | `RTA_EvaluateSafetyEnvelope()` fonksiyonu `(aoa_violated \|\| roll_violated \|\| alt_violated \|\| ai_faulted)` kararını değerlendirip aktüatör çıktısını seçmelidir. |
| **Doğrulama & MC/DC Testi**| `[UTEST-RTA-099]` | $N+1 = 5$ bağımsız MC/DC vektörü ve kilitli kalma (Latch) testi ile %100 yapısal kapsam doğrulaması. |

---

## 3. Çalıştırma ve Doğrulama

```bash
# 1. Python MC/DC Simülatörünü Çalıştırın:
python examples/rta-simplex-drone/sim_rta_simplex.py

# 2. C Birim Testini Derleyin ve Koşturun (GCC):
gcc -std=c99 -Wall -Wextra -Werror -Iexamples/rta-simplex-drone/include \
    examples/rta-simplex-drone/src/rta_simplex_monitor.c \
    examples/rta-simplex-drone/tests/test_rta_simplex_monitor.c \
    -o test_rta_simplex
./test_rta_simplex
```
