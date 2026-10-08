import math
import sys

# =====================================================================
#                PART 1: ANALYSIS MODULE FUNCTIONS (7 CASES)
# =====================================================================

# --- 1.1 BOLTED CONNECTIONS ANALYSIS ---

def calculate_bolt_value():
    """Case 1.1.1: Bolt Value Analysis (V_dsb & V_dpb)"""
    print("\n" + "=" * 65)
    print("  IS 800:2007 - BOLT VALUE ANALYSIS (1.1.1 Case 1)")
    print("=" * 65)

    print("\n--- [STEP 1: CONNECTION TYPE & GEOMETRY] ---")
    print("Select Shear Type:")
    print("  1. Single Shear (Lap Joint / Single Cover Butt Joint)")
    print("  2. Double Shear (Double Cover Butt Joint)")
    shear_choice = int(input("Enter choice (1 or 2): ").strip())

    if shear_choice == 1:
        t1 = float(input("Enter Main Plate 1 thickness t1 (mm): "))
        t2 = float(input("Enter Main Plate 2 / Gusset Plate thickness t2 (mm): "))
        t = min(t1, t2)
        shear_planes = 1
        print(f"-> Single shear selected. Governing thickness (t) = {t:.2f} mm")
    else:
        t_main = float(input("Enter Main Plate thickness t_main (mm): "))
        t_cover1 = float(input("Enter Top Cover Plate thickness t1 (mm): "))
        t_cover2 = float(input("Enter Bottom Cover Plate thickness t2 (mm): "))
        t = min(t_main, t_cover1 + t_cover2)
        shear_planes = 2
        print(f"-> Double shear selected. Governing thickness (t) = min({t_main}, {t_cover1}+{t_cover2}) = {t:.2f} mm")

    print("\n--- [STEP 2: BOLT PARAMETERS] ---")
    know_dn = input("Do you know the nominal bolt diameter (d_n)? (y/n): ").strip().lower()
    if know_dn == 'y':
        dn = float(input("Enter Nominal Bolt Diameter d_n (mm) [e.g., 16, 18, 20, 22, 24]: "))
    else:
        dn_unwin = 6.01 * math.sqrt(t)
        std_sizes = [12, 14, 16, 18, 20, 22, 24, 27, 30, 36]
        dn = next((s for s in std_sizes if s >= dn_unwin), math.ceil(dn_unwin))
        print(f"-> Calculated via Unwin's Formula (6.01 * sqrt({t})): {dn_unwin:.2f} mm")
        print(f"-> Selected Standard Diameter (d_n) = {dn} mm")

    bolt_grade = float(input("Enter Bolt Grade [e.g., 4.6, 4.8, 8.8]: "))
    f_ub = float(str(bolt_grade).split('.')[0]) * 100.0
    fu = float(input("Enter Ultimate Tensile Strength of Plate f_u (N/mm^2) [e.g., 410 for Fe 410]: "))

    dh = dn + (1.0 if dn <= 12 else (2.0 if dn <= 22 else 3.0))
    p = 2.5 * dn
    e = 1.5 * dh

    Asb = (math.pi / 4.0) * (dn ** 2)
    Anb = 0.78 * Asb
    gamma_mb = 1.25

    V_nsb = (f_ub / math.sqrt(3.0)) * (shear_planes * Anb)
    V_dsb = V_nsb / gamma_mb

    kb1 = e / (3.0 * dh)
    kb2 = (p / (3.0 * dh)) - 0.25
    kb3 = f_ub / fu
    kb4 = 1.0
    kb = min(kb1, kb2, kb3, kb4)

    V_npb = 2.5 * kb * dn * t * fu
    V_dpb = V_npb / gamma_mb

    bolt_value_N = min(V_dsb, V_dpb)
    bolt_value_kN = bolt_value_N / 1000.0

    print("\n" + "=" * 65)
    print("                      SUMMARY & RESULTS")
    print("=" * 65)
    print(f"  1. Nominal Bolt Diameter (d_n) : {dn:.2f} mm")
    print(f"  2. Bolt Hole Diameter (d_h)    : {dh:.2f} mm")
    print(f"  3. Minimum Pitch Distance (p)  : {p:.2f} mm (Provide ~ {math.ceil(p)} mm)")
    print(f"  4. Minimum Edge Distance (e)   : {e:.2f} mm (Provide ~ {math.ceil(e)} mm)")
    print("-" * 65)
    print(f"  - Design Shear Strength (V_dsb)   : {V_dsb/1000:.2f} kN")
    print(f"  - Design Bearing Strength (V_dpb) : {V_dpb/1000:.2f} kN")
    print("=" * 65)
    print(f"  >>> FINAL BOLT VALUE (B_r)       : {bolt_value_kN:.2f} kN ({bolt_value_N:.2f} N)")
    print("=" * 65)


def calculate_joint_efficiency():
    """Case 1.1.1: Joint Capacity & Efficiency Analysis"""
    print("\n" + "=" * 65)
    print("  IS 800:2007 - JOINT CAPACITY & EFFICIENCY ANALYSIS (1.1.1 Case 2)")
    print("=" * 65)

    print("\n--- [STEP 1: ANALYSIS MODE] ---")
    print("Select Calculation Basis:")
    print("  1. Per Pitch Width (Continuous Joint with Pitch p)")
    print("  2. Per Full Plate Width (Width w with n Bolts)")
    calc_mode = int(input("Enter choice (1 or 2): ").strip())

    print("\n--- [STEP 2: CONNECTION TYPE & GEOMETRY] ---")
    print("Select Shear Type:")
    print("  1. Single Shear (Lap Joint / Single Cover Butt Joint)")
    print("  2. Double Shear (Double Cover Butt Joint)")
    shear_choice = int(input("Enter choice (1 or 2): ").strip())

    if shear_choice == 1:
        t1 = float(input("Enter Main Plate 1 thickness t1 (mm): "))
        t2 = float(input("Enter Main Plate 2 / Gusset Plate thickness t2 (mm): "))
        t = min(t1, t2)
        shear_planes = 1
        print(f"-> Single shear selected. Governing thickness (t) = {t:.2f} mm")
    else:
        t_main = float(input("Enter Main Plate thickness t_main (mm): "))
        t_cover1 = float(input("Enter Top Cover Plate thickness t1 (mm): "))
        t_cover2 = float(input("Enter Bottom Cover Plate thickness t2 (mm): "))
        t = min(t_main, t_cover1 + t_cover2)
        shear_planes = 2
        print(f"-> Double shear selected. Governing thickness (t) = min({t_main}, {t_cover1}+{t_cover2}) = {t:.2f} mm")

    print("\n--- [STEP 3: BOLT PARAMETERS] ---")
    know_dn = input("Do you know nominal bolt diameter (d_n)? (y/n): ").strip().lower()
    if know_dn == 'y':
        dn = float(input("Enter Nominal Bolt Diameter d_n (mm) [e.g., 16, 20, 22]: "))
    else:
        dn_unwin = 6.01 * math.sqrt(t)
        std_sizes = [12, 14, 16, 18, 20, 22, 24, 27, 30, 36]
        dn = next((s for s in std_sizes if s >= dn_unwin), math.ceil(dn_unwin))
        print(f"-> Calculated via Unwin's Formula (6.01 * sqrt({t})): {dn_unwin:.2f} mm")
        print(f"-> Selected Standard Diameter (d_n) = {dn} mm")

    bolt_grade_str = input("Enter Bolt Grade [e.g., 4.6, 4.8, 8.8] (default 4.6): ").strip()
    bolt_grade = float(bolt_grade_str) if bolt_grade_str else 4.6
    f_ub = float(str(bolt_grade).split('.')[0]) * 100.0

    print("\n--- [STEP 4: PLATE MATERIAL PROPERTIES] ---")
    fu_str = input("Enter Ultimate Tensile Strength of Plate f_u (N/mm^2) [default 410]: ").strip()
    fu = float(fu_str) if fu_str else 410.0
    fy_default = 250.0 if fu == 410.0 else fu * 0.6
    fy_str = input(f"Enter Yield Strength of Plate f_y (N/mm^2) [default {fy_default:.0f}]: ").strip()
    fy = float(fy_str) if fy_str else fy_default

    dh = dn + (1.0 if dn <= 12 else (2.0 if dn <= 22 else 3.0))
    e_min = 1.5 * dh
    p_min = 2.5 * dn

    print("\n--- [STEP 5: SPACING & DIMENSIONS] ---")
    if calc_mode == 1:
        p_str = input(f"Enter Pitch distance p (mm) [min required {p_min:.1f} mm, press Enter to use min]: ").strip()
        p = float(p_str) if p_str else math.ceil(p_min)
        e_str = input(f"Enter Edge distance e (mm) [min required {e_min:.1f} mm, press Enter to use min]: ").strip()
        e = float(e_str) if e_str else math.ceil(e_min)
        num_bolts = 1
        num_bolts_line = 1
        width = p
    else:
        width = float(input("Enter Plate Width w (mm): "))
        num_bolts = int(input("Enter Total Number of Bolts in Joint (n): "))
        num_bolts_line = int(input("Enter Number of Bolts in Critical Row/Line (across width): "))
        p_str = input(f"Enter Pitch distance p (mm) [min required {p_min:.1f} mm, press Enter to use min]: ").strip()
        p = float(p_str) if p_str else math.ceil(p_min)
        e_str = input(f"Enter Edge distance e (mm) [min required {e_min:.1f} mm, press Enter to use min]: ").strip()
        e = float(e_str) if e_str else math.ceil(e_min)

    Asb = (math.pi / 4.0) * (dn ** 2)
    Anb = 0.78 * Asb
    gamma_mb = 1.25

    V_nsb = (f_ub / math.sqrt(3.0)) * (shear_planes * Anb)
    V_dsb = V_nsb / gamma_mb

    kb1 = e / (3.0 * dh)
    kb2 = (p / (3.0 * dh)) - 0.25
    kb3 = f_ub / fu
    kb4 = 1.0
    kb = min(kb1, kb2, kb3, kb4)

    V_npb = 2.5 * kb * dn * t * fu
    V_dpb = V_npb / gamma_mb

    Br_single = min(V_dsb, V_dpb)
    Br_total = num_bolts * Br_single

    gamma_m0 = 1.10
    gamma_m1 = 1.25

    A_net = (width - num_bolts_line * dh) * t
    T_dn = (0.9 * A_net * fu) / gamma_m1

    A_g = width * t
    T_dg = (A_g * fy) / gamma_m0

    P_j = min(Br_total, T_dn)
    efficiency = (P_j / T_dg) * 100.0

    print("\n" + "=" * 65)
    print("                      SUMMARY & RESULTS")
    print("=" * 65)
    print(f"  - Nominal Bolt Diameter (d_n) : {dn:.2f} mm")
    print(f"  - Hole Diameter (d_h)         : {dh:.2f} mm")
    print(f"  - Governing Thickness (t)     : {t:.2f} mm")
    print(f"  - Pitch Provided (p)          : {p:.2f} mm (Min: {p_min:.1f} mm)")
    print(f"  - Edge Provided (e)           : {e:.2f} mm (Min: {e_min:.1f} mm)")
    print(f"  - Plate Grades (f_u / f_y)    : {fu:.0f} N/mm² / {fy:.0f} N/mm²")
    print(f"  - Bearing Factor (k_b)        : {kb:.3f}")
    print("-" * 65)
    print(f"  1. Single Bolt Shear Capacity (V_dsb)   : {V_dsb/1000:.2f} kN")
    print(f"  2. Single Bolt Bearing Capacity (V_dpb) : {V_dpb/1000:.2f} kN")
    print(f"  3. Single Bolt Value (B_r)              : {Br_single/1000:.2f} kN")
    if calc_mode == 2:
        print(f"  4. Total Bolt Strength (n x B_r)        : {Br_total/1000:.2f} kN")
    print("-" * 65)
    print(f"  5. Net Area of Plate (A_net)            : {A_net:.2f} mm²")
    print(f"  6. Plate Tearing Strength (T_dn)        : {T_dn/1000:.2f} kN")
    print(f"  7. Solid Plate Strength (T_dg)          : {T_dg/1000:.2f} kN")
    print("=" * 65)
    print(f"  >>> JOINT LOAD CAPACITY (P_j)           : {P_j/1000:.2f} kN")
    print(f"  >>> JOINT EFFICIENCY (eta)              : {efficiency:.2f} %")
    print("=" * 65)


def calculate_hsfg_bolt_capacity():
    """Case 1.1.1: HSFG Bolt Slip-Resistance Capacity"""
    print("\n" + "=" * 65)
    print("  IS 800:2007 - HSFG BOLT SLIP-RESISTANCE CAPACITY (1.1.1 Case 3)")
    print("=" * 65)

    print("\n--- [STEP 1: CONNECTION TYPE & GEOMETRY] ---")
    print("Select Shear Type / Friction Interfaces:")
    print("  1. Single Shear / 1 Friction Interface (Lap Joint / Single Cover)")
    print("  2. Double Shear / 2 Friction Interfaces (Double Cover Butt Joint)")
    shear_choice = int(input("Enter choice (1 or 2): ").strip())

    if shear_choice == 1:
        t1 = float(input("Enter Main Plate 1 thickness t1 (mm): "))
        t2 = float(input("Enter Main Plate 2 / Gusset Plate thickness t2 (mm): "))
        t = min(t1, t2)
        nf = 1
        print(f"-> Single shear selected. Governing thickness (t) = {t:.2f} mm, Friction planes (n_f) = 1")
    else:
        t_main = float(input("Enter Main Plate thickness t_main (mm): "))
        t_cover1 = float(input("Enter Top Cover Plate thickness t1 (mm): "))
        t_cover2 = float(input("Enter Bottom Cover Plate thickness t2 (mm): "))
        t = min(t_main, t_cover1 + t_cover2)
        nf = 2
        print(f"-> Double shear selected. Governing thickness (t) = min({t_main}, {t_cover1}+{t_cover2}) = {t:.2f} mm, Friction planes (n_f) = 2")

    print("\n--- [STEP 2: HSFG BOLT PARAMETERS] ---")
    know_dn = input("Do you know nominal bolt diameter (d_n)? (y/n): ").strip().lower()
    if know_dn == 'y':
        dn = float(input("Enter Nominal Bolt Diameter d_n (mm) [e.g., 16, 20, 24]: "))
    else:
        dn_unwin = 6.01 * math.sqrt(t)
        std_sizes = [12, 14, 16, 18, 20, 22, 24, 27, 30, 36]
        dn = next((s for s in std_sizes if s >= dn_unwin), math.ceil(dn_unwin))
        print(f"-> Calculated via Unwin's Formula (6.01 * sqrt({t})): {dn_unwin:.2f} mm")
        print(f"-> Selected Standard Diameter (d_n) = {dn} mm")

    bolt_grade_str = input("Enter HSFG Bolt Grade [e.g., 8.8, 10.9] (default 8.8): ").strip()
    bolt_grade = float(bolt_grade_str) if bolt_grade_str else 8.8
    f_ub = float(str(bolt_grade).split('.')[0]) * 100.0

    print("\n--- [STEP 3: SLIP FACTOR & HOLE TYPE] ---")
    mu_str = input("Enter Slip Factor mu_f (mu) [default 0.55 for blasted surface]: ").strip()
    mu_f = float(mu_str) if mu_str else 0.55

    print("Select Hole Type:\n  1. Standard Clearance Hole (K_h = 1.0)\n  2. Over-sized / Short Slotted Hole (K_h = 0.85)\n  3. Long Slotted Hole (K_h = 0.70)")
    kh_choice_str = input("Enter choice (1-3) [default 1]: ").strip()
    kh_choice = int(kh_choice_str) if kh_choice_str else 1
    Kh = 1.0 if kh_choice == 1 else (0.85 if kh_choice == 2 else 0.70)

    print("Select Limit State:\n  1. Limit State of Serviceability (gamma_mf = 1.10)\n  2. Limit State of Strength / Ultimate (gamma_mf = 1.25)")
    ls_choice_str = input("Enter choice (1 or 2) [default 2]: ").strip()
    gamma_mf = 1.10 if ls_choice_str == '1' else 1.25

    print("\n--- [STEP 4: PLATE MATERIAL PROPERTIES] ---")
    fu_str = input("Enter Ultimate Tensile Strength of Plate f_u (N/mm^2) [default 410]: ").strip()
    fu = float(fu_str) if fu_str else 410.0

    dh = dn + (1.0 if dn <= 12 else (2.0 if dn <= 22 else 3.0))
    e_min = 1.5 * dh
    p_min = 2.5 * dn

    print("\n--- [STEP 5: SPACING & DIMENSIONS] ---")
    p_str = input(f"Enter Pitch distance p (mm) [min required {p_min:.1f} mm, press Enter to use min]: ").strip()
    p = float(p_str) if p_str else math.ceil(p_min)
    e_str = input(f"Enter Edge distance e (mm) [min required {e_min:.1f} mm, press Enter to use min]: ").strip()
    e = float(e_str) if e_str else math.ceil(e_min)

    Asb = (math.pi / 4.0) * (dn ** 2)
    Anb = 0.78 * Asb

    f_o = 0.70 * f_ub
    Fo = Anb * f_o

    V_nsf = mu_f * nf * Kh * Fo
    V_dsf = V_nsf / gamma_mf

    kb1 = e / (3.0 * dh)
    kb2 = (p / (3.0 * dh)) - 0.25
    kb3 = f_ub / fu
    kb4 = 1.0
    kb = min(kb1, kb2, kb3, kb4)

    V_npb = 2.5 * kb * dn * t * fu
    V_dpb = V_npb / gamma_mf

    Brf_N = min(V_dsf, V_dpb)
    Brf_kN = Brf_N / 1000.0

    print("\n" + "=" * 65)
    print("                      SUMMARY & RESULTS")
    print("=" * 65)
    print(f"  - Nominal Bolt Diameter (d_n) : {dn:.2f} mm")
    print(f"  - Hole Diameter (d_h)         : {dh:.2f} mm")
    print(f"  - Governing Plate Thickness(t): {t:.2f} mm")
    print(f"  - Bolt Grade                  : {bolt_grade}")
    print(f"  - Proof Load / Tension (F_o)  : {Fo/1000:.2f} kN (f_o = {f_o:.1f} N/mm²)")
    print(f"  - Slip Factor (mu_f)          : {mu_f:.2f}")
    print(f"  - Hole Factor (K_h)           : {Kh:.2f}")
    print(f"  - Safety Factor (gamma_mf)    : {gamma_mf:.2f}")
    print("-" * 65)
    print(f"  1. Nominal Slip Resistance (V_nsf) : {V_nsf/1000:.2f} kN")
    print(f"  2. Design Slip Resistance (V_dsf)  : {V_dsf/1000:.2f} kN")
    print(f"  3. Design Bearing Capacity (V_dpb) : {V_dpb/1000:.2f} kN")
    print("=" * 65)
    print(f"  >>> FINAL HSFG BOLT VALUE (B_rf)   : {Brf_kN:.2f} kN ({Brf_N:.2f} N)")
    print("=" * 65)


def calculate_eccentric_bolted_connection():
    """Case 1.1.1: Eccentric Bolted Bracket Connection Analysis"""
    print("\n" + "=" * 65)
    print("  IS 800:2007 - ECCENTRIC BOLTED BRACKET CONNECTION (1.1.1 Case 4)")
    print("=" * 65)

    print("\n--- [STEP 1: LOAD & ECCENTRICITY] ---")
    Pu = float(input("Enter Factored Eccentric Load P_u (kN): ").strip())
    e_ecc = float(input("Enter Eccentricity e (mm) [distance to load line]: ").strip())

    print("\n--- [STEP 2: BOLT GROUP ARRANGEMENT] ---")
    nr = int(input("Enter Number of Rows of bolts (n_r) [vertical]: ").strip())
    nc = int(input("Enter Number of Columns of bolts (n_c) [horizontal]: ").strip())
    n = nr * nc

    p = float(input("Enter Pitch distance p (mm) [vertical spacing]: ").strip())
    g = float(input("Enter Gauge distance g (mm) [horizontal spacing, enter 0 if 1 column]: ").strip()) if nc > 1 else 0.0

    print("\n--- [STEP 3: PLATE & CONNECTION DETAILS] ---")
    print("Select Shear Type:\n  1. Single Shear (Lap Joint / Bracket on 1 side)\n  2. Double Shear (Bracket on 2 sides / Double Cover)")
    shear_choice = int(input("Enter choice (1 or 2): ").strip())

    if shear_choice == 1:
        t1 = float(input("Enter Bracket Plate thickness t1 (mm): ").strip())
        t2 = float(input("Enter Column Flange / Main Plate thickness t2 (mm): ").strip())
        t = min(t1, t2)
        shear_planes = 1
    else:
        t_main = float(input("Enter Main Plate thickness t_main (mm): ").strip())
        t_cover1 = float(input("Enter Cover/Bracket Plate 1 thickness t1 (mm): ").strip())
        t_cover2 = float(input("Enter Cover/Bracket Plate 2 thickness t2 (mm): ").strip())
        t = min(t_main, t_cover1 + t_cover2)
        shear_planes = 2

    print("\n--- [STEP 4: BOLT PARAMETERS] ---")
    know_dn = input("Do you know nominal bolt diameter (d_n)? (y/n): ").strip().lower()
    if know_dn == 'y':
        dn = float(input("Enter Nominal Bolt Diameter d_n (mm) [e.g., 16, 20, 22]: ").strip())
    else:
        dn_unwin = 6.01 * math.sqrt(t)
        std_sizes = [12, 14, 16, 18, 20, 22, 24, 27, 30, 36]
        dn = next((s for s in std_sizes if s >= dn_unwin), math.ceil(dn_unwin))
        print(f"-> Calculated via Unwin's Formula (6.01 * sqrt({t})): {dn_unwin:.2f} mm")
        print(f"-> Selected Standard Diameter (d_n) = {dn} mm")

    bolt_grade_str = input("Enter Bolt Grade [e.g., 4.6, 4.8, 8.8] (default 4.6): ").strip()
    bolt_grade = float(bolt_grade_str) if bolt_grade_str else 4.6
    f_ub = float(str(bolt_grade).split('.')[0]) * 100.0

    fu_str = input("Enter Ultimate Tensile Strength of Plate f_u (N/mm^2) [default 410]: ").strip()
    fu = float(fu_str) if fu_str else 410.0

    dh = dn + (1.0 if dn <= 12 else (2.0 if dn <= 22 else 3.0))
    e_edge_min = 1.5 * dh
    e_edge_str = input(f"Enter Edge distance e_edge (mm) [min required {e_edge_min:.1f} mm, press Enter to use min]: ").strip()
    e_edge = float(e_edge_str) if e_edge_str else math.ceil(e_edge_min)

    sum_r_sq = 0.0
    x_coords = []
    y_coords = []

    for i in range(nr):
        y_i = (i - (nr - 1) / 2.0) * p
        y_coords.append(y_i)

    for j in range(nc):
        x_j = (j - (nc - 1) / 2.0) * g if nc > 1 else 0.0
        x_coords.append(x_j)

    for y_i in y_coords:
        for x_j in x_coords:
            sum_r_sq += (x_j**2 + y_i**2)

    x_max = max(abs(x) for x in x_coords) if nc > 1 else 0.0
    y_max = max(abs(y) for y in y_coords)
    r_max = math.sqrt(x_max**2 + y_max**2)

    F1 = Pu / n
    M = Pu * e_ecc
    F2 = (M * r_max) / sum_r_sq

    cos_theta = (x_max / r_max) if r_max > 0 else 0.0
    theta_deg = math.degrees(math.acos(cos_theta))

    Fr = math.sqrt(F1**2 + F2**2 + 2.0 * F1 * F2 * cos_theta)

    Asb = (math.pi / 4.0) * (dn ** 2)
    Anb = 0.78 * Asb
    gamma_mb = 1.25

    V_nsb = (f_ub / math.sqrt(3.0)) * (shear_planes * Anb)
    V_dsb = (V_nsb / gamma_mb) / 1000.0

    kb1 = e_edge / (3.0 * dh)
    kb2 = (p / (3.0 * dh)) - 0.25
    kb3 = f_ub / fu
    kb4 = 1.0
    kb = min(kb1, kb2, kb3, kb4)

    V_npb = 2.5 * kb * dn * t * fu
    V_dpb = (V_npb / gamma_mb) / 1000.0

    Br = min(V_dsb, V_dpb)
    is_safe = Fr <= Br

    print("\n" + "=" * 65)
    print("                      SUMMARY & RESULTS")
    print("=" * 65)
    print(f"  - Total Number of Bolts (n)   : {n} ({nr} rows x {nc} cols)")
    print(f"  - Nominal Bolt Diameter (d_n) : {dn:.2f} mm (Hole d_h = {dh:.2f} mm)")
    print(f"  - Governing Thickness (t)     : {t:.2f} mm")
    print(f"  - Critical Bolt Distance (r_max): {r_max:.2f} mm")
    print(f"  - Sum of r^2 (sum(r^2))       : {sum_r_sq:.2f} mm²")
    print("-" * 65)
    print(f"  1. Direct Shear Force (F_1)   : {F1:.2f} kN")
    print(f"  2. Torsional Moment (M)       : {M:.2f} kN·mm")
    print(f"  3. Torsional Force (F_2)      : {F2:.2f} kN")
    print(f"  4. Angle between F_1 & F_2 (theta): {theta_deg:.2f}° (cos theta = {cos_theta:.3f})")
    print(f"  >>> RESULTANT FORCE ON CRITICAL BOLT (F_r): {Fr:.2f} kN")
    print("-" * 65)
    print(f"  - Design Shear Capacity (V_dsb): {V_dsb:.2f} kN")
    print(f"  - Design Bearing Capacity (V_dpb): {V_dpb:.2f} kN")
    print(f"  >>> DESIGN BOLT VALUE (B_r)   : {Br:.2f} kN")
    print("=" * 65)
    if is_safe:
        print(f"  STATUS: SAFE (F_r = {Fr:.2f} kN <= B_r = {Br:.2f} kN)")
    else:
        print(f"  STATUS: UNSAFE (F_r = {Fr:.2f} kN > B_r = {Br:.2f} kN) -> Increase bolt diameter/rows!")
    print("=" * 65)


# --- 1.2 WELDED CONNECTIONS ANALYSIS ---

def calculate_fillet_weld_capacity():
    """Case 1.1.2: Design Strength of Fillet Weld"""
    print("\n" + "=" * 65)
    print("  IS 800:2007 - DESIGN STRENGTH OF FILLET WELD (1.1.2 Case 1)")
    print("=" * 65)

    print("\n--- [STEP 1: WELDING ENVIRONMENT] ---")
    print("Select Weld Type / Environment:\n  1. Shop Weld (gamma_mw = 1.25)\n  2. Field / Site Weld (gamma_mw = 1.50)")
    weld_env_str = input("Enter choice (1 or 2) [default 1]: ").strip()
    gamma_mw = 1.50 if weld_env_str == '2' else 1.25
    env_name = "Field / Site Weld" if gamma_mw == 1.50 else "Shop Weld"

    print("\n--- [STEP 2: PLATE THICKNESS & WELD SIZE] ---")
    t1 = float(input("Enter Thinner Plate thickness t1 (mm): ").strip())
    t2_str = input("Enter Thicker Plate thickness t2 (mm) [press Enter if same as t1]: ").strip()
    t2 = float(t2_str) if t2_str else t1
    t_thinner = min(t1, t2)
    t_thicker = max(t1, t2)

    s_min = 3.0 if t_thicker <= 10.0 else (5.0 if t_thicker <= 20.0 else (6.0 if t_thicker <= 32.0 else 8.0))
    s_max = max(1.0, t_thinner - 1.5)

    print(f"-> Min Weld Size (IS 800 Table 21): {s_min:.1f} mm")
    print(f"-> Max Weld Size (t_thinner - 1.5): {s_max:.1f} mm")

    s_str = input(f"Enter Weld Size s (mm) [default {min(s_max, max(s_min, 6.0)):.1f} mm]: ").strip()
    s = float(s_str) if s_str else min(s_max, max(s_min, 6.0))
    if s < s_min:
        s = s_min

    print("\n--- [STEP 3: FUSION FACE ANGLE & THROAT THICKNESS] ---")
    print("Select Fusion Face Angle Range:\n  1. 60° - 90°  (k = 0.70) [Standard]\n  2. 91° - 100° (k = 0.65)\n  3. 101° - 106° (k = 0.60)\n  4. 107° - 113° (k = 0.55)\n  5. 114° - 120° (k = 0.50)")
    angle_choice_str = input("Enter choice (1-5) [default 1]: ").strip()
    angle_choice = int(angle_choice_str) if angle_choice_str else 1
    k_values = {1: 0.70, 2: 0.65, 3: 0.60, 4: 0.55, 5: 0.50}
    k = k_values.get(angle_choice, 0.70)
    t_t = k * s

    print("\n--- [STEP 4: MATERIAL PROPERTIES] ---")
    fu_str = input("Enter Ultimate Tensile Strength of Weld/Plate f_u (N/mm^2) [default 410]: ").strip()
    fu = float(fu_str) if fu_str else 410.0
    f_wd = fu / (math.sqrt(3.0) * gamma_mw)

    print("\n--- [STEP 5: WELD LENGTH] ---")
    print("Select Length Input Type:\n  1. Provided Total Length L (mm) -> Auto-calculates Effective Length L_e = L - 2s\n  2. Direct Effective Length L_e (mm)")
    length_type_str = input("Enter choice (1 or 2) [default 1]: ").strip()

    if length_type_str == '2':
        Le = float(input("Enter Effective Length of Weld L_e (mm): ").strip())
        L_provided = Le + 2.0 * s
    else:
        L_provided = float(input("Enter Provided Length of Weld L (mm): ").strip())
        Le = max(0.0, L_provided - 2.0 * s)

    Pd_N = f_wd * Le * t_t
    Pd_kN = Pd_N / 1000.0
    qw_N = f_wd * t_t
    qw_kN = qw_N / 1000.0

    print("\n" + "=" * 65)
    print("                      SUMMARY & RESULTS")
    print("=" * 65)
    print(f"  - Weld Environment           : {env_name} (gamma_mw = {gamma_mw:.2f})")
    print(f"  - Plate Thicknesses (t1 / t2): {t1:.1f} mm / {t2:.1f} mm")
    print(f"  - Size of Weld (s)           : {s:.2f} mm (Min: {s_min:.1f} mm, Max: {s_max:.1f} mm)")
    print(f"  - Constant (k) & Angle       : k = {k:.2f}")
    print(f"  - Effective Throat Thickness : t_t = {t_t:.2f} mm")
    print(f"  - Ultimate Tensile Strength  : f_u = {fu:.0f} N/mm²")
    print(f"  - Design Shear Stress (f_wd) : {f_wd:.2f} N/mm²")
    print("-" * 65)
    print(f"  - Provided Length (L)        : {L_provided:.2f} mm")
    print(f"  - Effective Length (L_e)     : {Le:.2f} mm (L - 2s)")
    print(f"  - Strength per mm run (q_w)  : {qw_kN:.3f} kN/mm ({qw_N:.2f} N/mm)")
    print("=" * 65)
    print(f"  >>> DESIGN STRENGTH OF WELD (P_d) : {Pd_kN:.2f} kN ({Pd_N:.2f} N)")
    print("=" * 65)


def calculate_welded_joint_capacity():
    """Case 1.1.2: Total Load Capacity of Welded Joint"""
    print("\n" + "=" * 65)
    print("  IS 800:2007 - TOTAL CAPACITY OF WELDED JOINT (1.1.2 Case 2)")
    print("=" * 65)

    print("\n--- [STEP 1: WELD ENVIRONMENT] ---")
    weld_env = input("Select Weld Type (1: Shop Weld [1.25], 2: Field Weld [1.50]) [default 1]: ").strip()
    gamma_mw = 1.50 if weld_env == '2' else 1.25

    print("\n--- [STEP 2: PLATE & WELD DIMENSIONS] ---")
    t1 = float(input("Enter Main Plate / Connected Member thickness t1 (mm): ").strip())
    t2_str = input("Enter Gusset / Cover Plate thickness t2 (mm) [default t1]: ").strip()
    t2 = float(t2_str) if t2_str else t1
    t_thicker = max(t1, t2)

    s_min = 3.0 if t_thicker <= 10 else (5.0 if t_thicker <= 20 else (6.0 if t_thicker <= 32 else 8.0))
    s_max = max(1.0, min(t1, t2) - 1.5)

    print(f"-> Min Weld Size (IS 800 Table 21): {s_min:.1f} mm")
    print(f"-> Max Weld Size (Square edge): {s_max:.1f} mm")
    s_str = input(f"Enter Weld Size s (mm) [default {min(s_max, max(s_min, 6.0)):.1f} mm]: ").strip()
    s = float(s_str) if s_str else min(s_max, max(s_min, 6.0))

    k = 0.70
    t_t = k * s

    print("\n--- [STEP 3: MATERIAL PROPERTIES] ---")
    fu_str = input("Enter Ultimate Tensile Strength f_u (N/mm²) [default 410]: ").strip()
    fu = float(fu_str) if fu_str else 410.0

    fy_default = 250.0 if fu == 410.0 else fu * 0.6
    fy_str = input(f"Enter Yield Strength f_y (N/mm²) [default {fy_default:.0f}]: ").strip()
    fy = float(fy_str) if fy_str else fy_default

    f_wd = fu / (math.sqrt(3.0) * gamma_mw)
    qw_N = f_wd * t_t
    qw_kN = qw_N / 1000.0

    print("\n--- [STEP 4: WELD ARRANGEMENT & LENGTHS] ---")
    print("Select Weld Configuration:\n  1. Longitudinal Side Welds (2 parallel sides)\n  2. Three-Side Weld (2 longitudinal + 1 transverse end weld)\n  3. Custom / All-Around Total Length")
    weld_config = input("Enter choice (1-3) [default 1]: ").strip() or "1"

    if weld_config == "1":
        L_side = float(input("Enter Length of EACH side weld L_side (mm): ").strip())
        total_provided_L = 2 * L_side
        total_eff_Le = max(0.0, 2 * (L_side - 2 * s))
    elif weld_config == "2":
        L_top = float(input("Enter Top Longitudinal Weld Length L1 (mm): ").strip())
        L_bottom = float(input("Enter Bottom Longitudinal Weld Length L2 (mm): ").strip())
        L_end = float(input("Enter Transverse End Weld Length L3 (mm): ").strip())
        total_provided_L = L_top + L_bottom + L_end
        total_eff_Le = max(0.0, (L_top - 2*s)) + max(0.0, (L_bottom - 2*s)) + max(0.0, (L_end - 2*s))
    else:
        total_provided_L = float(input("Enter Total Provided Weld Length L (mm): ").strip())
        runs = int(input("Enter Number of individual weld runs/lines: ").strip() or "2")
        total_eff_Le = max(0.0, total_provided_L - runs * 2 * s)

    P_dw_N = f_wd * total_eff_Le * t_t
    P_dw_kN = P_dw_N / 1000.0

    print("\n--- [STEP 5: MEMBER / PLATE CAPACITY] ---")
    w_plate_str = input("Enter Plate Width w (mm) [press Enter to skip plate check]: ").strip()
    if w_plate_str:
        w_plate = float(w_plate_str)
        Ag = w_plate * t1
        T_dg_N = (Ag * fy) / 1.10
        T_dg_kN = T_dg_N / 1000.0
        P_joint_kN = min(P_dw_kN, T_dg_kN)
    else:
        T_dg_kN = None
        P_joint_kN = P_dw_kN

    print("\n" + "=" * 65)
    print("                      SUMMARY & RESULTS")
    print("=" * 65)
    print(f"  - Weld Environment           : {'Field Weld (gamma_mw=1.50)' if gamma_mw==1.50 else 'Shop Weld (gamma_mw=1.25)'}")
    print(f"  - Plate Thicknesses (t1 / t2): {t1:.1f} mm / {t2:.1f} mm")
    print(f"  - Size of Weld (s)           : {s:.2f} mm")
    print(f"  - Throat Thickness (t_t)    : {t_t:.2f} mm")
    print(f"  - Design Weld Stress (f_wd)  : {f_wd:.2f} N/mm²")
    print(f"  - Strength per mm run (q_w)  : {qw_kN:.3f} kN/mm ({qw_N:.2f} N/mm)")
    print("-" * 65)
    print(f"  - Total Provided Weld Length : {total_provided_L:.2f} mm")
    print(f"  - Total Effective Length(L_e): {total_eff_Le:.2f} mm")
    print(f"  >>> TOTAL WELD CAPACITY (P_dw): {P_dw_kN:.2f} kN")
    if T_dg_kN is not None:
        print(f"  - Plate Yield Capacity (T_dg): {T_dg_kN:.2f} kN")
        print("=" * 65)
        print(f"  >>> TOTAL JOINT CAPACITY (P_j): {P_joint_kN:.2f} kN")
    print("=" * 65)


def calculate_eccentric_welded_connection():
    """Case 1.1.2: Eccentric Welded Bracket Connection Analysis"""
    print("\n" + "=" * 65)
    print("  IS 800:2007 - ECCENTRIC WELDED CONNECTION (1.1.2 Case 3)")
    print("=" * 65)

    print("\n--- [STEP 1: ECCENTRICITY TYPE] ---")
    print("Select Eccentricity Configuration:\n  1. In-Plane Eccentricity (Torsion + Direct Shear)\n  2. Out-of-Plane Eccentricity (Bending + Direct Shear)")
    ecc_type = input("Enter choice (1 or 2) [default 1]: ").strip() or "1"

    print("\n--- [STEP 2: WELD & MATERIAL PROPERTIES] ---")
    weld_env = input("Select Weld Type (1: Shop Weld [1.25], 2: Field Weld [1.50]) [default 1]: ").strip()
    gamma_mw = 1.50 if weld_env == '2' else 1.25

    t1 = float(input("Enter Bracket Plate thickness t1 (mm): ").strip())
    t2 = float(input("Enter Column Flange / Main Member thickness t2 (mm) [default t1]: ").strip() or t1)
    t_thicker = max(t1, t2)

    s_min = 3.0 if t_thicker <= 10 else (5.0 if t_thicker <= 20 else (6.0 if t_thicker <= 32 else 8.0))
    s_max = max(1.0, min(t1, t2) - 1.5)

    s = float(input(f"Enter Weld Size s (mm) [min: {s_min}mm, max: {s_max}mm]: ").strip() or min(s_max, max(s_min, 6.0)))
    t_t = 0.70 * s

    fu = float(input("Enter Ultimate Tensile Strength f_u (N/mm²) [default 410]: ").strip() or "410")
    f_wd = fu / (math.sqrt(3.0) * gamma_mw)
    qw_kN = (f_wd * t_t) / 1000.0

    Pu = float(input("\nEnter Factored Eccentric Load P_u (kN): ").strip())
    e_ecc = float(input("Enter Eccentricity e (mm): ").strip())

    if ecc_type == "1":
        print("\n--- [STEP 3: WELD PATTERN & GEOMETRY (IN-PLANE)] ---")
        print("Select Weld Pattern:\n  1. Two Parallel Vertical Welds (Height D)\n  2. C-Shape / Channel Weld (Top & Bottom Flanges B + Vertical Web D)\n  3. Box / Rectangular All-Around Weld (Width B x Height D)")
        pattern = input("Enter choice (1-3) [default 1]: ").strip() or "1"

        D = float(input("Enter Vertical Height of Weld Group D (mm): ").strip())
        B = float(input("Enter Horizontal Width/Overlap of Weld Group B (mm) [if applicable, else 0]: ").strip()) if pattern in ["2", "3"] else 0.0

        if pattern == "1":
            L_eff = 2 * (D - 2*s)
            x_cg = 0.0
            I_p = (D**3) / 6.0
            x_max, y_max = 0.0, D / 2.0
            r_max = y_max
        elif pattern == "2":
            L_eff = max(0.0, D - 2*s) + 2 * max(0.0, B - 2*s)
            x_cg = (B**2) / (D + 2*B)
            I_xx = (D**3 / 12.0) + 2 * B * (D/2.0)**2
            I_yy = (D * x_cg**2) + 2 * ((B**3 / 12.0) + B * (B/2.0 - x_cg)**2)
            I_p = I_xx + I_yy
            x_max, y_max = B - x_cg, D / 2.0
            r_max = math.sqrt(x_max**2 + y_max**2)
        else:
            L_eff = 2 * max(0.0, D - 2*s) + 2 * max(0.0, B - 2*s)
            x_cg = B / 2.0
            I_xx = 2 * (D**3 / 12.0) + 2 * B * (D/2.0)**2
            I_yy = 2 * (B**3 / 12.0) + 2 * D * (B/2.0)**2
            I_p = I_xx + I_yy
            x_max, y_max = B / 2.0, D / 2.0
            r_max = math.sqrt(x_max**2 + y_max**2)

        q1_kN = Pu / L_eff if L_eff > 0 else 0.0
        M_kNmm = Pu * (e_ecc + x_cg)
        q2_x_kN = (M_kNmm * y_max) / I_p if I_p > 0 else 0.0
        q2_y_kN = (M_kNmm * x_max) / I_p if I_p > 0 else 0.0

        qr_kN = math.sqrt(q2_x_kN**2 + (q1_kN + q2_y_kN)**2)

        print("\n" + "=" * 65)
        print("                      SUMMARY & RESULTS")
        print("=" * 65)
        print(f"  - Weld Size (s) / Throat (t_t) : {s:.2f} mm / {t_t:.2f} mm")
        print(f"  - Total Effective Length (L_e) : {L_eff:.2f} mm")
        print(f"  - Polar Moment of Inertia (I_p): {I_p:.2f} mm³/mm")
        print(f"  - C.G. Distance from Web (x_cg): {x_cg:.2f} mm")
        print(f"  - Critical Point Distance(r_max): {r_max:.2f} mm")
        print("-" * 65)
        print(f"  1. Direct Shear Stress (q_1)   : {q1_kN:.3f} kN/mm")
        print(f"  2. Torsional Shear (q_2)      : {math.sqrt(q2_x_kN**2 + q2_y_kN**2):.3f} kN/mm")
        print(f"  >>> RESULTANT FORCE / MM (q_r) : {qr_kN:.3f} kN/mm")
        print(f"  >>> WELD STRENGTH / MM (q_w)   : {qw_kN:.3f} kN/mm")
        print("=" * 65)
        print(f"  STATUS : {'SAFE' if qr_kN <= qw_kN else 'UNSAFE'} (q_r = {qr_kN:.3f} kN/mm vs q_w = {qw_kN:.3f} kN/mm)")
        print("=" * 65)
    else:
        print("\n--- [STEP 3: WELD GEOMETRY (OUT-OF-PLANE)] ---")
        D = float(input("Enter Vertical Height of Weld Line D (mm): ").strip())
        welds_count = int(input("Enter Number of Vertical Weld Lines [default 2]: ").strip() or "2")

        L_eff = welds_count * max(0.0, D - 2*s)
        Zw = welds_count * (D**2 / 6.0)
        M_kNmm = Pu * e_ecc

        tau_Nmm2 = (Pu * 1000.0) / (L_eff * t_t) if (L_eff * t_t) > 0 else 0.0
        sig_b_Nmm2 = (M_kNmm * 1000.0) / (Zw * t_t) if (Zw * t_t) > 0 else 0.0
        f_eq = math.sqrt(sig_b_Nmm2**2 + 3.0 * tau_Nmm2**2)
        f_allow = fu / gamma_mw

        print("\n" + "=" * 65)
        print("                      SUMMARY & RESULTS")
        print("=" * 65)
        print(f"  - Direct Shear Stress (tau)    : {tau_Nmm2:.2f} N/mm²")
        print(f"  - Bending Stress (sigma_b)    : {sig_b_Nmm2:.2f} N/mm²")
        print(f"  >>> EQUIVALENT STRESS (f_eq)   : {f_eq:.2f} N/mm²")
        print(f"  >>> ALLOWABLE STRESS (f_allow) : {f_allow:.2f} N/mm²")
        print("=" * 65)
        print(f"  STATUS : {'SAFE' if f_eq <= f_allow else 'UNSAFE'} (f_eq = {f_eq:.2f} N/mm² vs f_allow = {f_allow:.2f} N/mm²)")
        print("=" * 65)


# =====================================================================
#                PART 2: DESIGN MODULE FUNCTIONS (6 CASES)
# =====================================================================

# --- 2.1 BOLTED CONNECTIONS DESIGN ---

def design_bolted_joint():
    """Case 2.1.1: Design of Bolted Joint (Lap / Butt Joint)"""
    print("\n" + "=" * 65)
    print("  IS 800:2007 - DESIGN OF BOLTED JOINT (2.1.1 Case 1)")
    print("=" * 65)

    print("\n--- [STEP 1: CONNECTION TYPE & LOAD] ---")
    print("Select Connection Type:\n  1. Lap Joint (Single Shear)\n  2. Single Cover Butt Joint (Single Shear)\n  3. Double Cover Butt Joint (Double Shear)")
    conn_choice = int(input("Enter choice (1-3) [default 1]: ").strip() or "1")

    Pu_kN = float(input("Enter Factored Load P_u (kN): ").strip())
    Pu_N = Pu_kN * 1000.0

    if conn_choice == 1:
        t1 = float(input("Enter Main Plate 1 thickness t1 (mm): ").strip())
        t2 = float(input("Enter Main Plate 2 / Gusset Plate thickness t2 (mm): ").strip())
        t = min(t1, t2)
        shear_planes = 1
        joint_type_str = "Lap Joint (Single Shear)"
    elif conn_choice == 2:
        t_main = float(input("Enter Main Plate thickness t_main (mm): ").strip())
        t_cover = float(input("Enter Single Cover Plate thickness t_cover (mm): ").strip())
        t = min(t_main, t_cover)
        shear_planes = 1
        joint_type_str = "Single Cover Butt Joint (Single Shear)"
    else:
        t_main = float(input("Enter Main Plate thickness t_main (mm): ").strip())
        t_cov1 = float(input("Enter Top Cover Plate thickness t1 (mm): ").strip())
        t_cov2 = float(input("Enter Bottom Cover Plate thickness t2 (mm): ").strip())
        t = min(t_main, t_cov1 + t_cov2)
        shear_planes = 2
        joint_type_str = "Double Cover Butt Joint (Double Shear)"

    print("\n--- [STEP 2: BOLT PARAMETERS] ---")
    know_dn = input("Do you know nominal bolt diameter (d_n)? (y/n): ").strip().lower()
    if know_dn == 'y':
        dn = float(input("Enter Nominal Bolt Diameter d_n (mm) [e.g., 16, 20, 22]: ").strip())
    else:
        dn_unwin = 6.01 * math.sqrt(t)
        std_sizes = [12, 14, 16, 18, 20, 22, 24, 27, 30, 36]
        dn = next((s for s in std_sizes if s >= dn_unwin), math.ceil(dn_unwin))
        print(f"-> Calculated via Unwin's Formula (6.01 * sqrt({t})): {dn_unwin:.2f} mm")
        print(f"-> Selected Standard Diameter (d_n) = {dn} mm")

    bolt_grade_str = input("Enter Bolt Grade [e.g., 4.6, 4.8, 8.8] (default 4.6): ").strip()
    bolt_grade = float(bolt_grade_str) if bolt_grade_str else 4.6
    f_ub = float(str(bolt_grade).split('.')[0]) * 100.0

    fu_str = input("Enter Ultimate Tensile Strength of Plate f_u (N/mm²) [default 410]: ").strip()
    fu = float(fu_str) if fu_str else 410.0

    dh = dn + (1.0 if dn <= 12 else (2.0 if dn <= 22 else 3.0))
    e = math.ceil(1.5 * dh)
    p = math.ceil(2.5 * dn)

    Asb = (math.pi / 4.0) * (dn ** 2)
    Anb = 0.78 * Asb
    gamma_mb = 1.25

    V_nsb = (f_ub / math.sqrt(3.0)) * (shear_planes * Anb)
    V_dsb = V_nsb / gamma_mb

    kb1 = e / (3.0 * dh)
    kb2 = (p / (3.0 * dh)) - 0.25
    kb3 = f_ub / fu
    kb4 = 1.0
    kb = min(kb1, kb2, kb3, kb4)

    V_npb = 2.5 * kb * dn * t * fu
    V_dpb = V_npb / gamma_mb

    Br = min(V_dsb, V_dpb)
    Br_kN = Br / 1000.0
    n_req = math.ceil(Pu_N / Br)

    print("\n--- [STEP 3: PLATE ARRANGEMENT & CHECK] ---")
    w_str = input("Enter Plate Width w (mm) [press Enter if unknown]: ").strip()
    if w_str:
        width = float(w_str)
        bolts_per_line = max(1, math.floor((width - 2 * e) / p) + 1) if width > 2 * e else 1
        n_rows = math.ceil(n_req / bolts_per_line)
        A_net = (width - bolts_per_line * dh) * t
        T_dn = (0.9 * A_net * fu) / 1.25
        T_dn_kN = T_dn / 1000.0
        plate_safe = T_dn >= Pu_N
    else:
        width = None
        bolts_per_line = None
        n_rows = None
        T_dn_kN = None
        plate_safe = None

    print("\n" + "=" * 65)
    print("                      DESIGN SUMMARY & RESULTS")
    print("=" * 65)
    print(f"  - Connection Type              : {joint_type_str}")
    print(f"  - Factored Design Load (P_u)   : {Pu_kN:.2f} kN")
    print(f"  - Governing Plate Thickness (t): {t:.2f} mm")
    print(f"  - Selected Bolt Diameter (d_n) : {dn:.2f} mm (Hole d_h = {dh:.2f} mm)")
    print(f"  - Bolt Grade / f_ub            : Grade {bolt_grade} ({f_ub:.0f} N/mm²)")
    print("-" * 65)
    print(f"  - Shear Capacity per Bolt (V_dsb)   : {V_dsb/1000:.2f} kN")
    print(f"  - Bearing Capacity per Bolt (V_dpb) : {V_dpb/1000:.2f} kN")
    print(f"  >>> SINGLE BOLT VALUE (B_r)         : {Br_kN:.2f} kN")
    print("=" * 65)
    print(f"  >>> NUMBER OF BOLTS REQUIRED (n)    : {n_req} bolts")
    print(f"  >>> MINIMUM PITCH DISTANCE (p)      : {p} mm")
    print(f"  >>> MINIMUM EDGE DISTANCE (e)       : {e} mm")
    if width:
        print("-" * 65)
        print(f"  - Recommended Layout across Width ({width} mm) : {bolts_per_line} bolts/line x {n_rows} lines")
        print(f"  - Design Tearing Strength (T_dn)    : {T_dn_kN:.2f} kN")
        print(f"  - Plate Tearing Status              : {'SAFE (T_dn >= P_u)' if plate_safe else 'UNSAFE (T_dn < P_u) -> Increase Width or Thickness!'}")
    print("=" * 65)


def design_packing_plate_bolted_joint():
    """Case 2.1.1: Bolted Connection with Packing Plate"""
    print("\n" + "=" * 65)
    print("  IS 800:2007 - BOLTED CONNECTION WITH PACKING PLATE (2.1.1 Case 2)")
    print("=" * 65)

    print("\n--- [STEP 1: LOAD & CONNECTION TYPE] ---")
    print("Select Shear Type:\n  1. Single Shear (Lap Joint / Single Cover Butt Joint)\n  2. Double Shear (Double Cover Butt Joint)")
    shear_choice = int(input("Enter choice (1 or 2) [default 2]: ").strip() or "2")
    shear_planes = 1 if shear_choice == 1 else 2

    Pu_kN = float(input("Enter Factored Load P_u (kN): ").strip())
    Pu_N = Pu_kN * 1000.0

    if shear_choice == 1:
        t1 = float(input("Enter Main Plate 1 thickness t1 (mm): ").strip())
        t2 = float(input("Enter Main Plate 2 thickness t2 (mm): ").strip())
        t_gov = min(t1, t2)
    else:
        t_main = float(input("Enter Main Plate thickness t_main (mm): ").strip())
        t_cov1 = float(input("Enter Top Cover Plate thickness t1 (mm): ").strip())
        t_cov2 = float(input("Enter Bottom Cover Plate thickness t2 (mm): ").strip())
        t_gov = min(t_main, t_cov1 + t_cov2)

    tpk = float(input("\nEnter Packing Plate thickness t_pk (mm): ").strip())

    if tpk > 6.0:
        beta_pk = 1.0 - 0.0125 * tpk
        beta_pk = max(0.75, beta_pk)
        print(f"-> Packing plate > 6 mm. Reduction factor beta_pk = 1 - 0.0125*{tpk} = {beta_pk:.4f}")
    else:
        beta_pk = 1.0
        print("-> Packing plate <= 6 mm. No reduction required (beta_pk = 1.0)")

    print("\n--- [STEP 2: BOLT PARAMETERS] ---")
    know_dn = input("Do you know nominal bolt diameter (d_n)? (y/n): ").strip().lower()
    if know_dn == 'y':
        dn = float(input("Enter Nominal Bolt Diameter d_n (mm) [e.g., 16, 20, 22]: ").strip())
    else:
        dn_unwin = 6.01 * math.sqrt(t_gov)
        std_sizes = [12, 14, 16, 18, 20, 22, 24, 27, 30, 36]
        dn = next((s for s in std_sizes if s >= dn_unwin), math.ceil(dn_unwin))
        print(f"-> Unwin's Formula (6.01 * sqrt({t_gov})): {dn_unwin:.2f} mm")
        print(f"-> Selected Standard Diameter (d_n) = {dn} mm")

    bolt_grade_str = input("Enter Bolt Grade [e.g., 4.6, 4.8, 8.8] (default 4.6): ").strip()
    bolt_grade = float(bolt_grade_str) if bolt_grade_str else 4.6
    f_ub = float(str(bolt_grade).split('.')[0]) * 100.0

    fu_str = input("Enter Ultimate Tensile Strength of Plate f_u (N/mm²) [default 410]: ").strip()
    fu = float(fu_str) if fu_str else 410.0

    dh = dn + (1.0 if dn <= 12 else (2.0 if dn <= 22 else 3.0))
    e = math.ceil(1.5 * dh)
    p = math.ceil(2.5 * dn)

    Asb = (math.pi / 4.0) * (dn ** 2)
    Anb = 0.78 * Asb
    gamma_mb = 1.25

    V_nsb = (f_ub / math.sqrt(3.0)) * (shear_planes * Anb)
    V_dsb_unreduced = V_nsb / gamma_mb
    V_dsb_reduced = beta_pk * V_dsb_unreduced

    kb = min(e / (3.0 * dh), (p / (3.0 * dh)) - 0.25, f_ub / fu, 1.0)
    V_dpb = (2.5 * kb * dn * t_gov * fu) / gamma_mb

    Br = min(V_dsb_reduced, V_dpb)
    Br_kN = Br / 1000.0
    n_req = math.ceil(Pu_N / Br)

    print("\n" + "=" * 65)
    print("                      DESIGN SUMMARY & RESULTS")
    print("=" * 65)
    print(f"  - Factored Design Load (P_u)   : {Pu_kN:.2f} kN")
    print(f"  - Governing Thickness (t)     : {t_gov:.2f} mm")
    print(f"  - Packing Plate Thickness(t_pk): {tpk:.2f} mm")
    print(f"  - Reduction Factor (beta_pk)  : {beta_pk:.4f}")
    print(f"  - Bolt Selected (d_n)         : {dn:.2f} mm (Hole d_h = {dh:.2f} mm)")
    print("-" * 65)
    print(f"  - Unreduced Shear Capacity (V_dsb)  : {V_dsb_unreduced/1000:.2f} kN")
    print(f"  - Reduced Shear Capacity (V_dsb_red): {V_dsb_reduced/1000:.2f} kN")
    print(f"  - Bearing Capacity (V_dpb)          : {V_dpb/1000:.2f} kN")
    print(f"  >>> GOVERNING BOLT VALUE (B_r)      : {Br_kN:.2f} kN")
    print("=" * 65)
    print(f"  >>> NUMBER OF BOLTS REQUIRED (n)    : {n_req} bolts")
    print(f"  >>> MINIMUM PITCH DISTANCE (p)      : {p} mm")
    print(f"  >>> MINIMUM EDGE DISTANCE (e)       : {e} mm")
    print("=" * 65)


def design_hsfg_connection():
    """Case 2.1.1: Design of HSFG Slip-Critical Connection"""
    print("\n" + "=" * 65)
    print("  IS 800:2007 - DESIGN OF HSFG SLIP-CRITICAL CONNECTION (2.1.1 Case 3)")
    print("=" * 65)

    print("\n--- [STEP 1: CONNECTION TYPE & LOAD] ---")
    shear_choice = int(input("Select Shear Type / Friction Interfaces:\n  1. Single Shear (1 Friction Plane)\n  2. Double Shear (2 Friction Planes)\nEnter choice (1 or 2) [default 2]: ").strip() or "2")
    nf = 1 if shear_choice == 1 else 2

    Pu_kN = float(input("Enter Factored Design Tensile/Shear Load P_u (kN): ").strip())
    Pu_N = Pu_kN * 1000.0

    if shear_choice == 1:
        t1 = float(input("Enter Main Plate 1 thickness t1 (mm): ").strip())
        t2 = float(input("Enter Main Plate 2 thickness t2 (mm): ").strip())
        t_gov = min(t1, t2)
    else:
        t_main = float(input("Enter Main Plate thickness t_main (mm): ").strip())
        t_cov1 = float(input("Enter Top Cover Plate thickness t1 (mm): ").strip())
        t_cov2 = float(input("Enter Bottom Cover Plate thickness t2 (mm): ").strip())
        t_gov = min(t_main, t_cov1 + t_cov2)

    print("\n--- [STEP 2: HSFG BOLT PARAMETERS] ---")
    know_dn = input("Do you know nominal bolt diameter (d_n)? (y/n): ").strip().lower()
    if know_dn == 'y':
        dn = float(input("Enter Nominal Bolt Diameter d_n (mm) [e.g., 16, 20, 24]: ").strip())
    else:
        dn_unwin = 6.01 * math.sqrt(t_gov)
        std_sizes = [12, 14, 16, 18, 20, 22, 24, 27, 30, 36]
        dn = next((s for s in std_sizes if s >= dn_unwin), math.ceil(dn_unwin))
        print(f"-> Calculated via Unwin's Formula (6.01 * sqrt({t_gov})): {dn_unwin:.2f} mm")
        print(f"-> Selected Standard Diameter (d_n) = {dn} mm")

    bolt_grade_str = input("Enter HSFG Bolt Grade [e.g., 8.8, 10.9] (default 8.8): ").strip()
    bolt_grade = float(bolt_grade_str) if bolt_grade_str else 8.8
    f_ub = float(str(bolt_grade).split('.')[0]) * 100.0

    fu_str = input("Enter Ultimate Tensile Strength of Plate f_u (N/mm²) [default 410]: ").strip()
    fu = float(fu_str) if fu_str else 410.0

    print("\n--- [STEP 3: SLIP FACTOR & SAFETY FACTOR] ---")
    mu_str = input("Enter Slip Factor mu_f (mu) [default 0.55 for blasted surface]: ").strip()
    mu_f = float(mu_str) if mu_str else 0.55

    print("Select Hole Type:\n  1. Standard Clearance Hole (K_h = 1.0)\n  2. Over-sized / Short Slotted Hole (K_h = 0.85)\n  3. Long Slotted Hole (K_h = 0.70)")
    kh_choice_str = input("Enter choice (1-3) [default 1]: ").strip()
    Kh = 1.0 if kh_choice_str == '1' or not kh_choice_str else (0.85 if kh_choice_str == '2' else 0.70)

    print("Select Limit State:\n  1. Limit State of Serviceability (gamma_mf = 1.10)\n  2. Limit State of Ultimate Strength (gamma_mf = 1.25)")
    ls_choice = input("Enter choice (1 or 2) [default 2]: ").strip()
    gamma_mf = 1.10 if ls_choice == '1' else 1.25

    dh = dn + (1.0 if dn <= 12 else (2.0 if dn <= 22 else 3.0))
    e = math.ceil(1.5 * dh)
    p = math.ceil(2.5 * dn)

    Asb = (math.pi / 4.0) * (dn ** 2)
    Anb = 0.78 * Asb

    f_o = 0.70 * f_ub
    Fo = Anb * f_o

    V_nsf = mu_f * nf * Kh * Fo
    V_dsf = V_nsf / gamma_mf
    V_dsf_kN = V_dsf / 1000.0

    n_req = math.ceil(Pu_N / V_dsf)

    print("\n" + "=" * 65)
    print("                      DESIGN SUMMARY & RESULTS")
    print("=" * 65)
    print(f"  - Factored Design Load (P_u)   : {Pu_kN:.2f} kN")
    print(f"  - Governing Plate Thickness (t): {t_gov:.2f} mm")
    print(f"  - HSFG Bolt Grade              : Grade {bolt_grade} (f_ub = {f_ub:.0f} N/mm²)")
    print(f"  - Selected Diameter (d_n)      : {dn:.2f} mm (Hole d_h = {dh:.2f} mm)")
    print(f"  - Proof Tension Load (F_o)     : {Fo/1000:.2f} kN")
    print(f"  - Slip Factor (mu_f) & K_h     : mu_f = {mu_f:.2f}, K_h = {Kh:.2f}")
    print(f"  - Safety Factor (gamma_mf)     : {gamma_mf:.2f}")
    print("-" * 65)
    print(f"  >>> SLIP RESISTANCE PER BOLT (V_dsf) : {V_dsf_kN:.2f} kN")
    print("=" * 65)
    print(f"  >>> REQUIRED NUMBER OF HSFG BOLTS (n): {n_req} bolts")
    print(f"  >>> MINIMUM PITCH DISTANCE (p)       : {p} mm")
    print(f"  >>> MINIMUM EDGE DISTANCE (e)        : {e} mm")
    print("=" * 65)


# --- 2.2 WELDED CONNECTIONS DESIGN ---

def design_fillet_weld():
    """Case 2.1.2: Design of Fillet Weld Size & Effective Length"""
    print("\n" + "=" * 65)
    print("  IS 800:2007 - DESIGN OF FILLET WELD (2.1.2 Case 1)")
    print("=" * 65)

    Pu_kN = float(input("Enter Factored Design Load P_u (kN): ").strip())
    Pu_N = Pu_kN * 1000.0

    weld_env = input("Select Weld Type (1: Shop Weld [1.25], 2: Field Weld [1.50]) [default 1]: ").strip()
    gamma_mw = 1.50 if weld_env == '2' else 1.25

    t1 = float(input("Enter Thinner Member thickness t1 (mm): ").strip())
    t2_str = input("Enter Thicker Member thickness t2 (mm) [default t1]: ").strip()
    t2 = float(t2_str) if t2_str else t1
    t_thicker = max(t1, t2)
    t_thinner = min(t1, t2)

    s_min = 3.0 if t_thicker <= 10.0 else (5.0 if t_thicker <= 20.0 else (6.0 if t_thicker <= 32.0 else 8.0))
    s_max = max(1.0, t_thinner - 1.5)

    print(f"\n-> IS 800 Limits for Weld Size (s): Minimum = {s_min:.1f} mm, Maximum = {s_max:.1f} mm")
    s_str = input(f"Enter Proposed Weld Size s (mm) [recommended {min(s_max, max(s_min, 6.0)):.1f} mm]: ").strip()
    s = float(s_str) if s_str else min(s_max, max(s_min, 6.0))

    if s < s_min or s > s_max:
        print(f"WARNING: Selected weld size s = {s:.1f} mm is outside standard limits [{s_min} mm, {s_max} mm].")

    k = 0.70
    t_t = k * s

    fu_str = input("\nEnter Ultimate Tensile Strength f_u (N/mm²) [default 410]: ").strip()
    fu = float(fu_str) if fu_str else 410.0

    f_wd = fu / (math.sqrt(3.0) * gamma_mw)
    qw_N_mm = f_wd * t_t
    qw_kN_mm = qw_N_mm / 1000.0

    Le_req = Pu_N / qw_N_mm

    print("\nSelect Weld Layout / Arrangement:\n  1. Two Parallel Side Longitudinal Welds\n  2. Three-Side Weld (2 Side + 1 End Transverse Weld)\n  3. Single Transverse End Weld")
    layout = input("Enter choice (1-3) [default 1]: ").strip() or "1"

    if layout == "1":
        Le_per_side = Le_req / 2.0
        L_provided_per_side = math.ceil(Le_per_side + 2.0 * s)
        total_L_provided = 2 * L_provided_per_side
        layout_str = "Two Parallel Side Longitudinal Welds"
    elif layout == "2":
        w_trans = float(input("Enter Width of End Transverse Weld w_end (mm): ").strip())
        Le_end = max(0.0, w_trans - 2.0 * s)
        Le_remaining_sides = max(0.0, Le_req - Le_end)
        Le_per_side = Le_remaining_sides / 2.0
        L_provided_per_side = math.ceil(Le_per_side + 2.0 * s) if Le_per_side > 0 else 0
        total_L_provided = 2 * L_provided_per_side + w_trans
        layout_str = f"Three-Side Weld (End = {w_trans:.1f} mm + 2 Sides)"
    else:
        total_L_provided = math.ceil(Le_req + 2.0 * s)
        layout_str = "Single Transverse End Weld"

    print("\n" + "=" * 65)
    print("                      DESIGN SUMMARY & RESULTS")
    print("=" * 65)
    print(f"  - Factored Design Load (P_u)   : {Pu_kN:.2f} kN")
    print(f"  - Thinner Plate / Member (t1)  : {t_thinner:.2f} mm")
    print(f"  - Selected Weld Size (s)       : {s:.2f} mm (Limits: {s_min} - {s_max} mm)")
    print(f"  - Effective Throat (t_t)      : {t_t:.2f} mm")
    print(f"  - Design Weld Stress (f_wd)    : {f_wd:.2f} N/mm²")
    print(f"  - Strength per mm run (q_w)    : {qw_kN_mm:.3f} kN/mm")
    print("-" * 65)
    print(f"  >>> REQ. TOTAL EFFECTIVE LENGTH (L_e) : {Le_req:.2f} mm")
    print(f"  - Selected Layout              : {layout_str}")
    if layout == "1":
        print(f"  >>> PROVIDE SIDE WELD LENGTH   : {L_provided_per_side} mm on EACH of the 2 sides")
    elif layout == "2":
        print(f"  >>> PROVIDE END TRANSVERSE WELD: {w_trans:.1f} mm")
        print(f"  >>> PROVIDE SIDE WELD LENGTH   : {L_provided_per_side} mm on EACH of the 2 sides")
    else:
        print(f"  >>> PROVIDE TOTAL WELD LENGTH  : {total_L_provided} mm")
    print(f"  - Total Provided Length        : {total_L_provided} mm")
    print("=" * 65)


def design_asymmetrical_angle_weld():
    """Case 2.1.2: Asymmetrical Angle Welded Connection Design"""
    print("\n" + "=" * 65)
    print("  IS 800:2007 - ASYMMETRICAL ANGLE WELDED CONNECTION (2.1.2 Case 2)")
    print("=" * 65)

    Pu_kN = float(input("Enter Factored Tensile Load P_u (kN): ").strip())
    Pu_N = Pu_kN * 1000.0

    weld_env = input("Select Weld Type (1: Shop Weld [1.25], 2: Field Weld [1.50]) [default 1]: ").strip()
    gamma_mw = 1.50 if weld_env == '2' else 1.25

    W = float(input("Enter Connected Leg Width of Angle W (mm) [e.g., 90, 100, 125]: ").strip())
    Cz = float(input("Enter Distance of C.G. from Root C_z (mm) [from steel table]: ").strip())
    t_angle = float(input("Enter Angle Thickness t_angle (mm): ").strip())
    t_gusset = float(input("Enter Gusset Plate Thickness t_gusset (mm): ").strip())

    t_thicker = max(t_angle, t_gusset)
    t_thinner = min(t_angle, t_gusset)

    s_min = 3.0 if t_thicker <= 10.0 else (5.0 if t_thicker <= 20.0 else (6.0 if t_thicker <= 32.0 else 8.0))
    s_max = max(1.0, t_thinner - 1.5)

    s_str = input(f"Enter Proposed Weld Size s (mm) [min: {s_min}mm, max: {s_max}mm]: ").strip()
    s = float(s_str) if s_str else min(s_max, max(s_min, 6.0))

    t_t = 0.70 * s
    fu = float(input("Enter Ultimate Strength f_u (N/mm²) [default 410]: ").strip() or "410")
    f_wd = fu / (math.sqrt(3.0) * gamma_mw)
    qw_kN_mm = (f_wd * t_t) / 1000.0

    print("\nInclude End Transverse Weld along the width W?\n  1. No (Only 2 side welds L1 at root and L2 at toe)\n  2. Yes (3-side weld: L1 at root, L2 at toe, and L3 at end width W)")
    trans_choice = input("Enter choice (1 or 2) [default 1]: ").strip() or "1"

    if trans_choice == "1":
        Pw2 = (Pu_N * Cz) / W
        Pw1 = Pu_N - Pw2

        Le1_req = Pw1 / (f_wd * t_t)
        Le2_req = Pw2 / (f_wd * t_t)

        L1_provided = math.ceil(Le1_req + 2.0 * s)
        L2_provided = math.ceil(Le2_req + 2.0 * s)

        print("\n" + "=" * 65)
        print("                      DESIGN SUMMARY & RESULTS")
        print("=" * 65)
        print(f"  - Angle Connected Leg (W)      : {W:.1f} mm")
        print(f"  - Distance to C.G. (C_z)       : {Cz:.2f} mm")
        print(f"  - Design Weld Stress (f_wd)    : {f_wd:.2f} N/mm²")
        print(f"  - Throat Thickness (t_t)      : {t_t:.2f} mm")
        print(f"  - Strength per mm run (q_w)    : {qw_kN_mm:.3f} kN/mm")
        print("-" * 65)
        print(f"  - Force at Root Weld (P_w1)    : {Pw1/1000:.2f} kN")
        print(f"  - Force at Toe Weld (P_w2)     : {Pw2/1000:.2f} kN")
        print(f"  >>> PROVIDE ROOT WELD LENGTH (L_1): {L1_provided} mm (Effective {Le1_req:.1f} mm)")
        print(f"  >>> PROVIDE TOE WELD LENGTH (L_2) : {L2_provided} mm (Effective {Le2_req:.1f} mm)")
        print("=" * 65)
    else:
        Le_end = max(0.0, W - 2.0 * s)
        Pw_end = f_wd * t_t * Le_end

        Pw2 = (Pu_N * Cz - Pw_end * (W / 2.0)) / W
        Pw1 = Pu_N - Pw2 - Pw_end

        Le1_req = max(0.0, Pw1 / (f_wd * t_t))
        Le2_req = max(0.0, Pw2 / (f_wd * t_t))

        L1_provided = math.ceil(Le1_req + 2.0 * s) if Le1_req > 0 else 0
        L2_provided = math.ceil(Le2_req + 2.0 * s) if Le2_req > 0 else 0

        print("\n" + "=" * 65)
        print("                      DESIGN SUMMARY & RESULTS")
        print("=" * 65)
        print(f"  - Angle Connected Leg (W)      : {W:.1f} mm")
        print(f"  - Distance to C.G. (C_z)       : {Cz:.2f} mm")
        print(f"  - Design Weld Stress (f_wd)    : {f_wd:.2f} N/mm²")
        print(f"  - Throat Thickness (t_t)      : {t_t:.2f} mm")
        print("-" * 65)
        print(f"  - Transverse End Weld Capacity : {Pw_end/1000:.2f} kN")
        print(f"  - Force at Root Weld (P_w1)    : {Pw1/1000:.2f} kN")
        print(f"  - Force at Toe Weld (P_w2)     : {Pw2/1000:.2f} kN")
        print(f"  >>> PROVIDE TRANSVERSE END WELD : {W:.1f} mm")
        print(f"  >>> PROVIDE ROOT WELD LENGTH (L_1): {L1_provided} mm")
        print(f"  >>> PROVIDE TOE WELD LENGTH (L_2) : {L2_provided} mm")
        print("=" * 65)


def design_eccentric_welded_connection():
    """Case 2.1.2: Design of Eccentric Welded Bracket Connection"""
    print("\n" + "=" * 65)
    print("  IS 800:2007 - DESIGN OF ECCENTRIC WELDED CONNECTION (2.1.2 Case 3)")
    print("=" * 65)

    print("Select Eccentricity Configuration:\n  1. In-Plane Eccentricity (Torsion + Direct Shear)\n  2. Out-of-Plane Eccentricity (Bending + Direct Shear)")
    ecc_type = input("Enter choice (1 or 2) [default 1]: ").strip() or "1"

    Pu_kN = float(input("\nEnter Factored Eccentric Load P_u (kN): ").strip())
    Pu_N = Pu_kN * 1000.0
    e_ecc = float(input("Enter Eccentricity e (mm): ").strip())

    weld_env = input("Select Weld Type (1: Shop Weld [1.25], 2: Field Weld [1.50]) [default 1]: ").strip()
    gamma_mw = 1.50 if weld_env == '2' else 1.25

    t1 = float(input("Enter Bracket Plate thickness t1 (mm): ").strip())
    t2_str = input("Enter Main Member thickness t2 (mm) [default t1]: ").strip()
    t2 = float(t2_str) if t2_str else t1
    t_thicker = max(t1, t2)
    t_thinner = min(t1, t2)

    s_min = 3.0 if t_thicker <= 10.0 else (5.0 if t_thicker <= 20.0 else (6.0 if t_thicker <= 32.0 else 8.0))
    s_max = max(1.0, t_thinner - 1.5)

    fu = float(input("Enter Ultimate Tensile Strength f_u (N/mm²) [default 410]: ").strip() or "410")
    f_wd = fu / (math.sqrt(3.0) * gamma_mw)

    if ecc_type == "1":
        print("\nSelect Weld Pattern:\n  1. Two Parallel Vertical Welds (Height D)\n  2. C-Shape / Channel Weld (Flanges B + Web D)\n  3. Box / Rectangular All-Around Weld (B x D)")
        pattern = input("Enter choice (1-3) [default 1]: ").strip() or "1"

        D = float(input("Enter Vertical Height D (mm): ").strip())
        B = float(input("Enter Width B (mm): ").strip()) if pattern in ["2", "3"] else 0.0

        if pattern == "1":
            L_eff = 2 * D
            x_cg = 0.0
            I_p = (D**3) / 6.0
            x_max, y_max = 0.0, D / 2.0
        elif pattern == "2":
            L_eff = D + 2 * B
            x_cg = (B**2) / (D + 2 * B)
            I_xx = (D**3 / 12.0) + 2 * B * (D / 2.0)**2
            I_yy = (D * x_cg**2) + 2 * ((B**3 / 12.0) + B * (B / 2.0 - x_cg)**2)
            I_p = I_xx + I_yy
            x_max, y_max = B - x_cg, D / 2.0
        else:
            L_eff = 2 * D + 2 * B
            x_cg = B / 2.0
            I_xx = 2 * (D**3 / 12.0) + 2 * B * (D / 2.0)**2
            I_yy = 2 * (B**3 / 12.0) + 2 * D * (B / 2.0)**2
            I_p = I_xx + I_yy
            x_max, y_max = B / 2.0, D / 2.0

        q1 = Pu_N / L_eff
        M_Nmm = Pu_N * (e_ecc + x_cg)

        q2_x = (M_Nmm * y_max) / I_p
        q2_y = (M_Nmm * x_max) / I_p
        qr = math.sqrt(q2_x**2 + (q1 + q2_y)**2)

        tt_req = qr / f_wd
        s_req = tt_req / 0.70
        s_provided = max(s_min, math.ceil(s_req))

        if s_provided > s_max:
            s_status = f"WARNING: Required size ({s_provided} mm) exceeds max size ({s_max:.1f} mm)! Increase D or B."
        else:
            s_status = f"SAFE: Provide s = {s_provided} mm (Min: {s_min} mm, Max: {s_max:.1f} mm)"

        print("\n" + "=" * 65)
        print("                      DESIGN SUMMARY & RESULTS")
        print("=" * 65)
        print(f"  - Total Effective Length (L_e) : {L_eff:.2f} mm")
        print(f"  - Unit Polar Moment (I_p)      : {I_p:.2f} mm³/mm")
        print(f"  - Resultant Unit Force (q_r)   : {qr:.2f} N/mm ({qr/1000:.3f} kN/mm)")
        print(f"  - Design Weld Stress (f_wd)    : {f_wd:.2f} N/mm²")
        print("-" * 65)
        print(f"  - Required Throat Thickness(t_t): {tt_req:.2f} mm")
        print(f"  - Required Weld Size (s_req)   : {s_req:.2f} mm")
        print(f"  >>> RECOMMENDED WELD SIZE (s)  : {s_provided} mm")
        print(f"  >>> {s_status}")
        print("=" * 65)
    else:
        D = float(input("Enter Vertical Height of Weld Line D (mm): ").strip())
        welds_count = int(input("Enter Number of Vertical Weld Lines [default 2]: ").strip() or "2")

        L_eff = welds_count * D
        Zw = welds_count * (D**2 / 6.0)
        M_Nmm = Pu_N * e_ecc

        q_v = Pu_N / L_eff
        q_b = M_Nmm / Zw
        f_allow = fu / gamma_mw
        q_eq = math.sqrt(q_b**2 + 3.0 * q_v**2)
        tt_req = q_eq / f_allow
        s_req = tt_req / 0.70
        s_provided = max(s_min, math.ceil(s_req))

        if s_provided > s_max:
            s_status = f"WARNING: Required size ({s_provided} mm) exceeds max size ({s_max:.1f} mm)! Increase D."
        else:
            s_status = f"SAFE: Provide s = {s_provided} mm (Min: {s_min} mm, Max: {s_max:.1f} mm)"

        print("\n" + "=" * 65)
        print("                      DESIGN SUMMARY & RESULTS")
        print("=" * 65)
        print(f"  - Direct Shear Force / mm (q_v) : {q_v:.2f} N/mm")
        print(f"  - Bending Force / mm (q_b)      : {q_b:.2f} N/mm")
        print(f"  - Equivalent Force / mm (q_eq)  : {q_eq:.2f} N/mm")
        print(f"  - Allowable Stress (f_allow)    : {f_allow:.2f} N/mm²")
        print("-" * 65)
        print(f"  - Required Throat Thickness(t_t): {tt_req:.2f} mm")
        print(f"  - Required Weld Size (s_req)   : {s_req:.2f} mm")
        print(f"  >>> RECOMMENDED WELD SIZE (s)  : {s_provided} mm")
        print(f"  >>> {s_status}")
        print("=" * 65)


# =====================================================================
#                PART 3: NAVIGATION MENU STRUCTURE
# =====================================================================

def bolted_analysis_menu():
    while True:
        print("\n--------------------------------------------------")
        print(">>> ANALYSIS MODULE -> BOLTED CONNECTIONS")
        print("--------------------------------------------------")
        print("  [1] Case 1: Bolt Value (Shear & Bearing Capacity)")
        print("  [2] Case 2: Joint Load Capacity & Efficiency")
        print("  [3] Case 3: HSFG Bolt Slip-Resistance Capacity")
        print("  [4] Case 4: Eccentric Bolted Bracket Connection")
        print("  [0] Back to Analysis Menu")
        print("--------------------------------------------------")
        choice = input("Enter choice (1-4, 0): ").strip()
        if choice == '1': calculate_bolt_value()
        elif choice == '2': calculate_joint_efficiency()
        elif choice == '3': calculate_hsfg_bolt_capacity()
        elif choice == '4': calculate_eccentric_bolted_connection()
        elif choice == '0': break
        else: print("Invalid choice! Please select 1-4 or 0.")


def welded_analysis_menu():
    while True:
        print("\n--------------------------------------------------")
        print(">>> ANALYSIS MODULE -> WELDED CONNECTIONS")
        print("--------------------------------------------------")
        print("  [1] Case 1: Design Strength of Fillet Weld")
        print("  [2] Case 2: Total Load Capacity of Welded Joint")
        print("  [3] Case 3: Eccentric Welded Bracket Connection")
        print("  [0] Back to Analysis Menu")
        print("--------------------------------------------------")
        choice = input("Enter choice (1-3, 0): ").strip()
        if choice == '1': calculate_fillet_weld_capacity()
        elif choice == '2': calculate_welded_joint_capacity()
        elif choice == '3': calculate_eccentric_welded_connection()
        elif choice == '0': break
        else: print("Invalid choice! Please select 1-3 or 0.")


def analysis_menu():
    while True:
        print("\n--------------------------------------------------")
        print(">>> MAIN MENU -> ANALYSIS MODULE (CHAPTER 1)")
        print("--------------------------------------------------")
        print("  [1] Bolted Connections Analysis (4 Cases)")
        print("  [2] Welded Connections Analysis (3 Cases)")
        print("  [0] Back to Main Menu")
        print("--------------------------------------------------")
        choice = input("Enter choice (1, 2, 0): ").strip()
        if choice == '1': bolted_analysis_menu()
        elif choice == '2': welded_analysis_menu()
        elif choice == '0': break
        else: print("Invalid choice! Please select 1, 2, or 0.")


def bolted_design_menu():
    while True:
        print("\n--------------------------------------------------")
        print(">>> DESIGN MODULE -> BOLTED CONNECTIONS")
        print("--------------------------------------------------")
        print("  [1] Case 1: Standard Bolted Joint Design (Lap / Butt)")
        print("  [2] Case 2: Joint with Packing Plate Design (beta_pk)")
        print("  [3] Case 3: HSFG Slip-Critical Connection Design")
        print("  [0] Back to Design Menu")
        print("--------------------------------------------------")
        choice = input("Enter choice (1-3, 0): ").strip()
        if choice == '1': design_bolted_joint()
        elif choice == '2': design_packing_plate_bolted_joint()
        elif choice == '3': design_hsfg_connection()
        elif choice == '0': break
        else: print("Invalid choice! Please select 1-3 or 0.")


def welded_design_menu():
    while True:
        print("\n--------------------------------------------------")
        print(">>> DESIGN MODULE -> WELDED CONNECTIONS")
        print("--------------------------------------------------")
        print("  [1] Case 1: Fillet Weld Size & Effective Length Layout")
        print("  [2] Case 2: Asymmetrical Angle Connection Design (C.G.)")
        print("  [3] Case 3: Eccentric Welded Bracket Connection Design")
        print("  [0] Back to Design Menu")
        print("--------------------------------------------------")
        choice = input("Enter choice (1-3, 0): ").strip()
        if choice == '1': design_fillet_weld()
        elif choice == '2': design_asymmetrical_angle_weld()
        elif choice == '3': design_eccentric_welded_connection()
        elif choice == '0': break
        else: print("Invalid choice! Please select 1-3 or 0.")


def design_menu():
    while True:
        print("\n--------------------------------------------------")
        print(">>> MAIN MENU -> DESIGN MODULE (CHAPTER 1)")
        print("--------------------------------------------------")
        print("  [1] Bolted Connections Design (3 Cases)")
        print("  [2] Welded Connections Design (3 Cases)")
        print("  [0] Back to Main Menu")
        print("--------------------------------------------------")
        choice = input("Enter choice (1, 2, 0): ").strip()
        if choice == '1': bolted_design_menu()
        elif choice == '2': welded_design_menu()
        elif choice == '0': break
        else: print("Invalid choice! Please select 1, 2, or 0.")


def main_menu():
    while True:
        print("\n==================================================")
        print(" STEEL STRUCTURES DESIGN AUTOMATION (IS 800:2007) ")
        print("         CHAPTER 1: CONNECTIONS MODULE            ")
        print("==================================================")
        print(" [1] Analysis Module (Calculate Capacities & Stresses)")
        print(" [2] Design Module (Size Sections & Connections)")
        print(" [0] Exit Program")
        print("==================================================")
        choice = input("Enter choice (1, 2, 0): ").strip()
        if choice == '1': analysis_menu()
        elif choice == '2': design_menu()
        elif choice == '0':
            print("\nExiting Program. All the best for tomorrow's presentation!")
            sys.exit()
        else:
            print("Invalid choice! Please select 1, 2, or 0.")


if __name__ == "__main__":
    main_menu()