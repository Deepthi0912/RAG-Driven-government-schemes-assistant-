
import streamlit as st
import requests
from pathlib import Path

# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="SchemeWise | Government Schemes Assistant",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_URL = "http://127.0.0.1:8000"
HERO_IMAGE = Path(__file__).parent / "assets" / "schemewise_hero.png"

# =========================================================
# 2. SESSION STATE
# =========================================================

defaults = {
    "token": None,
    "user": None,
    "last_response": None,
    "selected_category": None,
    "selected_scheme": None,
    "question_input": "",
    "page": "Home"
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def auth_headers():
    return {
        "Authorization": f"Bearer {st.session_state.token}"
    }


def logout():
    for key in defaults:
        if key == "page":
            st.session_state[key] = "Home"
        else:
            st.session_state[key] = defaults[key]
    st.rerun()


# =========================================================
# 3. SCHEME CATALOGUE
# =========================================================

CATEGORIES = {
    "Housing": {
        "icon": "🏠",
        "color": "#EAF1FF",
        "description": "Housing assistance and rural development",
        "schemes": [
            {
                "name": "PMAY-G",
                "full_name": "Pradhan Mantri Awaas Yojana - Gramin",
                "description": "Rural housing assistance scheme.",
                "category": "Housing"
            }
        ]
    },

    "Agriculture": {
        "icon": "🌾",
        "color": "#EAF5E9",
        "description": "Financial support and welfare for farmers",
        "schemes": [
            {
                "name": "PM-KISAN",
                "full_name": "Pradhan Mantri Kisan Samman Nidhi",
                "description": "Income support scheme for eligible farmer families.",
                "category": "Agriculture"
            }
        ]
    },

    "Women & Child Welfare": {
        "icon": "👩‍👧",
        "color": "#FCEAF2",
        "description": "Support for women, mothers and children",
        "schemes": [
            {
                "name": "PMMVY",
                "full_name": "Pradhan Mantri Matru Vandana Yojana",
                "description": "Maternity benefit scheme.",
                "category": "Women & Child Welfare"
            }
        ]
    },

    "Healthcare": {
        "icon": "🏥",
        "color": "#E7F5F5",
        "description": "Healthcare access and medical support",
        "schemes": []
    },

    "Education": {
        "icon": "🎓",
        "color": "#FFF2DF",
        "description": "Scholarships and educational assistance",
        "schemes": []
    }
}


# =========================================================
# 4. GLOBAL CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #F6F8FC;
}

.block-container {
    max-width: 1350px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

#MainMenu, footer {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    background: transparent;
}

/* BRANDING */

.brand-title {
    color: #153B50;
    font-size: 43px;
    font-weight: 800;
    letter-spacing: -1.8px;
}

.brand-tagline {
    color: #087F83;
    font-size: 19px;
    font-weight: 700;
    margin-top: 5px;
}

.brand-description {
    color: #64748B;
    font-size: 15px;
    line-height: 1.9;
}

/* AUTHENTICATION */

.auth-heading {
    color: #17374B;
    font-size: 30px;
    font-weight: 800;
}

.auth-subtitle {
    color: #718096;
    font-size: 14px;
}

div[data-testid="stForm"] {
    background: white;
    border: 1px solid #E6EAF0;
    border-radius: 16px;
    padding: 20px;
}

.stTextInput label,
.stTextArea label {
    color: #354B60;
    font-weight: 600;
}

.stTextInput input,
.stTextArea textarea {
    border-radius: 10px;
}

/* BUTTONS */

.stButton > button,
.stFormSubmitButton > button {
    border-radius: 10px;
    min-height: 42px;
    font-weight: 700;
    transition: all 0.2s ease;
}

.stButton > button[kind="primary"],
.stFormSubmitButton > button[kind="primary"] {
    background: #087F83;
    color: white;
    border: 1px solid #087F83;
}

.stButton > button[kind="primary"]:hover,
.stFormSubmitButton > button[kind="primary"]:hover {
    background: #06696D;
    border-color: #06696D;
}

/* SIDEBAR */

div[data-testid="stSidebar"] {
    background: #EDF4F5;
}

div[data-testid="stSidebar"] h1,
div[data-testid="stSidebar"] h2,
div[data-testid="stSidebar"] h3 {
    color: #17374B;
}

/* DASHBOARD */

.dashboard-heading {
    font-size: 30px;
    color: #17374B;
    font-weight: 800;
}

.dashboard-subtitle {
    color: #718096;
    font-size: 14px;
}

.category-card {
    background: white;
    border: 1px solid #E5EAF0;
    border-radius: 17px;
    padding: 19px;
    min-height: 145px;
    margin-bottom: 8px;
}

.category-icon {
    font-size: 34px;
}

.category-title {
    color: #17374B;
    font-size: 17px;
    font-weight: 800;
    margin-top: 8px;
}

.category-description {
    color: #718096;
    font-size: 12px;
    line-height: 1.5;
    margin-top: 5px;
}

.scheme-card {
    background: white;
    border: 1px solid #E5EAF0;
    border-radius: 15px;
    padding: 18px;
    margin-bottom: 12px;
}

.scheme-name {
    color: #087F83;
    font-size: 18px;
    font-weight: 800;
}

.scheme-description {
    color: #718096;
    font-size: 13px;
    line-height: 1.6;
}

.info-banner {
    background: #E8F4F4;
    border-radius: 16px;
    padding: 20px;
    color: #176B68;
}

.footer-note {
    color: #82909D;
    text-align: center;
    font-size: 12px;
    padding-top: 30px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# 5. LANDING PAGE
# =========================================================

if not st.session_state.token:

    left, right = st.columns([1.15, 0.85], gap="large")

    with left:

        st.markdown(
            '<div class="brand-title">✦ SchemeWise</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="brand-tagline">'
            'Bridging People with Government Benefits.'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown("""
        <div class="brand-description">
        Discover government schemes, understand eligibility,
        explore benefits and find the support you deserve.

        Your trusted AI-powered guide to Indian government schemes.
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        if HERO_IMAGE.exists():
            st.image(str(HERO_IMAGE), use_container_width=True)
        else:
            st.info(
                "Add schemewise_hero.png to frontend/assets "
                "to display the landing page illustration."
            )

        st.markdown("""
        <div class="info-banner">
        ✨ Discover schemes &nbsp; • &nbsp;
        Understand benefits &nbsp; • &nbsp;
        Get AI-powered guidance
        </div>
        """, unsafe_allow_html=True)

    with right:

        st.markdown("<br><br>", unsafe_allow_html=True)

        st.markdown(
            '<div class="auth-heading">Welcome to SchemeWise</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="auth-subtitle">'
            'Your journey towards discovering government benefits starts here.'
            '</div>',
            unsafe_allow_html=True
        )

        login_tab, register_tab = st.tabs(
            ["Login", "Create Account"]
        )

        # ---------------- LOGIN ----------------

        with login_tab:

            st.markdown("### Welcome back 👋")

            with st.form("login_form"):

                email = st.text_input(
                    "Email address",
                    placeholder="Enter your email"
                )

                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Enter your password"
                )

                login_button = st.form_submit_button(
                    "Login →",
                    type="primary",
                    use_container_width=True
                )

            if login_button:

                if not email.strip() or not password:
                    st.warning("Please enter your email and password.")

                else:

                    try:

                        response = requests.post(
                            f"{BASE_URL}/auth/login",
                            data={
                                "username": email.strip(),
                                "password": password
                            },
                            timeout=20
                        )

                        if response.status_code == 200:

                            token_data = response.json()

                            st.session_state.token = token_data[
                                "access_token"
                            ]

                            user_response = requests.get(
                                f"{BASE_URL}/auth/me",
                                headers=auth_headers(),
                                timeout=20
                            )

                            if user_response.status_code == 200:

                                st.session_state.user = (
                                    user_response.json()
                                )

                                st.success("Welcome to SchemeWise!")
                                st.rerun()

                            else:

                                st.session_state.token = None

                                st.error(
                                    "Could not retrieve account details."
                                )

                        else:
                            st.error("Invalid email or password.")

                    except requests.exceptions.RequestException:
                        st.error(
                            "Cannot connect to backend. "
                            "Check whether FastAPI is running."
                        )

        # ---------------- REGISTRATION ----------------

        with register_tab:

            st.markdown("### Join SchemeWise ✨")

            with st.form("register_form"):

                full_name = st.text_input(
                    "Full name",
                    placeholder="Your full name"
                )

                new_email = st.text_input(
                    "Email address",
                    placeholder="Your email address"
                )

                new_password = st.text_input(
                    "Create password",
                    type="password",
                    placeholder="At least 8 characters"
                )

                register_button = st.form_submit_button(
                    "Create Account →",
                    type="primary",
                    use_container_width=True
                )

            if register_button:

                if (
                    not full_name.strip()
                    or not new_email.strip()
                    or not new_password
                ):

                    st.warning("Please fill in all fields.")

                elif len(new_password) < 8:

                    st.warning(
                        "Password must contain at least 8 characters."
                    )

                else:

                    try:

                        response = requests.post(
                            f"{BASE_URL}/auth/register",
                            json={
                                "full_name": full_name.strip(),
                                "email": new_email.strip(),
                                "password": new_password
                            },
                            timeout=20
                        )

                        if response.status_code in (200, 201):

                            st.success(
                                "Account created successfully! "
                                "Please log in."
                            )

                        else:

                            try:
                                detail = response.json().get(
                                    "detail",
                                    "Registration failed."
                                )
                            except ValueError:
                                detail = "Registration failed."

                            st.error(detail)

                    except requests.exceptions.RequestException:
                        st.error("Cannot connect to backend.")

    st.markdown(
        '<div class="footer-note">'
        '© SchemeWise | Discover. Understand. Benefit.'
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# 6. LOGGED-IN APPLICATION
# =========================================================

else:

    user = st.session_state.user or {}

    # =====================================================
    # SIDEBAR
    # =====================================================

    st.sidebar.markdown("# ✦ SchemeWise")
    st.sidebar.caption("Your government schemes companion")

    st.sidebar.divider()

    st.sidebar.markdown("### 👤 My Profile")

    st.sidebar.write(
        f"**{user.get('full_name', 'User')}**"
    )

    st.sidebar.caption(user.get("email", ""))

    st.sidebar.divider()

    st.sidebar.markdown("### Navigation")

    if st.sidebar.button("🏠 Home", use_container_width=True):
        st.session_state.page = "Home"
        st.session_state.selected_category = None
        st.session_state.selected_scheme = None
        st.rerun()

    if st.sidebar.button("📚 All Categories", use_container_width=True):
        st.session_state.page = "Categories"
        st.session_state.selected_category = None
        st.session_state.selected_scheme = None
        st.rerun()

    if st.sidebar.button("✨ AI Assistant", use_container_width=True):
        st.session_state.page = "AI Assistant"
        st.rerun()

    st.sidebar.divider()

    st.sidebar.markdown("### 🕘 Query History")

    try:

        history_response = requests.get(
            f"{BASE_URL}/api/history",
            headers=auth_headers(),
            timeout=20
        )

        if history_response.status_code == 200:

            history = history_response.json()

            if isinstance(history, dict):
                history = history.get("history", history.get("items", []))

            if history:

                for index, item in enumerate(history):

                    question_text = item.get(
                        "question",
                        "Previous question"
                    )

                    with st.sidebar.expander(
                        question_text[:38],
                        expanded=False
                    ):

                        st.write(item.get("answer", ""))

                        st.caption(
                            f"Query ID: {item.get('id', 'N/A')}"
                        )

            else:
                st.sidebar.caption("No previous questions yet.")

        else:
            st.sidebar.caption("History unavailable.")

    except requests.exceptions.RequestException:
        st.sidebar.caption("Could not load history.")

    st.sidebar.divider()

    if st.sidebar.button("Logout ↗", use_container_width=True):
        logout()

    # =====================================================
    # DASHBOARD HOME
    # =====================================================

    if st.session_state.page in ("Home", "Categories"):

        st.markdown(
            '<div class="dashboard-heading">'
            'Welcome to SchemeWise 👋'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="dashboard-subtitle">'
            'Discover government schemes and find benefits that matter to you.'
            '</div>',
            unsafe_allow_html=True
        )

        st.write("")

        # SEARCH

        search_text = st.text_input(
            "🔎 Search schemes or categories",
            placeholder="Search Housing, Education, PM-KISAN..."
        )

        st.write("")

        # CATEGORY DISPLAY

        st.markdown("## Explore Categories")

        category_names = list(CATEGORIES.keys())

        if search_text.strip():

            search_lower = search_text.lower()

            matching_categories = [
                name for name in category_names
                if search_lower in name.lower()
                or any(
                    search_lower in scheme["name"].lower()
                    or search_lower in scheme["full_name"].lower()
                    for scheme in CATEGORIES[name]["schemes"]
                )
            ]

        else:
            matching_categories = category_names

        if not matching_categories:

            st.info("No matching categories or schemes found.")

        else:

            for start in range(0, len(matching_categories), 3):

                columns = st.columns(3)

                for column, category_name in zip(
                    columns,
                    matching_categories[start:start + 3]
                ):

                    category = CATEGORIES[category_name]

                    with column:

                        st.markdown(
                            f"""
                            <div class="category-card">
                                <div class="category-icon">
                                    {category['icon']}
                                </div>
                                <div class="category-title">
                                    {category_name}
                                </div>
                                <div class="category-description">
                                    {category['description']}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                        if st.button(
                            "Explore Category →",
                            key=f"category_{category_name}",
                            use_container_width=True
                        ):

                            st.session_state.selected_category = (
                                category_name
                            )

                            st.session_state.page = "Category"
                            st.rerun()

        st.divider()

        # SEARCH RESULTS

        if search_text.strip():

            st.markdown("## 🔍 Matching Schemes")

            found = False

            for category_name, category in CATEGORIES.items():

                for scheme in category["schemes"]:

                    matches = (
                        search_text.lower() in scheme["name"].lower()
                        or search_text.lower() in scheme["full_name"].lower()
                    )

                    if matches:

                        found = True

                        st.markdown(
                            f"""
                            <div class="scheme-card">
                                <div class="scheme-name">
                                    {scheme['name']}
                                </div>
                                <b>{scheme['full_name']}</b>
                                <div class="scheme-description">
                                    {scheme['description']}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                        if st.button(
                            f"View {scheme['name']} details →",
                            key=f"search_scheme_{scheme['name']}"
                        ):

                            st.session_state.selected_scheme = scheme
                            st.session_state.page = "Scheme Details"
                            st.rerun()

            if not found:
                st.info(
                    "No matching schemes found in the current catalogue."
                )

        # FEATURED SCHEMES

        else:

            st.markdown("## ⭐ Featured Schemes")

            featured = []

            for category in CATEGORIES.values():
                featured.extend(category["schemes"])

            columns = st.columns(3)

            for index, scheme in enumerate(featured):

                with columns[index % 3]:

                    st.markdown(
                        f"""
                        <div class="scheme-card">
                            <div class="scheme-name">
                                {scheme['name']}
                            </div>
                            <b>{scheme['full_name']}</b>
                            <div class="scheme-description">
                                {scheme['description']}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    if st.button(
                        "Explore Scheme →",
                        key=f"featured_{scheme['name']}",
                        use_container_width=True
                    ):

                        st.session_state.selected_scheme = scheme
                        st.session_state.page = "Scheme Details"
                        st.rerun()

        # QUICK AI ACCESS

        st.write("")

        st.markdown("""
        <div class="info-banner">
            <h3>✨ Need help finding the right scheme?</h3>
            Ask SchemeWise AI about eligibility, benefits,
            documents and application procedures.
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "Ask SchemeWise AI →",
            type="primary"
        ):

            st.session_state.page = "AI Assistant"
            st.rerun()


    # =====================================================
    # CATEGORY PAGE
    # =====================================================

    elif st.session_state.page == "Category":

        category_name = st.session_state.selected_category

        if category_name not in CATEGORIES:

            st.warning("Please select a valid category.")

        else:

            category = CATEGORIES[category_name]

            st.markdown(
                f"## {category['icon']} {category_name}"
            )

            st.caption(category["description"])

            if st.button("← Back to Dashboard"):
                st.session_state.page = "Home"
                st.session_state.selected_category = None
                st.rerun()

            st.divider()

            if category["schemes"]:

                st.markdown("### Available Schemes")

                for scheme in category["schemes"]:

                    st.markdown(
                        f"""
                        <div class="scheme-card">
                            <div class="scheme-name">
                                {scheme['name']}
                            </div>
                            <b>{scheme['full_name']}</b>
                            <div class="scheme-description">
                                {scheme['description']}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    if st.button(
                        "View Scheme Details →",
                        key=f"category_detail_{scheme['name']}"
                    ):

                        st.session_state.selected_scheme = scheme
                        st.session_state.page = "Scheme Details"
                        st.rerun()

            else:

                st.info(
                    "Schemes for this category will appear here "
                    "as official government documents are added "
                    "to the SchemeWise knowledge base."
                )


    # =====================================================
    # INDIVIDUAL SCHEME PAGE
    # =====================================================

    elif st.session_state.page == "Scheme Details":

        scheme = st.session_state.selected_scheme

        if not scheme:

            st.warning("No scheme selected.")

        else:

            st.markdown(f"## 📘 {scheme['name']}")

            st.markdown(
                f"### {scheme['full_name']}"
            )

            st.caption(
                f"Category: {scheme['category']}"
            )

            st.markdown(
                f"""
                <div class="scheme-card">
                    <div class="scheme-description">
                        {scheme['description']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown("### Explore Scheme Information")

            st.write(
                "Ask SchemeWise AI to retrieve detailed information "
                "from the indexed government documents."
            )

            detail_questions = [
                "Explain the scheme and its objectives.",
                "What are the eligibility criteria?",
                "What benefits does the scheme provide?",
                "What documents are required?",
                "How can someone apply for this scheme?"
            ]

            for index, prompt in enumerate(detail_questions):

                if st.button(
                    prompt,
                    key=f"detail_question_{index}",
                    use_container_width=True
                ):

                    st.session_state.question_input = (
                        f"For {scheme['full_name']}: {prompt}"
                    )

                    st.session_state.page = "AI Assistant"
                    st.rerun()

            st.divider()

            if st.button("← Back to Categories"):
                st.session_state.page = "Category"
                st.rerun()


    # =====================================================
    # AI ASSISTANT
    # =====================================================

    elif st.session_state.page == "AI Assistant":

        st.markdown("## ✨ SchemeWise AI Assistant")

        st.caption(
            "Your intelligent companion for government scheme information."
        )

        st.markdown("""
        <div class="info-banner">
            <h3>Namaste! 👋 Welcome to SchemeWise AI.</h3>
            I can help you understand government schemes,
            eligibility criteria, benefits and application procedures.
            <br><br>
            What would you like to know today?
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        with st.form("question_form"):

            question = st.text_area(
                "Ask your question",
                placeholder=(
                    "Example: What are the eligibility criteria "
                    "for PM-KISAN?"
                ),
                height=120,
                max_chars=1000,
                key="question_input"
            )

            ask_button = st.form_submit_button(
                "✨ Get Answer",
                type="primary",
                use_container_width=True
            )

        if ask_button:

            if not question.strip():

                st.warning("Please enter a question.")

            else:

                try:

                    with st.spinner(
                        "Searching government documents and preparing your answer..."
                    ):

                        response = requests.post(
                            f"{BASE_URL}/api/ask",
                            json={
                                "question": question.strip()
                            },
                            headers=auth_headers(),
                            timeout=(10, 180)
                        )

                    if response.status_code == 200:

                        st.session_state.last_response = (
                            response.json()
                        )

                        st.session_state.question_input = ""

                    elif response.status_code == 401:

                        st.error("Your session has expired.")
                        logout()

                    else:

                        st.error(
                            f"Backend error: {response.text}"
                        )

                except requests.exceptions.Timeout:

                    st.error(
                        "The request took too long. Please try again."
                    )

                except requests.exceptions.RequestException:

                    st.error(
                        "Could not connect to the backend."
                    )

        # ---------------------------------------------
        # AI RESPONSE
        # ---------------------------------------------

        result = st.session_state.last_response

        if result:

            st.divider()

            st.markdown("### 💡 SchemeWise Answer")

            st.markdown(
                result.get("answer", "No answer was returned.")
            )

            if result.get("query_id") is not None:

                st.caption(
                    f"Query ID: {result['query_id']}"
                )

            # SOURCE DOCUMENTS

            with st.expander("📚 View Source Documents"):

                sources = result.get("sources", [])

                if sources:

                    for source in sources:

                        st.write(
                            f"📄 **{source.get('source_file', 'Unknown')}**"
                        )

                        st.caption(
                            f"Page: {source.get('page_number', 'N/A')}"
                        )

                else:

                    st.info("No source documents were returned.")

            # PERFORMANCE

            timings = result.get("timings", {})

            if timings:

                with st.expander("⚡ Response Performance"):

                    for name, value in timings.items():

                        st.write(
                            f"**{name.replace('_', ' ').title()}:** "
                            f"{value:.2f} seconds"
                        )

            # FEEDBACK

            st.divider()

            st.markdown("### 💬 Was this answer helpful?")

            with st.form("feedback_form"):

                rating = st.radio(
                    "Rate this answer",
                    ["helpful", "not_helpful"],
                    format_func=lambda value: (
                        "👍 Helpful"
                        if value == "helpful"
                        else "👎 Not Helpful"
                    )
                )

                comment = st.text_area(
                    "Additional comments (optional)"
                )

                feedback_button = st.form_submit_button(
                    "Submit Feedback"
                )

            if feedback_button:

                try:

                    feedback_response = requests.post(
                        f"{BASE_URL}/api/feedback",
                        json={
                            "query_id": result["query_id"],
                            "rating": rating,
                            "comment": comment.strip() or None
                        },
                        headers=auth_headers(),
                        timeout=20
                    )

                    if feedback_response.status_code in (200, 201):

                        st.success(
                            "Thank you! Your feedback was submitted."
                        )

                    else:

                        st.error(
                            f"Could not save feedback: "
                            f"{feedback_response.text}"
                        )

                except requests.exceptions.RequestException:

                    st.error(
                        "Could not connect to the backend."
                    )


# =========================================================
# 7. FOOTER
# =========================================================

st.markdown(
    '<div class="footer-note">'
    'SchemeWise | Discover. Understand. Benefit. '
    '© 2026'
    '</div>',
    unsafe_allow_html=True
)
