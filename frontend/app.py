
import streamlit as st
import requests
import re
from pathlib import Path
from html import escape

# =========================================================
# CONFIGURATION
# =========================================================
import os

BASE_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
ASSETS_DIR = Path(__file__).parent / "assets"
HERO_IMAGE = ASSETS_DIR / "schemewise_hero.png"

st.set_page_config(
    page_title="SchemeWise | Discover. Understand. Benefit.",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# DESIGN SYSTEM
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
    --navy: #172554;
    --blue: #2563eb;
    --muted: #64748b;
    --border: #e8edf5;
    --background: #f7f9fd;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp { background: var(--background); }

.block-container {
    max-width: 1320px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: var(--muted);
}

h1, h2, h3 {
    font-family: 'Manrope', sans-serif;
    color: var(--navy);
    letter-spacing: -0.5px;
}

p { line-height: 1.65; }

.brand {
    font-family: 'Manrope', sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
    letter-spacing: -1.5px;
    color: var(--navy);
}

.brand span { color: var(--blue); }

.eyebrow {
    color: var(--blue);
    font-size: 0.75rem;
    font-weight: 800;
    letter-spacing: 1.7px;
    text-transform: uppercase;
}

.hero {
    background: linear-gradient(120deg, #172554 0%, #1e40af 55%, #2563eb 100%);
    border-radius: 26px;
    padding: 2.5rem;
    color: white;
    overflow: hidden;
    margin-bottom: 2rem;
    box-shadow: 0 16px 35px rgba(37, 99, 235, 0.13);
}

.hero h1 {
    color: white;
    font-size: 2.6rem;
    line-height: 1.2;
    font-weight: 800;
}

.hero p { color: #dbeafe; font-size: 1.02rem; }

.hero-tag {
    display: inline-block;
    padding: 7px 13px;
    background: rgba(255,255,255,0.14);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 30px;
    color: white;
    font-size: 0.78rem;
    margin-bottom: 1rem;
}

.section-title {
    font-family: 'Manrope', sans-serif;
    color: var(--navy);
    font-size: 1.55rem;
    font-weight: 800;
    margin-top: 1.2rem;
    margin-bottom: 0.2rem;
}

.section-subtitle {
    color: var(--muted);
    font-size: 0.92rem;
    margin-bottom: 1.2rem;
}

.category-card {
    min-height: 205px;
    padding: 1.35rem;
    border-radius: 20px;
    border: 1px solid var(--border);
    background: white;
    margin-bottom: 0.65rem;
}

.category-visual {
    width: 62px;
    height: 62px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 18px;
    font-size: 2rem;
    margin-bottom: 1rem;
}

.category-card h3 { font-size: 1.05rem; margin-bottom: 0.3rem; }

.category-card p {
    font-size: 0.82rem;
    color: var(--muted);
    margin-bottom: 0;
}

.scheme-card {
    background: white;
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 1.4rem;
    min-height: 230px;
    margin-bottom: 0.7rem;
}

.scheme-visual { font-size: 2.4rem; margin-bottom: 0.8rem; }
.scheme-card h3 { font-size: 1.08rem; margin-bottom: 0.45rem; }
.scheme-card p { font-size: 0.86rem; color: var(--muted); }

.scheme-tag {
    display: inline-block;
    background: #eff6ff;
    color: #1d4ed8;
    padding: 5px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 700;
    margin-bottom: 0.7rem;
}

.stat-card {
    background: white;
    border: 1px solid var(--border);
    border-radius: 17px;
    padding: 1.1rem;
}

.stat-card strong {
    display: block;
    font-size: 1.55rem;
    color: var(--navy);
}

.stat-card span { font-size: 0.8rem; color: var(--muted); }

.detail-banner {
    background: linear-gradient(120deg, #eaf2ff, #f5f8ff);
    border: 1px solid #dbeafe;
    border-radius: 22px;
    padding: 1.7rem;
    margin-bottom: 1.3rem;
}

.detail-icon { font-size: 3rem; }

.detail-section {
    background: white;
    border: 1px solid var(--border);
    padding: 1.3rem;
    border-radius: 17px;
    margin-bottom: 0.8rem;
}

.chat-user {
    background: #e8f0ff;
    border: 1px solid #dbeafe;
    border-radius: 18px 18px 5px 18px;
    padding: 1rem 1.2rem;
    margin: 1rem 0 1rem 14%;
    color: #172554;
}

.chat-ai {
    background: white;
    border: 1px solid var(--border);
    border-radius: 18px 18px 18px 5px;
    padding: 1rem 1.2rem;
    margin: 1rem 14% 1rem 0;
}

.chat-avatar {
    display: inline-block;
    background: #eff6ff;
    border-radius: 50%;
    padding: 8px;
    margin-right: 8px;
}

.source-box {
    background: #f8fafc;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 0.8rem;
    margin: 0.4rem 0;
    font-size: 0.85rem;
}

.auth-card {
    background: white;
    border: 1px solid var(--border);
    padding: 2rem;
    border-radius: 24px;
    box-shadow: 0 18px 45px rgba(15, 23, 42, 0.07);
    margin-top: 1rem;
}

.auth-heading {
    font-family: 'Manrope', sans-serif;
    color: var(--navy);
    font-size: 1.8rem;
    font-weight: 800;
    margin-bottom: 0.25rem;
}

.auth-description {
    color: var(--muted);
    font-size: 0.9rem;
    margin-bottom: 1.4rem;
}

.auth-divider { margin: 1.5rem 0; border-top: 1px solid var(--border); }

.register-prompt {
    background: linear-gradient(135deg, #f1f6ff, #f8faff);
    border: 1px solid #dce8ff;
    border-radius: 17px;
    padding: 1.25rem;
    margin-top: 1.2rem;
    text-align: center;
}

.register-prompt h4 {
    color: var(--navy);
    font-family: 'Manrope', sans-serif;
    font-size: 1.05rem;
    font-weight: 800;
    margin-bottom: 0.35rem;
}

.register-prompt p {
    color: var(--muted);
    font-size: 0.83rem;
    margin-bottom: 0.8rem;
}

.auth-back {
    text-align: center;
    color: var(--muted);
    font-size: 0.85rem;
    margin-top: 1rem;
}

.auth-note {
    text-align: center;
    color: #94a3b8;
    font-size: 0.78rem;
    padding-top: 1.5rem;
}

.footer {
    text-align: center;
    color: #94a3b8;
    font-size: 0.78rem;
    padding-top: 2rem;
}

.admin-card {
    background: white;
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 1.3rem;
    margin-bottom: 1rem;
}

.admin-label {
    color: #64748b;
    font-size: 0.82rem;
    font-weight: 700;
}

div.stButton > button {
    border-radius: 11px;
    min-height: 2.65rem;
    font-weight: 700;
    border: 1px solid #dbe3ef;
    transition: all 0.2s ease;
}

div.stButton > button:hover {
    border-color: #93b4f8;
    color: #1d4ed8;
}

div.stButton > button[kind="primary"] {
    background: var(--blue);
    border: none;
    color: white;
}

div.stButton > button[kind="primary"]:hover {
    background: #1d4ed8;
    border: none;
    color: white;
}

[data-testid="stForm"] {
    border: 1px solid var(--border);
    border-radius: 16px;
    background: white;
    padding: 1.1rem;
}

[data-testid="stMetric"] {
    background: white;
    padding: 1rem;
    border-radius: 14px;
    border: 1px solid var(--border);
}

hr { border-color: var(--border); }

div[data-baseweb="input"], div[data-baseweb="select"] {
    border-radius: 10px;
}

@media (max-width: 768px) {
    .hero { padding: 1.5rem; }
    .hero h1 { font-size: 2rem; }
    .auth-card { padding: 1.3rem; }
    .brand { font-size: 2rem; }
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# SESSION STATE
# =========================================================

DEFAULTS = {
    "token": None,
    "user": None,
    "page": "Home",
    "chat_messages": [],
    "selected_scheme": None,
    "selected_category": "All",
    "history_data": [],
    "auth_mode": "login",
    "saved_scheme_ids": [],
    "saved_schemes_loaded": False,
    "categories_data": [],
    "schemes_data": [],
    "catalogue_loaded": False
    
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

# =========================================================
# API FUNCTIONS
# =========================================================

def auth_headers():
    if st.session_state.token:
        return {"Authorization": f"Bearer {st.session_state.token}"}
    return {}


def api_get(endpoint):
    try:
        response = requests.get(
            BASE_URL + endpoint,
            headers=auth_headers(),
            timeout=30
        )
        response.raise_for_status()
        return response.json()

    except requests.RequestException as error:
        st.error(f"Could not connect to the backend: {error}")
        return None


def api_post(endpoint, payload=None, form_data=None, authenticated=False):
    try:
        headers = auth_headers() if authenticated else {}

        response = requests.post(
            BASE_URL + endpoint,
            json=payload,
            data=form_data,
            headers=headers,
            timeout=120
        )

        response.raise_for_status()
        return response.json() if response.content else {}

    except requests.RequestException as error:
        detail = str(error)

        if getattr(error, "response", None) is not None:
            try:
                detail = error.response.json().get("detail", detail)
            except Exception:
                pass

        st.error(f"Request failed: {detail}")
        return None


def api_delete(endpoint, authenticated=True):
    try:
        response = requests.delete(
            BASE_URL + endpoint,
            headers=auth_headers() if authenticated else {},
            timeout=30
        )

        response.raise_for_status()
        return response.json() if response.content else {}

    except requests.RequestException as error:
        detail = str(error)

        if getattr(error, "response", None) is not None:
            try:
                detail = error.response.json().get("detail", detail)
            except Exception:
                pass

        st.error(f"Request failed: {detail}")
        return None


def api_upload_document(endpoint, uploaded_file):
    try:
        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                uploaded_file.type or "application/pdf"
            )
        }

        response = requests.post(
            BASE_URL + endpoint,
            files=files,
            headers=auth_headers(),
            timeout=180
        )

        response.raise_for_status()
        return response.json() if response.content else {}

    except requests.RequestException as error:
        detail = str(error)

        if getattr(error, "response", None) is not None:
            try:
                detail = error.response.json().get("detail", detail)
            except Exception:
                pass

        st.error(f"Document upload failed: {detail}")
        return None


def ask_question(question):
    return api_post(
        "/api/ask",
        payload={"question": question},
        authenticated=True
    )


def load_history():
    data = api_get("/api/history")

    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        return data.get("history", data.get("items", []))

    return []


def extract_list(data, possible_keys):
    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        for key in possible_keys:
            if isinstance(data.get(key), list):
                return data[key]

    return []


# =========================================================
# DYNAMIC DATABASE CATALOGUE
# =========================================================

CATEGORY_VISUALS = {
    "housing": ("🏡", "🏠", "#eff6ff"),
    "agriculture": ("🌾", "🚜", "#f0fdf4"),
    "women & child welfare": ("👩", "🤱", "#fdf2f8"),
    "women and child welfare": ("👩", "🤱", "#fdf2f8"),
    "healthcare": ("🏥", "🩺", "#fff7ed"),
    "education": ("🎓", "📚", "#f5f3ff")
}


def get_category_visual(category_name):
    key = str(category_name).strip().lower()

    if key in CATEGORY_VISUALS:
        return CATEGORY_VISUALS[key]

    return ("📂", "📁", "#eff6ff")


def generate_scheme_code(name):
    """
    Creates a stable string code for saved schemes.

    Known schemes retain their original codes.
    Other database schemes receive a code generated from their name.
    """

    text = str(name).strip().upper()

    if "PM-KISAN" in text or "KISAN SAMMAN NIDHI" in text:
        return "PM-KISAN"

    if "PMAY-G" in text or (
        "AWAAS YOJANA" in text and "GRAMIN" in text
    ):
        return "PMAY-G"

    if "PMMVY" in text or "MATRU VANDANA" in text:
        return "PMMVY"

    code = re.sub(r"[^A-Z0-9]+", "-", text).strip("-")
    return code[:50] or "SCHEME"


def get_scheme_visual(scheme_name, category_name):
    code = generate_scheme_code(scheme_name)

    if code == "PM-KISAN":
        return "🌾", "#dcfce7"

    if code == "PMAY-G":
        return "🏠", "#dbeafe"

    if code == "PMMVY":
        return "🤱", "#fce7f3"

    _, visual, color = get_category_visual(category_name)
    return visual, color


def load_public_catalogue(force=False):
    """
    Fetches categories and schemes directly from PostgreSQL
    through the FastAPI endpoints.
    """

    if st.session_state.catalogue_loaded and not force:
        return

    try:
        category_response = requests.get(
            BASE_URL + "/categories",
            timeout=30
        )
        category_response.raise_for_status()

        scheme_response = requests.get(
            BASE_URL + "/schemes",
            timeout=30
        )
        scheme_response.raise_for_status()

        categories = extract_list(
            category_response.json(),
            ["categories", "items", "data"]
        )

        schemes = extract_list(
            scheme_response.json(),
            ["schemes", "items", "data"]
        )

        st.session_state.categories_data = categories
        st.session_state.schemes_data = schemes
        st.session_state.catalogue_loaded = True

    except requests.RequestException as error:
        st.error(
            f"Unable to load the government scheme catalogue: {error}"
        )


def refresh_public_catalogue():
    st.session_state.catalogue_loaded = False
    load_public_catalogue(force=True)


def get_dynamic_categories():
    result = []

    for category in st.session_state.categories_data:
        if not isinstance(category, dict):
            continue

        name = category.get("name")

        if not name:
            continue

        icon, visual, color = get_category_visual(name)

        result.append({
            "id": category.get("id"),
            "name": name,
            "description": category.get("description") or
                           "Explore government schemes in this category.",
            "icon": icon,
            "visual": visual,
            "color": color
        })

    return result


def get_dynamic_schemes():
    categories_by_id = {
        item.get("id"): item.get("name")
        for item in st.session_state.categories_data
        if isinstance(item, dict)
    }

    result = {}

    for item in st.session_state.schemes_data:
        if not isinstance(item, dict):
            continue

        name = item.get("name")

        if not name:
            continue

        category_name = categories_by_id.get(
            item.get("category_id"),
            "Other"
        )

        code = generate_scheme_code(name)
        icon, color = get_scheme_visual(name, category_name)

        result[code] = {
            "id": item.get("id"),
            "code": code,
            "name": name,
            "short_name": code,
            "category": category_name,
            "icon": icon,
            "color": color,
            "description": item.get("description") or
                           "More information about this scheme will be available soon.",
            "ministry": item.get("ministry"),
            "official_url": item.get("official_url"),
            "questions": {
                "Overview": (
                    f"Explain the overview and objectives of {name} "
                    "based on the official indexed documents."
                ),
                "Eligibility": (
                    f"Explain the eligibility criteria and exclusions "
                    f"for {name} based on the official indexed documents."
                ),
                "Benefits": (
                    f"Explain the financial assistance and benefits "
                    f"available under {name} based on the official indexed documents."
                ),
                "Documents": (
                    f"Explain the documents required for {name} "
                    "based on the official indexed documents."
                ),
                "Application Process": (
                    f"Explain the application and registration process "
                    f"for {name} based on the official indexed documents."
                )
            }
        }

    return result


def load_categories_from_backend(show_error=True):
    try:
        response = requests.get(
            BASE_URL + "/categories",
            headers=auth_headers(),
            timeout=30
        )
        response.raise_for_status()

        return extract_list(
            response.json(),
            ["categories", "items", "data"]
        )

    except requests.RequestException as error:
        if show_error:
            st.error(f"Could not load categories: {error}")
        return []


def load_admin_schemes():
    data = api_get("/schemes")
    return extract_list(data, ["schemes", "items", "data"])


def load_admin_documents():
    data = api_get("/documents")
    return extract_list(data, ["documents", "items", "data"])


# =========================================================
# SAVED SCHEMES
# =========================================================

def load_saved_schemes():
    data = api_get("/api/saved-schemes/")

    if data is None:
        return False

    saved_items = data.get("saved_schemes", [])

    st.session_state.saved_scheme_ids = [
        str(item["scheme_id"]).upper()
        for item in saved_items
        if isinstance(item, dict) and item.get("scheme_id")
    ]

    st.session_state.saved_schemes_loaded = True
    return True


def save_scheme(scheme_id):
    result = api_post(
        "/api/saved-schemes/",
        payload={"scheme_id": scheme_id},
        authenticated=True
    )

    if result is not None:
        if scheme_id not in st.session_state.saved_scheme_ids:
            st.session_state.saved_scheme_ids.append(scheme_id)

        st.success(f"❤️ {scheme_id} added to your saved schemes!")
        st.rerun()


def remove_saved_scheme(scheme_id):
    result = api_delete(f"/api/saved-schemes/{scheme_id}")

    if result is not None:
        st.session_state.saved_scheme_ids = [
            item for item in st.session_state.saved_scheme_ids
            if item != scheme_id
        ]

        st.success(f"{scheme_id} removed from your saved schemes.")
        st.rerun()


def render_save_button(scheme_id, key):
    is_saved = scheme_id in st.session_state.saved_scheme_ids

    if is_saved:
        if st.button(
            "❤️ Saved",
            key=key,
            use_container_width=True
        ):
            remove_saved_scheme(scheme_id)
    else:
        if st.button(
            "🤍 Save scheme",
            key=key,
            use_container_width=True
        ):
            save_scheme(scheme_id)


def get_user_name():
    user = st.session_state.user or {}

    return (
        user.get("full_name")
        or user.get("name")
        or user.get("email")
        or "User"
    )


# =========================================================
# REUSABLE UI FUNCTIONS
# =========================================================

def section_heading(title, subtitle=None):
    st.markdown(
        f'<div class="section-title">{title}</div>',
        unsafe_allow_html=True
    )

    if subtitle:
        st.markdown(
            f'<div class="section-subtitle">{subtitle}</div>',
            unsafe_allow_html=True
        )


def display_sources(sources):
    if not sources:
        st.caption("No source documents were returned.")
        return

    with st.expander("📚 View official source documents"):
        for source in sources:
            if isinstance(source, dict):
                filename = escape(
                    str(source.get("source_file", "Document"))
                )
                page = source.get("page_number")

                if page is not None:
                    st.markdown(
                        f'<div class="source-box">📄 <b>{filename}</b> · Page {page}</div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f'<div class="source-box">📄 <b>{filename}</b></div>',
                        unsafe_allow_html=True
                    )
            else:
                st.markdown(f"- {source}")


def display_timings(data):
    timings = data.get("timings") if isinstance(data, dict) else None

    if timings:
        with st.expander("⏱️ Response details"):
            st.json(timings)



def submit_feedback(query_id, rating, comment):

    payload = {
        "query_id": query_id,
        "rating": rating,
        "comment": comment
    }

    result = api_post(
        "/api/feedback",
        payload=payload,
        authenticated=True
    )

    if result:
        st.success("Thank you! Your feedback has been submitted.")




def render_feedback(query_id, suffix):
    if not query_id:
        return

    with st.expander("💬 Rate this answer"):

        rating = st.radio(
            "Was this answer helpful?",
            [5, 4, 3, 2, 1],
            format_func=lambda x: {
                5: "⭐⭐⭐⭐⭐ Excellent",
                4: "⭐⭐⭐⭐ Good",
                3: "⭐⭐⭐ Average",
                2: "⭐⭐ Needs improvement",
                1: "⭐ Not helpful"
            }[x],
            key=f"rating_{suffix}"
        )

        comment = st.text_area(
            "Additional comments (optional)",
            key=f"comment_{suffix}"
        )

        if st.button(
            "Submit feedback",
            key=f"feedback_{suffix}"
        ):

            # Convert five-star rating to backend-supported values
            feedback_rating = (
                "helpful" if rating >= 4 else "not_helpful"
            )

            submit_feedback(
                query_id,
                feedback_rating,
                comment
            )

# =========================================================
# AUTHENTICATION
# =========================================================

def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

    st.rerun()


def show_landing():
    left, right = st.columns([1.15, 0.85], gap="large")

    with left:
        st.markdown(
            '<div class="brand">Scheme<span>Wise</span></div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="eyebrow">DISCOVER · UNDERSTAND · BENEFIT</div>',
            unsafe_allow_html=True
        )

        st.markdown("## Government schemes, made simpler.")

        st.write(
            "A smarter way to discover government welfare schemes, "
            "understand eligibility and find the information that matters."
        )

        if HERO_IMAGE.exists():
            st.image(str(HERO_IMAGE), use_container_width=True)
        else:
            st.markdown("""
            <div class="hero">
                <h1>Discover the support available to you.</h1>
                <p>Explore government schemes with the help of AI.</p>
                <div style="font-size:60px;">🏠 🌾 👩‍👧 🎓 🏥</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("### Everything you need, in one place")

        features = [
            ("🔎", "Discover schemes", "Browse schemes by category."),
            ("📋", "Understand eligibility", "Explore benefits and requirements."),
            ("🤖", "Ask AI", "Get answers from indexed documents.")
        ]

        for icon, title, description in features:
            st.markdown(f"**{icon} {title}**")
            st.caption(description)

    with right:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)

        if st.session_state.auth_mode == "login":
            st.markdown(
                '<div class="auth-heading">Welcome to SchemeWise 👋</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="auth-description">'
                'Sign in to explore government schemes and discover benefits.'
                '</div>',
                unsafe_allow_html=True
            )

            st.markdown("#### 🔐 Sign in to your account")

            with st.form("login_form"):
                email = st.text_input(
                    "Email address",
                    placeholder="Enter your email address"
                )

                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Enter your password"
                )

                submitted = st.form_submit_button(
                    "Sign In  →",
                    type="primary",
                    use_container_width=True
                )

                if submitted:
                    if not email or not password:
                        st.warning("Please enter your email and password.")
                    else:
                        with st.spinner("Signing you in..."):
                            result = api_post(
                                "/auth/login",
                                form_data={
                                    "username": email,
                                    "password": password
                                }
                            )

                        if result and result.get("access_token"):
                            st.session_state.token = result["access_token"]

                            user = api_get("/auth/me")
                            st.session_state.user = user or {"email": email}

                            st.session_state.saved_schemes_loaded = False
                            st.session_state.catalogue_loaded = False

                            load_saved_schemes()

                            st.session_state.page = "Home"
                            st.rerun()

            st.markdown(
                '<div class="auth-divider"></div>'
                '<div class="register-prompt">'
                '<h4>✨ New to SchemeWise?</h4>'
                '<p>Create your free account and start discovering '
                'government welfare schemes.</p>'
                '</div>',
                unsafe_allow_html=True
            )

            if st.button(
                "📝  Register Here  →",
                key="open_register",
                use_container_width=True,
                type="primary"
            ):
                st.session_state.auth_mode = "register"
                st.rerun()

        else:
            st.markdown(
                '<div class="auth-heading">Create Your Account ✨</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="auth-description">'
                'Join SchemeWise and make discovering government benefits easier.'
                '</div>',
                unsafe_allow_html=True
            )

            st.markdown("#### 📝 Register with SchemeWise")

            with st.form("register_form"):
                full_name = st.text_input(
                    "Full name",
                    placeholder="Enter your full name"
                )

                reg_email = st.text_input(
                    "Email address",
                    placeholder="Enter your email address"
                )

                reg_password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Create a password"
                )

                confirm_password = st.text_input(
                    "Confirm password",
                    type="password",
                    placeholder="Re-enter your password"
                )

                submitted = st.form_submit_button(
                    "Create My Account  →",
                    type="primary",
                    use_container_width=True
                )

                if submitted:
                    if not full_name.strip() or not reg_email.strip() or not reg_password:
                        st.warning("Please complete all required fields.")
                    elif reg_password != confirm_password:
                        st.error("Passwords do not match.")
                    else:
                        with st.spinner("Creating your account..."):
                            result = api_post(
                                "/auth/register",
                                payload={
                                    "full_name": full_name.strip(),
                                    "email": reg_email.strip(),
                                    "password": reg_password
                                }
                            )

                        if result is not None:
                            st.success(
                                "🎉 Account created successfully! "
                                "You can now sign in."
                            )
                            st.session_state.auth_mode = "login"
                            st.rerun()

            st.markdown(
                '<div class="auth-back">Already have an account?</div>',
                unsafe_allow_html=True
            )

            if st.button(
                "← Back to Sign In",
                key="back_to_login",
                use_container_width=True
            ):
                st.session_state.auth_mode = "login"
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            '<div class="auth-note">'
            '🇮🇳 Your guide to government welfare schemes'
            '<br>Discover. Understand. Benefit.'
            '</div>',
            unsafe_allow_html=True
        )


# =========================================================
# SIDEBAR
# =========================================================

def show_sidebar():
    with st.sidebar:
        st.markdown(
            '<div class="brand" style="font-size:1.8rem;">Scheme<span>Wise</span></div>',
            unsafe_allow_html=True
        )

        st.caption("Your government schemes companion")
        st.divider()

        st.markdown(f"### 👋 Hello, {escape(str(get_user_name()))}")
        st.caption("Navigate your workspace")

        pages = [
            ("🏡", "Home"),
            ("🗂️", "Explore Schemes"),
            ("❤️", "Saved Schemes"),
            ("🤖", "AI Assistant"),
            ("📚", "My History"),
            ("👤", "My Profile")
        ]

        if is_admin():
            pages.append(("🛠️", "Admin Dashboard"))

        for icon, page in pages:
            if st.button(
                f"{icon}  {page}",
                key=f"nav_{page}",
                use_container_width=True,
                type="primary" if st.session_state.page == page else "secondary"
            ):
                st.session_state.page = page
                st.rerun()

        st.divider()

        st.markdown("**✨ SchemeWise AI**")
        st.caption("Information supported by indexed scheme documents.")

        if is_admin():
            st.success("Administrator access")

        if st.button("↪ Logout", use_container_width=True):
            logout()


def is_admin():
    user = st.session_state.user or {}
    return str(user.get("role", "")).lower() == "admin"


# =========================================================
# HOME DASHBOARD
# =========================================================

def show_home():
    categories = get_dynamic_categories()
    schemes = get_dynamic_schemes()

    st.markdown("""
    <div class="hero">
        <div class="hero-tag">🇮🇳 YOUR GOVERNMENT SCHEMES COMPANION</div>
        <h1>Find the support.<br>Understand your benefits.</h1>
        <p>
            Explore welfare schemes, discover eligibility and get
            reliable answers with your AI-powered assistant.
        </p>
    </div>
    """, unsafe_allow_html=True)

    section_heading(
        "🌈 Explore by category",
        "Find schemes based on the area of support you are looking for."
    )

    if not categories:
        st.info(
            "No categories are available yet. "
            "Please check the Admin Dashboard or add categories to the database."
        )
    else:
        for row_start in range(0, len(categories), 3):
            cols = st.columns(3)

            for col_index, category in enumerate(
                categories[row_start:row_start + 3]
            ):
                with cols[col_index]:
                    st.markdown(
                        f"""
                        <div class="category-card">
                            <div class="category-visual"
                                 style="background:{category['color']};">
                                {category['visual']}
                            </div>
                            <h3>{escape(category['name'])}</h3>
                            <p>{escape(category['description'])}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    if st.button(
                        "Explore category →",
                        key=f"home_category_{category['id']}",
                        use_container_width=True
                    ):
                        st.session_state.selected_category = category["name"]
                        st.session_state.page = "Explore Schemes"
                        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    section_heading(
        "⭐ Featured government schemes",
        "Explore schemes and save the ones you want to revisit."
    )

    scheme_items = list(schemes.items())[:3]

    if not scheme_items:
        st.info("No government schemes have been added to the catalogue yet.")
    else:
        cols = st.columns(3)

        for index, (scheme_code, scheme) in enumerate(scheme_items):
            with cols[index]:
                st.markdown(
                    f"""
                    <div class="scheme-card">
                        <div class="scheme-visual">{scheme['icon']}</div>
                        <div class="scheme-tag">{escape(scheme['category'])}</div>
                        <h3>{escape(scheme['short_name'])}</h3>
                        <p><b>{escape(scheme['name'])}</b></p>
                        <p>{escape(scheme['description'])}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                render_save_button(
                    scheme_code,
                    f"home_save_{scheme_code}"
                )

                if st.button(
                    "Explore scheme →",
                    key=f"home_scheme_{scheme_code}",
                    use_container_width=True
                ):
                    st.session_state.selected_scheme = scheme_code
                    st.session_state.page = "Scheme Details"
                    st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="detail-banner">
        <div class="eyebrow">💡 HAVE A QUESTION?</div>
        <h2>Let SchemeWise help you.</h2>
        <p>
            Ask about eligibility, benefits, documents or application
            procedures and get answers from indexed scheme documents.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("💬 Start a conversation with AI", type="primary"):
        st.session_state.page = "AI Assistant"
        st.rerun()


# =========================================================
# EXPLORE SCHEMES
# =========================================================

def show_explore():
    schemes = get_dynamic_schemes()
    categories = get_dynamic_categories()

    st.markdown("## 🗂️ Explore Government Schemes")
    st.caption("Browse schemes and save your favourites for later.")

    col1, col2 = st.columns([4, 1])

    with col1:
        search = st.text_input(
            "🔎 Search for a scheme",
            placeholder="Try PMAY-G, farmer support, maternity..."
        )

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("↻ Refresh", use_container_width=True):
            refresh_public_catalogue()
            st.rerun()

    category_options = ["All"] + [
        item["name"] for item in categories
    ]

    current = st.session_state.selected_category

    if current not in category_options:
        current = "All"

    category = st.selectbox(
        "Choose a category",
        category_options,
        index=category_options.index(current)
    )

    st.session_state.selected_category = category

    filtered = []

    for scheme_code, scheme in schemes.items():
        if category != "All" and scheme["category"] != category:
            continue

        search_text = (
            scheme["name"] + " " +
            scheme["short_name"] + " " +
            scheme["category"] + " " +
            scheme["description"]
        ).lower()

        if search and search.lower() not in search_text:
            continue

        filtered.append((scheme_code, scheme))

    st.caption(f"📋 {len(filtered)} scheme(s) found")

    if not filtered:
        st.info(
            "No matching schemes are currently listed. "
            "Additional schemes will appear here when added through "
            "the Admin Dashboard."
        )
        return

    for row_start in range(0, len(filtered), 2):
        cols = st.columns(2)

        for col_index, (scheme_code, scheme) in enumerate(
            filtered[row_start:row_start + 2]
        ):
            with cols[col_index]:
                st.markdown(
                    f"""
                    <div class="scheme-card">
                        <div class="scheme-visual">{scheme['icon']}</div>
                        <div class="scheme-tag">{escape(scheme['category'])}</div>
                        <h3>{escape(scheme['name'])}</h3>
                        <p>{escape(scheme['description'])}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                render_save_button(
                    scheme_code,
                    f"explore_save_{scheme_code}"
                )

                if st.button(
                    f"View {scheme_code} details →",
                    key=f"explore_{scheme_code}",
                    use_container_width=True
                ):
                    st.session_state.selected_scheme = scheme_code
                    st.session_state.page = "Scheme Details"
                    st.rerun()


# =========================================================
# SAVED SCHEMES
# =========================================================

def show_saved_schemes():
    schemes = get_dynamic_schemes()

    st.markdown("## ❤️ My Saved Schemes")

    st.caption(
        "Your personal collection of government schemes, "
        "saved for easy access whenever you need them."
    )

    if st.button("↻ Refresh saved schemes"):
        if load_saved_schemes():
            st.rerun()

    if not st.session_state.saved_schemes_loaded:
        with st.spinner("Loading your saved schemes..."):
            if not load_saved_schemes():
                return

    saved_ids = st.session_state.saved_scheme_ids

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.metric("❤️ Saved schemes", len(saved_ids))

    with col2:
        st.metric("📂 Available schemes", len(schemes))

    st.divider()

    if not saved_ids:
        st.markdown("""
        <div class="detail-banner">
            <div style="font-size:48px;">🤍</div>
            <h2>Your saved list is waiting!</h2>
            <p>
                You haven't saved any schemes yet.
                Explore government schemes and tap
                <b>Save scheme</b> to add them here.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🗂️ Explore Government Schemes", type="primary"):
            st.session_state.page = "Explore Schemes"
            st.rerun()

        return

    section_heading(
        "Your favourites",
        f"You have saved {len(saved_ids)} scheme(s)."
    )

    known_saved_ids = [
        scheme_code for scheme_code in saved_ids
        if scheme_code in schemes
    ]

    unknown_saved_ids = [
        scheme_code for scheme_code in saved_ids
        if scheme_code not in schemes
    ]

    for row_start in range(0, len(known_saved_ids), 2):
        cols = st.columns(2)

        for col_index, scheme_code in enumerate(
            known_saved_ids[row_start:row_start + 2]
        ):
            scheme = schemes[scheme_code]

            with cols[col_index]:
                st.markdown(
                    f"""
                    <div class="scheme-card">
                        <div class="scheme-visual">{scheme['icon']}</div>
                        <div class="scheme-tag">{escape(scheme['category'])}</div>
                        <h3>{escape(scheme['name'])}</h3>
                        <p>{escape(scheme['description'])}</p>
                        <p><b>Scheme code:</b> {escape(scheme_code)}</p>
                        <p style="color:#db2777;font-weight:700;">
                            ❤️ Saved to your collection
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                col_a, col_b = st.columns(2)

                with col_a:
                    if st.button(
                        "View details →",
                        key=f"saved_view_{scheme_code}",
                        use_container_width=True,
                        type="primary"
                    ):
                        st.session_state.selected_scheme = scheme_code
                        st.session_state.page = "Scheme Details"
                        st.rerun()

                with col_b:
                    if st.button(
                        "Remove ❤️",
                        key=f"saved_remove_{scheme_code}",
                        use_container_width=True
                    ):
                        remove_saved_scheme(scheme_code)

    if unknown_saved_ids:
        st.warning(
            "Some saved scheme codes are not present in the current "
            "database catalogue: " + ", ".join(unknown_saved_ids)
        )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("➕ Discover more schemes"):
        st.session_state.page = "Explore Schemes"
        st.rerun()


# =========================================================
# SCHEME DETAILS
# =========================================================

def show_scheme_details():
    schemes = get_dynamic_schemes()
    scheme_code = st.session_state.selected_scheme

    if scheme_code not in schemes:
        st.warning(
            "This scheme is not available in the current database catalogue."
        )

        if st.button("← Back to Explore Schemes"):
            st.session_state.page = "Explore Schemes"
            st.rerun()

        return

    scheme = schemes[scheme_code]

    if st.button("← Back to Explore Schemes"):
        st.session_state.page = "Explore Schemes"
        st.rerun()

    st.markdown(
        f"""
        <div class="detail-banner">
            <div class="detail-icon">{scheme['icon']}</div>
            <div class="eyebrow">{escape(scheme['category'])}</div>
            <h1>{escape(scheme['name'])}</h1>
            <p>{escape(scheme['description'])}</p>
            <div class="scheme-tag">{escape(scheme_code)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if scheme.get("ministry"):
        st.markdown(f"**Ministry:** {escape(str(scheme['ministry']))}")

    if scheme.get("official_url"):
        st.markdown(
            f"[🌐 Visit official website]({scheme['official_url']})"
        )

    render_save_button(
        scheme_code,
        f"details_save_{scheme_code}"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    section_heading(
        "📖 Understand this scheme",
        "Choose a section to retrieve information from official indexed documents."
    )

    section_icons = {
        "Overview": "📖",
        "Eligibility": "✅",
        "Benefits": "🎁",
        "Documents": "📄",
        "Application Process": "📝"
    }

    sections = list(scheme["questions"].keys())

    selected_section = st.selectbox(
        "What would you like to know?",
        sections,
        format_func=lambda x: f"{section_icons.get(x, '📌')}  {x}"
    )

    if st.button(
        f"Get {selected_section} information →",
        type="primary",
        use_container_width=True
    ):
        question = (
            f"Regarding the government scheme {scheme['name']} "
            f"({scheme_code}): {scheme['questions'][selected_section]}"
        )

        with st.spinner("Searching official scheme documents..."):
            result = ask_question(question)

        if result:
            st.markdown(
                f'<div class="detail-section"><h3>{section_icons.get(selected_section, "📌")} {selected_section}</h3></div>',
                unsafe_allow_html=True
            )

            st.markdown(result.get("answer", "No answer returned."))
            display_sources(result.get("sources", []))
            display_timings(result)

            render_feedback(
                result.get("query_id"),
                f"scheme_{scheme_code}_{selected_section}".replace(" ", "_")
            )

    st.divider()

    section_heading(
        "💬 Still have questions?",
        f"Ask a specific question about {scheme_code}."
    )

    custom_question = st.text_input(
        "Your question",
        placeholder=f"Ask anything about {scheme_code}..."
    )

    if st.button("Ask SchemeWise AI →", key=f"custom_{scheme_code}"):
        if not custom_question.strip():
            st.warning("Enter your question first.")
        else:
            with st.spinner("Finding the answer..."):
                result = ask_question(
                    f"Regarding government scheme {scheme['name']} "
                    f"({scheme_code}): {custom_question}"
                )

            if result:
                st.markdown("### 🤖 AI response")
                st.markdown(result.get("answer", "No answer returned."))

                display_sources(result.get("sources", []))
                display_timings(result)

                render_feedback(
                    result.get("query_id"),
                    f"custom_{scheme_code}"
                )


# =========================================================
# AI ASSISTANT
# =========================================================


def show_assistant():
    st.markdown("## 🤖 SchemeWise AI Assistant")
    st.caption(
        "Your conversational assistant for government scheme information."
    )

    st.markdown("""
    <div class="detail-banner">
        <h3>👋 Hello! How can I help you today?</h3>
        <p>
            Ask about scheme eligibility, benefits, required documents
            or application procedures. Answers are retrieved from
            the documents indexed in SchemeWise.
        </p>
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns([4, 1])

    with left:
        st.markdown("### 💬 Conversation")

    with right:
        if st.button("🗑️ Clear chat"):
            st.session_state.chat_messages = []
            st.session_state.chat_question = ""
            st.rerun()

    # Suggested questions
    if not st.session_state.chat_messages:
        st.markdown("**✨ Suggested questions**")

        suggestions = [
            "Who is eligible for PM-KISAN?",
            "Explain PM-KISAN benefits.",
            "What documents are required for PM-KISAN?",
            "How can I apply for PM-KISAN?"
        ]

        cols = st.columns(2)

        for index, suggestion in enumerate(suggestions):
            with cols[index % 2]:
                if st.button(
                    suggestion,
                    key=f"suggest_{index}",
                    use_container_width=True
                ):
                    st.session_state.chat_question = suggestion
                    st.session_state.pending_question = True
                    st.rerun()

    # Display previous messages
    for index, message in enumerate(st.session_state.chat_messages):

        if message["role"] == "user":
            st.markdown(
                f'<div class="chat-user"><b>You</b><br>'
                f'{escape(message["content"])}</div>',
                unsafe_allow_html=True
            )

        else:
            st.markdown(
                '<div class="chat-ai">'
                '<span class="chat-avatar">🤖</span>'
                '<b>SchemeWise AI</b></div>',
                unsafe_allow_html=True
            )

            st.markdown(message["content"])
            display_sources(message.get("sources", []))

            if message.get("timings"):
                display_timings({
                    "timings": message["timings"]
                })

            render_feedback(
                message.get("query_id"),
                f"chat_{index}"
            )

    # Question input
    with st.form("chat_form", clear_on_submit=True):

        question = st.text_area(
            "Type your question",
            placeholder="For example: What are the benefits of PM-KISAN?",
            height=90,
            key="chat_question"
        )

        submitted = st.form_submit_button(
            "Send message  ➤",
            type="primary",
            use_container_width=True
        )

    if submitted:

        # Read the submitted value from Streamlit session state
        user_question = st.session_state.get(
            "chat_question", ""
        ).strip()

        if not user_question:
            st.warning("Please type a question.")
            return

        # Save the user's question
        st.session_state.chat_messages.append({
            "role": "user",
            "content": user_question
        })

        # Ask the backend
        with st.spinner("SchemeWise is thinking..."):

            result = ask_question(user_question)

        if result:

            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": result.get(
                    "answer",
                    "No answer returned."
                ),
                "sources": result.get("sources", []),
                "query_id": result.get("query_id"),
                "timings": result.get("timings")
            })

        st.rerun()


# =========================================================
# HISTORY
# =========================================================

def show_history():
    st.markdown("## 📚 My Query History")
    st.caption("Revisit the questions you have asked SchemeWise.")

    if st.button("↻ Refresh history"):
        st.session_state.history_data = load_history()

    if not st.session_state.history_data:
        st.session_state.history_data = load_history()

    history = st.session_state.history_data

    if not history:
        st.info("Your previous questions will appear here.")
        return

    for index, item in enumerate(history):
        if not isinstance(item, dict):
            continue

        question = (
            item.get("question")
            or item.get("query")
            or "Previous question"
        )

        answer = item.get("answer", "Answer not available.")

        with st.expander(f"💬 {question}"):
            st.markdown("**🤖 SchemeWise response**")
            st.write(answer)

            if item.get("sources"):
                display_sources(item["sources"])


# =========================================================
# PROFILE
# =========================================================

def show_profile():
    user = st.session_state.user or {}

    st.markdown("## 👤 My Profile")
    st.caption("Manage your SchemeWise account.")

    st.markdown("""
    <div class="detail-banner">
        <div style="font-size:45px;">👤</div>
        <h2>Your SchemeWise account</h2>
        <p>Your personal workspace for discovering government schemes.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Account information")

    full_name = escape(str(user.get(
        "full_name",
        user.get("name", "Not available")
    )))
    email = escape(str(user.get("email", "Not available")))
    role = escape(str(user.get("role", "user")))

    st.markdown(
        f"""
        <div class="detail-section">
            <p><b>Full name</b></p>
            <p>{full_name}</p>
            <hr>
            <p><b>Email address</b></p>
            <p>{email}</p>
            <hr>
            <p><b>Account role</b></p>
            <p>{role.title()}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("↪ Logout", type="primary"):
        logout()


# =========================================================
# ADMIN DASHBOARD
# =========================================================

def show_admin_dashboard():
    if not is_admin():
        st.error("You do not have permission to access this page.")
        st.session_state.page = "Home"
        st.rerun()
        return

    st.markdown("## 🛠️ Admin Dashboard")
    st.caption(
        "Manage government schemes and their official documents in SchemeWise."
    )

    st.markdown("""
    <div class="detail-banner">
        <div class="eyebrow">SCHEMEWISE ADMINISTRATION</div>
        <h2>Manage your knowledge base.</h2>
        <p>
            Add government schemes, upload official PDF documents
            and monitor document processing.
        </p>
    </div>
    """, unsafe_allow_html=True)

    tab_overview, tab_add, tab_upload, tab_manage = st.tabs([
        "📊 Overview",
        "➕ Add Scheme",
        "📄 Upload PDF",
        "🗂️ Manage Documents"
    ])

    # -----------------------------------------------------
    # OVERVIEW
    # -----------------------------------------------------

    with tab_overview:
        st.markdown("### 📊 Platform overview")

        if st.button("↻ Refresh statistics", use_container_width=True):
            refresh_public_catalogue()
            st.rerun()

        schemes = load_admin_schemes()
        documents = load_admin_documents()

        total_schemes = len(schemes)
        total_documents = len(documents)

        processed = sum(
            1 for doc in documents
            if str(doc.get("processing_status", "")).lower() == "processed"
        )

        pending = sum(
            1 for doc in documents
            if str(doc.get("processing_status", "")).lower() == "pending"
        )

        failed = sum(
            1 for doc in documents
            if str(doc.get("processing_status", "")).lower() == "failed"
        )

        m1, m2, m3 = st.columns(3)

        m1.metric("Government schemes", total_schemes)
        m2.metric("Uploaded documents", total_documents)
        m3.metric("Processed documents", processed)

        m4, m5 = st.columns(2)

        m4.metric("Pending documents", pending)
        m5.metric("Failed documents", failed)

        st.divider()

        section_heading(
            "Recent schemes",
            "Schemes currently registered in the database."
        )

        if schemes:
            for scheme in schemes[:5]:
                st.markdown(
                    f"""
                    <div class="admin-card">
                        <b>{escape(str(scheme.get('name', 'Unnamed scheme')))}</b>
                        <p class="admin-label">
                            Scheme ID: {scheme.get('id', 'N/A')}
                            &nbsp; | &nbsp;
                            Category ID: {scheme.get('category_id', 'N/A')}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.info("No schemes have been added to the database yet.")

    # -----------------------------------------------------
    # ADD SCHEME
    # -----------------------------------------------------

    with tab_add:
        st.markdown("### ➕ Add a new government scheme")

        st.write(
            "Enter the scheme details below. The scheme will be saved "
            "in the SchemeWise database."
        )

        categories = load_categories_from_backend()

        if not categories:
            st.warning(
                "No categories were returned by the backend. "
                "Please check that your categories API is working."
            )
        else:
            category_options = {
                str(item.get("name", f"Category {item.get('id')}")): item.get("id")
                for item in categories
                if isinstance(item, dict) and item.get("id") is not None
            }

            if not category_options:
                st.warning(
                    "The categories API did not return category IDs and names."
                )
            else:
                with st.form("add_scheme_form"):
                    scheme_name = st.text_input(
                        "Scheme name",
                        placeholder="e.g. Pradhan Mantri Awaas Yojana"
                    )

                    scheme_description = st.text_area(
                        "Scheme description",
                        placeholder="Briefly describe the purpose of this scheme...",
                        height=110
                    )

                    category_name = st.selectbox(
                        "Select category",
                        list(category_options.keys())
                    )

                    ministry = st.text_input(
                        "Ministry",
                        placeholder="e.g. Ministry of Rural Development"
                    )

                    official_url = st.text_input(
                        "Official website URL",
                        placeholder="https://..."
                    )

                    submitted = st.form_submit_button(
                        "➕ Create Scheme",
                        type="primary",
                        use_container_width=True
                    )

                    if submitted:
                        if not scheme_name.strip():
                            st.warning("Please enter the scheme name.")
                        elif not scheme_description.strip():
                            st.warning("Please enter a scheme description.")
                        else:
                            payload = {
                                "category_id": category_options[category_name],
                                "name": scheme_name.strip(),
                                "description": scheme_description.strip(),
                                "ministry": ministry.strip() or None,
                                "official_url": official_url.strip() or None
                            }

                            with st.spinner("Creating scheme..."):
                                result = api_post(
                                    "/schemes",
                                    payload=payload,
                                    authenticated=True
                                )

                            if result is not None:
                                refresh_public_catalogue()
                                st.success(
                                    f"Successfully created: {scheme_name}"
                                )
                                st.json(result)

                                st.info(
                                    "The new scheme is now available in the "
                                    "database catalogue. Open Explore Schemes "
                                    "to view it."
                                )

    # -----------------------------------------------------
    # UPLOAD PDF
    # -----------------------------------------------------

    with tab_upload:
        st.markdown("### 📄 Upload official scheme document")

        st.write(
            "Upload a PDF containing official scheme information. "
            "The backend will save the document and process it."
        )

        schemes = load_admin_schemes()

        if not schemes:
            st.warning(
                "No schemes are available in the database. "
                "Add a scheme first using the Add Scheme tab."
            )
        else:
            scheme_options = {
                f"{item.get('name', 'Unnamed scheme')} (ID: {item.get('id')})":
                item.get("id")
                for item in schemes
                if isinstance(item, dict) and item.get("id") is not None
            }

            if not scheme_options:
                st.warning("No valid scheme IDs were returned by the backend.")
            else:
                selected_scheme_name = st.selectbox(
                    "Choose the scheme for this document",
                    list(scheme_options.keys()),
                    key="upload_scheme_select"
                )

                uploaded_file = st.file_uploader(
                    "Choose a PDF file",
                    type=["pdf"],
                    help="Only PDF files are accepted.",
                    key="scheme_pdf_upload"
                )

                if uploaded_file:
                    st.success(f"Selected file: {uploaded_file.name}")
                    st.caption(
                        f"File size: {uploaded_file.size / 1024:.2f} KB"
                    )

                if st.button(
                    "⬆️ Upload and Process Document",
                    type="primary",
                    use_container_width=True,
                    disabled=uploaded_file is None
                ):
                    scheme_id = scheme_options[selected_scheme_name]

                    with st.spinner("Uploading document. Please wait..."):
                        result = api_upload_document(
                            f"/documents/upload/{scheme_id}",
                            uploaded_file
                        )

                    if result is not None:
                        st.success("Document uploaded successfully!")
                        st.json(result)

                        st.info(
                            "Check the Manage Documents tab to view "
                            "the document processing status."
                        )

    # -----------------------------------------------------
    # MANAGE DOCUMENTS
    # -----------------------------------------------------

    with tab_manage:
        st.markdown("### 🗂️ Manage uploaded documents")

        if st.button(
            "↻ Refresh document list",
            key="refresh_admin_documents"
        ):
            st.rerun()

        documents = load_admin_documents()

        if not documents:
            st.info(
                "No documents were returned. Upload a PDF to get started."
            )
        else:
            st.caption(f"{len(documents)} document(s) found.")

            for document in documents:
                filename = document.get("file_name", "Unknown file")
                document_id = document.get("id", "N/A")
                scheme_id = document.get("scheme_id", "N/A")
                status = str(
                    document.get("processing_status", "unknown")
                ).lower()

                if status == "processed":
                    status_display = "🟢 Processed"
                elif status == "processing":
                    status_display = "🔵 Processing"
                elif status == "pending":
                    status_display = "🟡 Pending"
                elif status == "failed":
                    status_display = "🔴 Failed"
                else:
                    status_display = f"⚪ {status.title()}"

                with st.expander(f"📄 {filename}"):
                    col1, col2 = st.columns(2)

                    with col1:
                        st.write(f"**Document ID:** {document_id}")
                        st.write(f"**Scheme ID:** {scheme_id}")

                    with col2:
                        st.write(f"**Status:** {status_display}")

                    if document.get("file_path"):
                        st.caption(
                            f"File path: {document.get('file_path')}"
                        )

                    if document.get("uploaded_at"):
                        st.caption(
                            f"Uploaded at: {document.get('uploaded_at')}"
                        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.caption(
        "Note: Admin access in the frontend is for navigation and display. "
        "The backend must also enforce administrator permissions on "
        "scheme creation and document-management endpoints."
    )


# =========================================================
# MAIN
# =========================================================

def main():
    if not st.session_state.token:
        show_landing()
        return

    if not st.session_state.saved_schemes_loaded:
        load_saved_schemes()

    if not st.session_state.catalogue_loaded:
        load_public_catalogue()

    if st.session_state.page == "Admin Dashboard" and not is_admin():
        st.session_state.page = "Home"

    show_sidebar()

    page = st.session_state.page

    if page == "Home":
        show_home()

    elif page == "Explore Schemes":
        show_explore()

    elif page == "Saved Schemes":
        show_saved_schemes()

    elif page == "Scheme Details":
        show_scheme_details()

    elif page == "AI Assistant":
        show_assistant()

    elif page == "My History":
        show_history()

    elif page == "My Profile":
        show_profile()

    elif page == "Admin Dashboard":
        show_admin_dashboard()

    else:
        st.session_state.page = "Home"
        st.rerun()


if __name__ == "__main__":
    main()
