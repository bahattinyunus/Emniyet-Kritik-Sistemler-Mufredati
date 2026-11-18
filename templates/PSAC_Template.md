# 📑 RTCA DO-178C / EUROCAE ED-12C — Sertifikasyon Yazılım Boyutu Planı (PSAC) Şablonu
**Belge Kimliği:** `DOC-PSAC-2026-001` | **Revizyon:** `v1.0` | **Hedef Seviye:** `DAL A` | **Denetim Aşaması:** `SOI#1`

---

## 1. Amaç ve Kapsam (Purpose and Scope)
Bu **PSAC (Plan for Software Aspects of Certification)** dokümanı, `[PROJE_ADI]` uçuş kontrol yazılımının **RTCA DO-178C / EUROCAE ED-12C** (ve geçerli ekleri **DO-330, DO-331, DO-333**) hedeflerine uygun olarak nasıl geliştirileceğini, doğrulanacağını ve sertifikasyon otoritesine (FAA / EASA / TR-SHGM / Savunma Sertifikasyon Makamı) nasıl sunulacağını tanımlar.

---

## 2. Sistem ve Yazılım Genel Bakışı (System & Software Overview)

### 2.1 Sistem Mimarisi Özeti
- **Sistem Adı:** Birincil Uçuş Kontrol Bilgisayarı (Primary Flight Control Computer - PFCC)
- **Yedeklilik Mimarisi:** Çift Kanallı Komut/Monitör (`COM/MON` — Fail-Passive)
- **Hedef İşlemci & RTOS:** Dual-Core Lockstep ARM Cortex-R52 @ 400 MHz | ARINC 653 Uyumlu RTOS
- **Donanım/Yazılım Arayüzleri:** ARINC 429 (Sensör Girişleri), MIL-STD-1553B (Görev Bilgisayarı), CAN-FD (Aktüatör Sürücüleri)

### 2.2 Yazılım Partisyonları ve Kritiklik Tahsisi
| Partisyon ID | Partisyon Adı | ARP 4761A Hata Şiddeti | DO-178C Yazılım Seviyesi | Periyot / WCET Bütçesi |
| :--- | :--- | :---: | :---: | :---: |
| **`PART_01_FCS`** | Birincil Pitch/Roll Kontrol & RTA Simplex | Catastrophic ($<10^{-9}$/FH) | **DAL A** | $10\text{ ms}$ / $2.5\text{ ms}$ |
| **`PART_02_MON`** | Çapraz Kanal Tutarsızlık Monitörü | Catastrophic ($<10^{-9}$/FH) | **DAL A** | $10\text{ ms}$ / $1.0\text{ ms}$ |
| **`PART_03_BIT`** | Sürekli Dahili Test & Arıza Kayıt (CBIT/NVM) | Minor ($<10^{-3}$/FH) | **DAL D** | $100\text{ ms}$ / $5.0\text{ ms}$ |

---

## 3. Sertifikasyon Hususları ve Emniyet Tasarım İlkeleri (Certification Considerations)
1. **Ölü ve Devre Dışı Kod (Dead & Deactivated Code):** DAL A partisyonlarında hiçbir ölü kod (`Dead Code`) bulunmayacaktır. Yalnızca yer bakım modunda çalışan kodlar (`Deactivated Code`) `[SYS-SEC-101]` gereksinimi uyarınca donanımsal *Weight-on-Wheels (WoW)* kilidiyle korunacaktır.
2. **Türetilmiş Gereksinimler (Derived Requirements):** Yazılım mimari tasarımı sırasında ortaya çıkan tüm türetilmiş gereksinimler, Sistem Emniyet Grubu'na (ARP 4761A PSSA/SSA) geri bildirilerek tehlike analizi onayından geçirilecektir.
3. **Kodlama Standartları:** Tüm C kaynak kodları **MISRA C:2012** kurallarına %100 uyumlu olacak; dinamik bellek (`malloc/free`) ve özyineleme (`recursion`) kesinlikle kullanılmayacaktır.

---

## 4. Yazılım Yaşam Döngüsü Süreçleri ve Planları
Bu PSAC belgesi aşağıdaki 4 alt plan ve 3 standart ile birlikte yürütülür:
- **SDP:** *Software Development Plan* (`DOC-SDP-002`)
- **SVP:** *Software Verification Plan* (`DOC-SVP-003`)
- **SCMP:** *Software Configuration Management Plan* (`DOC-SCMP-004`)
- **SQAP:** *Software Quality Assurance Plan* (`DOC-SQAP-005`)
- **Standartlar:** Yazılım Gereksinim Standardı (EARS), Tasarım Standardı ve Kodlama Standardı (MISRA C:2012).

---

## 5. Araç Kalifikasyonu (DO-330 Tool Qualification Summary)

| Araç Adı | Kullanım Amacı | DO-330 Kriteri | Kalifikasyon Seviyesi (TQL) |
| :--- | :--- | :---: | :---: |
| **GCC C99 Cross-Compiler** | Kaynak koddan nesne kodu üretimi (Çıktısı hedef donanım testi ve Assembly incelemesi ile doğrulanır) | Kriter 1 (Doğrulamalı) | Kalifikasyon Gerekmez |
| **VectorCAST / LDRA** | Hedef işlemci üzerinde Birim Testi ve **MC/DC Yapısal Kapsam** ölçümü | Kriter 3 | **TQL-5** |
| **RTM & MISRA Denetleyici** | Çift yönlü izlenebilirlik (`rtm_generator.py`) ve statik kural denetimi | Kriter 3 | **TQL-5** |

---

## 6. Sertifikasyon Takvimi ve SOI (Stage of Involvement) Denetim Kilometre Taşları
- [x] **SOI#1 (Planlama Denetimi):** PSAC, SDP, SVP, SCMP, SQAP ve Standartların onayı.
- [ ] **SOI#2 (Geliştirme Denetimi):** HLR, LLR, Yazılım Mimarisi, Kaynak Kod ve RTM (%50+ tamamlanma).
- [ ] **SOI#3 (Doğrulama Denetimi):** Hedef donanım (HIL) test sonuçları, %100 MC/DC kapsamı, WCET ve Yığın (Stack) analizi.
- [ ] **SOI#4 (Nihai Uygunluk Denetimi):** SCI (*Software Configuration Index*), SAS (*Software Accomplishment Summary*) ve Açık Problem Raporlarının (PR) kapanışı.
