"""
═══════════════════════════════════════════════════════════════════════════════
WAD CONSTITUTIONAL MATHEMATICS — FIXED-POINT 1e18 PRECISION
═══════════════════════════════════════════════════════════════════════════════

WAD  = 1_000_000_000_000_000_000  (1e18 — the unit "one")

All probabilities, strengths, confidences live in [0, WAD].
All arithmetic is integer-only — no float obfuscation.

Constitutional operations:
  wmul(a, b) = (a * b) / WAD          — multiply two WAD values
  wdiv(a, b) = (a * WAD) / b          — divide two WAD values
  wadd(a, b) = a + b                  — addition (no scaling needed)
  wsub(a, b) = a - b                  — subtraction (no scaling needed)

Example: 0.85 confidence  →  850_000_000_000_000_000
         0.70 * 0.85      →  wmul(700e15, 850e15) = 595_000_000_000_000_000
═══════════════════════════════════════════════════════════════════════════════
"""

# ═══════════════════════════════════════════════════════════════════════════════
# WAD CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

WAD: int = 10 ** 18
HALF_WAD: int = WAD // 2

# Common WAD values
WAD_ZERO    = 0
WAD_ONE     = WAD
WAD_HALF    = HALF_WAD
WAD_95PCT   = round(0.95 * WAD)
WAD_90PCT   = round(0.90 * WAD)
WAD_85PCT   = round(0.85 * WAD)
WAD_80PCT   = round(0.80 * WAD)
WAD_75PCT   = round(0.75 * WAD)
WAD_70PCT   = round(0.70 * WAD)
WAD_60PCT   = round(0.60 * WAD)
WAD_50PCT   = round(0.50 * WAD)

# ═══════════════════════════════════════════════════════════════════════════════
# CONVERSION FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def to_wad(x: float) -> int:
    """Convert float to WAD integer representation."""
    return round(x * WAD)

def from_wad(w: int) -> float:
    """Convert WAD integer back to float (for display only)."""
    return w / WAD

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTITUTIONAL ARITHMETIC OPERATIONS
# ═══════════════════════════════════════════════════════════════════════════════

def wmul(a: int, b: int) -> int:
    """WAD multiply: (a * b) / WAD — both a and b are WAD-scaled."""
    return (a * b) // WAD

def wdiv(a: int, b: int) -> int:
    """WAD divide: (a * WAD) / b — result is WAD-scaled."""
    if b == 0:
        raise ZeroDivisionError("wdiv: denominator is zero")
    return (a * WAD) // b

def wadd(a: int, b: int) -> int:
    """WAD addition — no rescaling needed."""
    return a + b

def wsub(a: int, b: int) -> int:
    """WAD subtraction — no rescaling needed."""
    return a - b

def wclamp(w: int, lo: int = 0, hi: int = WAD) -> int:
    """Clamp a WAD value to [lo, hi]."""
    return max(lo, min(hi, w))

def wabs(w: int) -> int:
    """Absolute value of a WAD integer."""
    return abs(w)

# ═══════════════════════════════════════════════════════════════════════════════
# DISPLAY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def wformat(w: int, decimals: int = 4) -> str:
    """Format a WAD integer as a human-readable decimal string."""
    return f"{from_wad(w):.{decimals}f}"

def wpct(w: int) -> str:
    """Format a WAD integer as a percentage string."""
    return f"{from_wad(w):.1%}"

# ═══════════════════════════════════════════════════════════════════════════════
# SELF-VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════

def verify_constitution() -> bool:
    """Self-test to ensure WAD arithmetic is correct."""
    a = to_wad(0.85)
    b = to_wad(0.70)
    
    assert wmul(a, b) == 595_000_000_000_000_000
    assert from_wad(a) == 0.85
    assert wclamp(int(1.5 * WAD)) == WAD
    assert wdiv(a, b) == 1_214_285_714_285_714_285
    
    print("✅ WAD Constitutional Mathematics: VERIFIED")
    print(f"✅ Precision: {WAD:,} (1e18)")
    print("✅ Zero floating-point obfuscation in core")
    return True
