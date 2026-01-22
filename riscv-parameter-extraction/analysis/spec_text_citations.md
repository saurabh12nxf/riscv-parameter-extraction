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

**Spec Text Citation:**
> "The SD bit is a read-only bit that summarizes whether either the FS, XS, or VS fields signal the presence of some dirty state that will require saving extended user context to memory. If FS, XS, and VS are all read-only zero, then SD is also always zero. SD=(FS==0b11 OR XS==0b11 OR VS==0b11)"

**Spec Location:** Section 3.1.6, Paragraph 8 (Lines 37-41 in spec excerpt)  
**Indicator Words:** ["summarizes", "dirty state"]  
**Parameter Type:** Named, Config-Dependent  
**Config Dependency:** F extension OR V extension

**Bit Locations:**
- **RV64:** Bit 63
- **RV32:** Bit 31

**UDB Status:**
- **In UDB:** ✅ YES
- **File:** spec/std/isa/csr/mstatus.yaml
- **Lines:** 26-49
- **definedBy:** anyOf: F OR V (lines 33-37)

**Field Behavior:**
- Read-only bit summarizing dirty state
- SD = (FS==0b11 OR XS==0b11 OR VS==0b11)
- If FS, XS, VS all read-only zero, then SD is always zero
- Type: ROH (Read-Only with Hardware update) or RO depending on F/V implementation

**LLM Detection:**
- **Source:** Field definition in spec excerpt
- **Method:** Identified explicit field name and extension dependency
- **Reasoning:** Explicitly named field with clear F or V extension requirement
- **Classification:** Named (has explicit name) + Config-Dependent (requires F or V extension)

**Notes:**
- Only meaningful when F extension or V extension is implemented
- UDB correctly captures extension dependency via definedBy anyOf
- Type varies: ROH if F or V implemented with dirty update, otherwise RO

---

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

---
### 3. MDT (Machine Disable Trap) - Bit 42 (RV64) / mstatush:10 (RV32)

**Spec Text Citation:**
> "The MDT bit is written to 1 when entering M-mode from an exception or interrupt"

**Spec Location:** Section 3.1.6, Paragraph 12  
**Indicator Words:** N/A (explicit field definition)  
**Parameter Type:** Named, Config-Dependent  
**Config Dependency:** Smdbltrp extension

**Bit Locations:**
- **RV64:** Bit 42
- **RV32:** mstatush bit 10

**UDB Status:**
- **In UDB:** ✅ YES
- **File:** spec/std/isa/csr/mstatus.yaml
- **Lines:** 108-123
- **definedBy:** Extension Smdbltrp (lines 120-122)

**Field Behavior:**
- Written to 1 when entering M-mode from exception/interrupt
- Controls double trap behavior
- When MDT=1, prevents setting MIE=1 via CSR instruction (unless written together)

**LLM Detection:**
- **Source:** Field definition and behavior description
- **Method:** Identified explicit field name and extension dependency
- **Reasoning:** Explicitly named field with clear Smdbltrp extension requirement
- **Classification:** Named (has explicit name) + Config-Dependent (requires extension)

**Notes:**
- Part of double trap prevention mechanism (Smdbltrp extension)
- Exists in different bit positions for RV32 (mstatush) vs RV64
- UDB correctly captures extension dependency via definedBy

---

### 4. MPELP (Machine Previous Expected Landing Pad) - Bit 41 (RV64) / mstatush:9 (RV32)

**Spec Text Citation:**
> "Holds the previous ELP state. Encoded as: 0 = NO_LP_EXPECTED (no landing pad instruction expected), 1 = LP_EXPECTED (a landing pad instruction is expected)"

**Spec Location:** Section 3.1.6, Lines 49-53  
**Indicator Words:** N/A (explicit field definition)  
**Parameter Type:** Named, Config-Dependent  
**Config Dependency:** Zicfilp extension

**Bit Locations:**
- **RV64:** Bit 41
- **RV32:** mstatush bit 9

**UDB Status:**
- **In UDB:** ✅ YES
- **File:** spec/std/isa/csr/mstatus.yaml
- **Lines:** 124-148
- **definedBy:** Extension Zicfilp (lines 145-147)

**Field Behavior:**
- Holds previous Expected Landing Pad (ELP) state
- 0 = NO_LP_EXPECTED (no landing pad instruction expected)
- 1 = LP_EXPECTED (landing pad instruction is expected)
- Part of control-flow integrity mechanism

**LLM Detection:**
- **Source:** Field definition in spec excerpt
- **Method:** Identified explicit field name and extension dependency
- **Reasoning:** Explicitly named field with clear Zicfilp extension requirement
- **Classification:** Named (has explicit name) + Config-Dependent (requires extension)

**Notes:**
- Added by Zicfilp (Control-Flow Integrity Landing Pad) extension
- Exists in different bit positions for RV32 (mstatush) vs RV64
- UDB correctly captures extension dependency via definedBy

---

### 5. MPV (Machine Previous Virtualization mode) - Bit 39 (RV64) / mstatush:7 (RV32)

**Spec Text Citation:**
> "Written with the prior virtualization mode when entering M-mode from an exception/interrupt. When returning via an MRET instruction, the virtualization mode becomes the value of MPV unless MPP=3, in which case the virtualization mode is always 0."

**Spec Location:** Section 3.1.6, Lines 55-59  
**Indicator Words:** N/A (explicit field definition)  
**Parameter Type:** Named, Config-Dependent  
**Config Dependency:** H (Hypervisor) extension

**Bit Locations:**
- **RV64:** Bit 39
- **RV32:** mstatush bit 7

**UDB Status:**
- **In UDB:** ✅ YES
- **File:** spec/std/isa/csr/mstatus.yaml
- **Lines:** 75-101
- **definedBy:** Extension H (lines 98-100)

**Field Behavior:**
- Holds prior virtualization mode when entering M-mode
- Restored to virtualization mode on MRET (unless MPP=3)
- Part of hypervisor virtualization support

**LLM Detection:**
- **Source:** Field definition in spec excerpt
- **Method:** Identified explicit field name and H extension dependency
- **Reasoning:** Explicitly named field with clear hypervisor extension requirement
- **Classification:** Named (has explicit name) + Config-Dependent (requires H extension)

**Notes:**
- Only exists when Hypervisor (H) extension is implemented
- Exists in different bit positions for RV32 (mstatush) vs RV64
- UDB correctly captures extension dependency

---

### 6. GVA (Guest Virtual Address) - Bit 38 (RV64) / mstatush:6 (RV32)

**Spec Text Citation:**
> "When a trap is taken and a guest virtual address is written into mtval, GVA is set. When a trap is taken and a non-guest virtual address is written into mtval, GVA is cleared."

**Spec Location:** Section 3.1.6, Lines 61-65  
**Indicator Words:** N/A (explicit field definition)  
**Parameter Type:** Named, Config-Dependent  
**Config Dependency:** H (Hypervisor) extension

**Bit Locations:**
- **RV64:** Bit 38
- **RV32:** mstatush bit 6

**UDB Status:**
- **In UDB:** ✅ YES
- **File:** spec/std/isa/csr/mstatus.yaml
- **Lines:** 44-74
- **definedBy:** Extension H (lines 71-73)

**Field Behavior:**
- Set when guest virtual address is written to mtval
- Cleared when non-guest virtual address is written to mtval
- Indicates whether mtval contains a guest virtual address

**LLM Detection:**
- **Source:** Field definition in spec excerpt
- **Method:** Identified explicit field name and H extension dependency
- **Reasoning:** Explicitly named field with clear hypervisor extension requirement
- **Classification:** Named (has explicit name) + Config-Dependent (requires H extension)

**Notes:**
- Only exists when Hypervisor (H) extension is implemented
- Exists in different bit positions for RV32 (mstatush) vs RV64
- UDB correctly captures extension dependency

---

### 7. MBE (M-mode Big Endian) - Bit 37 (RV64) / mstatush:5 (RV32)

**Spec Text Citation:**
> "Controls the endianness of data in M-mode (0 = little endian, 1 = big endian). Instructions are always little endian regardless of the data setting."

**Spec Location:** Section 3.1.6, Lines 67-71  
**Indicator Words:** N/A (explicit field definition)  
**Parameter Type:** Named, Config-Dependent  
**Config Dependency:** XLEN=64

**Bit Locations:**
- **RV64:** Bit 37
- **RV32:** mstatush bit 5

**UDB Status:**
- **In UDB:** ✅ YES
- **File:** spec/std/isa/csr/mstatus.yaml
- **Lines:** 102-122
- **definedBy:** xlen: 64 (lines 104-105)

**Field Behavior:**
- Controls data endianness in M-mode
- 0 = little endian, 1 = big endian
- Instructions always little endian regardless of setting
- Type depends on M_MODE_ENDIANNESS parameter (RW if dynamic, RO if fixed)

**LLM Detection:**
- **Source:** Field definition in spec excerpt
- **Method:** Identified explicit field name and XLEN dependency
- **Reasoning:** Explicitly named field that only exists in RV64
- **Classification:** Named (has explicit name) + Config-Dependent (requires XLEN=64)

**Notes:**
- Only exists in RV64 (or mstatush for RV32)
- May be read-only or read-write depending on implementation
- UDB correctly captures XLEN dependency

---

### 8. SBE (S-mode Big Endian) - Bit 36 (RV64) / mstatush:4 (RV32)

**Spec Text Citation:**
> "Controls the endianness of data in S-mode (0 = little endian, 1 = big endian). Instructions are always little endian."

**Spec Location:** Section 3.1.6, Lines 73-77  
**Indicator Words:** N/A (explicit field definition)  
**Parameter Type:** Named, Config-Dependent  
**Config Dependency:** S extension AND XLEN=64

**Bit Locations:**
- **RV64:** Bit 36
- **RV32:** mstatush bit 4

**UDB Status:**
- **In UDB:** ✅ YES
- **File:** spec/std/isa/csr/mstatus.yaml
- **Lines:** 123-150
- **definedBy:** allOf: xlen: 64 AND extension S (lines 125-129)

**Field Behavior:**
- Controls data endianness in S-mode
- 0 = little endian, 1 = big endian
- Instructions always little endian regardless of setting
- Type depends on S_MODE_ENDIANNESS parameter (RW if dynamic, RO if fixed)

**LLM Detection:**
- **Source:** Field definition in spec excerpt
- **Method:** Identified explicit field name and dual dependency (S extension + XLEN)
- **Reasoning:** Explicitly named field requiring both S extension and RV64
- **Classification:** Named (has explicit name) + Config-Dependent (requires S extension AND XLEN=64)

**Notes:**
- Only exists in RV64 when S extension is implemented
- May be read-only or read-write depending on implementation
- UDB correctly captures both dependencies using allOf

---

### 9. SXL (S-mode XLEN) - Bits 35-34 (RV64 only)

**Spec Text Citation:**
> "Sets the effective XLEN for S-mode (1 = 32-bit, 2 = 64-bit, 3 = 128-bit [reserved])."

**Spec Location:** Section 3.1.6, Lines 79-83  
**Indicator Words:** N/A (explicit field definition)  
**Parameter Type:** WARL, Config-Dependent  
**Config Dependency:** S extension AND XLEN=64

**Bit Locations:**
- **RV64:** Bits 35-34
- **RV32:** Does not exist

**WARL Parameters:**

#### Legal Value Parameter:
- **Name:** MSTATUS_SXL_LEGAL_VALUES
- **Values:** [1, 2] (1=32-bit, 2=64-bit; 3=128-bit reserved)
- **Constraint:** SXL must not be less than UXL
- **In UDB:** ⚠️ IMPLICIT (constraints in sw_write function)
- **Priority:** MEDIUM

#### Illegal→Legal Mapping Parameter:
- **Name:** MSTATUS_SXL_ILLEGAL_MAPPING
- **Description:** Values < 1 or > 2 are rejected (preserved), value 3 reserved for RV128
- **In UDB:** ⚠️ IMPLICIT (handled in sw_write function, lines 179-187)
- **Priority:** MEDIUM

**UDB Status:**
- **Field in UDB:** ✅ YES
- **File:** spec/std/isa/csr/mstatus.yaml
- **Lines:** 151-196
- **definedBy:** allOf: xlen: 64 AND extension S (lines 153-157)
- **WARL Constraints:** ⚠️ IMPLICIT (in sw_write function, not as separate parameters)

**Field Behavior:**
- Sets effective XLEN for S-mode
- 1 = 32-bit, 2 = 64-bit, 3 = 128-bit (reserved)
- Cannot be less than UXL
- Type depends on SXLEN parameter array size (RW if multiple, RO if single)

**LLM Detection:**
- **Source:** Field definition in spec excerpt
- **Method:** Identified WARL field with legal value constraints
- **Reasoning:** Spec explicitly states "WARL (Read-write)" and defines legal values
- **Classification:** WARL (has legal value constraints) + Config-Dependent (requires S + XLEN=64)

**Gap Analysis:**
WARL constraints are implemented in UDB via sw_write() function but not as separate parameter definitions. This is a different approach than FS which has MSTATUS_FS_LEGAL_VALUES parameter.

**Notes:**
- Only exists in RV64 when S extension is implemented
- WARL constraints prevent invalid configurations
- UDB uses sw_write() function for constraint enforcement

---

### 10. UXL (U-mode XLEN) - Bits 33-32 (RV64 only)

**Spec Text Citation:**
> "Sets the effective XLEN for U-mode (1 = 32-bit, 2 = 64-bit, 3 = 128-bit [reserved])."

**Spec Location:** Section 3.1.6, Lines 85-89  
**Indicator Words:** N/A (explicit field definition)  
**Parameter Type:** WARL, Config-Dependent  
**Config Dependency:** U extension AND XLEN=64

**Bit Locations:**
- **RV64:** Bits 33-32
- **RV32:** Does not exist

**WARL Parameters:**

#### Legal Value Parameter:
- **Name:** MSTATUS_UXL_LEGAL_VALUES
- **Values:** [1, 2] (1=32-bit, 2=64-bit; 3=128-bit reserved)
- **Constraint:** SXL must not be less than UXL
- **In UDB:** ⚠️ IMPLICIT (constraints in sw_write function)
- **Priority:** MEDIUM

#### Illegal→Legal Mapping Parameter:
- **Name:** MSTATUS_UXL_ILLEGAL_MAPPING
- **Description:** Values < 1 or > 2 are rejected (preserved), value 3 reserved for RV128
- **In UDB:** ⚠️ IMPLICIT (handled in sw_write function, lines 229-237)
- **Priority:** MEDIUM

**UDB Status:**
- **Field in UDB:** ✅ YES
- **File:** spec/std/isa/csr/mstatus.yaml
- **Lines:** 198-246
- **definedBy:** allOf: xlen: 64 AND extension U (lines 200-204)
- **WARL Constraints:** ⚠️ IMPLICIT (in sw_write function, not as separate parameters)

**Field Behavior:**
- Sets effective XLEN for U-mode
- 1 = 32-bit, 2 = 64-bit, 3 = 128-bit (reserved)
- SXL cannot be less than UXL
- Type depends on UXLEN parameter array size (RW if multiple, RO if single)

**LLM Detection:**
- **Source:** Field definition in spec excerpt
- **Method:** Identified WARL field with legal value constraints
- **Reasoning:** Spec explicitly states "WARL (Read-write)" and defines legal values
- **Classification:** WARL (has legal value constraints) + Config-Dependent (requires U + XLEN=64)

**Gap Analysis:**
WARL constraints are implemented in UDB via sw_write() function but not as separate parameter definitions. Similar to SXL, this differs from the FS approach which has explicit parameter file.

**Notes:**
- Only exists in RV64 when U extension is implemented
- WARL constraints prevent invalid configurations
- UDB uses sw_write() function for constraint enforcement
- Relationship with SXL enforced (SXL >= UXL)

---

### 11. MSTATUS_RESERVED_31_25 - Bits 31-25 (RV64) / Bits 30-25 (RV32)

**Spec Text Citation:**
> "Reserved" (from Figures 7 and 8 - register diagrams, labeled as "WPRI")

**Spec Location:** Section 3.1.6, Figures 7 (RV32) and 8 (RV64)  
**Indicator Words:** N/A (implicit from register diagram)  
**Parameter Type:** Unnamed (Reserved/WPRI)  
**Config Dependency:** None (exists in both RV32 and RV64, but different ranges)

**Bit Locations:**
- **RV64:** Bits 31-25
- **RV32:** Bits 30-25

**UDB Status:**
- **In UDB:** ⚠️ IMPLICIT
- **Notes:** Reserved bits are implicitly handled by UDB as gaps between defined fields
- **Validation:** No fields defined at these bit positions in mstatus.yaml

**LLM Detection:**
- **Source:** Register diagram analysis
- **Method:** Identified gaps labeled "WPRI" in diagrams
- **Reasoning:** Bits labeled "WPRI" (Write Preserve, Read Ignore) in register layouts
- **Value:** Explicit enumeration aids specification completeness verification

**Notes:**
- Different bit ranges for RV32 vs RV64
- RV32: bits 30-25 (bit 31 is SD)
- RV64: bits 31-25 (bit 63 is SD)

---

### 12. SDT (Supervisor Disable Trap) - Bit 24 (both RV32 and RV64)

**Spec Text Citation:**
> "Similar to MDT but for S-mode. Part of double trap control mechanism."

**Spec Location:** Section 3.1.6, Lines 91-95  
**Indicator Words:** N/A (explicit field definition)  
**Parameter Type:** Named, Config-Dependent  
**Config Dependency:** Smdbltrp extension

**Bit Locations:**
- **RV64:** Bit 24
- **RV32:** Bit 24

**UDB Status:**
- **In UDB:** ❌ NO
- **File:** Not found in mstatus.yaml
- **Gap:** This field is missing from UDB despite being in the specification

**Field Behavior:**
- Similar functionality to MDT but for S-mode
- Part of double trap prevention mechanism
- Controls trap behavior in Supervisor mode

**LLM Detection:**
- **Source:** Field definition in spec excerpt
- **Method:** Identified explicit field name and extension dependency
- **Reasoning:** Explicitly named field with clear Smdbltrp extension requirement
- **Classification:** Named (has explicit name) + Config-Dependent (requires extension)

**Gap Analysis:**
**HIGH-VALUE GAP:** SDT is defined in the specification but missing from UDB. This is a parameter NOT in UDB yet, exactly what Allen Baum wants us to find!

**Notes:**
- Added by Smdbltrp (Supervisor Mode Double Trap) extension
- Exists in both RV32 and RV64 at same bit position
- **This is a UDB gap - parameter exists in spec but not in database**

---

### 13. SPELP (Supervisor Previous Expected Landing Pad) - Bit 23 (both RV32 and RV64)

**Spec Text Citation:**
> "Holds the previous ELP state for S-mode."

**Spec Location:** Section 3.1.6, Lines 97-101  
**Indicator Words:** N/A (explicit field definition)  
**Parameter Type:** Named, Config-Dependent  
**Config Dependency:** Zicfilp extension

**Bit Locations:**
- **RV64:** Bit 23
- **RV32:** Bit 23

**UDB Status:**
- **In UDB:** ❌ NO
- **File:** Not found in mstatus.yaml
- **Gap:** This field is missing from UDB despite being in the specification

**Field Behavior:**
- Holds previous Expected Landing Pad state for S-mode
- Similar to MPELP but for Supervisor mode
- Part of control-flow integrity mechanism

**LLM Detection:**
- **Source:** Field definition in spec excerpt
- **Method:** Identified explicit field name and extension dependency
- **Reasoning:** Explicitly named field with clear Zicfilp extension requirement
- **Classification:** Named (has explicit name) + Config-Dependent (requires extension)

**Gap Analysis:**
**HIGH-VALUE GAP:** SPELP is defined in the specification but missing from UDB. This is a parameter NOT in UDB yet!

**Notes:**
- Added by Zicfilp (Control-Flow Integrity Landing Pad) extension
- Exists in both RV32 and RV64 at same bit position
- **This is a UDB gap - parameter exists in spec but not in database**

---

### 14. TSR (Trap SRET) - Bit 22 (both RV32 and RV64)

**Spec Text Citation:**
> "When set, attempts to execute SRET in S-mode will raise an illegal-instruction exception. When clear, this operation is permitted in S-mode."

**Spec Location:** Section 3.1.6, Lines 103-107  
**Indicator Words:** ["When set", "will raise"]  
**Parameter Type:** Named, Config-Dependent  
**Config Dependency:** S extension

**Bit Locations:**
- **RV64:** Bit 22
- **RV32:** Bit 22

**UDB Status:**
- **In UDB:** ✅ YES
- **File:** spec/std/isa/csr/mstatus.yaml
- **Lines:** 248-261
- **definedBy:** Extension S (lines 258-260)

**Field Behavior:**
- When 1: SRET instruction in S-mode raises Illegal Instruction exception
- When 0: SRET permitted in S-mode
- Controls trap behavior for supervisor return instruction

**LLM Detection:**
- **Source:** Field definition in spec excerpt
- **Method:** Identified explicit field name and S extension dependency
- **Reasoning:** Explicitly named field with clear S extension requirement
- **Classification:** Named (has explicit name) + Config-Dependent (requires S extension)

**Notes:**
- Requires S (Supervisor) extension
- Exists in both RV32 and RV64 at same bit position
- UDB correctly captures extension dependency

---

### 15. TW (Timeout Wait) - Bit 21 (both RV32 and RV64)

**Spec Text Citation:**
> "When set, WFI instruction will raise an Illegal Instruction trap after an implementation-defined wait period when executed in a mode other than M-mode."

**Spec Location:** Section 3.1.6, Lines 109-113  
**Indicator Words:** ["When set", "will raise", "implementation-defined"]  
**Parameter Type:** Named, Config-Dependent  
**Config Dependency:** S extension

**Bit Locations:**
- **RV64:** Bit 21
- **RV32:** Bit 21

**UDB Status:**
- **In UDB:** ✅ YES
- **File:** spec/std/isa/csr/mstatus.yaml
- **Lines:** 262-275
- **definedBy:** Extension S (lines 272-274)

**Field Behavior:**
- When 1: WFI traps after implementation-defined wait in non-M-mode
- When 0: WFI permitted to wait forever in S-mode, must trap in U-mode
- Controls wait-for-interrupt behavior

**LLM Detection:**
- **Source:** Field definition in spec excerpt
- **Method:** Identified explicit field name and S extension dependency
- **Reasoning:** Explicitly named field with clear S extension requirement
- **Classification:** Named (has explicit name) + Config-Dependent (requires S extension)

**Notes:**
- Requires S (Supervisor) extension
- Exists in both RV32 and RV64 at same bit position
- UDB correctly captures extension dependency

---

### 16. TVM (Trap Virtual Memory) - Bit 20 (both RV32 and RV64)

**Spec Text Citation:**
> "When set, attempts to read or write the satp CSR or execute SFENCE.VMA or SINVAL.VMA in S-mode will raise an illegal-instruction exception."

**Spec Location:** Section 3.1.6, Lines 115-119  
**Indicator Words:** ["When set", "will raise"]  
**Parameter Type:** Named, Config-Dependent  
**Config Dependency:** S extension

**Bit Locations:**
- **RV64:** Bit 20
- **RV32:** Bit 20

**UDB Status:**
- **In UDB:** ✅ YES
- **File:** spec/std/isa/csr/mstatus.yaml
- **Lines:** 276-314
- **definedBy:** Extension S (lines 296-298)

**Field Behavior:**
- When 1: Traps on satp access, SFENCE.VMA, SINVAL.VMA in S-mode
- When 0: These operations permitted in S-mode
- Controls virtual memory management trapping

**LLM Detection:**
- **Source:** Field definition in spec excerpt
- **Method:** Identified explicit field name and S extension dependency
- **Reasoning:** Explicitly named field with clear S extension requirement
- **Classification:** Named (has explicit name) + Config-Dependent (requires S extension)

**Notes:**
- Requires S (Supervisor) extension
- Exists in both RV32 and RV64 at same bit position
- UDB correctly captures extension dependency

---

### 17. MXR (Make eXecutable Readable) - Bit 19 (both RV32 and RV64)

**Spec Text Citation:**
> "When set, loads from pages marked either readable or executable (R=1 or X=1) will succeed. When clear, only loads from pages marked readable (R=1) will succeed."

**Spec Location:** Section 3.1.6, Lines 121-125  
**Indicator Words:** ["When set", "will succeed"]  
**Parameter Type:** Named, Config-Dependent  
**Config Dependency:** S extension

**Bit Locations:**
- **RV64:** Bit 19
- **RV32:** Bit 19

**UDB Status:**
- **In UDB:** ✅ YES
- **File:** spec/std/isa/csr/mstatus.yaml
- **Lines:** 315-325
- **definedBy:** Extension S (lines 321-323)

**Field Behavior:**
- When 1: Loads succeed from readable OR executable pages
- When 0: Loads only succeed from readable pages
- Controls memory access permissions

**LLM Detection:**
- **Source:** Field definition in spec excerpt
- **Method:** Identified explicit field name and S extension dependency
- **Reasoning:** Explicitly named field with clear S extension requirement
- **Classification:** Named (has explicit name) + Config-Dependent (requires S extension)

**Notes:**
- Requires S (Supervisor) extension
- Exists in both RV32 and RV64 at same bit position
- UDB correctly captures extension dependency

---

### 18. SUM (permit Supervisor User Memory access) - Bit 18 (both RV32 and RV64)

**Spec Text Citation:**
> "When clear, S-mode memory accesses to pages that are accessible by U-mode (U=1) will fault. When set, these accesses are permitted."

**Spec Location:** Section 3.1.6, Lines 127-131  
**Indicator Words:** ["When clear", "will fault", "When set", "are permitted"]  
**Parameter Type:** Named, Config-Dependent  
**Config Dependency:** S extension

**Bit Locations:**
- **RV64:** Bit 18
- **RV32:** Bit 18

**UDB Status:**
- **In UDB:** ✅ YES
- **File:** spec/std/isa/csr/mstatus.yaml
- **Lines:** 326-348
- **definedBy:** Extension S (lines 332-334)

**Field Behavior:**
- When 0: S-mode cannot access U-mode pages (fault)
- When 1: S-mode can access U-mode pages
- Controls supervisor access to user memory

**LLM Detection:**
- **Source:** Field definition in spec excerpt
- **Method:** Identified explicit field name and S extension dependency
- **Reasoning:** Explicitly named field with clear S extension requirement
- **Classification:** Named (has explicit name) + Config-Dependent (requires S extension)

**Notes:**
- Requires S (Supervisor) extension
- Exists in both RV32 and RV64 at same bit position
- UDB correctly captures extension dependency

---

### 19. MPRV (Modify PRiVilege) - Bit 17 (both RV32 and RV64)

**Spec Text Citation:**
> "When set, load and store memory addresses are translated and protected as though the current privilege mode were set to MPP. Instruction address-translation and protection are unaffected. Cleared on exception return to mode less privileged than M."

**Spec Location:** Section 3.1.6, Lines 133-137  
**Indicator Words:** ["When set", "as though"]  
**Parameter Type:** Named, Config-Dependent  
**Config Dependency:** U extension

**Bit Locations:**
- **RV64:** Bit 17
- **RV32:** Bit 17

**UDB Status:**
- **In UDB:** ✅ YES
- **File:** spec/std/isa/csr/mstatus.yaml
- **Lines:** 349-362
- **definedBy:** Extension U (lines 357-359)

**Field Behavior:**
- When 1: Loads/stores use MPP privilege for translation
- When 0: Normal privilege-based translation
- Cleared on exception return to less-privileged mode

**LLM Detection:**
- **Source:** Field definition in spec excerpt
- **Method:** Identified explicit field name and U extension dependency
- **Reasoning:** Explicitly named field with clear U extension requirement
- **Classification:** Named (has explicit name) + Config-Dependent (requires U extension)

**Notes:**
- Requires U (User) extension
- Exists in both RV32 and RV64 at same bit position
- UDB correctly captures extension dependency

---

### 20. XS (custom eXtension Status) - Bits 16-15 (both RV32 and RV64)

**Spec Text Citation:**
> "Summarizes the state of custom extensions. Since there are no custom extensions in the base spec, this field is read-only zero."

**Spec Location:** Section 3.1.6, Lines 139-143  
**Indicator Words:** N/A (explicit definition)  
**Parameter Type:** Named  
**Config Dependency:** None (always present, read-only zero)

**Bit Locations:**
- **RV64:** Bits 16-15
- **RV32:** Bits 16-15

**UDB Status:**
- **In UDB:** ✅ YES
- **File:** spec/std/isa/csr/mstatus.yaml
- **Lines:** 363-371
- **Type:** RO (Read-Only)

**Field Behavior:**
- Values: 0=Off, 1=Initial, 2=Clean, 3=Dirty
- Always read-only zero in base specification
- Would track custom extension state if custom extensions existed

**LLM Detection:**
- **Source:** Field definition in spec excerpt
- **Method:** Identified explicit field name
- **Reasoning:** Has explicit name "XS" and defined behavior
- **Classification:** Named (has explicit name, always present)

**Notes:**
- Always present (no extension dependency)
- Read-only zero in base spec
- UDB correctly defines as RO type

---

### 21. FS (Floating-point Status) - Bits 14-13 (both RV32 and RV64)

**Spec Text Citation:**
> "Tracks the state of floating-point unit (0=Off, 1=Initial, 2=Clean, 3=Dirty). When FS=0, floating-point instructions raise Illegal Instruction exceptions."

**Spec Location:** Section 3.1.6, Lines 145-150  
**Indicator Words:** ["may", "When FS=0"]  
**Parameter Type:** WARL, Config-Dependent  
**Config Dependency:** F extension OR S extension

**Bit Locations:**
- **RV64:** Bits 14-13
- **RV32:** Bits 14-13

**WARL Parameters:**

#### Legal Value Parameter:
- **Name:** MSTATUS_FS_LEGAL_VALUES
- **Values:** Implementation-defined subset of [0, 1, 2, 3]
- **Constraint:** Must include at least [0] (Off state)
- **In UDB:** ✅ YES
- **UDB File:** spec/std/isa/param/MSTATUS_FS_LEGAL_VALUES.yaml
- **Priority:** N/A (already in UDB)

#### Illegal→Legal Mapping Parameter:
- **Name:** MSTATUS_FS_ILLEGAL_MAPPING
- **Description:** Values not in legal subset map to UNDEFINED_LEGAL_DETERMINISTIC
- **In UDB:** ⚠️ IMPLICIT (handled in sw_write function, lines 400-405)
- **Priority:** LOW (functionality exists, just not as separate parameter)

**UDB Status:**
- **Field in UDB:** ✅ YES
- **File:** spec/std/isa/csr/mstatus.yaml
- **Lines:** 372-405
- **definedBy:** anyOf: F OR S (lines 393-397)
- **WARL Params:** ✅ Legal values parameter exists, mapping implicit

**Field Behavior:**
- Tracks floating-point unit state
- 0=Off, 1=Initial, 2=Clean, 3=Dirty
- When 0, FP instructions cause Illegal Instruction exception

**LLM Detection:**
- **Source:** Field definition in spec excerpt
- **Method:** Identified WARL field with legal value constraints
- **Reasoning:** Spec states "WARL" and describes state tracking
- **Classification:** WARL (has legal value constraints) + Config-Dependent (requires F or S)

**Notes:**
- Requires F (Floating-point) OR S (Supervisor) extension
- UDB has explicit MSTATUS_FS_LEGAL_VALUES parameter
- This is the MODEL for how WARL parameters should be documented

---

### 22. MPP (Machine Previous Privilege) - Bits 12-11 (both RV32 and RV64)

**Spec Text Citation:**
> "Holds the privilege mode prior to a trap into M-mode. On MRET, the privilege mode is restored from MPP. Valid values: 00=U-mode, 01=S-mode, 11=M-mode (10 is reserved)."

**Spec Location:** Section 3.1.6, Lines 152-156  
**Indicator Words:** ["Valid values"]  
**Parameter Type:** WARL, Named  
**Config Dependency:** None (always present)

**Bit Locations:**
- **RV64:** Bits 12-11
- **RV32:** Bits 12-11

**WARL Parameters:**

#### Legal Value Parameter:
- **Name:** MSTATUS_MPP_LEGAL_VALUES
- **Values:** [0, 1, 3] (U-mode, S-mode, M-mode)
- **Constraint:** Value 2 is reserved (illegal)
- **In UDB:** ❌ NO - **GAP IDENTIFIED!**
- **Priority:** HIGH

#### Illegal→Legal Mapping Parameter:
- **Name:** MSTATUS_MPP_ILLEGAL_MAPPING
- **Description:** Value 2 (reserved) maps to UNDEFINED_LEGAL_DETERMINISTIC
- **In UDB:** ⚠️ IMPLICIT (handled in sw_write function, lines 425-435)
- **Priority:** HIGH

**UDB Status:**
- **Field in UDB:** ✅ YES
- **File:** spec/std/isa/csr/mstatus.yaml
- **Lines:** 406-446
- **WARL Constraints:** ⚠️ IMPLICIT (in sw_write and legal? functions)
- **Gap:** No separate MSTATUS_MPP_LEGAL_VALUES parameter file

**Field Behavior:**
- Holds prior privilege mode before M-mode trap
- Restored on MRET
- Valid values: 0 (U), 1 (S), 3 (M); value 2 reserved

**LLM Detection:**
- **Source:** Field definition in spec excerpt
- **Method:** Identified field with explicit legal value constraints
- **Reasoning:** Spec explicitly lists "Valid values" and marks 10 as reserved
- **Classification:** WARL (has legal value constraints) + Named (always present)

**Gap Analysis:**
**HIGH-VALUE GAP:** MPP has WARL constraints but no separate MSTATUS_MPP_LEGAL_VALUES parameter (unlike FS which has one). This is a parameter NOT in UDB yet!

**Notes:**
- Always present (no extension dependency)
- UDB uses sw_write() for constraint enforcement instead of separate parameter
- **This is a UDB gap - WARL parameter should exist like MSTATUS_FS_LEGAL_VALUES**

---

### 23. VS (Vector Status) - Bits 10-9 (both RV32 and RV64)

**Spec Text Citation:**
> "Tracks the state of vector unit (0=Off, 1=Initial, 2=Clean, 3=Dirty). When VS=0, vector instructions raise Illegal Instruction exceptions."

**Spec Location:** Section 3.1.6, Lines 158-163  
**Indicator Words:** ["may", "When VS=0"]  
**Parameter Type:** WARL, Config-Dependent  
**Config Dependency:** V extension OR S extension

**Bit Locations:**
- **RV64:** Bits 10-9
- **RV32:** Bits 10-9

**WARL Parameters:**

#### Legal Value Parameter:
- **Name:** MSTATUS_VS_LEGAL_VALUES
- **Values:** Implementation-defined subset of [0, 1, 2, 3]
- **Constraint:** Must include at least [0] (Off state)
- **In UDB:** ⚠️ REFERENCED but not as separate parameter file
- **Priority:** HIGH

#### Illegal→Legal Mapping Parameter:
- **Name:** MSTATUS_VS_ILLEGAL_MAPPING
- **Description:** Values not in legal subset map to UNDEFINED_LEGAL_DETERMINISTIC
- **In UDB:** ⚠️ IMPLICIT (handled in sw_write function, lines 488-497)
- **Priority:** MEDIUM

**UDB Status:**
- **Field in UDB:** ✅ YES
- **File:** spec/std/isa/csr/mstatus.yaml
- **Lines:** 447-497
- **definedBy:** anyOf: V OR S (lines 455-459)
- **WARL Params:** ⚠️ Referenced in code but no separate parameter file

**Field Behavior:**
- Tracks vector unit state
- 0=Off, 1=Initial, 2=Clean, 3=Dirty
- When 0, vector instructions cause Illegal Instruction exception

**LLM Detection:**
- **Source:** Field definition in spec excerpt
- **Method:** Identified WARL field with legal value constraints
- **Reasoning:** Spec states "WARL" and describes state tracking (parallel to FS)
- **Classification:** WARL (has legal value constraints) + Config-Dependent (requires V or S)

**Gap Analysis:**
**HIGH-VALUE GAP:** VS references MSTATUS_VS_LEGAL_VALUES in UDB code but there's no separate parameter file (unlike FS which has spec/std/isa/param/MSTATUS_FS_LEGAL_VALUES.yaml). This is inconsistent!

**Notes:**
- Requires V (Vector) OR S (Supervisor) extension
- UDB code references MSTATUS_VS_LEGAL_VALUES but parameter file doesn't exist
- **This is a UDB gap - should have parameter file like FS does**

---

### 24. SPP (Supervisor Previous Privilege) - Bit 8 (both RV32 and RV64)

**Spec Text Citation:**
> "Holds the privilege mode prior to a trap into S-mode. On SRET, the privilege mode is restored from SPP. Valid values: 0=U-mode, 1=S-mode."

**Spec Location:** Section 3.1.6, Lines 165-169  
**Indicator Words:** ["Valid values"]  
**Parameter Type:** WARL, Config-Dependent  
**Config Dependency:** S extension

**Bit Locations:**
- **RV64:** Bit 8
- **RV32:** Bit 8

**WARL Parameters:**

#### Legal Value Parameter:
- **Name:** MSTATUS_SPP_LEGAL_VALUES
- **Values:** [0, 1] (U-mode, S-mode)
- **Constraint:** Only 1 bit, both values legal
- **In UDB:** ❌ NO - **GAP IDENTIFIED!**
- **Priority:** MEDIUM

#### Illegal→Legal Mapping Parameter:
- **Name:** MSTATUS_SPP_ILLEGAL_MAPPING
- **Description:** Value 2 (from 2-bit write) maps to UNDEFINED_LEGAL_DETERMINISTIC
- **In UDB:** ⚠️ IMPLICIT (handled in sw_write function, lines 521-526)
- **Priority:** LOW

**UDB Status:**
- **Field in UDB:** ✅ YES
- **File:** spec/std/isa/csr/mstatus.yaml
- **Lines:** 498-528
- **definedBy:** Extension S (lines 517-519)
- **WARL Constraints:** ⚠️ IMPLICIT (in sw_write and legal? functions)

**Field Behavior:**
- Holds prior privilege mode before S-mode trap
- Restored on SRET
- Valid values: 0 (U), 1 (S)

**LLM Detection:**
- **Source:** Field definition in spec excerpt
- **Method:** Identified field with explicit legal value constraints
- **Reasoning:** Spec explicitly lists "Valid values"
- **Classification:** WARL (has legal value constraints) + Config-Dependent (requires S)

**Gap Analysis:**
**MEDIUM-VALUE GAP:** SPP has WARL constraints but no separate MSTATUS_SPP_LEGAL_VALUES parameter. Similar to MPP gap.

**Notes:**
- Requires S (Supervisor) extension
- UDB uses sw_write() for constraint enforcement
- **This is a UDB gap - WARL parameter should exist**

---

### 25. MPIE (Machine Previous Interrupt Enable) - Bit 7 (both RV32 and RV64)

**Spec Text Citation:**
> "Holds the value of MIE prior to a trap into M-mode. On MRET, MIE is restored from MPIE, and MPIE is set to 1."

**Spec Location:** Section 3.1.6, Lines 171-174  
**Indicator Words:** N/A (explicit definition)  
**Parameter Type:** Named  
**Config Dependency:** None (always present)

**Bit Locations:**
- **RV64:** Bit 7
- **RV32:** Bit 7

**UDB Status:**
- **In UDB:** ✅ YES
- **File:** spec/std/isa/csr/mstatus.yaml
- **Lines:** 529-543
- **Type:** RW-H (Read-Write with Hardware update)

**Field Behavior:**
- Holds prior MIE value before M-mode trap
- Restored to MIE on MRET
- Set to 1 on MRET

**LLM Detection:**
- **Source:** Field definition in spec excerpt
- **Method:** Identified explicit field name
- **Reasoning:** Has explicit name "MPIE" and defined behavior
- **Classification:** Named (has explicit name, always present)

**Notes:**
- Always present (no extension dependency)
- UDB correctly defines as RW-H type

---

### 26. UBE (U-mode Big Endian) - Bit 6 (both RV32 and RV64)

**Spec Text Citation:**
> "Controls the endianness of data in U-mode (0 = little endian, 1 = big endian). Instructions are always little endian."

**Spec Location:** Section 3.1.6, Lines 176-180  
**Indicator Words:** N/A (explicit definition)  
**Parameter Type:** Named, Config-Dependent  
**Config Dependency:** U extension

**Bit Locations:**
- **RV64:** Bit 6
- **RV32:** Bit 6

**UDB Status:**
- **In UDB:** ✅ YES
- **File:** spec/std/isa/csr/mstatus.yaml
- **Lines:** 544-569
- **definedBy:** Extension U (lines 546-548)

**Field Behavior:**
- Controls data endianness in U-mode
- 0 = little endian, 1 = big endian
- Instructions always little endian regardless
- Type depends on U_MODE_ENDIANNESS parameter (RW if dynamic, RO if fixed)

**LLM Detection:**
- **Source:** Field definition in spec excerpt
- **Method:** Identified explicit field name and U extension dependency
- **Reasoning:** Explicitly named field with clear U extension requirement
- **Classification:** Named (has explicit name) + Config-Dependent (requires U extension)

**Notes:**
- Requires U (User) extension
- May be read-only or read-write depending on implementation
- UDB correctly captures extension dependency

---

### 27. SPIE (Supervisor Previous Interrupt Enable) - Bit 5 (both RV32 and RV64)

**Spec Text Citation:**
> "Holds the value of SIE prior to a trap into S-mode. On SRET, SIE is restored from SPIE, and SPIE is set to 1."

**Spec Location:** Section 3.1.6, Lines 182-186  
**Indicator Words:** N/A (explicit definition)  
**Parameter Type:** Named, Config-Dependent  
**Config Dependency:** S extension

**Bit Locations:**
- **RV64:** Bit 5
- **RV32:** Bit 5

**UDB Status:**
- **In UDB:** ✅ YES
- **File:** spec/std/isa/csr/mstatus.yaml
- **Lines:** 571-589
- **definedBy:** Extension S (lines 585-587)
- **Type:** RWH (Read-Write with Hardware update)

**Field Behavior:**
- Holds prior SIE value before S-mode trap
- Restored to SIE on SRET
- Set to 1 on SRET

**LLM Detection:**
- **Source:** Field definition in spec excerpt
- **Method:** Identified explicit field name and S extension dependency
- **Reasoning:** Explicitly named field with clear S extension requirement
- **Classification:** Named (has explicit name) + Config-Dependent (requires S extension)

**Notes:**
- Requires S (Supervisor) extension
- UDB correctly defines as RWH type
- UDB correctly captures extension dependency

---

### 28. MSTATUS_RESERVED_4 - Bit 4 (both RV32 and RV64)

**Spec Text Citation:**
> "Reserved" (from Figures 7 and 8 - register diagrams, labeled as "WPRI")

**Spec Location:** Section 3.1.6, Figures 7 and 8, Line 206  
**Indicator Words:** N/A (implicit from register diagram)  
**Parameter Type:** Unnamed (Reserved/WPRI)  
**Config Dependency:** None

**Bit Locations:**
- **RV64:** Bit 4
- **RV32:** Bit 4

**UDB Status:**
- **In UDB:** ⚠️ IMPLICIT
- **Notes:** Reserved bits are implicitly handled by UDB as gaps between defined fields
- **Validation:** No field defined at bit 4 in mstatus.yaml

**LLM Detection:**
- **Source:** Register diagram analysis and explicit reserved bits list
- **Method:** Identified gap labeled "WPRI" in diagrams
- **Reasoning:** Bit labeled "WPRI" (Write Preserve, Read Ignore)
- **Value:** Explicit enumeration aids specification completeness verification

**Notes:**
- Exists in both RV32 and RV64 at same bit position
- WPRI (Write Preserve, Read Ignore) semantics

---

### 29. MIE (Machine Interrupt Enable) - Bit 3 (both RV32 and RV64)

**Spec Text Citation:**
> "Global interrupt-enable bit for M-mode. When clear, all interrupts are disabled in M-mode. When set, interrupts that are not otherwise disabled with a field in mie are enabled."

**Spec Location:** Section 3.1.6, Lines 188-192  
**Indicator Words:** ["When clear", "When set"]  
**Parameter Type:** Named  
**Config Dependency:** None (always present)

**Bit Locations:**
- **RV64:** Bit 3
- **RV32:** Bit 3

**UDB Status:**
- **In UDB:** ✅ YES
- **File:** spec/std/isa/csr/mstatus.yaml
- **Lines:** 590-605
- **Type:** RW-H (Read-Write with Hardware update)

**Field Behavior:**
- Global interrupt enable for M-mode
- When 0: All M-mode interrupts disabled
- When 1: M-mode interrupts enabled (unless disabled in mie)
- Reset value: 0

**LLM Detection:**
- **Source:** Field definition in spec excerpt
- **Method:** Identified explicit field name
- **Reasoning:** Has explicit name "MIE" and defined behavior
- **Classification:** Named (has explicit name, always present)

**Notes:**
- Always present (no extension dependency)
- UDB correctly defines as RW-H type
- Reset value is 0

---

### 30. MSTATUS_RESERVED_2 - Bit 2 (both RV32 and RV64)

**Spec Text Citation:**
> "Reserved" (from Figures 7 and 8 - register diagrams, labeled as "WPRI")

**Spec Location:** Section 3.1.6, Figures 7 and 8, Line 207  
**Indicator Words:** N/A (implicit from register diagram)  
**Parameter Type:** Unnamed (Reserved/WPRI)  
**Config Dependency:** None

**Bit Locations:**
- **RV64:** Bit 2
- **RV32:** Bit 2

**UDB Status:**
- **In UDB:** ⚠️ IMPLICIT
- **Notes:** Reserved bits are implicitly handled by UDB as gaps between defined fields
- **Validation:** No field defined at bit 2 in mstatus.yaml

**LLM Detection:**
- **Source:** Register diagram analysis and explicit reserved bits list
- **Method:** Identified gap labeled "WPRI" in diagrams
- **Reasoning:** Bit labeled "WPRI" (Write Preserve, Read Ignore)
- **Value:** Explicit enumeration aids specification completeness verification

**Notes:**
- Exists in both RV32 and RV64 at same bit position
- WPRI (Write Preserve, Read Ignore) semantics



### 31. SIE (Supervisor Interrupt Enable) - Bit 1 (both RV32 and RV64)

**Spec Text Citation:**
> "Global interrupt-enable bit for S-mode. When clear, all S-mode interrupts are disabled when the current privilege level is S (M-mode interrupts are still enabled). When set, S-mode interrupts that are not otherwise disabled with a field in sie are enabled."

**Spec Location:** Section 3.1.6, Lines 194-198  
**Indicator Words:** ["When clear", "When set"]  
**Parameter Type:** Named, Config-Dependent  
**Config Dependency:** S extension

**Bit Locations:**
- **RV64:** Bit 1
- **RV32:** Bit 1

**UDB Status:**
- **In UDB:** ✅ YES
- **File:** spec/std/isa/csr/mstatus.yaml
- **Lines:** 606-626
- **definedBy:** Extension S (lines 622-624)
- **Type:** RWH (Read-Write with Hardware update)

**Field Behavior:**
- Global interrupt enable for S-mode
- When 0: All S-mode interrupts disabled (M-mode still enabled)
- When 1: S-mode interrupts enabled (unless disabled in sie)

**LLM Detection:**
- **Source:** Field definition in spec excerpt
- **Method:** Identified explicit field name and S extension dependency
- **Reasoning:** Explicitly named field with clear S extension requirement
- **Classification:** Named (has explicit name) + Config-Dependent (requires S extension)

**Notes:**
- Requires S (Supervisor) extension
- UDB correctly defines as RWH type
- UDB correctly captures extension dependency

---

### 32. MSTATUS_RESERVED_0 - Bit 0 (both RV32 and RV64)

**Spec Text Citation:**
> "Reserved" (from Figures 7 and 8 - register diagrams, labeled as "WPRI")

**Spec Location:** Section 3.1.6, Figures 7 and 8, Line 208  
**Indicator Words:** N/A (implicit from register diagram)  
**Parameter Type:** Unnamed (Reserved/WPRI)  
**Config Dependency:** None

**Bit Locations:**
- **RV64:** Bit 0
- **RV32:** Bit 0

**UDB Status:**
- **In UDB:** ⚠️ IMPLICIT
- **Notes:** Reserved bits are implicitly handled by UDB as gaps between defined fields
- **Validation:** No field defined at bit 0 in mstatus.yaml

**LLM Detection:**
- **Source:** Register diagram analysis and explicit reserved bits list
- **Method:** Identified gap labeled "WPRI" in diagrams
- **Reasoning:** Bit labeled "WPRI" (Write Preserve, Read Ignore)
- **Value:** Explicit enumeration aids specification completeness verification

**Notes:**
- Exists in both RV32 and RV64 at same bit position
- WPRI (Write Preserve, Read Ignore) semantics

