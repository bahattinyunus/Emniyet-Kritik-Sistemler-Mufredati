# 📘 Modül 4.2: Radyasyon Etkileri, SEU (Single Event Upset) ve TMR Donanım Tasarımı

## 1. Havacılık ve Uzayda Radyasyon Tehlikesi
Yüksek irtifalarda (özellikle 30.000 ft üzerinde ve uzay ortamında) kozmik ışınlar ve nötron parçacıkları yarı iletken entegrelerin silikon tabakasına çarparak yük birikmesine neden olur.

### Temel Radyasyon Hata Türleri:
- **SEE (Single Event Effects):** Tekil parçacık etkileri.
- **SEU (Single Event Upset - Bit Flip):** Bellek hücresinde veya yazmaçta (flip-flop) bir bitin `0` iken `1`'e (veya tersi) dönmesi (Yumuşak hata - Soft error).
- **SEL (Single Event Latchup):** Entegrenin aşırı akım çekerek kısa devre olması ve yanması (Sert hata - Hard error).

---

## 2. FPGA Seviyesinde Savunma Mekanizmaları

### A. TMR (Triple Modular Redundancy) ile Flip-Flop Koruması
FPGA'deki kritik durum makinelerinin (FSM) registerları 3 kopyaya çıkarılır ve oylayıcı (voter) ile birleştirilir:

```vhdl
-- VHDL Örneği: TMR Çoğunluk Oylayıcısı
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity TMR_Voter is
    Port (
        din_a  : in  std_logic;
        din_b  : in  std_logic;
        din_c  : in  std_logic;
        dout   : out std_logic;
        fault  : out std_logic  -- Hata tespit bayrağı
    );
end TMR_Voter;

architecture Behavioral of TMR_Voter is
begin
    -- Çoğunluk Mantığı: En az 2 giriş '1' ise çıkış '1'dir
    dout  <= (din_a and din_b) or (din_b and din_c) or (din_a and din_c);
    
    -- Kanallardan biri diğerlerinden farklıysa SEU hatası algılanır
    fault <= (din_a xor din_b) or (din_b xor din_c);
end Behavioral;
```

### B. Konfigürasyon Belleği Temizleme (Memory Scrubbing)
SRAM tabanlı FPGA'lerde mantık kapılarını tanımlayan bit akışını (bitstream) tutan bellek periyodik olarak taranır, CRC kontrolü yapılır ve bozulan bitler yeniden yazılarak düzeltilir (Blind Scrubbing & Readback Scrubbing).

---

## 3. İzlenebilirlik İlişkisi
- `[HWR-RAD-040]` Uçuş bilgisayarı FPGA konfigürasyonu, SEU hatalarını 1 ms içinde tespit eden aktif bellek scrubbing devresine sahip olmalıdır.
- `[HIL-RAD-040]` Nötron ışınlama test rig'i ile bit-flip enjeksiyonu doğrulaması.
