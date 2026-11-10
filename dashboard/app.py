import streamlit as st
import pandas as pd
import joblib
from pathlib import Path
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Sri Lankan Fish Price Intelligence",
    page_icon="🐟",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# GLOBAL CSS + TOP OCEAN ANIMATION
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       REMOVE STREAMLIT TOP WHITE SPACE
       ======================================================== */

    [data-testid="stAppViewContainer"] {
        background-color: #061B2A;
    }

    [data-testid="stAppViewContainer"] .main {
        background-color: #061B2A;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
        height: 0px !important;
    }

    [data-testid="stToolbar"] {
        visibility: hidden;
        height: 0px;
    }

    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 1rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 100% !important;
    }


    /* ========================================================
       GLOBAL APPLICATION
       ======================================================== */

    .stApp {
        background-color: #061B2A;
        color: #FFFFFF;
    }

    .main {
        background-color: #061B2A;
    }


    /* ========================================================
       ALL TEXT
       ======================================================== */

    .stApp,
    .stApp p,
    .stApp label,
    .stApp span,
    .stApp div {
        color: #FFFFFF;
    }


    /* ========================================================
       HEADINGS
       ======================================================== */

    h1 {
        color: #FFFFFF !important;
        font-size: 38px !important;
        font-weight: 900 !important;
        margin-top: 8px !important;
        margin-bottom: 5px !important;
    }

    h2 {
        color: #FFFFFF !important;
        font-size: 27px !important;
        font-weight: 850 !important;
        margin-top: 12px !important;
        margin-bottom: 5px !important;
    }

    h3 {
        color: #FFFFFF !important;
        font-size: 21px !important;
        font-weight: 800 !important;
        margin-top: 8px !important;
        margin-bottom: 5px !important;
    }


    /* ========================================================
       TOP OCEAN ANIMATION
       This replaces the empty space above the title
       ======================================================== */

    .top-ocean {

        position: relative;

        width: 100%;

        height: 125px;

        overflow: hidden;

        margin: 0 0 5px 0;

        border-radius: 0 0 22px 22px;

        background:
            linear-gradient(
                180deg,
                #061B2A 0%,
                #07364A 45%,
                #07566A 75%,
                #087F8C 100%
            );

        border-bottom:
            1px solid rgba(255,255,255,0.15);

        box-shadow:
            0 8px 25px rgba(0,0,0,0.20);
    }


    /* ========================================================
       OCEAN WAVES
       ======================================================== */

    .ocean-wave {

        position: absolute;

        left: -5%;

        bottom: -42px;

        width: 110%;

        height: 70px;

        border-radius: 50% 50% 0 0;

        background:
            rgba(255,255,255,0.09);

        animation:
            waveMove 6s ease-in-out infinite;
    }


    .ocean-wave.two {

        bottom: -50px;

        opacity: 0.55;

        animation:
            waveMoveReverse 8s ease-in-out infinite;
    }


    @keyframes waveMove {

        0%, 100% {
            transform: translateX(-20px);
        }

        50% {
            transform: translateX(20px);
        }
    }


    @keyframes waveMoveReverse {

        0%, 100% {
            transform: translateX(20px);
        }

        50% {
            transform: translateX(-20px);
        }
    }


    /* ========================================================
       FISH
       ======================================================== */

    .animated-fish {

        position: absolute;

        font-size: 32px;

        z-index: 10;

        animation:
            fishSwim 14s linear infinite;
    }


    .fish-one {

        top: 42px;

        left: -60px;

        animation-delay: 0s;
    }


    .fish-two {

        top: 72px;

        left: -100px;

        font-size: 24px;

        animation-delay: 4s;

        opacity: 0.75;
    }


    .fish-three {

        top: 28px;

        left: -120px;

        font-size: 20px;

        animation-delay: 8s;

        opacity: 0.55;
    }


    @keyframes fishSwim {

        0% {
            transform:
                translateX(-100px)
                translateY(0px)
                scaleX(1);
        }

        25% {
            transform:
                translateX(25vw)
                translateY(-8px)
                scaleX(1);
        }

        50% {
            transform:
                translateX(50vw)
                translateY(5px)
                scaleX(1);
        }

        75% {
            transform:
                translateX(75vw)
                translateY(-7px)
                scaleX(1);
        }

        100% {
            transform:
                translateX(110vw)
                translateY(2px)
                scaleX(1);
        }
    }


    /* ========================================================
       BOAT
       ======================================================== */

    .animated-boat {

        position: absolute;

        right: 8%;

        top: 20px;

        font-size: 48px;

        z-index: 12;

        filter:
            drop-shadow(
                0 7px 5px rgba(0,0,0,0.35)
            );

        animation:
            boatFloat 4s ease-in-out infinite;
    }


    @keyframes boatFloat {

        0%, 100% {
            transform:
                translateY(0px)
                rotate(-2deg);
        }

        50% {
            transform:
                translateY(-8px)
                rotate(2deg);
        }
    }


    /* ========================================================
       SMALL BUBBLES
       ======================================================== */

    .ocean-bubble {

        position: absolute;

        border-radius: 50%;

        border:
            1px solid rgba(255,255,255,0.35);

        background:
            rgba(255,255,255,0.08);

        bottom: 5px;

        z-index: 5;

        animation:
            bubbleRise 7s linear infinite;
    }


    .bubble-one {

        width: 10px;
        height: 10px;
        left: 18%;
        animation-delay: 0s;
    }


    .bubble-two {

        width: 7px;
        height: 7px;
        left: 32%;
        animation-delay: 2s;
    }


    .bubble-three {

        width: 14px;
        height: 14px;
        left: 50%;
        animation-delay: 4s;
    }


    .bubble-four {

        width: 8px;
        height: 8px;
        left: 65%;
        animation-delay: 1s;
    }


    .bubble-five {

        width: 11px;
        height: 11px;
        left: 78%;
        animation-delay: 3s;
    }


    @keyframes bubbleRise {

        0% {
            transform:
                translateY(20px)
                scale(0.6);

            opacity: 0;
        }

        20% {
            opacity: 0.7;
        }

        100% {
            transform:
                translateY(-110px)
                scale(1.1);

            opacity: 0;
        }
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {

        background-color: #03131F;

        border-right:
            1px solid #1B5268;
    }

    section[data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }


    /* ========================================================
       SIDEBAR TITLE
       ======================================================== */

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
    }


    /* ========================================================
       RADIO BUTTON
       ======================================================== */

    div[role="radiogroup"] label {

        color: #FFFFFF !important;

        font-weight: 600 !important;
    }


    /* ========================================================
       SELECTBOX
       ======================================================== */

    .stSelectbox label {

        color: #FFFFFF !important;

        font-weight: 800 !important;

        font-size: 15px !important;
    }

    div[data-baseweb="select"] {

        background-color:
            #12384A !important;
    }

    div[data-baseweb="select"] > div {

        background-color:
            #12384A !important;

        border:
            1px solid #3A7487 !important;

        border-radius:
            8px !important;

        min-height:
            42px !important;
    }

    div[data-baseweb="select"] span {

        color:
            #FFFFFF !important;

        font-weight:
            600 !important;
    }


    /* ========================================================
       METRIC CARDS
       ======================================================== */

    [data-testid="stMetric"] {

        background-color:
            #0D3042;

        border:
            1px solid #285D70;

        border-radius:
            10px;

        padding:
            12px 16px !important;

        min-height:
            105px;
    }

    [data-testid="stMetricLabel"] {

        color:
            #C7EAF2 !important;

        font-size:
            14px !important;

        font-weight:
            700 !important;
    }

    [data-testid="stMetricValue"] {

        color:
            #FFFFFF !important;

        font-size:
            30px !important;

        font-weight:
            900 !important;
    }

    [data-testid="stMetricDelta"] {

        font-weight:
            700 !important;
    }


    /* ========================================================
       BUTTON
       ======================================================== */

    .stButton > button {

        width:
            100%;

        background-color:
            #087F8C;

        color:
            #FFFFFF !important;

        border:
            1px solid #39B8C4;

        border-radius:
            8px;

        min-height:
            46px;

        font-size:
            16px;

        font-weight:
            850;
    }

    .stButton > button:hover {

        background-color:
            #0A9AA8;

        color:
            #FFFFFF !important;

        border-color:
            #FFFFFF;

        transform:
            translateY(-2px);
    }


    /* ========================================================
       DATAFRAME
       ======================================================== */

    [data-testid="stDataFrame"] {

        border:
            1px solid #285D70;

        border-radius:
            8px;
    }


    /* ========================================================
       ALERTS
       ======================================================== */

    .stAlert {

        border-radius:
            8px !important;
    }


    /* ========================================================
       DIVIDERS
       ======================================================== */

    hr {

        border-color:
            #285D70 !important;

        margin-top:
            8px !important;

        margin-bottom:
            8px !important;
    }


    /* ========================================================
       RESPONSIVE
       ======================================================== */

    @media (max-width: 900px) {

        .block-container {

            padding-left:
                1rem !important;

            padding-right:
                1rem !important;
        }

        .top-ocean {

            height:
                100px;
        }

        .animated-boat {

            font-size:
                36px;

            right:
                5%;

            top:
                20px;
        }

        .animated-fish {

            font-size:
                25px;
        }

        h1 {

            font-size:
                30px !important;
        }

        h2 {

            font-size:
                23px !important;
        }

        [data-testid="stMetricValue"] {

            font-size:
                24px !important;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TOP ANIMATED OCEAN
# ============================================================

st.markdown(
    """
    <div class="top-ocean">

        <!-- FISH -->
        <div class="animated-fish fish-one">
            🐟
        </div>

        <div class="animated-fish fish-two">
            🐠
        </div>

        <div class="animated-fish fish-three">
            🐟
        </div>


        <!-- BOAT -->
        <div class="animated-boat">
            🚤
        </div>


        <!-- BUBBLES -->
        <div class="ocean-bubble bubble-one"></div>
        <div class="ocean-bubble bubble-two"></div>
        <div class="ocean-bubble bubble-three"></div>
        <div class="ocean-bubble bubble-four"></div>
        <div class="ocean-bubble bubble-five"></div>


        <!-- WAVES -->
        <div class="ocean-wave"></div>
        <div class="ocean-wave two"></div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "fish_price_ready_for_model.csv"
)

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "best_model.pkl"
)


# ============================================================
# LOAD DATASET
# ============================================================

if not DATA_PATH.exists():

    st.error(
        f"Dataset not found:\n\n{DATA_PATH}"
    )

    st.stop()


try:

    df = pd.read_csv(DATA_PATH)

except Exception as e:

    st.error(
        f"Unable to load dataset: {e}"
    )

    st.stop()


# ============================================================
# REQUIRED COLUMNS
# ============================================================

required_columns = [

    "Species",
    "MarketType",
    "Year",
    "MonthNumber",
    "Week",
    "Price_2025",
    "Price_LastWeek",
    "Change_LastYear_%",
    "Price_Current"

]


missing_columns = [

    column
    for column in required_columns
    if column not in df.columns

]


if missing_columns:

    st.error(
        "The following required columns are missing:"
    )

    st.write(missing_columns)

    st.stop()


# ============================================================
# LOAD MODEL
# ============================================================

if not MODEL_PATH.exists():

    st.warning(
        f"Model file not found:\n\n{MODEL_PATH}"
    )

    model = None

else:

    try:

        model = joblib.load(MODEL_PATH)

    except Exception as e:

        st.error(
            f"Unable to load model: {e}"
        )

        model = None


# ============================================================
# BASIC DATA PREPARATION
# ============================================================

df["Price_Current"] = pd.to_numeric(
    df["Price_Current"],
    errors="coerce"
)

df["Price_2025"] = pd.to_numeric(
    df["Price_2025"],
    errors="coerce"
)

df["Price_LastWeek"] = pd.to_numeric(
    df["Price_LastWeek"],
    errors="coerce"
)

df["Change_LastYear_%"] = pd.to_numeric(
    df["Change_LastYear_%"],
    errors="coerce"
)


# ============================================================
# GLOBAL STATISTICS
# ============================================================

total_records = len(df)

total_species = df["Species"].nunique()

total_markets = df["MarketType"].nunique()

average_price = df["Price_Current"].mean()

highest_price = df["Price_Current"].max()

lowest_price = df["Price_Current"].min()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🐟 Fish Intelligence")

    st.caption(
        "Sri Lankan Fish Market Price Prediction"
    )

    st.divider()

    st.subheader("Navigation")

    page = st.radio(

        "Select Page",

        [
            "🏠 Overview",
            "🔮 Price Prediction",
            "📊 Market Analytics",
            "🤖 Model Insights"
        ],

        label_visibility="collapsed"

    )

    st.divider()

    st.subheader("Dataset")

    st.write(
        f"**Records:** {total_records:,}"
    )

    st.write(
        f"**Species:** {total_species}"
    )

    st.write(
        f"**Markets:** {total_markets}"
    )

    st.write(
        f"**Year:** {df['Year'].min()} - {df['Year'].max()}"
    )


# ============================================================
# PAGE HEADER
# ============================================================

st.title(
    "🐟 Sri Lankan Fish Price Intelligence"
)

st.write(
    "Machine Learning-Based Fish Market Price Prediction System for Sri Lanka"
)

st.divider()


# ============================================================
# OVERVIEW
# ============================================================

if page == "🏠 Overview":

    st.header(
        "📊 Dashboard Overview"
    )

    st.write(
        "Historical fish market prices, market behaviour and "
        "machine learning-based price intelligence."
    )


    # ========================================================
    # KPI ROW
    # ========================================================

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "📋 Historical Records",
            f"{total_records:,}"
        )

    with c2:

        st.metric(
            "🐟 Fish Species",
            f"{total_species}"
        )

    with c3:

        st.metric(
            "🏪 Market Types",
            f"{total_markets}"
        )

    with c4:

        st.metric(
            "💰 Average Current Price",
            f"Rs. {average_price:,.0f}"
        )


    # ========================================================
    # PRICE RANGE
    # ========================================================

    st.header(
        "💰 Price Overview"
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Lowest Price",
            f"Rs. {lowest_price:,.2f}"
        )

    with c2:

        st.metric(
            "Average Price",
            f"Rs. {average_price:,.2f}"
        )

    with c3:

        st.metric(
            "Highest Price",
            f"Rs. {highest_price:,.2f}"
        )


    # ========================================================
    # CHARTS
    # ========================================================

    st.header(
        "📈 Market Price Trends"
    )

    col1, col2 = st.columns(2)


    # --------------------------------------------------------
    # PRICE DISTRIBUTION
    # --------------------------------------------------------

    with col1:

        fig = px.histogram(

            df,

            x="Price_Current",

            nbins=30,

            title="Current Price Distribution",

            labels={
                "Price_Current":
                    "Current Price (Rs.)"
            }

        )

        fig.update_layout(

            template="plotly_dark",

            paper_bgcolor="#061B2A",

            plot_bgcolor="#061B2A",

            font=dict(
                color="white",
                size=13
            ),

            title_font=dict(
                color="white",
                size=18
            ),

            margin=dict(
                l=40,
                r=20,
                t=60,
                b=40
            )

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # --------------------------------------------------------
    # MONTHLY PRICE
    # --------------------------------------------------------

    with col2:

        monthly = (

            df

            .groupby(
                "MonthNumber"
            )["Price_Current"]

            .mean()

            .reset_index()

        )

        fig = px.line(

            monthly,

            x="MonthNumber",

            y="Price_Current",

            markers=True,

            title="Monthly Average Current Price",

            labels={

                "MonthNumber":
                    "Month",

                "Price_Current":
                    "Average Price (Rs.)"

            }

        )

        fig.update_layout(

            template="plotly_dark",

            paper_bgcolor="#061B2A",

            plot_bgcolor="#061B2A",

            font=dict(
                color="white",
                size=13
            ),

            title_font=dict(
                color="white",
                size=18
            ),

            margin=dict(
                l=40,
                r=20,
                t=60,
                b=40
            )

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )


    # ========================================================
    # TOP SPECIES
    # ========================================================

    st.header(
        "🐟 Average Price by Fish Species"
    )

    species_prices = (

        df

        .groupby(
            "Species"
        )["Price_Current"]

        .mean()

        .sort_values(
            ascending=False
        )

        .reset_index()

    )

    fig = px.bar(

        species_prices,

        x="Species",

        y="Price_Current",

        title="Average Current Price by Species",

        labels={

            "Species":
                "Fish Species",

            "Price_Current":
                "Average Price (Rs.)"

        }

    )

    fig.update_xaxes(
        tickangle=-45
    )

    fig.update_layout(

        template="plotly_dark",

        paper_bgcolor="#061B2A",

        plot_bgcolor="#061B2A",

        font=dict(
            color="white",
            size=12
        ),

        title_font=dict(
            color="white",
            size=18
        ),

        margin=dict(
            l=40,
            r=20,
            t=60,
            b=100
        )

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )


# ============================================================
# PRICE PREDICTION
# ============================================================

elif page == "🔮 Price Prediction":

    st.header(
        "🔮 Fish Price Prediction"
    )

    st.write(
        "Select the required market conditions to generate "
        "a machine learning-based current price prediction."
    )

    st.divider()


    # ========================================================
    # INPUTS
    # ========================================================

    col1, col2 = st.columns(2)

    with col1:

        species = st.selectbox(

            "🐟 Fish Species",

            sorted(
                df["Species"]
                .dropna()
                .unique()
            )

        )

    with col2:

        market = st.selectbox(

            "🏪 Market Type",

            sorted(
                df["MarketType"]
                .dropna()
                .unique()
            )

        )


    col3, col4 = st.columns(2)

    with col3:

        year = st.selectbox(

            "📅 Year",

            sorted(
                df["Year"]
                .dropna()
                .unique()
            )

        )

    with col4:

        month = st.selectbox(

            "🗓️ Month",

            sorted(
                df["MonthNumber"]
                .dropna()
                .unique()
            )

        )


    col5, col6 = st.columns(2)

    with col5:

        week = st.selectbox(

            "📆 Week",

            sorted(
                df["Week"]
                .dropna()
                .unique()
            )

        )

    with col6:

        st.write("")
        st.write("")

        predict_button = st.button(
            "🔮 PREDICT CURRENT PRICE"
        )


    # ========================================================
    # FIND HISTORICAL RECORD
    # ========================================================

    matching = df[

        (df["Species"] == species)

        &

        (df["MarketType"] == market)

        &

        (df["Year"] == year)

        &

        (df["MonthNumber"] == month)

        &

        (df["Week"] == week)

    ]


    if not matching.empty:

        record = matching.iloc[0]


        price_2025 = float(
            record["Price_2025"]
        )

        price_last_week = float(
            record["Price_LastWeek"]
        )

        change_last_year = float(
            record["Change_LastYear_%"]
        )


        # ====================================================
        # HISTORICAL INFORMATION
        # ====================================================

        st.header(
            "📚 Historical Price Information"
        )

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(

                "💰 Same Week Last Year",

                f"Rs. {price_2025:,.2f}"

            )

        with c2:

            st.metric(

                "📆 Previous Week",

                f"Rs. {price_last_week:,.2f}"

            )

        with c3:

            st.metric(

                "📊 Change From Last Year",

                f"{change_last_year:+.2f}%"

            )


        # ====================================================
        # PREDICTION
        # ====================================================

        if predict_button:

            if model is None:

                st.error(
                    "Machine learning model is not available."
                )

            else:

                input_data = pd.DataFrame({

                    "Species":
                        [species],

                    "MarketType":
                        [market],

                    "Year":
                        [year],

                    "MonthNumber":
                        [month],

                    "Week":
                        [week],

                    "Price_2025":
                        [price_2025],

                    "Price_LastWeek":
                        [price_last_week],

                    "Change_LastYear_%":
                        [change_last_year]

                })


                try:

                    prediction = model.predict(
                        input_data
                    )[0]

                    prediction = max(
                        0,
                        float(prediction)
                    )


                    # ========================================
                    # MAIN RESULT
                    # ========================================

                    st.divider()

                    st.header(
                        "🎯 Prediction Result"
                    )

                    st.metric(

                        "🐟 Predicted Current Fish Price",

                        f"Rs. {prediction:,.2f}"

                    )


                    # ========================================
                    # COMPARISON
                    # ========================================

                    st.header(
                        "📊 Price Comparison"
                    )

                    c1, c2, c3 = st.columns(3)

                    with c1:

                        st.metric(

                            "Predicted Price",

                            f"Rs. {prediction:,.2f}"

                        )

                    with c2:

                        st.metric(

                            "Previous Week",

                            f"Rs. {price_last_week:,.2f}"

                        )

                    with c3:

                        if price_last_week != 0:

                            percentage_change = (

                                (

                                    prediction
                                    -
                                    price_last_week

                                )

                                /

                                price_last_week

                            ) * 100

                        else:

                            percentage_change = 0


                        st.metric(

                            "Expected Change",

                            f"{percentage_change:+.2f}%"

                        )


                    # ========================================
                    # INTERPRETATION
                    # ========================================

                    if percentage_change > 0:

                        st.success(

                            f"📈 The predicted price is "
                            f"{percentage_change:.2f}% higher "
                            f"than the previous week's price."

                        )

                    elif percentage_change < 0:

                        st.warning(

                            f"📉 The predicted price is "
                            f"{abs(percentage_change):.2f}% lower "
                            f"than the previous week's price."

                        )

                    else:

                        st.info(

                            "➡️ The predicted price is approximately "
                            "the same as the previous week's price."

                        )


                except Exception as e:

                    st.error(
                        "Prediction failed."
                    )

                    st.exception(e)


    else:

        st.info(

            "No matching historical record was found for "
            "the selected combination."

        )


# ============================================================
# MARKET ANALYTICS
# ============================================================

elif page == "📊 Market Analytics":

    st.header(
        "📊 Market Analytics"
    )

    st.write(
        "Explore fish-specific price behaviour and market trends."
    )

    st.divider()


    # ========================================================
    # SPECIES SELECTION
    # ========================================================

    selected_species = st.selectbox(

        "🐟 Select Fish Species",

        sorted(
            df["Species"]
            .dropna()
            .unique()
        )

    )


    species_df = df[
        df["Species"] == selected_species
    ]


    # ========================================================
    # SPECIES KPIs
    # ========================================================

    avg_price = species_df[
        "Price_Current"
    ].mean()

    max_price = species_df[
        "Price_Current"
    ].max()

    min_price = species_df[
        "Price_Current"
    ].min()

    record_count = len(
        species_df
    )


    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "📋 Records",
            f"{record_count:,}"
        )

    with c2:

        st.metric(
            "💰 Average Price",
            f"Rs. {avg_price:,.2f}"
        )

    with c3:

        st.metric(
            "⬆️ Highest Price",
            f"Rs. {max_price:,.2f}"
        )

    with c4:

        st.metric(
            "⬇️ Lowest Price",
            f"Rs. {min_price:,.2f}"
        )


    # ========================================================
    # SPECIES TREND
    # ========================================================

    st.header(
        f"📈 {selected_species} Price Trend"
    )


    trend = (

        species_df

        .groupby(
            [
                "Year",
                "MonthNumber",
                "Week"
            ]
        )["Price_Current"]

        .mean()

        .reset_index()

    )


    trend["Period"] = (

        trend["Year"].astype(str)

        + " / M"

        + trend["MonthNumber"].astype(str)

        + " / W"

        + trend["Week"].astype(str)

    )


    fig = px.line(

        trend,

        x="Period",

        y="Price_Current",

        markers=True,

        title=f"{selected_species} Current Price Trend",

        labels={

            "Period":
                "Period",

            "Price_Current":
                "Current Price (Rs.)"

        }

    )


    fig.update_layout(

        template="plotly_dark",

        paper_bgcolor="#061B2A",

        plot_bgcolor="#061B2A",

        font=dict(
            color="white",
            size=13
        ),

        title_font=dict(
            color="white",
            size=18
        ),

        margin=dict(
            l=40,
            r=20,
            t=60,
            b=80
        )

    )


    st.plotly_chart(

        fig,

        use_container_width=True

    )


    # ========================================================
    # MARKET COMPARISON
    # ========================================================

    st.header(
        "🏪 Average Price by Market Type"
    )


    market_prices = (

        df

        .groupby(
            "MarketType"
        )["Price_Current"]

        .mean()

        .sort_values(
            ascending=False
        )

        .reset_index()

    )


    fig = px.bar(

        market_prices,

        x="MarketType",

        y="Price_Current",

        title="Average Current Price by Market Type",

        labels={

            "MarketType":
                "Market Type",

            "Price_Current":
                "Average Price (Rs.)"

        }

    )


    fig.update_layout(

        template="plotly_dark",

        paper_bgcolor="#061B2A",

        plot_bgcolor="#061B2A",

        font=dict(
            color="white",
            size=13
        ),

        title_font=dict(
            color="white",
            size=18
        ),

        margin=dict(
            l=40,
            r=20,
            t=60,
            b=60
        )

    )


    st.plotly_chart(

        fig,

        use_container_width=True

    )


    # ========================================================
    # PRICE CHANGE
    # ========================================================

    st.header(
        "📊 Price Change Compared With Last Year"
    )


    change_data = (

        df

        .groupby(
            "Species"
        )["Change_LastYear_%"]

        .mean()

        .sort_values(
            ascending=False
        )

        .reset_index()

    )


    fig = px.bar(

        change_data,

        x="Species",

        y="Change_LastYear_%",

        title="Average Price Change From Same Week Last Year",

        labels={

            "Species":
                "Fish Species",

            "Change_LastYear_%":
                "Change (%)"

        }

    )


    fig.update_xaxes(
        tickangle=-45
    )


    fig.update_layout(

        template="plotly_dark",

        paper_bgcolor="#061B2A",

        plot_bgcolor="#061B2A",

        font=dict(
            color="white",
            size=12
        ),

        title_font=dict(
            color="white",
            size=18
        ),

        margin=dict(
            l=40,
            r=20,
            t=60,
            b=100
        )

    )


    st.plotly_chart(

        fig,

        use_container_width=True

    )


# ============================================================
# MODEL INSIGHTS
# ============================================================

elif page == "🤖 Model Insights":

    st.header(
        "🤖 Machine Learning Model Insights"
    )

    st.write(
        "Explore the numerical relationships in the dataset "
        "and information used by the prediction system."
    )

    st.divider()


    # ========================================================
    # MODEL STATUS
    # ========================================================

    if model is not None:

        st.success(
            "✅ Machine learning model loaded successfully."
        )

    else:

        st.error(
            "❌ Machine learning model is not available."
        )


    # ========================================================
    # DATASET INFORMATION
    # ========================================================

    st.header(
        "📋 Dataset Information"
    )


    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.metric(
            "Records",
            f"{len(df):,}"
        )


    with c2:

        st.metric(
            "Features",
            f"{len(df.columns)}"
        )


    with c3:

        st.metric(
            "Species",
            f"{df['Species'].nunique()}"
        )


    with c4:

        st.metric(
            "Market Types",
            f"{df['MarketType'].nunique()}"
        )


    # ========================================================
    # CORRELATION
    # ========================================================

    st.header(
        "🔗 Feature Correlation"
    )


    numeric_columns = [

        "Year",
        "MonthNumber",
        "Week",
        "Price_2025",
        "Price_LastWeek",
        "Change_LastYear_%",
        "Price_Current"

    ]


    correlation = df[
        numeric_columns
    ].corr()


    fig = px.imshow(

        correlation,

        text_auto=".2f",

        aspect="auto",

        title="Correlation Matrix"

    )


    fig.update_layout(

        template="plotly_dark",

        paper_bgcolor="#061B2A",

        plot_bgcolor="#061B2A",

        font=dict(
            color="white",
            size=13
        ),

        title_font=dict(
            color="white",
            size=18
        )

    )


    st.plotly_chart(

        fig,

        use_container_width=True

    )


    # ========================================================
    # IMPORTANT PRICE FEATURES
    # ========================================================

    st.header(
        "💰 Price Feature Relationships"
    )


    col1, col2 = st.columns(2)


    # --------------------------------------------------------
    # LAST WEEK VS CURRENT
    # --------------------------------------------------------

    with col1:

        fig = px.scatter(

            df,

            x="Price_LastWeek",

            y="Price_Current",

            title="Previous Week Price vs Current Price",

            labels={

                "Price_LastWeek":
                    "Previous Week Price (Rs.)",

                "Price_Current":
                    "Current Price (Rs.)"

            },

            hover_data=[

                "Species",
                "MarketType"

            ]

        )


        fig.update_layout(

            template="plotly_dark",

            paper_bgcolor="#061B2A",

            plot_bgcolor="#061B2A",

            font=dict(
                color="white",
                size=12
            ),

            title_font=dict(
                color="white",
                size=17
            )

        )


        st.plotly_chart(

            fig,

            use_container_width=True

        )


    # --------------------------------------------------------
    # LAST YEAR VS CURRENT
    # --------------------------------------------------------

    with col2:

        fig = px.scatter(

            df,

            x="Price_2025",

            y="Price_Current",

            title="Same Week Last Year vs Current Price",

            labels={

                "Price_2025":
                    "2025 Price (Rs.)",

                "Price_Current":
                    "Current Price (Rs.)"

            },

            hover_data=[

                "Species",
                "MarketType"

            ]

        )


        fig.update_layout(

            template="plotly_dark",

            paper_bgcolor="#061B2A",

            plot_bgcolor="#061B2A",

            font=dict(
                color="white",
                size=12
            ),

            title_font=dict(
                color="white",
                size=17
            )

        )


        st.plotly_chart(

            fig,

            use_container_width=True

        )


    # ========================================================
    # DATA PREVIEW
    # ========================================================

    st.header(
        "📋 Dataset Preview"
    )


    st.dataframe(

        df,

        use_container_width=True,

        hide_index=True

    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🐟 Sri Lankan Fish Price Intelligence | "
    "Machine Learning-Based Fish Market Price Prediction System"
)