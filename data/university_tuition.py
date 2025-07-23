import pandas as pd
import dash
from dash import dcc, html, Input, Output, callback_context
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load data
df = pd.read_excel("data/cleaned_tuition_fees_updated.xlsx")

# Clean data: remove rows with no tuition info and rename column
df = df.dropna(subset=["tuition_fee_numeric"])
df = df.rename(columns={"tuition_fee_numeric": "tuition_per_semester"})

# Start Dash app
app = dash.Dash(__name__)
app.title = "Tuition Fees Dashboard"

# Custom CSS styles
custom_styles = {
    'container': {
        'fontFamily': 'Arial, sans-serif',
        'margin': '0 auto',
        'maxWidth': 'auto',
        'padding': '2rem'
    },
    'header': {
        'textAlign': 'center',
        'color': '#2c3e50',
        'marginBottom': '30px',
        'fontSize': '2.5em',
        'fontWeight': 'bold'
    },
    'control_panel': {
        'backgroundColor': '#f8f9fa',
        'padding': '20px',
        'borderRadius': '10px',
        'marginBottom': '20px',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
    },
    'dropdown': {
        'width': '30%',
        'display': 'inline-block',
        'marginRight': '5%'
    },
    'slider_container': {
        'width': '60%',
        'display': 'inline-block',
        'marginRight': '5%'
    },
    'button_container': {
        'width': '25%',
        'display': 'inline-block',
        'verticalAlign': 'top'
    },
    'button': {
        'backgroundColor': '#3498db',
        'color': 'white',
        'border': 'none',
        'padding': '10px 20px',
        'margin': '5px',
        'borderRadius': '5px',
        'cursor': 'pointer',
        'fontSize': '14px',
        'width': '100%'
    },
    'stats_container': {
        'display': 'flex',
        'justifyContent': 'space-around',
        'marginBottom': '20px'
    },
    'stats_card': {
        'backgroundColor': '#fff',
        'padding': '3rem',
        'borderRadius': '12px',
        'textAlign': 'center',
        'boxShadow': '0 4px 8px rgba(0,0,0,0.15)',
        'minWidth': '180px',
        'fontSize': '24px'
    }
}

# Layout
app.layout = html.Div([
    html.H1("📊 Dashboard ค่าเทอมต่อภาคการศึกษาจากเว็ปไซต์ MyTCAS(68) โดยเฉพาะในสาขา วิศวกรรมคอมพิวเตอร์, วิศวกรรมปัญญาประดิษฐ์ และชื่อสาขาอื่นๆ ที่เกี่ยวข้อง", style=custom_styles['header']),
    
    # Control Panel
    html.Div([
        # html.H3("🎛️ Setting", style={'marginBottom': '15px', 'color': '#34495e'}),
        
        html.Div([
            # Faculty Dropdown
            html.Div([
                html.Label("เลือกคณะ:", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                dcc.Dropdown(
                    id="faculty-dropdown",
                    options=[{"label": fac, "value": fac} for fac in sorted(df['faculty'].unique()) if pd.notna(fac)],
                    value=None,
                    placeholder="เลือกคณะ...",
                    multi=False,
                    clearable=True
                )
            ], style=custom_styles['dropdown']),
            
            # Tuition Range Slider
            html.Div([
                html.Label("ช่วงค่าเทอม (บาท):", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                dcc.RangeSlider(
                    id="tuition-range-slider",
                    min=0,
                    max=int(df['tuition_per_semester'].max()),
                    step=5000,
                    marks={i: f'{i:,}' for i in range(0, int(df['tuition_per_semester'].max()) + 1, 50000)},
                    value=[0, int(df['tuition_per_semester'].max())],
                    tooltip={"placement": "bottom", "always_visible": True}
                )
            ], style=custom_styles['slider_container']),
            
            # Action Buttons
            html.Div([
                html.Label("แสดงข้อมูล:", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                html.Button("🔝 Top 10 แพงสุด", id="top10-btn", style=custom_styles['button']),
                html.Button("🔻 Top 10 ถูกสุด", id="bottom10-btn", style=custom_styles['button']),
                html.Button("📋 ทั้งหมด", id="all-btn", style=custom_styles['button'])
            ], style=custom_styles['button_container'])
        ])
    ], style=custom_styles['control_panel']),
    
    # Statistics Cards
    html.Div(id="stats-cards", children=[], style=custom_styles['stats_container']),
    
    # Main Chart
    html.Div([
    html.H2(id="graph-title", style={
        'textAlign': 'center',
        'marginTop': '2rem',
        'marginBottom': '2rem',
        'fontSize': '2rem',
        'color': '#2c3e50'
    }),
    dcc.Graph(id="tuition-bar", style={'height': '50rem'})
]),
    
    # Summary Table
    html.Div([
        html.H3("📋 ตารางสรุปข้อมูล", style={'color': '#34495e', 'marginTop': '30px'}),
        html.Div(id="summary-table")
    ])
    
], style=custom_styles['container'])

# Callback to update everything
@app.callback(
    [Output("tuition-bar", "figure"),
     Output("stats-cards", "children"),
     Output("summary-table", "children"),
     Output("graph-title", "children")],
    [Input("faculty-dropdown", "value"),
     Input("tuition-range-slider", "value"),
     Input("top10-btn", "n_clicks"),
     Input("bottom10-btn", "n_clicks"),
     Input("all-btn", "n_clicks")]
)
def update_dashboard(selected_faculty, tuition_range, top10_clicks, bottom10_clicks, all_clicks):
    # Filter data based on selections
    filtered_df = df.copy()
    
    # Filter by faculty
    if selected_faculty:
        filtered_df = filtered_df[filtered_df["faculty"] == selected_faculty]
    
    # Filter by tuition range
    if tuition_range:
        filtered_df = filtered_df[
            (filtered_df["tuition_per_semester"] >= tuition_range[0]) & 
            (filtered_df["tuition_per_semester"] <= tuition_range[1])
        ]
    
    # Determine which button was clicked
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    display_df = filtered_df.copy()
    
    chart_title = "เปรียบเทียบค่าเทอมต่อภาคการศึกษา"
    
    if 'top10-btn' in changed_id:
        display_df = filtered_df.nlargest(10, 'tuition_per_semester')
        chart_title = "🔝 ค่าเทอมแพงสุด 10 อันดับแรก"
    elif 'bottom10-btn' in changed_id:
        display_df = filtered_df.nsmallest(10, 'tuition_per_semester')
        chart_title = "🔻 ค่าเทอมถูกสุด 10 อันดับแรก"
    elif 'all-btn' in changed_id:
        chart_title = "📊 ค่าเทอมทั้งหมด"
    
    # Sort for better visualization
    display_df = display_df.sort_values("tuition_per_semester", ascending=False)
    
    # Create main chart
    if len(display_df) > 0:
        fig = px.bar(
            display_df,
            x="university",
            y="tuition_per_semester",
            color="campus",
            hover_data=["program", "faculty"],
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        fig.update_layout(
            margin=dict(t=100),
            xaxis_title="มหาวิทยาลัย",
            yaxis_title="ค่าเทอม (บาท)",
            template="plotly_white",
            xaxis_tickangle=-45,
            font=dict(size=12),
            title_font_size=30,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        # Add value labels on bars
        fig.update_traces(texttemplate='%{y:,.0f}', textposition='outside')
        
    else:
        fig = go.Figure()
        fig.add_annotation(
            text="ไม่มีข้อมูลที่ตรงตามเงื่อนไขที่เลือก",
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            font=dict(size=16, color="gray")
        )
        fig.update_layout(template="plotly_white", title=chart_title)
    
    # Create statistics cards
    if len(filtered_df) > 0:
        stats_cards = [
            html.Div([
                html.H4(f"{len(filtered_df):,}", style={'color': '#3498db', 'margin': '0'}),
                html.P("จำนวนหลักสูตร", style={'margin': '0', 'fontSize': '12px'})
            ], style=custom_styles['stats_card']),
            
            html.Div([
                html.H4(f"{filtered_df['tuition_per_semester'].mean():,.0f}", style={'color': '#e74c3c', 'margin': '0'}),
                html.P("ค่าเทอมเฉลี่ย (บาท)", style={'margin': '0', 'fontSize': '12px'})
            ], style=custom_styles['stats_card']),
            
            html.Div([
                html.H4(f"{filtered_df['tuition_per_semester'].max():,.0f}", style={'color': '#e67e22', 'margin': '0'}),
                html.P("ค่าเทอมสูงสุด (บาท)", style={'margin': '0', 'fontSize': '12px'})
            ], style=custom_styles['stats_card']),
            
            html.Div([
                html.H4(f"{filtered_df['tuition_per_semester'].min():,.0f}", style={'color': '#27ae60', 'margin': '0'}),
                html.P("ค่าเทอมต่ำสุด (บาท)", style={'margin': '0', 'fontSize': '12px'})
            ], style=custom_styles['stats_card']),
            
            html.Div([
                html.H4(f"{len(filtered_df['university'].unique()):,}", style={'color': '#9b59b6', 'margin': '0'}),
                html.P("จำนวนมหาวิทยาลัย", style={'margin': '0', 'fontSize': '12px'})
            ], style=custom_styles['stats_card'])
        ]
    else:
        stats_cards = []
    
    # Create summary table
    if len(display_df) > 0:
        table_data = display_df[['university', 'faculty', 'program', 'campus', 'tuition_per_semester']].head(20)
        table_rows = []
        
        # Table header
        table_rows.append(
            html.Tr([
                html.Th("มหาวิทยาลัย", style={'padding': '10px', 'backgroundColor': '#34495e', 'color': 'white'}),
                html.Th("คณะ", style={'padding': '10px', 'backgroundColor': '#34495e', 'color': 'white'}),
                html.Th("หลักสูตร", style={'padding': '10px', 'backgroundColor': '#34495e', 'color': 'white'}),
                html.Th("วิทยาเขต", style={'padding': '10px', 'backgroundColor': '#34495e', 'color': 'white'}),
                html.Th("ค่าเทอม (บาท)", style={'padding': '10px', 'backgroundColor': '#34495e', 'color': 'white'})
            ])
        )
        
        # Table rows
        for idx, row in table_data.iterrows():
            table_rows.append(
                html.Tr([
                    html.Td(row['university'], style={'padding': '8px', 'borderBottom': '1px solid #ddd'}),
                    html.Td(row['faculty'], style={'padding': '8px', 'borderBottom': '1px solid #ddd'}),
                    html.Td(row['program'], style={'padding': '8px', 'borderBottom': '1px solid #ddd', 'fontSize': '12px'}),
                    html.Td(row['campus'], style={'padding': '8px', 'borderBottom': '1px solid #ddd'}),
                    html.Td(f"{row['tuition_per_semester']:,.0f}", 
                           style={'padding': '8px', 'borderBottom': '1px solid #ddd', 'textAlign': 'right', 'fontWeight': 'bold'})
                ])
            )
        
        summary_table = html.Table(
            table_rows,
            style={
                'width': '100%',
                'borderCollapse': 'collapse',
                'backgroundColor': 'white',
                'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                'borderRadius': '8px',
                'overflow': 'hidden'
            }
        )
    else:
        summary_table = html.P("ไม่มีข้อมูลแสดง", style={'textAlign': 'center', 'color': 'gray'})
    
    return fig, stats_cards, summary_table, chart_title

# Run server
if __name__ == "__main__":
    app.run(debug=True)