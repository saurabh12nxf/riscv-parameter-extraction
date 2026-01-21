# Spec Text Citations for All Parameters

**Register:** mstatus  
**Spec Source:** RISC-V Privileged ISA Specification v1.13, Section 3.1.6  
**Total Parameters:** 35  
**Purpose:** Provide verifiable spec citations for each parameter per Allen Baum's evaluation criteria

---

## Methodology

Per Allen Baum (Jan 21, 2026):
> "Each parameter found should be able to point to the spec text that defines it (e.g., the words optionally, may, can, etc.)"

For each parameter, we provide:
1. **Spec Text Citation** - Exact quote from specification
2. **Spec Location** - Section and paragraph number
3. **Indicator Words** - Words that signal this is a parameter ("may", "can", etc.)
4. **Parameter Type** - Named, WARL, Config-Dependent, or Unnamed
5. **UDB Status** - Whether parameter exists in UDB and where

---

## Parameters (Ordered by Bit Position)

### 1. SD (State Dirty) - Bit 31 (RV32) / Bit 63 (RV64)

**Spec Text Citation:** "The SD bit is a read-only bit that summarizes whether either the FS, VS, or XS fields signal the presence of some dirty state that will require saving extended user context to memory. If FS, XS, and VS are all read-only zero, then SD is also always zero. SD=(FS==0b11 OR XS==0b11 OR VS==0b11)"

**Spec Location:** Section 3.1.6, Paragraph 8

**Indicator Words:** "summarizes", "dirty state", "saving extended user context"

**Parameter Type:** Named


**UDB Status:**
- **In UDB:** ✅ YES
- **File:** spec/std/isa/csr/mstatus.yaml
- **Lines:** 26-42
- **Notes:** Fully documented with definedBy extension dependencies


### 2. MSTATUS_RESERVED_47_43 - Bits 47-43 (RV64)

**Spec Text Citation:**
> "Reserved" (labeled in Figure 3.7 - RV64 mstatus register diagram)

**Spec Location:** Section 3.1.6, Figure 3.7  
**Indicator Words:** N/A (visual diagram notation)  
**Parameter Type:** Unnamed (Reserved/WPRI)  
**Config Dependency:** XLEN=64 (RV64 only)

**UDB Status:**
- **In UDB:** ⚠️ IMPLICIT
- **Explicit Field:** ❌ NO
- **Implicit Handling:** ✅ YES (gap between defined fields)
- **Validation:** In mstatus.yaml, no fields defined at bits 47-43, confirming reserved status

**LLM Detection:**
- **Source:** Register diagram analysis (Figure 3.7)
- **Method:** Identified gaps in bit position assignments
- **Reasoning:** Bits labeled "Reserved" in diagram but no corresponding field definition
- **Value:** Explicit enumeration of reserved regions aids specification completeness checking

**Notes:**
- Reserved bits are WPRI (Write Preserve, Read Ignore)
- Software should preserve values on writes
- Reads return unpredictable values
- This is a spec documentation pattern - reserved bits shown in diagrams but not described in prose

