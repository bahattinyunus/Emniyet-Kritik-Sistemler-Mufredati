# 📘 Modül 4.1: RTCA DO-254 Karmaşık Elektronik Donanım (CEH) Tasarım Güvencesi

## 1. DO-254 Nedir?
**RTCA DO-254 / EUROCAE ED-80**, sivil hava araçlarındaki karmaşık elektronik donanımların (FPGA, ASIC, CPLD, PLD ve karmaşık kart tasarımları) tasarım güvencesini sağlayan standarttır.

DO-178C yazılım için ne ise, DO-254 donanım için odur. FPGA'ler artık saf donanım değil, VHDL/Verilog ile yazılan "kodlanabilir donanım" oldukları için katı bir sertifikasyon sürecine tabidir.

---

## 2. Tasarım Yaşam Döngüsü Aşamaları
1. **Planlama Süreci:** PHAC (Plan for Hardware Aspects of Certification) hazırlanması.
2. **Donanım Gereksinimleri:** Donanımın fonksiyonel ve çevresel kısıtlarının tanımlanması.
3. **Kavramsal Tasarım:** Blok diyagramlar ve mimari tercihler (örn: TMR, Saat alanları - Clock Domain Crossing).
4. **Detaylı Tasarım:** VHDL / Verilog / SystemVerilog RTL kodlaması ve sentez.
5. **Doğrulama & Geçerleme:** Simülasyon, statik zamanlama analizi (STA) ve FPGA-in-the-Loop testleri.

---

## 3. Donanım Tasarım Güvence Seviyeleri (DAL A - E)
DO-254'te de yazılım gibi DAL A, B, C, D ve E seviyeleri bulunur. DAL A ve B seviyelerinde:
- Kod Kapsamı (RTL Code Coverage: Statement, Branch, Condition, Toggle, FSM State/Transition).
- Bağımsız doğrulama zorunludur.

---

## 4. İzlenebilirlik Örneği
- `[HWR-FPGA-01]` FPGA, 10 MHz senkron saat frekansında çalışmalı ve DCM kilitlenene kadar reset durumunu korumalıdır.
- `[HIL-FPGA-01]` Osiloskop ve lojik analizör ile başlatma sinyalinin doğrulanması.
