# 📘 Modül 3.1: RTCA DO-178C / EUROCAE ED-12C İlkeleri ve DAL Seviyeleri

## 1. DO-178C Standardının Doğası
**DO-178C**, havacılık yazılımlarının uçuşa elverişlilik (airworthiness) onayını alabilmesi için yerine getirilmesi gereken hedefleri (objectives) belirleyen uluslararası standarttır.

> **Önemli İlke:** DO-178C yazılımın *nasıl yazılacağını* (hangi dilde, hangi kütüphaneyle) söylemez; geliştirme ve doğrulama süreçlerinin *nasıl kontrol altında tutulduğunu, belgelendiğini ve doğrulandığını (Process Assurance)* denetler.

---

## 2. Yazılım Seviyeleri (DAL - Design Assurance Level)

| Seviye | Hata Durum Şiddeti | Örnek Uçuş Fonksiyonu | Toplam Hedef Sayısı | Bağımsız Doğrulama Hedefi | Zorunlu Yapısal Kapsam |
| :---: | :--- | :--- | :---: | :---: | :--- |
| **DAL A** | **Catastrophic (Felaket)** | Fly-By-Wire Uçuş Kontrol, FADEC | **71** | 33 | **MC/DC**, Decision, Statement |
| **DAL B** | **Hazardous (Ağır-Büyük)** | Kabin Basınçlandırma, Fren Kontrol | **69** | 21 | **Decision**, Statement |
| **DAL C** | **Major (Büyük)** | Otopilot Seyrüsefer Ekranı | **62** | 8 | **Statement** |
| **DAL D** | **Minor (Küçük)** | Uçuş Veri Kaydedici (FDR), Bakım Sistemi | **28** | 2 | Yok |
| **DAL E** | **No Safety Effect** | Yolcu Eğlence Sistemi (IFE) | **0** | 0 | Yok |

---

## 3. Bağımsızlık (Independence) Prensibi
DAL A ve B seviyelerinde, bir gereksinimi veya kodu yazan mühendis, o gereksinimin veya kodun testini/doğrulamasını **kendisi yapamaz**. 
- Hedeflerin "With Independence" olarak yerine getirilmesi şarttır.
- Bu kural, insanın kendi yaptığı hatayı görme körlüğünü (developer bias) ortadan kaldırır.

---

## 4. Dört Temel SOI (Stage of Involvement) Denetimi
FAA veya EASA sertifikasyon yetkilisi yazılım geliştirme sürecini 4 ana aşamada denetler:
1. **SOI#1 - Planlama:** PSAC (Plan for Software Aspects of Certification), SDP, SVP belgelerinin onayı.
2. **SOI#2 - Geliştirme:** Gereksinimlerin (HLR/LLR) ve mimarinin standartlara uyumu.
3. **SOI#3 - Doğrulama:** Test sonuçları, yapısal kapsam (MC/DC) ve izlenebilirlik matrisi (RTM).
4. **SOI#4 - Nihai Onay:** SAS (Software Accomplishment Summary) ve konfigürasyon dökümü.

---

## 5. İzlenebilirlik İlişkisi
- `[HLR-SYS-001]` Yazılım başlatıldığında (Cold Boot) 500 ms içinde sensör iletişimini başlatmalıdır.
- `[LLR-INIT-012]` `bsp_init_i2c()` fonksiyonu register yapılandırmasını tamamlayıp `READY` durumuna geçmelidir.
