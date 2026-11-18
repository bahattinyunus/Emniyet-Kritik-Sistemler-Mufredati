# 📘 Modül 10.2: Yazılım ve Donanım Araç Kalifikasyonu (RTCA DO-330 & ISO 26262 Part 8)

## 1. Neden Araç Kalifikasyonu (Tool Qualification) Zorunludur?
Emniyet-kritik sistem geliştirirken kod üretmek, derlemek, test koşturmak veya MC/DC kapsamını ölçmek için onlarca yazılım aracı kullanırız.
> **Kritik Soru:** *"Uçuş yazılımını doğrulayan test aracının veya otomatik kod üreten aracın kendisinde bir yazılım hatası (Bug) varsa ve bu hata uçaktaki bir hatayı gizliyorsa ne olur?"*

**RTCA DO-330 / EUROCAE ED-215** (*Software Tool Qualification Considerations*), bir geliştirme veya doğrulama aracının çıktısına insan incelemesi olmaksızın güvenilecekse, o aracın kendisinin de belirli bir güvence seviyesinde sertifiye edilmesini (kalifiye edilmesini) zorunlu kılar.

---

## 2. DO-330 Araç Kriterleri (Tool Criteria 1, 2, 3)
Bir aracın hangi seviyede kalifiye edileceğini iki faktör belirler:
1. Uçuş yazılımının **DAL seviyesi (DAL A – D)**
2. Aracın yaşam döngüsündeki **Kriteri (Criteria 1, 2 veya 3)**:

```mermaid
flowchart TD
    Q1{"Araç bir yaşam döngüsü sürecini<br/>otomatikleştiriyor mu?"}
    Q1 -->|Hayır| NO_QUAL["Kalifikasyon Gerekmez"]
    Q1 -->|Evet| Q2{"Aracın çıktısı başka bir kalifiye süreç veya<br/>insan incelemesiyle doğrulanıyor mu?"}
    Q2 -->|Evet: Tamamen Doğrulanıyor| NO_QUAL
    Q2 -->|Hayır: Çıktıya Doğrudan Güveniliyor| Q3{"Aracın uçuş yazılımına etkisi nedir?"}

    Q3 -->|Çıktısı uçuş kodunun bir parçası oluyor<br/>(Kod Üretici, Derleyici, Linker)| C1["KRİTER 1 (Criteria 1)<br/>Hata doğrudan koda enjekte edilebilir!<br/>(En Yüksek Risk: TQL-1 .. TQL-4)"]
    Q3 -->|Diğer geliştirme/doğrulama araçlarını<br/>veya süreci yönetiyor ama hatayı gizleyebilir| C2["KRİTER 2 (Criteria 2)<br/>Geliştirme/Doğrulama hatasını kaçırabilir<br/>(Orta Risk: TQL-4 .. TQL-5)"]
    Q3 -->|Mevcut bir doğrulama testinin yerini alıyor<br/>(MC/DC Aracı, Statik Analizör, RTM Motoru)| C3["KRİTER 3 (Criteria 3)<br/>Uçuş kodundaki hatayı tespit edemeyebilir<br/>(Standart Doğrulama Riski: TQL-5)"]

    classDef crit1 fill:#991b1b,stroke:#f87171,stroke-width:2px,color:#fff;
    classDef crit2 fill:#9a3412,stroke:#fb923c,stroke-width:2px,color:#fff;
    classDef crit3 fill:#1e3a8a,stroke:#60a5fa,stroke-width:2px,color:#fff;
    class C1 crit1;
    class C2 crit2;
    class C3 crit3;
```

---

## 3. TQL (Tool Qualification Level) Atama Matrisi (DO-178C / DO-330)

DO-330, **TQL-1** (en sıkı, neredeyse DAL A uçuş yazılımı kadar ağır) ile **TQL-5** (en yaygın doğrulama aracı seviyesi) arasında 5 seviye tanımlar:

| Uçuş Yazılımı DAL Seviyesi | Kriter 1 (Kod Üreten Araçlar)<br/>*Örn: SCADE KCG, Simulink Coder* | Kriter 2 (Kural / Süreç Denetleyen)<br/>*Örn: Otomatik Model Dönüştürücü* | Kriter 3 (Test / Kapsam / RTM Araçları)<br/>*Örn: VectorCAST, LDRA, Polyspace, RTM* |
| :---: | :---: | :---: | :---: |
| **DAL A** | **TQL-1** | **TQL-4** | **TQL-5** |
| **DAL B** | **TQL-2** | **TQL-4** | **TQL-5** |
| **DAL C** | **TQL-3** | **TQL-5** | **TQL-5** |
| **DAL D** | **TQL-4** | **TQL-5** | **TQL-5** |

> 💡 **Sık Sorulan Mülakat Sorusu: GCC veya Clang Derleyicisi (Compiler) neden TQL-1 olarak kalifiye edilmez?**  
> Bir C derleyicisi teknik olarak kaynak kodu makine koduna çevirir. Ancak derleyiciyi TQL-1 seviyesinde kalifiye etmek milyonlarca dolar tutar. Bunun yerine DO-178C'de tüm testler **derlenmiş makine kodunun koştuğu gerçek hedef işlemci (Target Hardware)** üzerinde yapılır ve DAL A'da **Kaynak Koddan Nesne Koduna İzlenebilirlik (Source-to-Object Code Traceability - Assembly incelemesi)** gerçekleştirilir. Böylece derleyicinin çıktısı tamamen doğrulandığı için derleyici kalifikasyonuna gerek kalmaz! (Ancak Airbus gibi firmalar ek güvence için formel olarak ispatlanmış **CompCert C** derleyicisini kullanmaktadır).

---

## 4. Otomotivde Araç Kalifikasyonu (ISO 26262-8: TI, TD ve TCL Seviyeleri)
ISO 26262 Bölüm 8 Madde 11, DO-330 ile aynı felsefeyi **TCL (Tool Confidence Level - TCL1, TCL2, TCL3)** üzerinden uygular:
- **TI (Tool Impact - TI1 / TI2):** Aracın hatası emniyet-kritik ürüne hata sokabilir veya hatayı gizleyebilir mi? (Evet ise **TI2**).
- **TD (Tool Error Detection - TD1 / TD2 / TD3):** Aracın yapacağı bir hatayı sonraki süreçlerde yakalama olasılığımız yüksek mi (**TD1**), orta mı (**TD2**), düşük mü (**TD3**)?
- Eğer `TI2` ve `TD3` ise araç **TCL3** (En yüksek risk) sınıflandırmasına girer ve ASIL D projede resmi kalifikasyon paketi (Tool Qualification Kit - QKit) gerektirir.

---

## 5. Araç Kalifikasyon Belgeleri (DO-330 Çıktıları)
Bir aracı (örneğin şirket içi geliştirdiğiniz bir RTM veya otomatik test üretici scripti) TQL-5 seviyesinde kalifiye etmek için şu 4 belge hazırlanır:
1. **TQP (Tool Qualification Plan):** Aracın hangi amaçla kullanılacağı ve nasıl kalifiye edileceği.
2. **TOR (Tool Operational Requirements):** Aracın operasyonel ortamda ne yapması gerektiğini tanımlayan gereksinimler (`[TOR-RTM-001]`).
3. **TVP & Результаты (Tool Verification Results):** Aracın hem normal hem de hatalı (bozuk dosya, eksik etiket) girdilerle test edildiğini gösteren doğrulama testleri.
4. **TAS (Tool Accomplishment Summary):** SOI denetçisine sunulan araç başarım özeti.

---

## 6. İzlenebilirlik Zinciri
- Sistem / Süreç Gereksinimi: `[SYS-TOOL-001]` İzlenebilirlik ve yapısal kapsam analizlerinde kullanılan tüm otomasyon araçları DO-330 TQL-5 (Kriter 3) operasyonel gereksinimlerini karşılamalıdır.
- Araç Gereksinimi: `[HLR-TOOL-010]` RTM analiz motoru, kaynak kod veya dokümanlardaki yetim (orphan) ve doğrulanmamış gereksinimleri %100 doğrulukla raporlamalıdır.
- Alt Seviye Tasarım: `[LLR-TOOL-020]` `analyze_traceability()` fonksiyonu her `LLR` etiketinin en az bir `TEST/UTEST` etiketine bağlı olduğunu kontrol etmelidir.
- Doğrulama Testi: `[UTEST-TOOL-030]` Bilinçli olarak test bağı koparılmış sahte gereksinim dosyası ile aracın açık (gap) tespit yeteneğinin doğrulanması.
