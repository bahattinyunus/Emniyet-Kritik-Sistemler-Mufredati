# 📘 Modül 1.1: Emniyet-Kritik Sistem Yaşam Döngüsü ve V-Model

## 1. Giriş
Emniyet-kritik sistemlerin tasarımı geleneksel yazılım geliştirme modellerinden (Agile, Scrum, vb.) farklı olarak katı bir sertifikasyon ve süreç güvencesi (Process Assurance) gerektirir.

## 2. V-Model İlkeleri
* **Sol Kanat (Tasarım & Dekompozisyon):**
  - Müşteri ve pazar gereksinimlerinden konsept seviyeye iniş.
  - Tehlike analizi (FHA) ile her fonksiyonun risk seviyesinin belirlenmesi.
  - Fonksiyonel mimariden fiziksel mimariye geçiş (ARP 4754B).
* **V'nin Tabanı (Uygulama):**
  - Deterministik kodlama (MISRA C, SPARK Ada) ve donanım sentezi (VHDL).
* **Sağ Kanat (Doğrulama & Geçerleme - V&V):**
  - Birim testleri, MC/DC yapısal kapsam analizleri (DO-178C).
  - Donanım ve yazılım entegrasyonu (HIL - Hardware-in-the-Loop).
  - Sistem Emniyet Doğrulaması (SSA - ARP 4761A).

## 3. İzlenebilirlik Zinciri
Sistemdeki her bir öge `[HAZ-xxx]` -> `[SYS-xxx]` -> `[HLR-xxx]` -> `[LLR-xxx]` şeklinde kesintisiz bağlanmalıdır.
