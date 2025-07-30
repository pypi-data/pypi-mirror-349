# Please Don'T Mess With My Rights
# I Got Tired Of Designing 
# This Is My Telegram Account To Contact Me~@f_g_d_6~I am Name (•-•) Sajad

from hashlib import sha256
from typing import Union as U
import os,os as G
import hmac
a = b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

# Please Don'T Mess With My Rights
# I Got Tired Of Designing 
# This Is My Telegram Account To Contact Me~@f_g_d_6~I am Name (•-•) Sajad
def b(v: U[str,bytes]) -> bytes:
    return v.encode("utf-8") if isinstance(v,str) else v

# Please Don'T Mess With My Rights
# I Got Tired Of Designing 
# This Is My Telegram Account To Contact Me~@f_g_d_6~I am Name (•-•) Sajad
def c(i: int,z: bytes = a) -> bytes:
    if not i:
        return z[0:1]
    s = b""
    r = len(z)
    while i:
        i,d = divmod(i,r)
        s = z[d:d+1] + s
    return s

# Please Don'T Mess With My Rights
# I Got Tired Of Designing 
# This Is My Telegram Account To Contact Me~@f_g_d_6~I am Name (•-•) Sajad
def d(x: bytes,k: bytes) -> bytes: 
    return bytes(b ^ k[i % len(k)] for i,b in enumerate(x))

# Please Don'T Mess With My Rights
# I Got Tired Of Designing 
# This Is My Telegram Account To Contact Me~@f_g_d_6~I am Name (•-•) Sajad
def F_L(code: bytes,key: bytes,rounds: int) -> bytes: 
    out = code
    for _ in range(rounds):
        out = d(out,key)
        key = sha256(key + b'Sajad').digest()
    return out

# Please Don'T Mess With My Rights
# I Got Tired Of Designing 
# This Is My Telegram Account To Contact Me~@f_g_d_6~I am Name (•-•) Sajad
def JS(code: bytes,key: bytes,rounds: int = 5) -> bytes: 
    out = F_L(code,key,2)
    for _ in range(rounds):
        out = d(out,key)
        key = sha256(key).digest()
    return F_L(out,key,3)

# Please Don'T Mess With My Rights
# I Got Tired Of Designing 
# This Is My Telegram Account To Contact Me~@f_g_d_6~I am Name (•-•) Sajad
def e(v: U[str,bytes],z: bytes = a) -> int:
    v = b(v)
    n = 0
    r = len(z)
    for c in v:
        n = n * r + z.index(c)
    return n

# Please Don'T Mess With My Rights
# I Got Tired Of Designing 
# This Is My Telegram Account To Contact Me~@f_g_d_6~I am Name (•-•) Sajad
def Implement(obj,token: bytes = b'SajadXS-Secret',globals_=None,locals_=None): 
    if obj.get("auth") != sha256(token).digest():
        raise PermissionError("كوم بي لك 😂")
    code = obj.get("code",b"")
    if isinstance(code,bytes):
        code = code.decode(errors='ignore')
    if os.path.isfile(code):
        with open(code,'r',encoding='utf-8') as f:
            code = f.read()
    if globals_ is None:
        globals_ = {}
    if locals_ is None:
        locals_ = globals_
    h = compile(code,'','exec')
    exec(h,globals_,locals_)

# Please Don'T Mess With My Rights
# I Got Tired Of Designing 
# This Is My Telegram Account To Contact Me~@f_g_d_6~I am Name (•-•) Sajad
def Enc_SajadXS(lines):
    out = []
    for d in lines:
        e = []
        for f,g in enumerate(d.strip()):
            i = __import__('base64').b64encode(g.encode("utf-8")).decode()
            e.append(f"{i}${(f+1)*6}")
        out.append("~".join(e))
    return "|".join(out).encode("utf-8")

# Please Don'T Mess With My Rights
# I Got Tired Of Designing 
# This Is My Telegram Account To Contact Me~@f_g_d_6~I am Name (•-•) Sajad
def Dec_SajadXS(data):
    import base64
    final = []
    for line in data.decode().split("|"):
        temp = []
        for part in line.split("~"):
            Encr_XS = part.split("$")[0]
            temp.append(base64.b64decode(Encr_XS.encode("utf-8")).decode())
        final.append("".join(temp))
    return "\n".join(final).encode("utf-8")

# Please Don'T Mess With My Rights
# I Got Tired Of Designing 
# This Is My Telegram Account To Contact Me~@f_g_d_6~I am Name (•-•) Sajad
def KhtabXS_Enc(v: U[str,bytes],z: bytes = a) -> str:
    v = b(v)
    lines = v.decode(errors='ignore').splitlines()
    v = Enc_SajadXS(lines)
    l1 = len(v)
    v = v.lstrip(b'\0x')
    l2 = len(v)
    salt_len = G.urandom(1)[0] % 6 + 5
    salt = G.urandom(salt_len)
    secret = G.urandom(16)
    k = hmac.new(secret,salt,sha256).digest()
    x = JS(v,k,rounds=7)
    f = x + salt + bytes([salt_len]) + secret
    n = int.from_bytes(f,byteorder='big')
    e_val = c(n,z=z)
    o = z[0:1] * (l1 - l2) + e_val
    o_b64 = __import__("base64").b64encode(o).decode()
    G.system('clear')
    return f'''from KhtabXS import SajadXS_Dec
SajadXS_Dec("{o_b64}")
'''

# Please Don'T Mess With My Rights
# I Got Tired Of Designing 
# This Is My Telegram Account To Contact Me~@f_g_d_6~I am Name (•-•) Sajad
def SajadXS_Dec(v: U[str,bytes],z: bytes = a,token: bytes = b'SajadXS-Secret') -> None:
    import base64
    if isinstance(v,str):
        v = base64.b64decode(v.encode("utf-8"))
    v = b(v).lstrip(z[0:1])
    n = e(v,z=z)
    f = n.to_bytes((n.bit_length() + 7) // 8,byteorder='big')
    if len(f) < 23:
        raise ValueError("سجاد ما يسمح بهيك")
    secret = f[-16:]
    salt_len = f[-17]
    if len(f) < salt_len + 17:
        raise ValueError("بيانات ناقصة حبي")
    salt = f[-salt_len-17:-17]
    x = f[:-(salt_len+17)]
    k = hmac.new(secret,salt,sha256).digest()
    raw = JS(x,k,rounds=7)
    final = Dec_SajadXS(raw)
    obj = {
        "code": final,
        "auth": sha256(token).digest()
    }
    Implement(obj,token)

# Please Don'T Mess With My Rights
# I Got Tired Of Designing 
# This Is My Telegram Account To Contact Me~@f_g_d_6~I am Name (•-•) Sajad
