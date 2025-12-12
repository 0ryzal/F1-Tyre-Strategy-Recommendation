import streamlit as st
import sys
sys.path.append('.')
from pit_stop_strategy_engine import F1PitStopStrategyEngine, format_strategy_output
import plotly.graph_objects as go
import plotly.express as px

# Page config
st.set_page_config(
    page_title="F1 Pit Stop Strategy Planner",
    page_icon="⛽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Titillium+Web:wght@300;400;600;700;900&display=swap');
    
    * {
        font-family: 'Titillium Web', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #15151E 0%, #1E1E2E 100%);
    }
    
    .strategy-header {
        background: linear-gradient(90deg, #E10600 0%, #FF1E1E 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(225, 6, 0, 0.3);
    }
    
    .strategy-title {
        font-size: 2.5rem;
        font-weight: 900;
        color: white;
        margin: 0;
        text-transform: uppercase;
    }
    
    .stint-card {
        background: linear-gradient(135deg, rgba(225, 6, 0, 0.15) 0%, rgba(30, 30, 46, 0.8) 100%);
        border-left: 5px solid #E10600;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .pit-stop-marker {
        background: #FF6B00;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-weight: 700;
        display: inline-block;
        margin: 0.5rem 0;
    }
    
    h1, h2, h3 {
        color: white !important;
    }
    
    .stSelectbox label, .stSlider label, .stNumberInput label, .stRadio label {
        color: white !important;
        font-weight: 600 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="strategy-header">
        <h1 class="strategy-title">⛽ F1 Pit Stop Strategy Planner</h1>
        <p style="color: rgba(255,255,255,0.9); font-size: 1.1rem; margin-top: 0.5rem;">
            Complete Race Strategy: Pit Stops, Compound Selection & Timing
        </p>
    </div>
""", unsafe_allow_html=True)

# Sidebar inputs
st.sidebar.header("🏁 Race Configuration")

# Basic race info
st.sidebar.subheader("📊 Race Details")
total_laps = st.sidebar.number_input("Total Race Laps", 50, 78, 58)
circuit_name = st.sidebar.text_input("Circuit Name", "Monaco")

# Weather conditions
st.sidebar.subheader("🌤️ Weather Conditions")
col1, col2 = st.sidebar.columns(2)
air_temp = col1.slider("Air Temp (°C)", 10, 45, 28)
track_temp = col2.slider("Track Temp (°C)", 15, 65, 35, help="Higher temps = harder compounds")
rainfall = st.sidebar.checkbox("🌧️ Rainfall", value=False)

# Track characteristics
st.sidebar.subheader("🛣️ Track Characteristics")
tyre_severity = st.sidebar.select_slider(
    "Tyre Degradation Severity",
    options=["low", "medium", "high"],
    value="medium",
    help="Track abrasiveness - affects tyre wear rate"
)

# Generate button
st.sidebar.markdown("---")
generate_button = st.sidebar.button("🚀 Generate Strategy Options", use_container_width=True)

# Main content
if generate_button:
    # Initialize engine
    engine = F1PitStopStrategyEngine()
    
    # Generate strategies
    with st.spinner("🔄 Calculating optimal pit stop strategies..."):
        strategies = engine.generate_strategies(
            total_race_laps=total_laps,
            track_temp=track_temp,
            air_temp=air_temp,
            tyre_severity=tyre_severity,
            rainfall=rainfall
        )
    
    # Display race info summary
    st.markdown("### 📋 Race Summary")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Circuit", circuit_name)
    with col2:
        st.metric("Total Laps", total_laps)
    with col3:
        st.metric("Track Temp", f"{track_temp}°C")
    with col4:
        st.metric("Conditions", "🌧️ Wet" if rainfall else "☀️ Dry")
    
    st.markdown("---")
    
    # Display each strategy
    for idx, strategy in enumerate(strategies, 1):
        st.markdown(f"## Option {idx}: {strategy.strategy_name}")
        
        # Strategy overview
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Pit Stops", f"{strategy.total_pit_stops} ⛽")
        with col2:
            st.metric("Risk Level", strategy.risk_level)
        with col3:
            st.metric("Confidence", f"{strategy.confidence_score*100:.1f}%")
        with col4:
            race_time_min = int(strategy.estimated_race_time // 60)
            race_time_sec = int(strategy.estimated_race_time % 60)
            st.metric("Est. Time", f"{race_time_min}m {race_time_sec}s")
        
        # Stint breakdown
        st.markdown("### 🔧 Stint-by-Stint Breakdown")
        
        # Create timeline visualization
        fig = go.Figure()
        
        colors = {
            'SOFT': '#FF0000',
            'MEDIUM': '#FFD700',
            'HARD': '#FFFFFF',
            'INTERMEDIATE': '#00FF00',
            'WET': '#0000FF'
        }
        
        for stint in strategy.stint_plans:
            fig.add_trace(go.Bar(
                name=f"Stint {stint.stint_number}: {stint.compound}",
                x=[stint.total_laps],
                y=[f"Stint {stint.stint_number}"],
                orientation='h',
                marker=dict(
                    color=colors.get(stint.compound, '#888888'),
                    line=dict(color='rgba(0,0,0,0.5)', width=2)
                ),
                text=f"{stint.compound}<br>{stint.total_laps} laps<br>L{stint.start_lap}-{stint.end_lap}",
                textposition='inside',
                textfont=dict(size=14, color='black', family='Titillium Web', weight='bold'),
                hovertemplate=f"<b>{stint.compound}</b><br>" +
                            f"Laps: {stint.start_lap} → {stint.end_lap}<br>" +
                            f"Duration: {stint.total_laps} laps<br>" +
                            "<extra></extra>"
            ))
        
        fig.update_layout(
            barmode='stack',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', family='Titillium Web'),
            height=200,
            margin=dict(l=20, r=20, t=20, b=20),
            showlegend=False,
            xaxis=dict(
                title="Laps",
                showgrid=True,
                gridcolor='rgba(255,255,255,0.1)',
                range=[0, total_laps]
            ),
            yaxis=dict(
                showgrid=False,
                showticklabels=False
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed stint cards
        for stint in strategy.stint_plans:
            st.markdown(f"""
                <div class="stint-card">
                    <h4 style="color: #E10600; margin-top: 0;">Stint {stint.stint_number}: {stint.compound} Compound</h4>
                    <p style="color: rgba(255,255,255,0.9); font-size: 1.1rem;">
                        📍 <strong>Laps:</strong> {stint.start_lap} → {stint.end_lap} ({stint.total_laps} laps total)
                    </p>
                    {f'<div class="pit-stop-marker">⛽ PIT STOP after Lap {stint.pit_after_lap}</div>' if stint.pit_after_lap > 0 else '<p style="color: #00FF00;">✅ FINISH - No pit stop</p>'}
                </div>
            """, unsafe_allow_html=True)
        
        # Strategy reasoning
        st.markdown("### 💡 Strategy Reasoning")
        st.info(strategy.reasoning)
        
        # Pit stop timing chart
        if strategy.total_pit_stops > 0:
            st.markdown("### ⏱️ Pit Stop Timing")
            pit_laps = [stint.pit_after_lap for stint in strategy.stint_plans if stint.pit_after_lap > 0]
            
            fig_pit = go.Figure()
            
            fig_pit.add_trace(go.Scatter(
                x=list(range(1, total_laps + 1)),
                y=[1] * total_laps,
                mode='lines',
                line=dict(color='rgba(255,255,255,0.3)', width=2),
                name='Race Progress',
                showlegend=False
            ))
            
            for i, pit_lap in enumerate(pit_laps, 1):
                fig_pit.add_trace(go.Scatter(
                    x=[pit_lap],
                    y=[1],
                    mode='markers+text',
                    marker=dict(
                        size=20,
                        color='#FF6B00',
                        symbol='diamond',
                        line=dict(color='white', width=2)
                    ),
                    text=f"PIT {i}",
                    textposition='top center',
                    textfont=dict(size=12, color='#FF6B00', family='Titillium Web', weight='bold'),
                    name=f'Pit Stop {i}',
                    hovertemplate=f"<b>Pit Stop {i}</b><br>Lap: {pit_lap}<br><extra></extra>"
                ))
            
            fig_pit.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', family='Titillium Web'),
                height=150,
                margin=dict(l=20, r=20, t=20, b=40),
                showlegend=False,
                xaxis=dict(
                    title="Lap Number",
                    showgrid=True,
                    gridcolor='rgba(255,255,255,0.1)',
                    range=[0, total_laps + 1]
                ),
                yaxis=dict(
                    showgrid=False,
                    showticklabels=False,
                    range=[0.8, 1.2]
                )
            )
            
            st.plotly_chart(fig_pit, use_container_width=True)
        
        st.markdown("---")
    
    # Comparison table
    if len(strategies) > 1:
        st.markdown("## 📊 Strategy Comparison")
        
        comparison_data = {
            'Strategy': [s.strategy_name for s in strategies],
            'Pit Stops': [s.total_pit_stops for s in strategies],
            'Compounds Used': [' → '.join([stint.compound for stint in s.stint_plans]) for s in strategies],
            'Est. Time (min)': [f"{s.estimated_race_time//60:.0f}:{s.estimated_race_time%60:02.0f}" for s in strategies],
            'Risk Level': [s.risk_level for s in strategies],
            'Confidence': [f"{s.confidence_score*100:.1f}%" for s in strategies]
        }
        
        df = pd.DataFrame(comparison_data)
        st.dataframe(df, use_container_width=True)

else:
    # Welcome screen
    st.markdown("### 👋 Welcome to F1 Pit Stop Strategy Planner")
    
    st.info("""
    🏎️ **This tool helps you plan the complete pit stop strategy for an F1 race:**
    
    1️⃣ **Number of Pit Stops**: Should you do 1-stop, 2-stop, or 3-stop?
    
    2️⃣ **Tyre Compound Selection**: Which compounds to use in each stint (SOFT, MEDIUM, HARD)?
    
    3️⃣ **Pit Stop Timing**: On which lap should you pit?
    
    4️⃣ **Strategy Comparison**: Compare multiple strategies with confidence scores
    
    **How to use:**
    - Configure race parameters in the left sidebar
    - Click "Generate Strategy Options" button
    - Review multiple strategy options with detailed breakdowns
    - Compare estimated race times and risk levels
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div style="background: rgba(225, 6, 0, 0.1); padding: 1.5rem; border-radius: 10px; text-align: center;">
                <h3 style="color: #E10600;">⛽ Pit Stops</h3>
                <p style="color: rgba(255,255,255,0.8);">Optimal number and timing</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style="background: rgba(225, 6, 0, 0.1); padding: 1.5rem; border-radius: 10px; text-align: center;">
                <h3 style="color: #E10600;">🏎️ Compounds</h3>
                <p style="color: rgba(255,255,255,0.8);">SOFT, MEDIUM, or HARD per stint</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div style="background: rgba(225, 6, 0, 0.1); padding: 1.5rem; border-radius: 10px; text-align: center;">
                <h3 style="color: #E10600;">⏱️ Timing</h3>
                <p style="color: rgba(255,255,255,0.8);">Exact lap for each pit stop</p>
            </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style="text-align: center; color: rgba(255,255,255,0.5); padding: 2rem 0; margin-top: 3rem; border-top: 1px solid rgba(255,255,255,0.1);">
        <p>⛽ F1 Pit Stop Strategy Planner | Rule-based Strategy Engine</p>
        <p style="font-size: 0.9rem;">Optimized for modern F1 regulations and tyre compounds</p>
    </div>
""", unsafe_allow_html=True)
