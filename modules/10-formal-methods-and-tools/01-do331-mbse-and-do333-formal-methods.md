# 📘 Modül 10.1: Model Tabanlı Geliştirme (DO-331) ve Formel Yöntemler (DO-333)

## 1. DO-178C Teknoloji Ekleri (Supplements)
2011 yılında yayınlanan **RTCA DO-178C**, temel yazılım yaşam döngüsünü değiştirmeden modern yazılım mühendisliği tekniklerini 4 resmi ek standartla (Supplement) sertifikasyon kapsamına almıştır:
1. **DO-330:** Yazılım Araçları Kalifikasyonu (*Software Tool Qualification Considerations*)
2. **DO-331:** Model Tabanlı Geliştirme ve Doğrulama (*Model-Based Development and Verification - MBDV*)
3. **DO-332:** Nesne Yönelimli Teknolojiler (*Object-Oriented Technology and Related Techniques - OOT*)
4. **DO-333:** Formel Yöntemler (*Formal Methods Supplement*)

---

## 2. DO-331: Model Tabanlı Geliştirme ve Doğrulama (MBSE / MBDV)
Modern uçuş kontrol (Fly-By-Wire), FADEC ve otonom sürüş yazılımlarının büyük bölümü elle C kodu yazılarak değil; **Ansys SCADE Suite** veya **MathWorks Simulink / Stateflow** ortamlarında matematiksel blok diyagramlar ve sonlu durum makineleri (FSM) olarak modellenip **Nitelikli Kod Üreticiler (Qualified Code Generators - Örn: SCADE KCG, Embedded Coder)** ile otomatik C/Ada koduna dönüştürülerek geliştirilir.

```mermaid
flowchart LR
    SYS["Sistem Gereksinimi<br/>[SYS-FCS-010]"] --> SPEC["Spesifikasyon Modeli (HLR)<br/>Simulink / System Composer"]
    SPEC --> DESIGN["Tasarım Modeli (LLR)<br/>Ansys SCADE / Simulink"]
    DESIGN -->|Model Simülasyonu &<br/>Model Coverage| MCOV["Model Doğrulama<br/>(DO-331 Tablo MB.A-7)"]
    DESIGN -->|TQL-1 Nitelikli<br/>Kod Üretici (KCG)| CODE["Otomatik Üretilen<br/>Deterministik C Kodu"]
    CODE -->|Hedef İşlemci Testi| TARGET["Target HIL &<br/>Object Code Doğrulama"]

    classDef mbd fill:#1e293b,stroke:#a855f7,stroke-width:2px,color:#fff;
    class SYS,SPEC,DESIGN,MCOV,CODE,TARGET mbd;
```

### DO-331'in Kritik Kuralları:
- **Model Simülasyonu $\neq$ Hedef Donanım Testi:** Bir modelin PC üzerinde Simulink'te doğru çalışması sertifikasyon için tek başına yetmez! Kaynak kod derlendikten sonra **gerçek hedef işlemci (Target Processor)** üzerinde kayan nokta aritmetiği, yığın kullanımı ve zamanlama açısından doğrulanmalıdır.
- **Model Kapsamı (Model Coverage) + Kod Kapsamı (Code Coverage):** Tasarım modelinde %100 model kapsamı (MCDC düzeyinde blok ve durum geçiş kapsamı) sağlanmalı; ayrıca üretilen C kodunda modele izlenemeyen fazladan kod (Unintended functionality) bulunmadığı kanıtlanmalıdır.

---

## 3. DO-333: Formel Yöntemler (Matematiksel İspat ile Doğrulama)
Geleneksel test (Dynamic Testing), yazılımın sadece test edilen girdi vektörleri için doğru çalıştığını gösterir.
> *"Program testi hataların varlığını gösterebilir, ancak hiçbir zaman hataların yokluğunu kanıtlayamaz."* — **Edsger W. Dijkstra**

**DO-333 Formel Yöntemler**, yazılımın olası **tüm girdi uzayı** ($-\infty$ ile $+\infty$ arasındaki tüm tamsayı/kayan nokta kombinasyonları) için spesifikasyona uyduğunu ve çalışma zamanı hatası (Run-Time Error) içermediğini **matematiksel mantık ve teorem ispatıyla** kanıtlar.

### Üç Temel Formel Yöntem Kategorisi:

| Yöntem | Matematiksel Temel | Endüstriyel Araçlar | Çözülen / Kanıtlanan Problem |
| :--- | :--- | :--- | :--- |
| **1. Soyut Yorumlama (Abstract Interpretation)** | Kafes Teorisi (Lattice Theory) ve Sabit Nokta Yaklaşımı | MathWorks Polyspace Code Prover, AbsInt Astrée,ait (WCET) | Sıfıra bölme, dizi sınır aşımı, aritmetik taşma (Overflow), NULL dereference hatalarının **sıfır yanlış negatifle (%100 seslilikle - Soundness)** yokluğunun ispatı ve kesin WCET hesabı. |
| **2. Model Denetimi (Model Checking)** | Zamansal Mantık (LTL / CTL) ve Durum Uzayı Taraması | NuSMV, SPIN, Kind 2, SCADE Design Verifier | Durum makinelerinde kilitlenme (Deadlock), canlılık kaybı (Livelock) ve "İniş takımı kilitliyken kapak asla kapanamaz" gibi zamansal emniyet özelliklerinin tüm durum geçişlerinde ispatı. |
| **3. Tümdengelimli Doğrulama (Deductive Verification)** | Hoare Mantığı ($\{P\}\ C\ \{Q\}$) ve SMT Çözücüler (Z3, Alt-Ergo) | SPARK Ada (GNATprove), Frama-C (WP), Dafny | Fonksiyonun ön koşulu ($P$) sağlandığında, fonksiyon ($C$) bittiğinde son koşulun ($Q$) matematiksel olarak her zaman doğru olduğunun teorem ispatı. |

---

## 4. Hoare Mantığı ve Sözleşmeli Tasarım (Design by Contract - SPARK Ada / Frama-C)

Hoare üçlüsü:
$$\{P\} \ S \ \{Q\}$$
- $P$ (**Precondition - Ön Koşul**): Fonksiyon çağrılmadan önce doğru olması gereken matematiksel bağıntı.
- $S$ (**Statement / Program**): İcra edilen deterministik algoritma.
- $Q$ (**Postcondition - Son Koşul**): Fonksiyon tamamlandığında garanti edilen matematiksel durum.

### Örnek: Frama-C (ACSL) ile Matematiksel Olarak İspatlanmış Emniyet Fonksiyonu
```c
#include <stdint.h>

#define MAX_ACTUATOR_CMD  (1000)
#define MIN_ACTUATOR_CMD  (-1000)

/*@
  @ requires \valid(out_cmd);
  @ requires -5000 <= raw_input <= 5000;
  @ assigns *out_cmd;
  @ ensures MIN_ACTUATOR_CMD <= *out_cmd <= MAX_ACTUATOR_CMD;
  @ behavior within_bounds:
  @   assumes MIN_ACTUATOR_CMD <= raw_input <= MAX_ACTUATOR_CMD;
  @   ensures *out_cmd == raw_input;
  @ behavior saturated_high:
  @   assumes raw_input > MAX_ACTUATOR_CMD;
  @   ensures *out_cmd == MAX_ACTUATOR_CMD;
  @ behavior saturated_low:
  @   assumes raw_input < MIN_ACTUATOR_CMD;
  @   ensures *out_cmd == MIN_ACTUATOR_CMD;
  @ complete behaviors;
  @ disjoint behaviors;
  @*/
void Actuator_SaturateCommand(const int32_t raw_input, int32_t * const out_cmd)
{
    /* [LLR-FORMAL-01] Aktüatör komutu saturasyon bariyeri */
    if (raw_input > MAX_ACTUATOR_CMD) {
        *out_cmd = MAX_ACTUATOR_CMD;
    } else if (raw_input < MIN_ACTUATOR_CMD) {
        *out_cmd = MIN_ACTUATOR_CMD;
    } else {
        *out_cmd = raw_input;
    }
}
```
> **Sertifikasyon Kredisi (DO-333):** Yukarıdaki fonksiyonun ACSL sözleşmesi Frama-C WP ve Z3 SMT çözücüsü ile %100 ispatlandığında, DO-178C kapsamında bu fonksiyon için geleneksel birim testi vakaları yazılmasına gerek kalmadan **Formel Doğrulama Kredisi** alınabilir!

---

## 5. İzlenebilirlik Zinciri
- Sistem Gereksinimi: `[SYS-FCS-090]` Uçuş kontrol yazılımında çalışma zamanı aritmetik taşma (Overflow) veya sıfıra bölme istisnası oluşma olasılığı matematiksel olarak sıfır olmalıdır.
- Üst Seviye Yazılım Gereksinimi: `[HLR-FORMAL-010]` Tüm DAL A kontrol döngüsü fonksiyonları Soyut Yorumlama (Abstract Interpretation) ve Ön/Son Koşul sözleşmeleriyle doğrulanmalıdır.
- Alt Seviye Tasarım Gereksinimi: `[LLR-FORMAL-01]` `Actuator_SaturateCommand()` fonksiyonu çıktıyı her zaman `[-1000, +1000]` kapalı aralığında sınırlandırmalıdır.
- Doğrulama Kanıtı: `[VAL-FORMAL-001]` Polyspace Code Prover / Frama-C WP %100 Yeşil (Proven Safe) doğrulama raporu.
