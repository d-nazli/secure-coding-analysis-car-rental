"""
Docstring for admin
"""

from utils import dangerous_eval

"""
Admin modülü, yönetici paneli ve ilgili işlevleri içerir.
"""

def admin_panel(code):
    return dangerous_eval(code)

def complex_calculation(x, y, z):
    """
    Karmaşık bir hesaplama fonksiyonu - Radon analizi için yüksek CC
    """
    if x > 0:
        if y > 0:
            if z > 0:
                return x + y + z
            elif z < 0:
                return x + y - z
            else:
                return x + y
        elif y < 0:
            if z > 0:
                return x - y + z
            elif z < 0:
                return x - y - z
            else:
                return x - y
        else:
            if z > 0:
                return x + z
            elif z < 0:
                return x - z
            else:
                return x
    elif x < 0:
        if y > 0:
            if z > 0:
                return -x + y + z
            elif z < 0:
                return -x + y - z
            else:
                return -x + y
        elif y < 0:
            if z > 0:
                return -x - y + z
            elif z < 0:
                return -x - y - z
            else:
                return -x - y
        else:
            if z > 0:
                return -x + z
            elif z < 0:
                return -x - z
            else:
                return -x
    else:
        if y > 0:
            if z > 0:
                return y + z
            elif z < 0:
                return y - z
            else:
                return y
        elif y < 0:
            if z > 0:
                return -y + z
            elif z < 0:
                return -y - z
            else:
                return -y
        else:
            if z > 0:
                return z
            elif z < 0:
                return -z
            else:
                return 0

def unused_function():
    """
    Kullanılmayan fonksiyon - Vulture analizi için
    """
    a = 1
    b = 2
    return a + b
