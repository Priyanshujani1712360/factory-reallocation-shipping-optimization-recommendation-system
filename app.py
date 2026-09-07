import streamlit as st
import pandas as pd

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Factory Reallocation & Shipping Optimization Recommendation System for Nassau Candy Distributor",
    page_icon="🏭",
    layout="wide"
)

# APPLICATION TITLE
st.title("🏭 Factory Reallocation & Shipping Optimization Recommendation System for Nassau Candy Distributor")

st.markdown(
    """
    This dashboard analyzes factory allocation scenarios and provides
    data-driven recommendations to improve operational lead time while
    considering profitability and scenario reliability.
    """
)


# LOAD DATA
@st.cache_data
def load_data():
    recommendations = pd.read_csv(
        "streamlit_recommendations.csv"
    )

    kpi_summary = pd.read_csv(
        "streamlit_kpi_summary.csv"
    )

    return recommendations, kpi_summary


recommendations, kpi_summary = load_data()


# DATA VALIDATION
st.success("Data loaded successfully! ✅")

st.write("### Dataset Overview")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Recommendation Records",
        len(recommendations)
    )

with col2:
    st.metric(
        "Products Covered",
        recommendations["Product ID"].nunique()
    )


# PREVIEW DATA
with st.expander("View Recommendation Dataset"):
    st.dataframe(
        recommendations.head(),
        use_container_width=True
    )

with st.expander("View KPI Dataset"):
    st.dataframe(
        kpi_summary,
        use_container_width=True
    )


# KPI OVERVIEW
st.divider()

st.header("📊 Key Performance Indicators")

# Convert KPI summary into an easy lookup dictionary
kpi_values = dict(
    zip(
        kpi_summary["KPI"],
        kpi_summary["Value"]
    )
)

# Create four KPI columns
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Lead Time Reduction",
        value=f"{kpi_values['Lead Time Reduction (%)']:.2f}%"
    )

with col2:
    st.metric(
        label="Profit Impact Stability",
        value=f"{kpi_values['Profit Impact Stability (%)']:.2f}%"
    )

with col3:
    st.metric(
        label="Scenario Confidence",
        value=f"{kpi_values['Scenario Confidence Score']:.2f}"
    )

with col4:
    st.metric(
        label="Recommendation Coverage",
        value=f"{kpi_values['Recommendation Coverage (%)']:.2f}%"
    )


# KPI EXPLANATION
st.caption(
    """
    These KPIs summarize the expected operational improvement,
    financial stability, scenario reliability, and coverage of
    the factory reallocation recommendation system.
    """
)   


# FACTORY OPTIMIZATION SIMULATOR
# st.divider()

# st.header("🎛️ Factory Optimization Simulator")

# st.write(
#     """
#     Select a product, destination region, and shipping mode
#     to explore available factory optimization recommendations.
#     """
# )

# # USER INPUTS
# col1, col2, col3 = st.columns(3)

# with col1:
#     selected_product = st.selectbox(
#         "Select Product",
#         sorted(recommendations["Product Name"].unique())
#     )

# with col2:
#     selected_region = st.selectbox(
#         "Select Destination Region",
#         sorted(recommendations["Region"].unique())
#     )

# with col3:
#     selected_ship_mode = st.selectbox(
#         "Select Ship Mode",
#         sorted(recommendations["Ship Mode"].unique())
#     )


# # FILTER SELECTED SCENARIO
# selected_scenarios = recommendations[
#     (
#         recommendations["Product Name"] == selected_product
#     )
#     &
#     (
#         recommendations["Region"] == selected_region
#     )
#     &
#     (
#         recommendations["Ship Mode"] == selected_ship_mode
#     )
# ].copy()


# # DISPLAY SELECTED SCENARIO
# if selected_scenarios.empty:

#     st.warning(
#         "No recommendation scenario is available for this combination."
#     )

# else:

#     st.success(
#         f"{len(selected_scenarios)} factory recommendation option(s) found."
#     )

#     # Display selected scenario details
#     st.subheader("Available Factory Recommendations")

#     display_columns = [
#         "Current Factory",
#         "Recommended Factory",
#         "Lead Time Reduction (%)",
#         "Scenario Reliability",
#         "Profit Risk",
#         "Recommendation Score",
#         "Recommendation Status"
#     ]

#     st.dataframe(
#         selected_scenarios[
#             display_columns
#         ],
#         use_container_width=True,
#         hide_index=True
#     )

# =========================================================
# FACTORY OPTIMIZATION SIMULATOR
# =========================================================

# =========================================================
# FACTORY OPTIMIZATION SIMULATOR
# =========================================================

st.divider()

st.header("🎛️ Factory Optimization Simulator")

st.write(
    """
    Select a product, destination region, and shipping mode
    to explore available factory optimization recommendations.
    """
)

# ---------------------------------------------------------
# 1. SELECT PRODUCT
# ---------------------------------------------------------

selected_product = st.selectbox(
    "Select Product",
    sorted(recommendations["Product Name"].unique())
)


# ---------------------------------------------------------
# 2. FILTER AVAILABLE REGIONS FOR SELECTED PRODUCT
# ---------------------------------------------------------

available_regions = sorted(
    recommendations[
        recommendations["Product Name"] == selected_product
    ]["Region"].unique()
)

selected_region = st.selectbox(
    "Select Destination Region",
    available_regions
)


# ---------------------------------------------------------
# 3. FILTER AVAILABLE SHIP MODES
#    BASED ON PRODUCT + REGION
# ---------------------------------------------------------

available_ship_modes = sorted(
    recommendations[
        (recommendations["Product Name"] == selected_product)
        &
        (recommendations["Region"] == selected_region)
    ]["Ship Mode"].unique()
)

selected_ship_mode = st.selectbox(
    "Select Ship Mode",
    available_ship_modes
)


# ---------------------------------------------------------
# 4. FILTER SELECTED SCENARIO
# ---------------------------------------------------------

selected_scenarios = recommendations[
    (
        recommendations["Product Name"] == selected_product
    )
    &
    (
        recommendations["Region"] == selected_region
    )
    &
    (
        recommendations["Ship Mode"] == selected_ship_mode
    )
].copy()


# ---------------------------------------------------------
# 5. DISPLAY SELECTED SCENARIOS
# ---------------------------------------------------------

if selected_scenarios.empty:

    st.warning(
        "No recommendation scenario is available for this combination."
    )

else:

    st.success(
        f"{len(selected_scenarios)} factory recommendation option(s) found."
    )

    st.subheader("Available Factory Recommendations")

    display_columns = [
        "Current Factory",
        "Recommended Factory",
        "Lead Time Reduction (%)",
        "Scenario Reliability",
        "Profit Risk",
        "Recommendation Score",
        "Recommendation Status"
    ]

    st.dataframe(
        selected_scenarios[
            display_columns
        ],
        use_container_width=True,
        hide_index=True
    )




# WHAT-IF SCENARIO ANALYSIS
st.divider()

st.header("🔄 What-If Scenario Analysis")

st.write(
    """
    Compare the current factory assignment with the recommended
    factory scenario to understand the expected operational impact.
    """
)


# CHECK WHETHER A SCENARIO IS AVAILABLE
if selected_scenarios.empty:

    st.info(
        "Select a valid Product, Region, and Ship Mode combination "
        "to view the What-If Scenario Analysis."
    )

else:

    
    # SELECT A RECOMMENDED FACTORY SCENARIO
    scenario_options = selected_scenarios[
        "Recommended Factory"
    ].tolist()

    selected_factory = st.selectbox(
        "Select Factory Scenario to Compare",
        scenario_options,
        key="what_if_factory"
    )


    # Get selected factory scenario
    what_if_scenario = selected_scenarios[
        selected_scenarios["Recommended Factory"]
        == selected_factory
    ].iloc[0]


    # FACTORY COMPARISON
    st.subheader("🏭 Factory Assignment Comparison")

    col1, col2 = st.columns(2)

    with col1:
        st.info(
            f"""
            **Current Factory**

            {what_if_scenario['Current Factory']}
            """
        )

    with col2:
        st.success(
            f"""
            **Recommended Factory**

            {what_if_scenario['Recommended Factory']}
            """
        )


    # OPERATIONAL IMPACT METRICS
    st.subheader("📊 Expected Scenario Impact")

    col1, col2, col3 = st.columns(3)

    with col1:

        lead_time_reduction = (
            what_if_scenario["Lead Time Reduction (%)"]
        )

        st.metric(
            "Expected Lead Time Reduction",
            f"{lead_time_reduction:.2f}%"
        )

    with col2:

        recommendation_score = (
            what_if_scenario["Recommendation Score"]
        )

        st.metric(
            "Recommendation Score",
            f"{recommendation_score:.2f}"
        )

    with col3:

        scenario_reliability = (
            what_if_scenario["Scenario Reliability"]
        )

        st.metric(
            "Scenario Reliability",
            scenario_reliability
        )


    # RISK AND STATUS INFORMATION
    st.subheader("⚠️ Risk and Recommendation Assessment")

    col1, col2 = st.columns(2)

    with col1:

        profit_risk = what_if_scenario["Profit Risk"]

        if profit_risk == "High Profit Risk":

            st.error(
                f"Profit Risk: {profit_risk}"
            )

        else:

            st.success(
                f"Profit Risk: {profit_risk}"
            )


    with col2:

        recommendation_status = (
            what_if_scenario["Recommendation Status"]
        )

        if recommendation_status == "Strong Candidate":

            st.success(
                f"Recommendation Status: {recommendation_status}"
            )

        elif recommendation_status == "Potential Candidate":

            st.warning(
                f"Recommendation Status: {recommendation_status}"
            )

        else:

            st.info(
                f"Recommendation Status: {recommendation_status}"
            )


    # DECISION SUMMARY
    st.subheader("💡 Decision Summary")

    if lead_time_reduction > 0:

        if recommendation_status == "Strong Candidate":

            st.success(
                f"""
                This scenario is a strong reassignment candidate.

                Reassigning **{selected_product}** from
                **{what_if_scenario['Current Factory']}**
                to **{what_if_scenario['Recommended Factory']}**
                is expected to reduce lead time by
                approximately **{lead_time_reduction:.2f}%**.
                """
            )

        elif recommendation_status == "Potential Candidate":

            st.warning(
                f"""
                This scenario shows positive operational improvement.

                The recommended factory configuration may reduce
                lead time by approximately **{lead_time_reduction:.2f}%**,
                but additional operational or financial review is recommended.
                """
            )

        else:

            st.info(
                f"""
                This scenario demonstrates some positive lead-time improvement
                of approximately **{lead_time_reduction:.2f}%**.

                However, the overall recommendation remains Low Priority
                because other decision factors, such as profit risk,
                scenario reliability, or the composite recommendation score,
                reduce its overall priority.
                """
            )

    else:

        st.warning(
            f"""
            This factory reassignment is not expected to improve
            lead-time performance.

            The estimated lead-time change is
            **{lead_time_reduction:.2f}%**.

            Therefore, this scenario should not be prioritized
            for operational reassignment.
            """
        )



# RECOMMENDATION DASHBOARD
st.divider()

st.header("📊 Recommendation Dashboard")

st.write(
    """
    Explore ranked factory reassignment recommendations and identify
    the scenarios with the strongest expected operational benefits.
    """
)

# DASHBOARD FILTERS
st.subheader("Filter Recommendations")

filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)

with filter_col1:
    selected_dashboard_product = st.selectbox(
        "Product",
        ["All"] + sorted(recommendations["Product Name"].unique()),
        key="dashboard_product"
    )

with filter_col2:
    selected_dashboard_region = st.selectbox(
        "Region",
        ["All"] + sorted(recommendations["Region"].unique()),
        key="dashboard_region"
    )

with filter_col3:
    selected_dashboard_ship_mode = st.selectbox(
        "Ship Mode",
        ["All"] + sorted(recommendations["Ship Mode"].unique()),
        key="dashboard_ship_mode"
    )

with filter_col4:
    selected_dashboard_status = st.selectbox(
        "Recommendation Status",
        ["All"] + sorted(
            recommendations["Recommendation Status"].unique()
        ),
        key="dashboard_status"
    )


# CREATE FILTERED DATASET
dashboard_data = recommendations.copy()

if selected_dashboard_product != "All":
    dashboard_data = dashboard_data[
        dashboard_data["Product Name"]
        == selected_dashboard_product
    ]

if selected_dashboard_region != "All":
    dashboard_data = dashboard_data[
        dashboard_data["Region"]
        == selected_dashboard_region
    ]

if selected_dashboard_ship_mode != "All":
    dashboard_data = dashboard_data[
        dashboard_data["Ship Mode"]
        == selected_dashboard_ship_mode
    ]

if selected_dashboard_status != "All":
    dashboard_data = dashboard_data[
        dashboard_data["Recommendation Status"]
        == selected_dashboard_status
    ]


# SORT RECOMMENDATIONS
dashboard_data = dashboard_data.sort_values(
    by="Recommendation Score",
    ascending=False
)


# DASHBOARD SUMMARY METRICS
st.subheader("Recommendation Summary")

summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)

with summary_col1:
    st.metric(
        "Available Scenarios",
        len(dashboard_data)
    )

with summary_col2:
    strong_count = (
        dashboard_data["Recommendation Status"]
        == "Strong Candidate"
    ).sum()

    st.metric(
        "Strong Candidates",
        strong_count
    )

with summary_col3:
    potential_count = (
        dashboard_data["Recommendation Status"]
        == "Potential Candidate"
    ).sum()

    st.metric(
        "Potential Candidates",
        potential_count
    )

with summary_col4:
    if len(dashboard_data) > 0:
        average_improvement = dashboard_data[
            "Lead Time Reduction (%)"
        ].mean()

        st.metric(
            "Avg. Lead Time Reduction",
            f"{average_improvement:.2f}%"
        )
    else:
        st.metric(
            "Avg. Lead Time Reduction",
            "N/A"
        )


# DISPLAY RECOMMENDATIONS
st.subheader("Ranked Factory Reassignment Recommendations")

if dashboard_data.empty:

    st.warning(
        "No recommendations match the selected filters."
    )

else:

    dashboard_display_columns = [
        "Product Name",
        "Region",
        "Ship Mode",
        "Current Factory",
        "Recommended Factory",
        "Lead Time Reduction (%)",
        "Scenario Reliability",
        "Profit Risk",
        "Recommendation Score",
        "Recommendation Status"
    ]

    st.dataframe(
        dashboard_data[
            dashboard_display_columns
        ],
        use_container_width=True,
        hide_index=True
    )




# RISK & IMPACT PANEL
st.divider()

st.header("⚠️ Risk & Impact Panel")

st.write(
    """
    This section highlights profit-related risks and scenario reliability
    to support informed factory reassignment decisions.
    """
)


# CALCULATE RISK METRICS
total_scenarios = len(recommendations)

high_profit_risk_count = (
    recommendations["Profit Risk"]
    == "High Profit Risk"
).sum()

stable_profit_count = (
    recommendations["Profit Risk"]
    == "Stable / Positive"
).sum()

high_reliability_count = (
    recommendations["Scenario Reliability"]
    == "High"
).sum()

average_recommendation_score = (
    recommendations["Recommendation Score"]
    .mean()
)


# DISPLAY RISK METRICS
risk_col1, risk_col2, risk_col3, risk_col4 = st.columns(4)

with risk_col1:
    st.metric(
        "Total Scenarios",
        total_scenarios
    )

with risk_col2:
    st.metric(
        "High Profit Risk",
        high_profit_risk_count
    )

with risk_col3:
    st.metric(
        "High Reliability",
        high_reliability_count
    )

with risk_col4:
    st.metric(
        "Average Recommendation Score",
        f"{average_recommendation_score:.2f}"
    )


# PROFIT RISK DISTRIBUTION
st.subheader("Profit Risk Distribution")

profit_risk_distribution = (
    recommendations["Profit Risk"]
    .value_counts()
)

st.bar_chart(profit_risk_distribution)

st.caption(
    """
    This chart represents the overall profit risk distribution across
    all available recommendation scenarios and is not affected by the
    filters applied in the Recommendation Dashboard.
    """
)

# HIGH-RISK SCENARIOS
st.subheader("High Profit Risk Scenarios")

high_risk_scenarios = recommendations[
    recommendations["Profit Risk"]
    == "High Profit Risk"
].copy()


if high_risk_scenarios.empty:

    st.success(
        "No high-profit-risk reassignment scenarios were identified."
    )

else:

    st.warning(
        f"{len(high_risk_scenarios)} scenario(s) are classified as "
        "High Profit Risk and should be reviewed before implementation."
    )

    high_risk_scenarios = high_risk_scenarios.sort_values(
        by="Recommendation Score",
        ascending=False
    )

    risk_display_columns = [
        "Product Name",
        "Region",
        "Ship Mode",
        "Current Factory",
        "Recommended Factory",
        "Lead Time Reduction (%)",
        "Scenario Reliability",
        "Recommendation Score",
        "Recommendation Status"
    ]

    st.dataframe(
        high_risk_scenarios[
            risk_display_columns
        ],
        use_container_width=True,
        hide_index=True
    )


# DECISION GUIDANCE
st.subheader("💡 Decision Guidance")

st.info(
    """
    Strong Candidate recommendations with positive lead-time improvement
    and stable profit conditions should generally receive higher priority.

    High Profit Risk scenarios should be reviewed carefully before
    operational implementation, even when the predicted lead-time
    improvement appears favorable.
    """
)    


# --OPTIMIZATION PRIORITY SLIDER--
st.divider()

st.header(" Optimization Priority")

st.write(
    """
    Adjust the optimization priority to explore how factory
    recommendations change when operational speed or profit
    stability is given greater importance.
    """
)

# PRIORITY SLIDER
speed_priority = st.slider(
    "Optimization Priority:  Profit Stability ← →  Speed",
    min_value=0,
    max_value=100,
    value=50,
    step=10,
    help=(
        "Move left to prioritize profit stability and right "
        "to prioritize lead-time improvement."
    )
)

# DISPLAY CURRENT PRIORITY
profit_priority = 100 - speed_priority

priority_col1, priority_col2 = st.columns(2)

with priority_col1:
    st.metric(
        "Speed Priority",
        f"{speed_priority}%"
    )

with priority_col2:
    st.metric(
        "Profit Stability Priority",
        f"{profit_priority}%"
    )


# CREATE INTERACTIVE PRIORITY DATA
priority_data = recommendations.copy()

# -> SPEED SCORE
# Normalize Lead Time Reduction so that scenarios with
# higher positive improvement receive a higher score.

lead_time_min = priority_data[
    "Lead Time Reduction (%)"
].min()

lead_time_max = priority_data[
    "Lead Time Reduction (%)"
].max()

if lead_time_max != lead_time_min:

    priority_data["Interactive_Speed_Score"] = (
        (
            priority_data["Lead Time Reduction (%)"]
            - lead_time_min
        )
        /
        (
            lead_time_max
            - lead_time_min
        )
    )

else:

    priority_data["Interactive_Speed_Score"] = 0


# -> PROFIT STABILITY SCORE
# Use the existing Profit Risk classification as a
# profit-stability proxy.

priority_data["Interactive_Profit_Score"] = (
    priority_data["Profit Risk"]
    .map(
        {
            "Stable / Positive": 1.0,
            "High Profit Risk": 0.0
        }
    )
    .fillna(0.5)
)


# -> INTERACTIVE PRIORITY SCORE
# This score is created only for interactive dashboard
# exploration and does not replace the validated
# Recommendation Score from the analytical model.

priority_data["Interactive_Priority_Score"] = (
    priority_data["Interactive_Speed_Score"]
    * (speed_priority / 100)
    +
    priority_data["Interactive_Profit_Score"]
    * (profit_priority / 100)
)


# SORT BASED ON USER PRIORITY
priority_data = priority_data.sort_values(
    by="Interactive_Priority_Score",
    ascending=False
)


# PRIORITY MODE MESSAGE
if speed_priority > 50:

    st.success(
        "⚡ Speed-focused optimization is active. "
        "Factory scenarios with stronger predicted lead-time "
        "improvement receive greater priority."
    )

elif speed_priority < 50:

    st.success(
        "💰 Profit-stability-focused optimization is active. "
        "Scenarios with Stable / Positive profit conditions "
        "receive greater priority."
    )

else:

    st.info(
        "⚖️ Balanced optimization is active. "
        "Lead-time improvement and profit stability are "
        "given equal importance."
    )


# DISPLAY TOP PRIORITY RECOMMENDATIONS
st.subheader("Top Recommendations Based on Selected Priority")

top_priority_data = priority_data.head(10)

priority_display_columns = [
    "Product Name",
    "Region",
    "Ship Mode",
    "Current Factory",
    "Recommended Factory",
    "Lead Time Reduction (%)",
    "Profit Risk",
    "Scenario Reliability",
    "Interactive_Priority_Score",
    "Recommendation Status"
]

st.dataframe(
    top_priority_data[
        priority_display_columns
    ],
    use_container_width=True,
    hide_index=True
)


# EXPLANATION
st.caption(
    """
    Note: The Interactive Priority Score is created for
    dashboard exploration based on the selected Speed vs
    Profit Stability preference. It does not replace the
    validated Recommendation Score generated by the
    analytical recommendation model.
    """
)


# Executive Decision Summary
st.divider()

st.header(" Executive Decision Summary")

st.write(
    """
    This section come up with a high-level summary of the factory
    reallocation opportunities recognized by the recommendation system.
    """
)


# CALCULATE EXECUTIVE METRICS
strong_candidates = recommendations[
    recommendations["Recommendation Status"]
    == "Strong Candidate"
]

potential_candidates = recommendations[
    recommendations["Recommendation Status"]
    == "Potential Candidate"
]

eligible_recommendations = recommendations[
    recommendations["Lead Time Reduction (%)"] > 0
]


# Summary metrics
exec_col1, exec_col2, exec_col3, exec_col4 = st.columns(4)


with exec_col1:

    st.metric(
        "Strong Candidates",
        len(strong_candidates)
    )


with exec_col2:

    st.metric(
        "Potential Candidates",
        len(potential_candidates)
    )


with exec_col3:

    if len(eligible_recommendations) > 0:

        best_improvement = eligible_recommendations[
            "Lead Time Reduction (%)"
        ].max()

        st.metric(
            "Best Lead-Time Improvement",
            f"{best_improvement:.2f}%"
        )

    else:

        st.metric(
            "Best Lead-Time Improvement",
            "N/A"
        )


with exec_col4:

    stable_recommendations = recommendations[
        recommendations["Profit Risk"]
        == "Stable / Positive"
    ]

    stable_percentage = (
        len(stable_recommendations)
        / len(recommendations)
    ) * 100

    st.metric(
        "Stable Profit Scenarios",
        f"{stable_percentage:.1f}%"
    )


# EXECUTIVE INSIGHTS
st.subheader(" Key Decision Insights")


if len(strong_candidates) > 0:

    best_recommendation = strong_candidates.sort_values(
        by="Recommendation Score",
        ascending=False
    ).iloc[0]


    st.success(
        f"""
        **Highest-Priority Recommendation**

        The strongest identified opportunity is the reassignment of
        **{best_recommendation['Product Name']}** for the
        **{best_recommendation['Region']}** region using
        **{best_recommendation['Ship Mode']}** shipping.

        The recommended factory is
        **{best_recommendation['Recommended Factory']}**.

        This scenario is expected to reduce lead time by approximately
        **{best_recommendation['Lead Time Reduction (%)']:.2f}%**
        and has a recommendation score of
        **{best_recommendation['Recommendation Score']:.2f}**.
        """
    )


# MANAGEMENT RECOMMENDATION
st.subheader(" Management Recommendation")


st.info(
    f"""
    Based on the recommendation analysis, management should prioritize
    the **{len(strong_candidates)} Strong Candidate** scenarios that
    demonstrate positive lead-time improvement and satisfy the
    refined recommendation eligibility criteria.

    The **{len(potential_candidates)} Potential Candidate** scenarios
    may also be considered after additional operational or financial
    review.

    Scenarios classified as **Low Priority** should generally not be
    prioritized for immediate factory reassignment unless future
    operational conditions change.
    """
)


# IMPLEMENTATION NOTE
st.caption(
    """
    The recommendations presented in this dashboard are based on
    historical data, predictive modeling, scenario simulation, and
    the defined recommendation scoring framework. Final operational
    decisions should consider additional real-world factors that may
    not be fully represented in the available dataset.
    """
)