# PyEnosPy

Basit ve kullanışlı bir mouse ve klavye kontrol kütüphanesi.

## Kurulum

```bash
pip install pyenospy
```

## Kullanım

```python
from pyenospy import MyInput

# Kütüphaneyi başlat
input = MyInput()

# Mouse kontrolü
input.mouse_move(100, 200)  # Mouse'u (100,200) konumuna taşı
input.mouse_click('left')   # Sol tıklama yap
input.mouse_double_click()  # Çift tıklama yap

# Klavye kontrolü
input.key_press('a')        # 'a' tuşuna bas
input.type_text("Merhaba")  # "Merhaba" yaz

# Tuş kombinasyonu
input.key_down('shift')     # Shift tuşunu basılı tut
input.key_press('a')        # Shift+A kombinasyonu
input.key_up('shift')       # Shift tuşunu bırak

# Bekleme
input.wait(1.5)            # 1.5 saniye bekle
```

## Özellikler

- Mouse kontrolü (hareket, tıklama, çift tıklama)
- Klavye kontrolü (tuş basma, tuş kombinasyonları, metin yazma)
- Bekleme fonksiyonu
- Basit ve anlaşılır API
- Türkçe dokümantasyon

## Gereksinimler

- Python 3.6 veya üzeri
- Windows işletim sistemi
- pywin32 paketi

## Lisans

MIT License 