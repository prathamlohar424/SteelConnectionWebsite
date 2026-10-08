import streamlit as st
import project
import builtins
import io
import contextlib
import base64
import os


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Steel Structures Design Automation",
    page_icon="🏗️",
    layout="wide"
)


# ============================================================
# BACKGROUND IMAGE
# ============================================================

def get_background_image():

    image_path = os.path.join(
        "img",
        "steel_background.jpg"
    )

    if os.path.exists(image_path):

        with open(image_path, "rb") as image_file:

            encoded = base64.b64encode(
                image_file.read()
            ).decode()

        return encoded

    return None


background_image = get_background_image()


# ============================================================
# CUSTOM CSS
# ============================================================

if background_image:

    st.markdown(
        f"""
        <style>

        .stApp {{
            background-image:
                linear-gradient(
                    rgba(0, 0, 0, 0.55),
                    rgba(0, 0, 0, 0.55)
                ),
                url("data:image/jpeg;base64,{background_image}");

            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        .main-title {{
            text-align: center;
            font-size: 42px;
            font-weight: bold;
            color: white;
            margin-top: 80px;
            margin-bottom: 10px;
            text-shadow: 2px 2px 6px black;
        }}

        .subtitle {{
            text-align: center;
            font-size: 21px;
            color: white;
            margin-bottom: 40px;
            text-shadow: 2px 2px 5px black;
        }}

        .card {{
            padding: 25px;
            border-radius: 15px;
            border: 1px solid rgba(255,255,255,0.3);
            background-color: rgba(255,255,255,0.92);
            margin-bottom: 15px;
        }}

        .case-title {{
            font-size: 21px;
            font-weight: bold;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )

else:

    st.markdown(
        """
        <style>

        .main-title {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
        }

        .subtitle {
            text-align: center;
            font-size: 18px;
            color: #666666;
            margin-bottom: 30px;
        }

        .card {
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #dddddd;
            background-color: #f8f9fa;
            margin-bottom: 15px;
        }

        .case-title {
            font-size: 20px;
            font-weight: bold;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "case" not in st.session_state:
    st.session_state.case = None

if "inputs" not in st.session_state:
    st.session_state.inputs = []

if "current_prompt" not in st.session_state:
    st.session_state.current_prompt = None

if "calculation_started" not in st.session_state:
    st.session_state.calculation_started = False

if "calculation_finished" not in st.session_state:
    st.session_state.calculation_finished = False

if "result" not in st.session_state:
    st.session_state.result = ""


# ============================================================
# CALCULATION FUNCTIONS
# ============================================================

CALCULATIONS = {

    # ---------------- ANALYSIS ----------------

    "bolt_analysis_1": (
        "Bolt Value",
        project.calculate_bolt_value
    ),

    "bolt_analysis_2": (
        "Joint Load Capacity & Efficiency",
        project.calculate_joint_efficiency
    ),

    "bolt_analysis_3": (
        "HSFG Bolt Slip-Resistance Capacity",
        project.calculate_hsfg_bolt_capacity
    ),

    "bolt_analysis_4": (
        "Eccentric Bolted Bracket Connection",
        project.calculate_eccentric_bolted_connection
    ),

    "weld_analysis_1": (
        "Design Strength of Fillet Weld",
        project.calculate_fillet_weld_capacity
    ),

    "weld_analysis_2": (
        "Total Load Capacity of Welded Joint",
        project.calculate_welded_joint_capacity
    ),

    "weld_analysis_3": (
        "Eccentric Welded Bracket Connection",
        project.calculate_eccentric_welded_connection
    ),

    # ---------------- DESIGN ----------------

    "bolt_design_1": (
        "Standard Bolted Joint Design",
        project.design_bolted_joint
    ),

    "bolt_design_2": (
        "Joint with Packing Plate Design",
        project.design_packing_plate_bolted_joint
    ),

    "bolt_design_3": (
        "HSFG Slip-Critical Connection Design",
        project.design_hsfg_connection
    ),

    "weld_design_1": (
        "Fillet Weld Size & Effective Length Layout",
        project.design_fillet_weld
    ),

    "weld_design_2": (
        "Asymmetrical Angle Connection Design",
        project.design_asymmetrical_angle_weld
    ),

    "weld_design_3": (
        "Eccentric Welded Bracket Connection Design",
        project.design_eccentric_welded_connection
    )
}


# ============================================================
# RESET CALCULATION
# ============================================================

def reset_calculation():

    st.session_state.inputs = []

    st.session_state.current_prompt = None

    st.session_state.calculation_started = False

    st.session_state.calculation_finished = False

    st.session_state.result = ""


# ============================================================
# INPUT HANDLING
# ============================================================

class NeedMoreInput(Exception):

    def __init__(self, prompt):

        self.prompt = prompt


def run_original_function(function, previous_inputs):

    values = list(previous_inputs)

    index = 0

    original_input = builtins.input

    def fake_input(prompt=""):

        nonlocal index

        if index < len(values):

            value = values[index]

            index += 1

            return value

        raise NeedMoreInput(prompt)

    builtins.input = fake_input

    output = io.StringIO()

    try:

        with contextlib.redirect_stdout(output):

            function()

        return {
            "status": "finished",
            "prompt": None,
            "output": output.getvalue()
        }

    except NeedMoreInput as e:

        return {
            "status": "need_input",
            "prompt": e.prompt,
            "output": output.getvalue()
        }

    except Exception as e:

        return {
            "status": "error",
            "prompt": None,
            "output": output.getvalue(),
            "error": str(e)
        }

    finally:

        builtins.input = original_input


# ============================================================
# START CALCULATION
# ============================================================

def start_calculation():

    reset_calculation()

    st.session_state.calculation_started = True

    function = CALCULATIONS[
        st.session_state.case
    ][1]

    result = run_original_function(
        function,
        []
    )

    if result["status"] == "need_input":

        st.session_state.current_prompt = result["prompt"]

    elif result["status"] == "finished":

        st.session_state.calculation_finished = True

        st.session_state.result = result["output"]

    else:

        st.session_state.calculation_finished = True

        st.session_state.result = (
            result["output"]
            + "\n\nERROR: "
            + result["error"]
        )


# ============================================================
# PROCESS INPUT
# ============================================================

def process_input(value):

    st.session_state.inputs.append(value)

    function = CALCULATIONS[
        st.session_state.case
    ][1]

    result = run_original_function(
        function,
        st.session_state.inputs
    )

    if result["status"] == "need_input":

        st.session_state.current_prompt = result["prompt"]

    elif result["status"] == "finished":

        st.session_state.calculation_finished = True

        st.session_state.current_prompt = None

        st.session_state.result = result["output"]

    else:

        st.session_state.calculation_finished = True

        st.session_state.current_prompt = None

        st.session_state.result = (
            result["output"]
            + "\n\nERROR: "
            + result["error"]
        )


# ============================================================
# HOME PAGE
# ============================================================

def home_page():

    st.markdown(
        '<div class="main-title">'
        '🏗️ Steel Structures Design Automation'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'IS 800:2007 - Chapter 1: Connections Module'
        '</div>',
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            """
            <div class="card">

            <div class="case-title">
            📊 Analysis Module
            </div>

            <br>

            Calculate capacities, stresses and efficiencies for:

            - Bolted connections
            - HSFG bolts
            - Eccentric bolted connections
            - Fillet welds
            - Welded joints
            - Eccentric welded connections

            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Open Analysis Module",
            use_container_width=True
        ):

            reset_calculation()

            st.session_state.page = "analysis"

            st.rerun()

    with col2:

        st.markdown(
            """
            <div class="card">

            <div class="case-title">
            📐 Design Module
            </div>

            <br>

            Design:

            - Standard bolted joints
            - Packing plate connections
            - HSFG connections
            - Fillet welds
            - Asymmetrical angle connections
            - Eccentric welded connections

            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Open Design Module",
            use_container_width=True
        ):

            reset_calculation()

            st.session_state.page = "design"

            st.rerun()


# ============================================================
# ANALYSIS PAGE
# ============================================================

def analysis_page():

    st.title("📊 Analysis Module")

    st.write(
        "Select the type of connection you want to analyse."
    )

    if st.button("⬅️ Back to Home"):

        reset_calculation()

        st.session_state.page = "home"

        st.rerun()

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🔩 Bolted Connections Analysis",
            use_container_width=True
        ):

            reset_calculation()

            st.session_state.page = "bolted_analysis"

            st.rerun()

    with col2:

        if st.button(
            "🔥 Welded Connections Analysis",
            use_container_width=True
        ):

            reset_calculation()

            st.session_state.page = "welded_analysis"

            st.rerun()


# ============================================================
# BOLTED ANALYSIS
# ============================================================

def bolted_analysis_page():

    st.title("🔩 Bolted Connections Analysis")

    if st.button("⬅️ Back"):

        reset_calculation()

        st.session_state.page = "analysis"

        st.rerun()

    st.divider()

    cases = {

        "Case 1 - Bolt Value (Shear & Bearing Capacity)":
            "bolt_analysis_1",

        "Case 2 - Joint Load Capacity & Efficiency":
            "bolt_analysis_2",

        "Case 3 - HSFG Bolt Slip-Resistance Capacity":
            "bolt_analysis_3",

        "Case 4 - Eccentric Bolted Bracket Connection":
            "bolt_analysis_4"
    }

    selected = st.selectbox(
        "Select Analysis Case",
        list(cases.keys())
    )

    st.session_state.case = cases[selected]

    st.info(selected)

    if st.button(
        "▶️ Start Calculation",
        use_container_width=True
    ):

        start_calculation()

        st.rerun()

    calculation_interface()


# ============================================================
# WELDED ANALYSIS
# ============================================================

def welded_analysis_page():

    st.title("🔥 Welded Connections Analysis")

    if st.button("⬅️ Back"):

        reset_calculation()

        st.session_state.page = "analysis"

        st.rerun()

    st.divider()

    cases = {

        "Case 1 - Design Strength of Fillet Weld":
            "weld_analysis_1",

        "Case 2 - Total Load Capacity of Welded Joint":
            "weld_analysis_2",

        "Case 3 - Eccentric Welded Bracket Connection":
            "weld_analysis_3"
    }

    selected = st.selectbox(
        "Select Analysis Case",
        list(cases.keys())
    )

    st.session_state.case = cases[selected]

    st.info(selected)

    if st.button(
        "▶️ Start Calculation",
        use_container_width=True
    ):

        start_calculation()

        st.rerun()

    calculation_interface()


# ============================================================
# DESIGN PAGE
# ============================================================

def design_page():

    st.title("📐 Design Module")

    if st.button("⬅️ Back to Home"):

        reset_calculation()

        st.session_state.page = "home"

        st.rerun()

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🔩 Bolted Connections Design",
            use_container_width=True
        ):

            reset_calculation()

            st.session_state.page = "bolted_design"

            st.rerun()

    with col2:

        if st.button(
            "🔥 Welded Connections Design",
            use_container_width=True
        ):

            reset_calculation()

            st.session_state.page = "welded_design"

            st.rerun()


# ============================================================
# BOLTED DESIGN
# ============================================================

def bolted_design_page():

    st.title("🔩 Bolted Connections Design")

    if st.button("⬅️ Back"):

        reset_calculation()

        st.session_state.page = "design"

        st.rerun()

    st.divider()

    cases = {

        "Case 1 - Standard Bolted Joint Design (Lap / Butt)":
            "bolt_design_1",

        "Case 2 - Joint with Packing Plate Design":
            "bolt_design_2",

        "Case 3 - HSFG Slip-Critical Connection Design":
            "bolt_design_3"
    }

    selected = st.selectbox(
        "Select Design Case",
        list(cases.keys())
    )

    st.session_state.case = cases[selected]

    st.info(selected)

    if st.button(
        "▶️ Start Design",
        use_container_width=True
    ):

        start_calculation()

        st.rerun()

    calculation_interface()


# ============================================================
# WELDED DESIGN
# ============================================================

def welded_design_page():

    st.title("🔥 Welded Connections Design")

    if st.button("⬅️ Back"):

        reset_calculation()

        st.session_state.page = "design"

        st.rerun()

    st.divider()

    cases = {

        "Case 1 - Fillet Weld Size & Effective Length Layout":
            "weld_design_1",

        "Case 2 - Asymmetrical Angle Connection Design (C.G.)":
            "weld_design_2",

        "Case 3 - Eccentric Welded Bracket Connection Design":
            "weld_design_3"
    }

    selected = st.selectbox(
        "Select Design Case",
        list(cases.keys())
    )

    st.session_state.case = cases[selected]

    st.info(selected)

    if st.button(
        "▶️ Start Design",
        use_container_width=True
    ):

        start_calculation()

        st.rerun()

    calculation_interface()


# ============================================================
# CALCULATION INTERFACE
# ============================================================

def calculation_interface():

    if not st.session_state.calculation_started:

        return

    st.divider()

    if st.session_state.calculation_finished:

        st.success(
            "Calculation completed successfully."
        )

        st.subheader("📋 Results")

        st.code(
            st.session_state.result,
            language="text"
        )

        if st.button(
            "🔄 New Calculation",
            use_container_width=True
        ):

            reset_calculation()

            st.rerun()

        return

    if st.session_state.current_prompt is None:

        return

    st.subheader("📝 Enter Input")

    prompt = st.session_state.current_prompt

    st.write(
        prompt.strip()
    )

    value = st.text_input(
        "Enter value:",
        key=f"input_box_{len(st.session_state.inputs)}"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "➡️ Next",
            use_container_width=True
        ):

            if value.strip() == "":

                st.warning(
                    "Please enter a value."
                )

            else:

                process_input(
                    value.strip()
                )

                st.rerun()

    with col2:

        if st.button(
            "🔄 Restart",
            use_container_width=True
        ):

            reset_calculation()

            st.rerun()

    if len(st.session_state.inputs) > 0:

        st.caption(
            f"Inputs entered: "
            f"{len(st.session_state.inputs)}"
        )


# ============================================================
# ROUTER
# ============================================================

if st.session_state.page == "home":

    home_page()

elif st.session_state.page == "analysis":

    analysis_page()

elif st.session_state.page == "bolted_analysis":

    bolted_analysis_page()

elif st.session_state.page == "welded_analysis":

    welded_analysis_page()

elif st.session_state.page == "design":

    design_page()

elif st.session_state.page == "bolted_design":

    bolted_design_page()

elif st.session_state.page == "welded_design":

    welded_design_page()

else:

    st.session_state.page = "home"

    st.rerun()