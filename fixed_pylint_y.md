# Pylint Hatalarının Çözümleri

Bu dosya, `analysis_results/pylint.json` dosyasındaki tüm hataların çözümlerini içermektedir.

## 1. Eksik Modül Docstring'leri (C0114)

### admin.py
```python
"""Admin panel modülü."""
from utils import dangerous_eval

def admin_panel(code):
    return dangerous_eval(code)
```

### app.py
```python
"""Flask uygulama ana modülü."""
from datetime import date

from flask import Flask, render_template, request, redirect, session

from database import (
    init_db, seed_cars, get_all_cars,
    insert_rental, get_rentals_by_user
)
from auth import login_user, register_user

# ... rest of the code
```

### auth.py
```python
"""Kullanıcı kimlik doğrulama modülü."""
from database import get_user_by_username, create_user

# ... rest of the code
```

### cars.py
```python
"""Araç listeleme modülü."""
from database import get_all_cars

# ... rest of the code
```

### database.py
```python
"""Veritabanı işlemleri modülü."""
import sqlite3
import os

# ... rest of the code
```

### file_ops.py
```python
"""Dosya işlemleri modülü."""
def read_file(filename):
    """Dosya okuma fonksiyonu."""
    with open("data/" + filename, "r", encoding="utf-8") as f:
        return f.read()
```

### rental.py
```python
"""Araç kiralama işlemleri modülü."""
from database import get_connection

# ... rest of the code
```

### user_panel.py
```python
"""Kullanıcı paneli modülü."""
from database import get_connection

# ... rest of the code
```

### utils.py
```python
"""Yardımcı fonksiyonlar modülü."""
import os

# ... rest of the code
```

---

## 2. Eksik Fonksiyon Docstring'leri (C0116)

### admin.py
```python
def admin_panel(code):
    """Admin panel kodunu çalıştırır.
    
    Args:
        code: Çalıştırılacak kod string'i
        
    Returns:
        Kodun çalıştırılması sonucu
    """
    return dangerous_eval(code)
```

### app.py
```python
@app.route("/")
def root():
    """Ana sayfa yönlendirmesi."""
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Kullanıcı giriş sayfası."""
    if request.method == "POST":
        # ... existing code
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Kullanıcı kayıt sayfası."""
    if request.method == "POST":
        # ... existing code
    return render_template("register.html")


@app.route("/logout")
def logout():
    """Kullanıcı çıkış işlemi."""
    session.clear()
    return redirect("/login")


@app.route("/cars")
def cars():
    """Araç listesi sayfası."""
    if "user" not in session:
        return redirect("/login")

    available_cars = get_all_cars()  # ✅ Değişken adı değiştirildi
    return render_template("cars.html", cars=available_cars)


@app.route("/rent/<int:car_id>", methods=["GET", "POST"])
def rent(car_id):
    """Araç kiralama sayfası."""
    if "user" not in session:
        return redirect("/login")
    # ... existing code


@app.route("/my-rentals")
def my_rentals():
    """Kullanıcının kiralama geçmişi sayfası."""
    if "user" not in session:
        return redirect("/login")
    # ... existing code
```

### auth.py
```python
def login_user(username, password):
    """Kullanıcı giriş işlemini gerçekleştirir.
    
    Args:
        username: Kullanıcı adı
        password: Şifre
        
    Returns:
        Kullanıcı bilgileri tuple'ı veya None
    """
    user = get_user_by_username(username)
    # ... existing code


def register_user(username, password):
    """Yeni kullanıcı kaydı oluşturur.
    
    Args:
        username: Kullanıcı adı
        password: Şifre
        
    Returns:
        True
    """
    create_user(username, password)
    return True
```

### cars.py
```python
def list_cars():
    """Mevcut araçları listeler.
    
    Returns:
        Müsait araçların listesi
    """
    cars = get_all_cars()
    result = []

    for c in cars:
        if c[4] == 1:
            result.append(c)

    return result
```

### database.py
```python
def get_connection():
    """Veritabanı bağlantısı oluşturur.
    
    Returns:
        SQLite bağlantı nesnesi
    """
    return sqlite3.connect(DB_NAME)


def init_db():
    """Veritabanını başlatır ve tabloları oluşturur."""
    conn = get_connection()
    # ... existing code


def get_user_by_username(username):
    """Kullanıcı adına göre kullanıcı bilgilerini getirir.
    
    Args:
        username: Kullanıcı adı
        
    Returns:
        Kullanıcı bilgileri tuple'ı veya None
    """
    conn = get_connection()
    # ... existing code


def create_user(username, password):
    """Yeni kullanıcı oluşturur.
    
    Args:
        username: Kullanıcı adı
        password: Şifre
    """
    conn = get_connection()
    # ... existing code


def get_all_cars():
    """Tüm araçları getirir.
    
    Returns:
        Araç listesi
    """
    conn = get_connection()
    # ... existing code


def insert_rental(user_id, car_id, start_date, end_date, note):
    """Yeni kiralama kaydı oluşturur.
    
    Args:
        user_id: Kullanıcı ID
        car_id: Araç ID
        start_date: Başlangıç tarihi
        end_date: Bitiş tarihi
        note: Not
    """
    conn = get_connection()
    # ... existing code


def get_rentals_by_user(user_id):
    """Kullanıcının kiralama geçmişini getirir.
    
    Args:
        user_id: Kullanıcı ID
        
    Returns:
        Kiralama listesi
    """
    conn = get_connection()
    # ... existing code
```

### file_ops.py
```python
def read_file(filename):
    """Dosya okuma fonksiyonu.
    
    Args:
        filename: Okunacak dosya adı
        
    Returns:
        Dosya içeriği
    """
    with open("data/" + filename, "r", encoding="utf-8") as f:
        return f.read()
```

### rental.py
```python
def rent_car(user_id, car_id, days, note):
    """Araç kiralaması oluşturur.
    
    Args:
        user_id: Kullanıcı ID
        car_id: Araç ID
        days: Kiralama gün sayısı
        note: Not
    """
    conn = get_connection()
    # ... existing code


def approve_rental(role, days):
    """Kiralama onayını kontrol eder.
    
    Args:
        role: Kullanıcı rolü
        days: Kiralama gün sayısı
        
    Returns:
        Onay durumu (bool)
    """
    # ✅ Basitleştirilmiş versiyon
    return role == "admin" and 0 < days < 30
```

### user_panel.py
```python
def get_user_rentals(user_id):
    """Kullanıcının kiralama geçmişini getirir.
    
    Args:
        user_id: Kullanıcı ID
        
    Returns:
        Kiralama listesi
    """
    conn = get_connection()
    # ... existing code


def unused_user_helper():
    """Kullanılmayan yardımcı fonksiyon.
    
    Not: Bu fonksiyon kullanılmamaktadır ve silinebilir.
    """
    print("unused")
```

### utils.py
```python
def run_command(cmd):
    """Sistem komutu çalıştırır.
    
    Args:
        cmd: Çalıştırılacak komut
        
    Warning:
        Bu fonksiyon güvenlik riski taşır, kullanılmamalıdır.
    """
    os.system(cmd)


def dangerous_eval(expr):
    """Güvensiz eval fonksiyonu.
    
    Args:
        expr: Değerlendirilecek ifade
        
    Returns:
        Eval sonucu
        
    Warning:
        Bu fonksiyon güvenlik riski taşır, kullanılmamalıdır.
    """
    return eval(expr)


def unused_helper():
    """Kullanılmayan yardımcı fonksiyon.
    
    Not: Bu fonksiyon kullanılmamaktadır ve silinebilir.
    """
    pass
```

---

## 3. Yanlış Import Sırası (C0411) - app.py

**Hata:** `datetime.date` standard import'u, `flask.Flask` third-party import'undan önce gelmeli.

**Çözüm:**
```python
"""Flask uygulama ana modülü."""
from datetime import date  # ✅ Standard library önce

from flask import Flask, render_template, request, redirect, session  # ✅ Third-party sonra

from database import (
    init_db, seed_cars, get_all_cars,
    insert_rental, get_rentals_by_user
)
from auth import login_user, register_user
```

---

## 4. Dış Kapsamdaki İsmin Yeniden Tanımlanması (W0621) - app.py

**Hata:** `cars` fonksiyonu içinde `cars` değişkeni tanımlanmış.

**Çözüm:**
```python
@app.route("/cars")
def cars():
    """Araç listesi sayfası."""
    if "user" not in session:
        return redirect("/login")

    available_cars = get_all_cars()  # ✅ Değişken adı değiştirildi
    return render_template("cars.html", cars=available_cars)
```

---

## 5. Belirtilmemiş Encoding (W1514) - file_ops.py

**Hata:** `open()` fonksiyonunda encoding belirtilmemiş.

**Çözüm:**
```python
def read_file(filename):
    """Dosya okuma fonksiyonu.
    
    Args:
        filename: Okunacak dosya adı
        
    Returns:
        Dosya içeriği
    """
    with open("data/" + filename, "r", encoding="utf-8") as f:  # ✅ encoding eklendi
        return f.read()
```

---

## 6. Basitleştirilebilir If İfadesi (R1703) - rental.py

**Hata:** `approve_rental` fonksiyonundaki if ifadesi basitleştirilebilir.

**Çözüm:**
```python
def approve_rental(role, days):
    """Kiralama onayını kontrol eder.
    
    Args:
        role: Kullanıcı rolü
        days: Kiralama gün sayısı
        
    Returns:
        Onay durumu (bool)
    """
    # ✅ Basitleştirilmiş versiyon
    return role == "admin" and 0 < days < 30
```

---

## 7. Gereksiz Else Return (R1705) - rental.py

**Hata:** Return'den sonra else kullanılmamalı.

**Çözüm:**
```python
def approve_rental(role, days):
    """Kiralama onayını kontrol eder.
    
    Args:
        role: Kullanıcı rolü
        days: Kiralama gün sayısı
        
    Returns:
        Onay durumu (bool)
    """
    # ✅ Else kaldırıldı, direkt return
    if role != "admin":
        return False
    
    if days <= 0:
        return False
    
    if days >= 30:
        return False
    
    return True
    
    # VEYA daha basit:
    return role == "admin" and 0 < days < 30
```

---

## 8. Eval Kullanımı (W0123) - utils.py

**Hata:** `eval()` fonksiyonu güvenlik riski taşır.

**Çözüm:**
```python
def dangerous_eval(expr):
    """Güvensiz eval fonksiyonu.
    
    Args:
        expr: Değerlendirilecek ifade
        
    Returns:
        Eval sonucu
        
    Warning:
        Bu fonksiyon güvenlik riski taşır, kullanılmamalıdır.
        Alternatif olarak ast.literal_eval() kullanılabilir.
    """
    # ⚠️ UYARI: eval() güvenlik riski taşır!
    # ✅ Alternatif: ast.literal_eval() kullanılabilir (sadece literal değerler için)
    import ast
    try:
        return ast.literal_eval(expr)  # Güvenli alternatif
    except (ValueError, SyntaxError):
        # Eğer literal değilse, eval kullanmak zorundaysanız:
        return eval(expr)  # ⚠️ Hala riskli!
```

**Daha Güvenli Alternatif:**
```python
import ast

def safe_eval(expr):
    """Güvenli değerlendirme fonksiyonu (sadece literal değerler için).
    
    Args:
        expr: Değerlendirilecek ifade (sadece literal değerler)
        
    Returns:
        Değerlendirme sonucu
        
    Raises:
        ValueError: Geçersiz ifade durumunda
    """
    return ast.literal_eval(expr)
```

---

## Özet

Tüm pylint hatalarını düzeltmek için:

1. ✅ Tüm modüllere docstring ekleyin
2. ✅ Tüm fonksiyonlara docstring ekleyin
3. ✅ Import sırasını düzeltin (standard → third-party → local)
4. ✅ Değişken isim çakışmalarını çözün
5. ✅ `open()` fonksiyonlarında encoding belirtin
6. ✅ Basitleştirilebilir if ifadelerini düzeltin
7. ✅ Gereksiz else bloklarını kaldırın
8. ✅ `eval()` kullanımını güvenli alternatiflerle değiştirin

Bu değişiklikler yapıldıktan sonra pylint skorunuz önemli ölçüde artacaktır.

