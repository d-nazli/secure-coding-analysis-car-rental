# Bandit Güvenlik Hatalarının Çözümleri

Bu dosya, `analysis_results/bandit.json` dosyasındaki tüm güvenlik hatalarının çözümlerini içermektedir.

---

## 1. Hardcoded Password (B105) - app.py

### Hata Açıklaması
**Dosya:** `app.py`  
**Satır:** 11  
**Test ID:** B105  
**Severity:** LOW  
**Confidence:** MEDIUM  
**CWE:** 259 (Use of Hard-coded Password)

**Sorun:** Flask uygulamasında secret key hardcoded (kod içine sabitlenmiş) olarak yazılmış. Bu, güvenlik riski oluşturur çünkü:
- Secret key kaynak kodda görünür
- Kod versiyon kontrol sistemine (Git) commit edildiğinde herkes görebilir
- Production ve development ortamları aynı key'i kullanır
- Key değiştirmek için kod değişikliği gerekir

**Mevcut Kod:**
```python
app = Flask(__name__)
app.secret_key = "hardcoded_secret_key_123"  # ❌
```

### Çözüm

**Çözüm 1: Ortam Değişkeni Kullanımı (Önerilen)**
```python
import os

app = Flask(__name__)
# ✅ Ortam değişkeninden secret key al
app.secret_key = os.environ.get('SECRET_KEY', 'fallback-dev-key-only')

# Production'da şöyle kullanılır:
# export SECRET_KEY="güvenli-random-string"
# veya
# SECRET_KEY=güvenli-random-string python app.py
```

**Çözüm 2: .env Dosyası Kullanımı (python-dotenv ile)**
```python
from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()  # .env dosyasını yükle

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# .env dosyası (Git'e eklenmemeli, .gitignore'da olmalı):
# SECRET_KEY=your-super-secret-key-here
```

**Çözüm 3: Güçlü Random Key Üretme**
```python
import secrets

app = Flask(__name__)
# ✅ Her uygulama başlatıldığında yeni key üret (development için)
# Production'da ortam değişkeni kullanılmalı
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))
```

**Önerilen Uygulama:**
```python
"""Flask uygulama ana modülü."""
import os
from datetime import date

from flask import Flask, render_template, request, redirect, session

# ✅ Secret key ortam değişkeninden alınır
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("SECRET_KEY ortam değişkeni ayarlanmalıdır!")

app = Flask(__name__)
app.secret_key = SECRET_KEY
```

---

## 2. Flask Debug Mode (B201) - app.py

### Hata Açıklaması
**Dosya:** `app.py`  
**Satır:** 102  
**Test ID:** B201  
**Severity:** HIGH  
**Confidence:** MEDIUM  
**CWE:** 94 (Code Injection)

**Sorun:** Flask uygulaması `debug=True` modunda çalıştırılıyor. Bu çok ciddi bir güvenlik riskidir çünkü:
- Werkzeug debugger'ı aktif olur ve hata sayfalarında interaktif debugger gösterilir
- Saldırganlar debugger üzerinden Python kodunu çalıştırabilir
- Uygulama içindeki tüm verilere erişim sağlanabilir
- Production ortamında kesinlikle kullanılmamalıdır

**Mevcut Kod:**
```python
if __name__ == "__main__":
    app.run(debug=True)  # ❌ debug açık
```

### Çözüm

**Çözüm 1: Ortam Değişkeni ile Kontrol (Önerilen)**
```python
if __name__ == "__main__":
    # ✅ Debug sadece development ortamında açık
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
```

**Çözüm 2: Production için WSGI Server Kullanımı**
```python
# app.py
if __name__ == "__main__":
    # ✅ Development için
    app.run(debug=False, host='127.0.0.1', port=5000)
    
# Production'da şöyle çalıştırılmalı:
# gunicorn -w 4 -b 0.0.0.0:5000 app:app
# veya
# uwsgi --http :5000 --wsgi-file app.py --callable app
```

**Çözüm 3: Flask Config Kullanımı**
```python
import os

# Development ve Production ayarları
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True  # ✅ Sadece development config'de

class ProductionConfig(Config):
    DEBUG = False

# Ortam değişkenine göre config seç
config_name = os.environ.get('FLASK_ENV', 'production')
if config_name == 'development':
    app.config.from_object(DevelopmentConfig)
else:
    app.config.from_object(ProductionConfig)

if __name__ == "__main__":
    app.run(debug=app.config['DEBUG'])
```

**Önerilen Uygulama:**
```python
if __name__ == "__main__":
    # ✅ Debug mode ortam değişkeninden kontrol edilir
    # Production'da FLASK_DEBUG ayarlanmamalı
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    if debug:
        print("⚠️  UYARI: Debug mode aktif! Production'da kullanmayın!")
    
    app.run(debug=debug, host='0.0.0.0', port=5000)
```

---

## 3. Hardcoded Password (B105) - auth.py

### Hata Açıklaması
**Dosya:** `auth.py`  
**Satır:** 4  
**Test ID:** B105  
**Severity:** LOW  
**Confidence:** MEDIUM  
**CWE:** 259 (Use of Hard-coded Password)

**Sorun:** Admin şifresi kod içine sabitlenmiş. Bu güvenlik riski oluşturur çünkü:
- Şifre kaynak kodda görünür
- Versiyon kontrol sisteminde saklanır
- Şifre değiştirmek için kod değişikliği gerekir
- Herkes admin şifresini görebilir

**Mevcut Kod:**
```python
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"  # ❌ hard-coded
```

### Çözüm

**Çözüm 1: Ortam Değişkeni Kullanımı (Önerilen)**
```python
"""Kullanıcı kimlik doğrulama modülü."""
import os
from database import get_user_by_username, create_user

# ✅ Ortam değişkenlerinden admin bilgileri alınır
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')

def login_user(username, password):
    user = get_user_by_username(username)
    
    if user and user[2] == password:
        return user
    
    # ✅ Admin şifresi ortam değişkeninden kontrol edilir
    if ADMIN_PASSWORD and username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return (0, ADMIN_USERNAME, ADMIN_PASSWORD, "admin")
    
    return None
```

**Çözüm 2: Veritabanında Admin Kullanıcısı (Daha İyi Çözüm)**
```python
"""Kullanıcı kimlik doğrulama modülü."""
from database import get_user_by_username, create_user
import hashlib

def hash_password(password):
    """Şifreyi hash'ler."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    """Şifre doğrulaması yapar."""
    return hash_password(password) == hashed

def login_user(username, password):
    """Kullanıcı giriş işlemini gerçekleştirir."""
    user = get_user_by_username(username)
    
    if not user:
        return None
    
    # ✅ Şifre hash'lenmiş olarak saklanmalı
    # Veritabanında admin kullanıcısı olmalı
    if verify_password(password, user[2]):  # user[2] = hashed_password
        return user
    
    return None

# Admin kullanıcısı veritabanında oluşturulmalı:
# INSERT INTO users (username, password, role) 
# VALUES ('admin', '<hashed_password>', 'admin');
```

**Çözüm 3: Şifre Hash'leme ile Güvenli Admin Kontrolü**
```python
"""Kullanıcı kimlik doğrulama modülü."""
import os
import hashlib
from database import get_user_by_username, create_user

def hash_password(password):
    """Şifreyi hash'ler."""
    return hashlib.sha256(password.encode()).hexdigest()

def login_user(username, password):
    """Kullanıcı giriş işlemini gerçekleştirir."""
    user = get_user_by_username(username)
    
    if user and user[2] == password:
        return user
    
    # ✅ Admin şifresi hash'lenerek kontrol edilir
    admin_password_hash = os.environ.get('ADMIN_PASSWORD_HASH')
    if admin_password_hash:
        if username == 'admin' and hash_password(password) == admin_password_hash:
            return (0, 'admin', password, "admin")
    
    return None
```

**Önerilen Uygulama:**
```python
"""Kullanıcı kimlik doğrulama modülü."""
import os
import hashlib
from database import get_user_by_username, create_user

def hash_password(password):
    """Şifreyi SHA-256 ile hash'ler."""
    return hashlib.sha256(password.encode()).hexdigest()

def login_user(username, password):
    """Kullanıcı giriş işlemini gerçekleştirir."""
    user = get_user_by_username(username)
    
    if user and user[2] == password:
        return user
    
    # ✅ Admin kullanıcısı veritabanında olmalı, hardcoded olmamalı
    # Eğer geçici olarak gerekliyse, ortam değişkeni kullanılmalı
    admin_user = get_user_by_username('admin')
    if admin_user and admin_user[2] == password:
        return admin_user
    
    return None
```

---

## 4. SQL Injection (B608) - database.py

### Hata Açıklaması
**Dosya:** `database.py`  
**Satır:** 111  
**Test ID:** B608  
**Severity:** MEDIUM  
**Confidence:** LOW  
**CWE:** 89 (SQL Injection)

**Sorun:** SQL sorgusu string interpolation (f-string) ile oluşturuluyor. Bu ciddi bir güvenlik açığıdır çünkü:
- Kullanıcı girdisi doğrudan SQL sorgusuna eklenir
- Saldırganlar özel karakterlerle SQL komutları enjekte edebilir
- Veritabanındaki tüm verilere erişim sağlanabilir
- Veriler silinebilir veya değiştirilebilir

**Mevcut Kod:**
```python
def get_user_by_username(username):
    conn = get_connection()
    cur = conn.cursor()
    
    # ❌ SQL Injection (bilerek)
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cur.execute(query)
    
    row = cur.fetchone()
    conn.close()
    return row
```

**Örnek Saldırı:**
```python
# Normal kullanım:
username = "john"
# SQL: SELECT * FROM users WHERE username = 'john'

# Saldırı:
username = "admin' OR '1'='1"
# SQL: SELECT * FROM users WHERE username = 'admin' OR '1'='1'
# Bu sorgu TÜM kullanıcıları döndürür!

# Daha tehlikeli saldırı:
username = "admin'; DROP TABLE users; --"
# SQL: SELECT * FROM users WHERE username = 'admin'; DROP TABLE users; --'
# Bu sorgu users tablosunu SİLER!
```

### Çözüm

**Çözüm: Parametreli Sorgular (Parameterized Queries) - Önerilen**

SQLite ve diğer veritabanları parametreli sorguları destekler. Bu yöntem SQL injection saldırılarını tamamen engeller.

```python
def get_user_by_username(username):
    """Kullanıcı adına göre kullanıcı bilgilerini getirir.
    
    Args:
        username: Kullanıcı adı
        
    Returns:
        Kullanıcı bilgileri tuple'ı veya None
    """
    conn = get_connection()
    cur = conn.cursor()
    
    # ✅ Parametreli sorgu kullanılır
    # ? placeholder'ı kullanıcı girdisini güvenli şekilde yerleştirir
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    
    row = cur.fetchone()
    conn.close()
    return row
```

**Açıklama:**
- `?` placeholder kullanılır
- Kullanıcı girdisi tuple olarak ayrı parametre olarak verilir: `(username,)`
- Veritabanı motoru otomatik olarak özel karakterleri escape eder
- SQL injection saldırıları engellenir

**Diğer Veritabanları için:**
```python
# PostgreSQL (psycopg2):
cur.execute("SELECT * FROM users WHERE username = %s", (username,))

# MySQL (mysql-connector):
cur.execute("SELECT * FROM users WHERE username = %s", (username,))

# SQLite (mevcut):
cur.execute("SELECT * FROM users WHERE username = ?", (username,))
```

**Önerilen Uygulama:**
```python
def get_user_by_username(username):
    """Kullanıcı adına göre kullanıcı bilgilerini getirir.
    
    Args:
        username: Kullanıcı adı
        
    Returns:
        Kullanıcı bilgileri tuple'ı veya None
        
    Note:
        Parametreli sorgu kullanılarak SQL injection saldırıları engellenir.
    """
    conn = get_connection()
    cur = conn.cursor()
    
    # ✅ Parametreli sorgu - SQL injection koruması
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    
    row = cur.fetchone()
    conn.close()
    return row
```

**Ek Güvenlik Önlemleri:**
```python
def get_user_by_username(username):
    """Kullanıcı adına göre kullanıcı bilgilerini getirir."""
    # ✅ Input validation
    if not username or not isinstance(username, str):
        return None
    
    # ✅ Username'i temizle (opsiyonel, ama iyi pratik)
    username = username.strip()
    
    if len(username) > 50:  # Maksimum uzunluk kontrolü
        return None
    
    conn = get_connection()
    cur = conn.cursor()
    
    # ✅ Parametreli sorgu
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    
    row = cur.fetchone()
    conn.close()
    return row
```

---

## 5. Shell Injection (B605) - utils.py

### Hata Açıklaması
**Dosya:** `utils.py`  
**Satır:** 6  
**Test ID:** B605  
**Severity:** HIGH  
**Confidence:** HIGH  
**CWE:** 78 (OS Command Injection)

**Sorun:** `os.system()` fonksiyonu kullanılıyor. Bu çok tehlikeli bir güvenlik açığıdır çünkü:
- Kullanıcı girdisi doğrudan shell komutuna dönüştürülür
- Saldırganlar shell komutlarını çalıştırabilir
- Sistem dosyalarına erişim sağlanabilir
- Veriler silinebilir veya sistem ele geçirilebilir

**Mevcut Kod:**
```python
def run_command(cmd):
    # ❌ os.system
    os.system(cmd)
```

**Örnek Saldırı:**
```python
# Normal kullanım:
cmd = "ls"
# Komut: ls

# Saldırı:
cmd = "ls; rm -rf /"
# Komut: ls; rm -rf /
# Bu komut tüm dosyaları SİLER!

# Başka bir saldırı:
cmd = "cat /etc/passwd"
# Sistem dosyalarına erişim

# Daha tehlikeli:
cmd = "python -c 'import os; os.system(\"rm -rf /\")'"
# Python kodu çalıştırma
```

### Çözüm

**Çözüm 1: subprocess Modülü Kullanımı (Önerilen)**

`subprocess` modülü shell injection saldırılarını engeller.

```python
import subprocess
import shlex

def run_command(cmd):
    """Güvenli komut çalıştırma.
    
    Args:
        cmd: Çalıştırılacak komut (string veya liste)
        
    Returns:
        Komut çıktısı
        
    Warning:
        Mümkünse bu fonksiyon kullanılmamalıdır.
        Eğer kullanılacaksa, cmd parametresi güvenilir kaynaklardan gelmelidir.
    """
    # ✅ subprocess.run() kullanılır, shell=False ile
    # Komut liste olarak verilir, shell kullanılmaz
    if isinstance(cmd, str):
        # String ise, güvenli şekilde parse et
        cmd = shlex.split(cmd)
    
    result = subprocess.run(
        cmd,
        shell=False,  # ✅ Shell kullanılmaz
        capture_output=True,
        text=True,
        timeout=30  # ✅ Timeout eklenir
    )
    
    return result.stdout
```

**Çözüm 2: Whitelist Yaklaşımı (Daha Güvenli)**

Sadece izin verilen komutların çalıştırılmasına izin verilir.

```python
import subprocess

ALLOWED_COMMANDS = ['ls', 'pwd', 'date', 'whoami']  # ✅ İzin verilen komutlar

def run_command(cmd):
    """Güvenli komut çalıştırma (whitelist ile).
    
    Args:
        cmd: Çalıştırılacak komut
        
    Returns:
        Komut çıktısı veya None
        
    Raises:
        ValueError: İzin verilmeyen komut durumunda
    """
    # ✅ Komut parse edilir
    if isinstance(cmd, str):
        parts = cmd.split()
        command = parts[0] if parts else None
    else:
        command = cmd[0] if cmd else None
    
    # ✅ Whitelist kontrolü
    if command not in ALLOWED_COMMANDS:
        raise ValueError(f"İzin verilmeyen komut: {command}")
    
    # ✅ subprocess ile güvenli çalıştırma
    result = subprocess.run(
        cmd if isinstance(cmd, list) else cmd.split(),
        shell=False,
        capture_output=True,
        text=True,
        timeout=30
    )
    
    return result.stdout
```

**Çözüm 3: Komut Yerine Python API Kullanımı (En Güvenli)**

Mümkünse shell komutları yerine Python API'leri kullanılmalıdır.

```python
import os
import subprocess

def list_files(directory='.'):
    """Dosyaları listeler (os.system yerine os.listdir).
    
    Args:
        directory: Listelenecek dizin
        
    Returns:
        Dosya listesi
    """
    # ✅ Python API kullanılır, shell komutu değil
    return os.listdir(directory)

def get_current_directory():
    """Mevcut dizini döndürür (pwd yerine os.getcwd).
    
    Returns:
        Mevcut dizin yolu
    """
    # ✅ Python API kullanılır
    return os.getcwd()

# Eğer mutlaka komut çalıştırılması gerekiyorsa:
def run_safe_command(command, args=None):
    """Güvenli komut çalıştırma.
    
    Args:
        command: Çalıştırılacak komut (whitelist'ten olmalı)
        args: Komut argümanları (liste)
        
    Returns:
        Komut çıktısı
    """
    ALLOWED = ['ls', 'pwd', 'date']
    
    if command not in ALLOWED:
        raise ValueError(f"İzin verilmeyen komut: {command}")
    
    cmd_list = [command]
    if args:
        cmd_list.extend(args)
    
    result = subprocess.run(
        cmd_list,
        shell=False,
        capture_output=True,
        text=True,
        timeout=30
    )
    
    if result.returncode != 0:
        raise RuntimeError(f"Komut başarısız: {result.stderr}")
    
    return result.stdout
```

**Önerilen Uygulama:**
```python
"""Yardımcı fonksiyonlar modülü."""
import subprocess
import shlex

def run_command(cmd):
    """Güvenli komut çalıştırma.
    
    Args:
        cmd: Çalıştırılacak komut (string veya liste)
        
    Returns:
        Komut çıktısı (stdout)
        
    Raises:
        subprocess.TimeoutExpired: Timeout durumunda
        subprocess.CalledProcessError: Komut hata döndürdüğünde
        
    Warning:
        Bu fonksiyon güvenlik riski taşır.
        Mümkünse Python API'leri kullanılmalıdır.
        Eğer kullanılacaksa, cmd parametresi güvenilir kaynaklardan gelmelidir.
    """
    # ✅ String ise güvenli şekilde parse et
    if isinstance(cmd, str):
        cmd = shlex.split(cmd)
    
    # ✅ subprocess.run() kullan, shell=False
    result = subprocess.run(
        cmd,
        shell=False,  # ✅ Shell injection engellenir
        capture_output=True,
        text=True,
        timeout=30,  # ✅ Timeout koruması
        check=False  # Hata durumunda exception fırlatma
    )
    
    if result.returncode != 0:
        raise subprocess.CalledProcessError(
            result.returncode,
            cmd,
            result.stdout,
            result.stderr
        )
    
    return result.stdout
```

---

## 6. Eval Kullanımı (B307) - utils.py

### Hata Açıklaması
**Dosya:** `utils.py`  
**Satır:** 11  
**Test ID:** B307  
**Severity:** MEDIUM  
**Confidence:** HIGH  
**CWE:** 78 (OS Command Injection)

**Sorun:** `eval()` fonksiyonu kullanılıyor. Bu güvenlik riski oluşturur çünkü:
- Kullanıcı girdisi doğrudan Python kodu olarak çalıştırılır
- Saldırganlar rastgele Python kodunu çalıştırabilir
- Dosya sistemi erişimi sağlanabilir
- Sistem komutları çalıştırılabilir

**Mevcut Kod:**
```python
def dangerous_eval(expr):
    # ❌ eval
    return eval(expr)
```

**Örnek Saldırı:**
```python
# Normal kullanım:
expr = "2 + 2"
# Sonuç: 4

# Saldırı:
expr = "__import__('os').system('rm -rf /')"
# Bu komut tüm dosyaları SİLER!

# Başka bir saldırı:
expr = "__import__('os').listdir('/etc')"
# Sistem dosyalarına erişim

# Daha tehlikeli:
expr = "open('/etc/passwd').read()"
# Sistem dosyalarını okuma
```

### Çözüm

**Çözüm 1: ast.literal_eval() Kullanımı (Önerilen)**

Sadece literal değerler (sayılar, stringler, listeler, dict'ler) için güvenlidir.

```python
import ast

def safe_eval(expr):
    """Güvenli değerlendirme (sadece literal değerler için).
    
    Args:
        expr: Değerlendirilecek ifade (sadece literal değerler)
        
    Returns:
        Değerlendirme sonucu
        
    Raises:
        ValueError: Geçersiz ifade durumunda
        
    Note:
        Bu fonksiyon sadece literal değerleri değerlendirir.
        Fonksiyon çağrıları, import'lar ve diğer kodlar çalıştırılamaz.
    """
    try:
        # ✅ ast.literal_eval() güvenlidir
        # Sadece literal değerleri değerlendirir
        return ast.literal_eval(expr)
    except (ValueError, SyntaxError) as e:
        raise ValueError(f"Geçersiz ifade: {expr}") from e

# Kullanım örnekleri:
# safe_eval("123") -> 123
# safe_eval("[1, 2, 3]") -> [1, 2, 3]
# safe_eval("{'key': 'value'}") -> {'key': 'value'}
# safe_eval("__import__('os')") -> ValueError (güvenli!)
```

**Çözüm 2: Whitelist Yaklaşımı**

Sadece izin verilen ifadelerin değerlendirilmesine izin verilir.

```python
import ast
import operator

# ✅ İzin verilen operatörler
ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
}

def safe_calculator(expr):
    """Güvenli matematiksel ifade değerlendirme.
    
    Args:
        expr: Matematiksel ifade (sadece sayılar ve temel operatörler)
        
    Returns:
        Hesaplama sonucu
        
    Raises:
        ValueError: Geçersiz ifade durumunda
    """
    try:
        # ✅ AST parse et
        node = ast.parse(expr, mode='eval')
        
        def eval_node(node):
            # ✅ Sadece sayılar ve izin verilen operatörler
            if isinstance(node, ast.Constant):
                return node.value
            elif isinstance(node, ast.BinOp):
                op = ALLOWED_OPERATORS.get(type(node.op))
                if op is None:
                    raise ValueError(f"İzin verilmeyen operatör: {type(node.op)}")
                return op(eval_node(node.left), eval_node(node.right))
            elif isinstance(node, ast.UnaryOp):
                if isinstance(node.op, ast.USub):
                    return -eval_node(node.operand)
                raise ValueError(f"İzin verilmeyen operatör: {type(node.op)}")
            else:
                raise ValueError(f"İzin verilmeyen ifade: {type(node)}")
        
        return eval_node(node.body)
    except SyntaxError as e:
        raise ValueError(f"Geçersiz ifade: {expr}") from e

# Kullanım:
# safe_calculator("2 + 2") -> 4
# safe_calculator("10 * 5") -> 50
# safe_calculator("__import__('os')") -> ValueError (güvenli!)
```

**Çözüm 3: JSON Kullanımı**

Eğer sadece veri yapıları gerekliyse, JSON kullanılabilir.

```python
import json

def parse_data(data_str):
    """JSON string'i parse eder.
    
    Args:
        data_str: JSON string
        
    Returns:
        Parse edilmiş veri
        
    Raises:
        json.JSONDecodeError: Geçersiz JSON durumunda
    """
    # ✅ JSON güvenlidir, kod çalıştırmaz
    return json.loads(data_str)

# Kullanım:
# parse_data('{"key": "value"}') -> {'key': 'value'}
# parse_data('[1, 2, 3]') -> [1, 2, 3]
```

**Çözüm 4: Fonksiyon Kaldırma veya Kısıtlama**

Eğer eval gerçekten gerekli değilse, fonksiyon kaldırılmalı veya çok kısıtlanmalıdır.

```python
def dangerous_eval(expr):
    """Güvensiz eval fonksiyonu - KULLANILMAMALI.
    
    Args:
        expr: Değerlendirilecek ifade
        
    Returns:
        Eval sonucu
        
    Warning:
        Bu fonksiyon güvenlik riski taşır ve kullanılmamalıdır.
        Alternatif olarak ast.literal_eval() kullanılmalıdır.
    """
    # ⚠️ UYARI: Bu fonksiyon kullanılmamalıdır!
    raise NotImplementedError(
        "Bu fonksiyon güvenlik riski taşır. "
        "Lütfen ast.literal_eval() veya başka bir alternatif kullanın."
    )
```

**Önerilen Uygulama:**
```python
"""Yardımcı fonksiyonlar modülü."""
import ast

def safe_eval(expr):
    """Güvenli değerlendirme (sadece literal değerler için).
    
    Args:
        expr: Değerlendirilecek ifade (sadece literal değerler)
        
    Returns:
        Değerlendirme sonucu
        
    Raises:
        ValueError: Geçersiz ifade durumunda
        
    Note:
        Bu fonksiyon sadece literal değerleri değerlendirir:
        - Sayılar: 123, 45.67
        - Stringler: "hello", 'world'
        - Listeler: [1, 2, 3]
        - Dict'ler: {"key": "value"}
        - Tuple'lar: (1, 2, 3)
        
        Fonksiyon çağrıları, import'lar ve diğer kodlar çalıştırılamaz.
    """
    try:
        # ✅ ast.literal_eval() güvenlidir
        return ast.literal_eval(expr)
    except (ValueError, SyntaxError) as e:
        raise ValueError(f"Geçersiz ifade veya güvenlik riski: {expr}") from e

# Eski fonksiyon deprecated olarak işaretlenir
def dangerous_eval(expr):
    """DEPRECATED: Güvensiz eval fonksiyonu.
    
    Bu fonksiyon kullanılmamalıdır. Bunun yerine safe_eval() kullanın.
    """
    import warnings
    warnings.warn(
        "dangerous_eval() güvenlik riski taşır. safe_eval() kullanın.",
        DeprecationWarning,
        stacklevel=2
    )
    return safe_eval(expr)  # Güvenli versiyona yönlendir
```

---

## Özet ve Genel Öneriler

### Güvenlik En İyi Pratikleri

1. **Secret Key ve Şifreler:**
   - ✅ Ortam değişkenleri kullanın
   - ✅ .env dosyası kullanın (python-dotenv)
   - ✅ Production'da güçlü, random key'ler kullanın
   - ❌ Kod içine hardcode etmeyin

2. **Debug Mode:**
   - ✅ Production'da debug=False
   - ✅ Ortam değişkeni ile kontrol edin
   - ❌ Production'da debug=True kullanmayın

3. **SQL Injection:**
   - ✅ Parametreli sorgular kullanın (? veya %s)
   - ✅ Input validation yapın
   - ❌ String interpolation kullanmayın

4. **Shell Injection:**
   - ✅ subprocess.run() kullanın (shell=False)
   - ✅ Whitelist yaklaşımı
   - ✅ Python API'leri kullanın (mümkünse)
   - ❌ os.system() kullanmayın

5. **Code Injection (eval):**
   - ✅ ast.literal_eval() kullanın
   - ✅ JSON kullanın (veri yapıları için)
   - ✅ Whitelist yaklaşımı
   - ❌ eval() kullanmayın

### Güvenlik Kontrol Listesi

- [ ] Tüm secret key'ler ortam değişkenlerinde
- [ ] Debug mode production'da kapalı
- [ ] Tüm SQL sorguları parametreli
- [ ] Shell komutları subprocess ile güvenli
- [ ] eval() kullanılmıyor veya güvenli alternatifler kullanılıyor
- [ ] Input validation yapılıyor
- [ ] Error handling uygun şekilde yapılıyor
- [ ] Logging güvenli (sensitive data loglanmıyor)

Bu değişiklikler yapıldıktan sonra bandit skorunuz önemli ölçüde artacak ve uygulamanız çok daha güvenli olacaktır.

