# https://stackoverflow.com/questions/62732631/how-to-collapsed-sidebar-in-dash-plotly-dash-bootstrap-components
import os
import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
#import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash_bootstrap_components._components.Container import Container


#s3_client = boto3.client('s3')
BUCKET = "map-2022-01-08"
FILE_NAME = "map.html"
"""
response = s3_client.list_objects_v2(Bucket=BUCKET)
files = response.get("Contents")
for file in files:
        print(type(file))
        print(file)
        s3_client.download_file(BUCKET, file['Key'], "./static/"+ str(file['Key']))
"""
maps = os.listdir("./app/static")
maps = [ map for map in maps if map.endswith( '.html') ]
maps = [os.path.splitext(map)[0] for map in maps]
home_about = ['about']
maps.remove('about')
maps.sort()
maps = home_about + maps
dict = {}
index =0
for map in maps:
    dict[map] = map
dict['about'] = "About IX Power Cartographica"
   
dict['colorado_districtmap_7mar22'] = "Colorado District Map"

dict['register'] = "Colorado Voter Information"

    #if '.DS_Store' in maps: maps.remove('.DS_Store')
 

#application = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
application = dash.Dash(external_stylesheets=[dbc.themes.CERULEAN])
#application = dash.Dash(external_stylesheets=[dbc.themes.UNITED])
#application = dash.Dash(external_stylesheets=[dbc.themes.FLATLY])


PLOTLY_LOGO = "./static/img/IX_PCarto_sm_23Feb21.png"



search_bar = dbc.Row(
    [    dbc.Col(
            dbc.Button(
                "Sidebar",  color="primary", className="ms-2", id="btn_sidebar", size="sm"
            ),
            width="auto",
        ),  
        
    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="60px")),
                        #dbc.Col(dbc.NavbarBrand("Navbar", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://ixwater.com/",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                search_bar,
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ],
        
    ),
    style={
           "background-image": "url(/assets/banner.png)",
           "background-repeat": "no-repeat",
           "background-size" : "cover",
           },
    color="dark",
    dark=True,
)



# add callback for toggling the collapse on small screens
@application.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 75.5,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0.5rem 1rem",
    "background-color": "#f2f1ed",
}

SIDEBAR_HIDEN = {
    "position": "fixed",
    "top": 82.5,
    "left": "-16rem",
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0rem 0rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "transition": "margin-left .5s",
    "margin-left": "18rem",
    "margin-right": "1rem",
    "padding": "1rem 3rem",
    "background-color": "#f2f1ed",
}

CONTENT_STYLE1 = {
    "transition": "margin-left .5s",
    "margin-left": "2rem",
    "margin-right": "2rem",
    "padding": "1rem 1rem",
    "background-color": "#f8f9fa",
}

sidebar = html.Div(
    [
        #html.H2("Maps", className="display-100"),
        html.Hr(),
        
        html.P(
            "Map of Colorado's Congressional Districts", className="lead"
        ),
        dbc.Nav(
            [  
                dbc.NavLink(str(dict[map]), href="/" + str(map), id="page-" + str(map) + "-link") for map in maps
            
            ],
            vertical=True,
            pills=True,
        ),
    ],
    id="sidebar",
    style=SIDEBAR_STYLE,
)

content = html.Div(

    id="page-content",
    style=CONTENT_STYLE)

application.layout = html.Div(
    [
        dcc.Store(id='side_click'),
        dcc.Location(id="url"),
        navbar,
        sidebar,
        content,
    ],
    style={ "background-color": "#f2f1ed"}
)


@application.callback(
    [
        Output("sidebar", "style"),
        Output("page-content", "style"),
        Output("side_click", "data"),
    ],

    [Input("btn_sidebar", "n_clicks")],
    [
        State("side_click", "data"),
    ]
)
def toggle_sidebar(n, nclick):
    if n:
        if nclick == "SHOW":
            sidebar_style = SIDEBAR_HIDEN
            content_style = CONTENT_STYLE1
            cur_nclick = "HIDDEN"
        else:
            sidebar_style = SIDEBAR_STYLE
            content_style = CONTENT_STYLE
            cur_nclick = "SHOW"
    else:
        sidebar_style = SIDEBAR_STYLE
        content_style = CONTENT_STYLE
        cur_nclick = 'SHOW'

    return sidebar_style, content_style, cur_nclick

# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell see page they are on

@application.callback(

    [Output("page-" + str(map) + "-link", "active") for map in maps],
    [Input("url", "pathname")],
)   

def toggle_active_links(pathname):
    if pathname == ["/"]:
        # Treat page 1 as the homepage / index
        #return True, False, False, False
        #list = [False for i in len(maps)]
        #list[0] = True
        return [True] + [False for i in range(len(maps)-1)]
    return [pathname == "/" + str(map) for map in maps]


@application.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/"]:
        #return html.P("IX Power Maps")
        mymap = "./app/static/colorado_districtmap_7mar22.html"
        return html.Div(
              html.Iframe(id="map", srcDoc= open(mymap,'r').read(), width='100%', height='600' )
        )
    elif pathname in ["/register"]:
        return   html.Div(
            dbc.Container(
            [  
                html.Br(),
                html.H4("Colorado Voter Information"),
                html.Br(),
                html.P(
                    "Look up your official Colorado Voter Registration here "
                    "to see what district and precinct you are in.",
                    className="lead",
                ),
                html.Br(),
                html.A(
                   "Check your Colorado Voter Registration here.", href='https://www.sos.state.co.us/voter/pages/pub/olvr/findVoterReg.xhtml', target="_blank"
                ),
                html.Br(),
                html.Hr(className="my-2"),
                html.Br(),
                html.P(

                    "Please note that the voter lookup is very particular."
                    "  You MUST enter the requested information exactly"
                    "like your voter registration "
                    "(i.e. 'Sam A. Smith' will return an error if you registered as 'Sam Adam Smith.')"
        
                ),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br()

           ],
           fluid=False,
           className="py-3",
        ),
        className="p-2 bg-light rounded-3",
)

    elif pathname in ["/" + str(map) for map in maps]:


        mymap = "./app/static/" + pathname[1:] + ".html"
        return html.Div(
              html.Iframe(id="map", srcDoc= open(mymap,'r').read(), width='100%', height='600' )
        )
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P("The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == "__main__":
      
    #print(f"file_name: {file&#91;'Key']}, size: {file&#91;'Size']}")
    application.run_server(debug=True,port=8050,host='0.0.0.0')
