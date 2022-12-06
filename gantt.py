###  1. LIBRARY
import plotly.graph_objects as go
import pandas as pd
import datetime
import numpy as np
import textwrap


TITLE_A = "Zeitplan"
TITLE_B = "für die Klimaschutz-Austauschplattform"
TITLE = f"<b>{TITLE_A}</b><br>" + TITLE_B

df = pd.read_csv(r'C:/Users/david/Plotly Gantt Chart/Zeit-und Kostentabelle.csv')

np.random.seed(3452)
random_color_value = np.random.randint(255, size=(df['Kategorie'].nunique(),3))
color_values_opaque = {}
for i, unique_value in enumerate(df['Kategorie'].unique()):
    color_values_opaque[unique_value] = 'rgb({},{},{})'.format(
        random_color_value[i][0],
        random_color_value[i][1],
        random_color_value[i][2])
color_values_transparent = {}
for i, unique_value in enumerate(df['Kategorie'].unique()):
    color_values_transparent[unique_value] = 'rgb({},{},{},{})'.format(
        random_color_value[i][0],
        random_color_value[i][1],
        random_color_value[i][2],
        0.5)
        

df['Start'] = pd.to_datetime(df['Start'], format="%d.%m.%Y")
start = min(df['Start'])
df['Ende'] = pd.to_datetime(df['Ende'], format="%d.%m.%Y")
end = max(df['Ende'])

df["Dauer"] = (df["Ende"] - df["Start"])
df["Fortschritts-Anzeige"] = pd.to_datetime(df["Dauer"] * df["Fortschritt"] / 100 + df["Start"], format="%d.%m.%Y")

df['Beschreibung'] = df['Beschreibung'].astype(str) 
df['Beschreibung'] = df['Beschreibung'].apply(
    lambda t: "<br>".join(textwrap.wrap(t, width=60))
    )

template = "<b>%{customdata[1]}</b><br>Von: %{customdata[2]}<br>Bis: %{customdata[3]}<br>Beschreibung:<br>%{customdata[5]}<extra></extra>"


fig = go.Figure()
for cat in df['Kategorie']:
    sdf = df[df['Kategorie'] == cat]
    
    # full bar
    fig.add_trace(go.Bar(base=sdf["Start"],
                        x=np.array((sdf["Ende"] - sdf["Start"]))/1E6,
                        y=sdf["Aufgabe"],
                        orientation='h', 
                        marker_color=color_values_opaque[cat],
                        marker_line_width=0, 
                        width=0.9,
                        customdata=df[df['Kategorie'] == cat],
                        hovertemplate=template,
                        showlegend=not(cat in [data['name'] for data in list(fig.data)]),
                        name=cat,
                        legendgroup=cat))
                                
    # completion bar
    fig.add_trace(go.Bar(base=sdf["Start"],
                        x=np.array((sdf["Fortschritts-Anzeige"] - sdf["Start"]))/1E6,
                        y=sdf["Aufgabe"],
                        orientation='h', 
                        marker_color=color_values_transparent[cat],
                        marker_line_width=0, 
                        width=0.9,
                        customdata=df[df['Kategorie'] == cat],
                        hovertemplate=template,
                        legendgroup=cat,
                        showlegend=False
                        ))
                        
    # text bar
    fig.add_trace(go.Bar(base=sdf["Start"],
                        x=np.array((sdf["Ende"] - sdf["Start"]))/1E6,
                        y=sdf["Aufgabe"],
                        orientation='h', 
                        marker_color='rgba(255, 0, 0, 0)',
                        marker_line_width=0, 
                        width=0.9,
                        text=sdf["Beschreibung"],
                        texttemplate='%{text}',
                        textposition='inside', 
                        insidetextanchor='start', 
                        textfont=dict(color='white', family="Lato", size=12),
                        hoverinfo='skip',
                        legendgroup=cat,
                        showlegend=False
                        ))

# 5.2. other info
# marker for today
today = datetime.datetime.today().strftime("%d.%m.%Y")
fig.add_trace(go.Scatter(x=[pd.to_datetime(today, format="%d.%m.%Y") for i in range(len(df))], 
                          y=df["Aufgabe"],
                          mode='lines',
                          line=dict(color='Gray', dash='dot', width=1), 
                          hovertemplate="Heute: {}<extra></extra>".format(today),
                          name="Heute"
                          ))

## 5.3. layout
fig.update_yaxes(autorange="reversed")

fig.update_xaxes(
    type="date",
    tickformat="%d %b %Y",
    range=[start, end],
    tickfont=dict(size=13, family="Lato"),
    showline=True,
    linewidth=2, 
    linecolor='SlateGrey',
    showgrid=True,
    gridcolor='LightGrey',
    gridwidth=0.5, 
    ticks="outside",
    tickcolor='SlateGrey',
    ticklen=4,
    tickwidth=2,
    tickangle=0,
    ticklabelmode='period',
    nticks=12
)

fig.update_xaxes(
    rangeslider_visible=True,
    # rangeselector=dict(
    #     buttons=list([
    #         dict(count=7, label="1 semaine", step="day", stepmode="backward"),
    #         dict(count=14, label="2 semaine", step="day", stepmode="backward"),
    #         dict(count=1, label="1 mois", step="month", stepmode="backward"),
    #         dict(label="toute la période", step="all")
    #     ])),
    # tickformatstops = [
    #     dict(dtickrange=[None, 86400000], value="%e %b"),
    #     dict(dtickrange=[86400000, 604800000], value="sem. %W"),
    #     dict(dtickrange=[604800000, None], value="%b %Y"),
    #     ]
)

fig.update_yaxes(
    title='',
    tickfont=dict(size=13, family="Lato"),
    type='category',
    categoryorder='category ascending',
    showline=True,
    linewidth=2, 
    linecolor='SlateGrey',
    ticks="outside",
    tickcolor='SlateGrey',
    ticklen=4,
    tickwidth=2,
    fixedrange=True
)

fig.update_layout(
    title={'text': TITLE,
        'font':dict(size=24),
        'y':0.96,
        'x':0.085},
    barmode='overlay',
    margin=dict(l=80, r=10, t=140, b=60),
    plot_bgcolor='white', 
    height=1100, 
    width=1300)

# plotting
fig.write_html(f"{TITLE_A}.html")
fig.show()

