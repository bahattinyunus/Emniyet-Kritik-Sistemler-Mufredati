# 📋 Şablon: Sistem Tehlike Kaydı ve Takip Formu (Hazard Log)

| Tehlike ID | Fonksiyon / Alt Sistem | Tehlike Açıklaması | Başarısızlık Durumu (Failure Condition) | DAL / ASIL Seviyesi | Kök Neden & Hata Modu | Emniyet Bariyeri / Önlem | Doğrulama Yöntemi | Statü |
| :--- | :--- | :--- | :--- | :---: | :--- | :--- | :--- | :---: |
| **`[HAZ-001]`** | Uçuş Kontrol (FCC) | İrtifa dümeninin istenmeyen dalış açısına kilitlenmesi | Catastrophic | DAL A | COM/MON işlemcileri arasında hesaplama sapması | `[SYS-FCC-043]` COM/MON tutarsızlık izleme ve otomatik bypass | HIL Rig Testi & MC/DC | AÇIK |
| **`[HAZ-002]`** | Yakıt Yönetimi | Yakıt pompası aşırı ısınması ve alev alma | Catastrophic | DAL A | Pompa kuru çalışma veya mekanik kilitlenme | `[SYS-FUEL-012]` Çift redundan sıcaklık sensörü ve acil kapatma valfi | DO-160G Çevresel & Birim Test | KAPALI |
| **`[HAZ-003]`** | Otopilot Seyrüsefer | GPS sinyalinin aniden kaybolması veya yanıltılması (Spoofing) | Hazardous | DAL B | Harici RF bozulması veya anten arızası | `[SYS-NAV-020]` Çoklu sensör füzyonu (GPS + INS + Baro) | Simülasyon & Uçuş Testi | AÇIK |
