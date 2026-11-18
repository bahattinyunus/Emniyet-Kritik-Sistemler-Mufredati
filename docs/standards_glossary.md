# 📖 Emniyet-Kritik Sistemler Terminoloji ve Kısaltmalar Sözlüğü (Glossary)

| Kısaltma | Açılımı | Standardı | Tanım |
| :--- | :--- | :--- | :--- |
| **AFDX** | Avionics Full-Duplex Switched Ethernet | ARINC 664 P7 | Sanal bağlantı (VL) ve BAG ile deterministik hale getirilmiş aviyonik Ethernet ağı |
| **ARP** | Aerospace Recommended Practice | SAE | Havacılık tavsiye edilen sistem ve emniyet mühendislik uygulamaları (ARP 4754B / 4761A) |
| **ASIL** | Automotive Safety Integrity Level | ISO 26262 | Otomotiv fonksiyonel emniyet bütünlük seviyesi (ASIL A, B, C, D) |
| **BAG** | Bandwidth Allocation Gap | ARINC 664 P7 | AFDX ağında bir sanal bağlantıdan gönderilen iki paket arasındaki minimum süre ($1..128\text{ ms}$) |
| **CAST-32A** | Certification Authorities Software Team Position Paper 32A | FAA / EASA AMC 20-193 | Çok çekirdekli (Multi-Core) işlemcilerde paylaşılan kaynak girişimlerinin (Interference) yönetimi |
| **CCA** | Common Cause Analysis | ARP 4761A | Yedekli kanalları aynı anda çökertebilecek ortak nedenlerin analizi (ZSA, PRA, CMA) |
| **CCF** | Common Cause Failure | ARP 4761A / ISO 26262 | Ortak kök nedene bağlı çoklu bağımsız bileşen arızası |
| **CEH** | Complex Electronic Hardware | RTCA DO-254 | İç durumları sadece dış pin testleriyle tamamen doğrulanamayan FPGA, ASIC ve PLD donanımları |
| **COM/MON** | Command and Monitor Architecture | ARP 4754B | Bir kanalın kontrol komutu ürettiği, bağımsız ikinci kanalın ise çıktıyı denetlediği mimari |
| **COTS** | Commercial Off-The-Shelf | Genel | Ticari hazır raf ürünü donanım veya yazılım bileşeni |
| **DAL** | Design Assurance Level | DO-178C / DO-254 | Yazılım ve donanım tasarım güvence seviyesi (DAL A: Catastrophic ... DAL E: No Safety Effect) |
| **DO-160G** | Environmental Conditions and Test Procedures for Airborne Equipment | RTCA / EUROCAE ED-14G | Aviyonik donanımların sıcaklık, titreşim, yıldırım, HIRF ve güç dalgalanması test standardı |
| **DO-178C** | Software Considerations in Airborne Systems and Equipment Certification | RTCA / EUROCAE ED-12C | Havacılık yazılımlarının uçuşa elverişlilik sertifikasyonu için temel süreç standardı |
| **DO-254** | Design Assurance Guidance for Airborne Electronic Hardware | RTCA / EUROCAE ED-80 | Uçuşa elverişli karmaşık elektronik donanımların (FPGA/ASIC/ Kart) tasarım güvence standardı |
| **DO-326A** | Airworthiness Security Process Specification | RTCA / EUROCAE ED-202A | Havacılık sistemlerinde siber güvenlik risk değerlendirme ve uçuşa elverişlilik güvenlik süreci |
| **DO-330** | Software Tool Qualification Considerations | RTCA / EUROCAE ED-215 | Geliştirme ve doğrulama yazılım araçlarının (TQL-1 .. TQL-5) kalifikasyon standardı |
| **DO-331** | Model-Based Development and Verification Supplement | RTCA / EUROCAE ED-218 | Simulink / SCADE gibi model tabanlı geliştirme ve otomatik kod üretimi sertifikasyon eki |
| **DO-333** | Formal Methods Supplement to DO-178C | RTCA / EUROCAE ED-216 | Soyut yorumlama, model denetimi ve teorem ispatı ile formel yazılım doğrulama eki |
| **E2E** | End-to-End Communication Protection | AUTOSAR / ISO 26262 | Veri yolu mesajlarının CRC, Alive Counter ve Data ID ile uçtan uca bütünlük koruması |
| **EARS** | Easy Approach to Requirements Syntax | Rolls-Royce / INCOSE | `WHEN / WHILE / IF-THEN / WHERE` kalıplarıyla belirsizlikten uzak atomik gereksinim yazım dili |
| **FADEC** | Full Authority Digital Engine Control | Havacılık | Pilot müdahalesi olmaksızın motor parametrelerini tam yetkiyle yöneten çift kanallı bilgisayar |
| **FCC** | Flight Control Computer | Havacılık | Fly-By-Wire uçuş kontrol yüzeylerini yöneten emniyet-kritik bilgisayar |
| **FDAL / IDAL**| Functional / Item Development Assurance Level | SAE ARP 4754B | Sistem fonksiyonu (FDAL) ve alt donanım/yazılım bileşeni (IDAL) tasarım güvence seviyeleri |
| **FHA** | Functional Hazard Assessment | SAE ARP 4761A | Sistem ve hava aracı fonksiyonlarının arıza durumlarını ve şiddetlerini belirleyen ilk analiz |
| **FIT** | Failure In Time | ISO 26262 / IEC 61508 | $10^9$ (1 Milyar) çalışma saati başına beklenen donanım arıza sayısı ($\text{ASIL D} < 10\text{ FIT}$) |
| **FMEA / FMECA**| Failure Mode, Effects, and Criticality Analysis | ARP 4761A / MIL-STD-1629| Bileşen arızalarından sistem etkisine giden aşağıdan yukarıya (indüktif) güvenilirlik analizi |
| **FTA** | Fault Tree Analysis | ARP 4761A / IEC 61025 | İstenmeyen tepe olaydan kök nedenlere inen yukarıdan aşağıya (dedüktif) Boolean hata ağacı analizi |
| **GSN** | Goal Structuring Notation | Safety Case | Emniyet dosyası iddia (Goal), strateji ve kanıtlarını (Solution) görsel modelleme notasyonu |
| **HARA** | Hazard Analysis and Risk Assessment | ISO 26262-3 | Otomotivde Şiddet (S), Maruziyet (E) ve Kontrol Edilebilirlik (C) ile ASIL belirleme analizi |
| **HIL** | Hardware-in-the-Loop | Doğrulama | Gerçek uçuş bilgisayarının sanal uçak ve sensör simülatörüne bağlanarak gerçek zamanlı testi |
| **HLR / LLR** | High-Level / Low-Level Requirements | RTCA DO-178C | Üst seviye ("Ne yapılacak?") ve alt seviye ("Nasıl kodlanacak?") yazılım gereksinimleri |
| **HSM** | Hardware Security Module | ISO/SAE 21434 | Kriptografik anahtarları ve Secure Boot doğrulamasını izole donanımda yürüten güvenlik çekirdeği |
| **IMA** | Integrated Modular Avionics | ARINC 653 / DO-297 | Farklı kritiklikteki uygulamaların uzamsal ve zamansal izole partisyonlarda ortak CPU'da koşması |
| **MC/DC** | Modified Condition/Decision Coverage | DO-178C (DAL A) | Karar içindeki her bir alt koşulun sonucu tek başına değiştirebildiğini kanıtlayan yapısal kapsam |
| **MCS** | Minimal Cut Set | ARP 4761A (FTA) | Tepe olayın gerçekleşmesi için birlikte arızalanması gereken en küçük temel olaylar kümesi |
| **MILS** | Multiple Independent Levels of Security | Siber Güvenlik | Ayrıştırma çekirdeği (Separation Kernel) ile farklı güvenlik seviyeli partisyonların izolasyonu |
| **MISRA** | Motor Industry Software Reliability Association | MISRA C:2012 / C++:2023 | Tanımsız davranışları ve bellek hatalarını önleyen deterministik C/C++ kodlama kural seti |
| **ODD** | Operational Design Domain | EASA AI / ISO 21448 | Otonom veya yapay zeka sisteminin emniyetle çalışmak üzere tasarlandığı çevre ve hız zarfı |
| **PSAC** | Plan for Software Aspects of Certification | RTCA DO-178C | SOI#1 aşamasında otoriteye sunulan ana yazılım sertifikasyon yol haritası belgesi |
| **PSSA / SSA** | Preliminary / System Safety Assessment | SAE ARP 4761A | Mimari tasarım sırasında yapılan ön emniyet (PSSA) ve nihai kanıt (SSA) değerlendirmeleri |
| **RTA** | Run-Time Assurance | ASTM F3269 | Sertifikasız/AI kontrolcüyü çalışma zamanında denetleyip güvenli kontrolcüye geçen Simplex mimari |
| **RTM** | Requirements Traceability Matrix | ARP 4754B / DO-178C | Tehlikeden (`HAZ`) gereksinime (`SYS/HLR/LLR`), koda ve teste (`TEST`) çift yönlü izlenebilirlik |
| **SAL** | Security Assurance Level | RTCA DO-326A / DO-356A | Siber güvenlik bariyerlerinin tasarım ve doğrulama sıkılık seviyesi (SAL 0 – SAL 3) |
| **SAS** | Software Accomplishment Summary | RTCA DO-178C | SOI#4 sonunda sertifikasyon otoritesine sunulan nihai yazılım başarım ve uyumluluk özeti |
| **SecOC** | Secure Onboard Communication | AUTOSAR / ISO 21434 | Araç içi ağ mesajlarının CMAC ve Freshness Value ile kriptografik kimlik doğrulaması |
| **SEU / SEL** | Single Event Upset / Latchup | RTCA DO-254 / Uzay | Kozmik radyasyon/nötron çarpması kaynaklı bit devrilmesi (SEU) veya yarı iletken kısa devresi (SEL) |
| **SIL** | Safety Integrity Level | IEC 61508 / EN 50128 | Endüstriyel ve demiryolu sistemleri emniyet bütünlük seviyesi (SIL 1 – SIL 4) |
| **SOI** | Stage of Involvement | FAA / EASA | Otoritenin projeyi denetlediği 4 aşama (SOI#1 Planlama, SOI#2 Geliştirme, SOI#3 Test, SOI#4 Onay) |
| **SOTIF** | Safety of the Intended Functionality | ISO 21448 | Donanım/yazılım arızası olmasa dahi sensör ve AI algı sınırlarından kaynaklanan risklerin yönetimi |
| **STPA** | System-Theoretic Process Analysis | STAMP (MIT) | Kazaları bileşen arızası yerine kontrol döngüsü ve güvensiz kontrol eylemleri (UCA) ile çözen analiz |
| **TARA** | Threat Analysis and Risk Assessment | ISO/SAE 21434 | Otomotiv siber güvenlik tehdit, saldırı yolu fizibilitesi ve risk değerlendirme metodolojisi |
| **TMR** | Triple Modular Redundancy | Donanım / Mimari | Üç paralel modülün çıktısının çoğunluk oylayıcı (2-out-of-3 Majority Voter) ile birleştirilmesi |
| **TQL** | Tool Qualification Level | RTCA DO-330 | Geliştirme ve doğrulama araçlarının kalifikasyon seviyesi (TQL-1 en yüksek ... TQL-5) |
| **WCET** | Worst-Case Execution Time | RTOS / DO-178C | Bir kod bloğunun hedef işlemcide çalışabileceği matematiksel olarak kanıtlanmış en uzun süre |
| **ZSA** | Zonal Safety Analysis | SAE ARP 4761A | Uçak içindeki fiziksel bölgelerde kablo, boru ve ekipmanların yakınlık/etkileşim emniyet analizi |
