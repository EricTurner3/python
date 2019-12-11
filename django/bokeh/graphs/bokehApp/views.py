from django.shortcuts import render
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import HoverTool, LassoSelectTool, WheelZoomTool, PointDrawTool, ColumnDataSource

from bokeh.palettes import Category20c, Spectral6, Spectral3
from bokeh.transform import cumsum
from .models import Products
# from numpy import pi
# import pandas as pd
from bokeh.resources import CDN

# Create your views here.
def home(request):
    # plot points and title
    x = [1, 2, 3, 4, 5]
    y = [6, 10, 2, -4, 10]
    title = 'My Leaning Graph'

    # create the plot, set up labels and the size
    plot = figure(
        title = title,
        x_axis_label = "High and Lows",
        y_axis_label = "Learning Topics",
        plot_width = 700,
        plot_height = 700,
        tools = "",
        toolbar_location=None,
    )
    
    # add a circle to the graph
    cr = plot.circle(
        # basic coords, size and colors
        x, y, size = 10, color = "blue",

        # advanced settings for fill colors and opacities
        fill_color = "grey",
        hover_fill_color = "firebrick",

        fill_alpha = 0.05,
        hover_alpha = 0.3,

        line_color = None,
        hover_line_color = "white"
    )

    # add a hover tool
    plot.add_tools(HoverTool(tooltips=None, renderers=[cr], mode="hline"))
    # set the font size of the title
    plot.title.text_font_size = '20pt'
    # add a line to the plot
    plot.line(x, y, legend="Leaning Line", line_width = 4, line_color = 'brown', line_dash = 'dashed')
    # set the background color of the plot
    plot.background_fill_color = "lightgrey"
    # set all sorts of colors and borders and other options
    plot.border_fill_color = "whitesmoke"
    plot.min_border_left = 40
    plot.min_border_right = 40
    plot.outline_line_width = 7
    plot.outline_line_alpha = 0.2
    plot.outline_line_color = "purple"

    # store the components
    script, div = components(plot)

    # return to the view
    return render(request, 'home.html', {'script': script, 'div': div})

# render a bokeh graph
def starter(request):
    # create a  plot using bokeh
    plot = figure()
    # add a circle to the plot
    plot.circle([1, 10, 35, 27], [0, 0, 0, 0], size=20, color="blue")

    # returns the script JS tag and the div tag to be used in an HTML view
    script, div = components(plot)

    return render(request, 'starter.html', {'script': script, 'div': div})

def combo(request):

    # prepare some data
    x = [0.1, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    # using list comprehension to create 3 other data sets
    y0 = [i**2 for i in x]
    y1 = [10**i for i in x]
    y2 = [10**(i**2) for i in x]

    # create a new plot
    p = figure(
    tools="pan,wheel_zoom,box_zoom,reset, hover, tap, crosshair", # this gives us our tools
    y_axis_type="log", y_range=[0.001, 10**11], title="log axis example",
    x_axis_label='sections', y_axis_label='particles'
    )

    # add some renderers
    p.line(x, x, legend="y=x") #thin blue line
    p.circle(x, x, legend="y=x", fill_color="white", size=8) # adds circles to y=x line

    p.line(x, y0, legend="y=x^2", line_width=3) # thick blue line

    p.line(x, y1, legend="y=10^x", line_color="red") # red line
    p.circle(x, y1, legend="y=10^x", fill_color="red", line_color="red", size=6) # adds red circles

    p.line(x, y2, legend="y=10^x^2", line_color="orange", line_dash="4 4") # orange dotted line  

    script, div = components(p)

    return render(request, 'combo.html' , {'script': script, 'div':div})


def programming(request):

    lang = ['Python', 'JavaScript', 'C#', 'PHP', 'C++', 'Java']
    counts = [25, 30, 8, 22, 12, 17]

    p = figure(x_range=lang, plot_height=450, title="Programming Languages Popularity",
           toolbar_location="below", tools="pan,wheel_zoom,box_zoom,reset, hover, tap, crosshair")
    
    # ColumnDataSource allows us to modify the data so each bar has a different color
    # Spectral6 is from the bokeh.palettes module
    # the 6 denotes we need 6 of the colors from Spectral colormap
    source = ColumnDataSource(data=dict(lang=lang, counts=counts, color=Spectral6))
    p.add_tools(LassoSelectTool())
    p.add_tools(WheelZoomTool())       

    p.vbar(x='lang', top='counts', width=.8, color='color', legend="lang", source=source)
    p.legend.orientation = "horizontal"
    p.legend.location = "top_center"

    p.xgrid.grid_line_color = "black"
    p.y_range.start = 0
    p.line(x=lang, y=counts, color="black", line_width=2) # line that touches all the points on the bars

    script, div = components(p)

    return render(request, 'programming.html' , {'script': script, 'div':div})

# retrieve information from a django DB
def products(request):
    # placeholder variables
    shoes = 0
    belts = 0
    shirts = 0
    counts = []
    items = ["Shoes", "Belts", "Shirts"]

    # query the Products model for the data
    prod = Products.objects.values()

    # iterate over the database results to fill our placeholder variables
    for i in prod:
        if "Shoes" in i.values():
            shoes  += 1
        elif "Belts" in i.values():
            belts  += 1
        elif "Shirts" in i.values():
            shirts += 1

    # add the final counts to the counts array
    # ensure the order matches the order of the items array
    counts.extend([shoes, belts, shirts])

    # create a plot, specifiy the range, size, title, and toolbar items
    plot = figure(x_range = items, plot_height = 600, plot_width = 600, 
        title="Products",toolbar_location="right", tools="pan,wheel_zoom,box_zoom,reset,hover,tap,crosshair")
    plot.title.text_font_size = '20pt'

    plot.xaxis.major_label_text_font_size = "14pt"
    # my addition, similar to programming method, lets change the bar color
    source = ColumnDataSource(data=dict(items=items, counts=counts, color=Spectral3))
    # create a vertical bar using the label of items and the counts as the numbers
    # original from tutorial:
    # plot.vbar(items, counts, width=.4, color='firebrick', legend="Product Counts")
    plot.vbar(x='items', top='counts', width=.4, color='color', legend="Product Counts", source=source)
    # set the size of the text under each bar graph (usually is very small)
    plot.legend.label_text_font_size = '14pt'

    # grab the script and div tags to display in the UI
    script, div = components(plot)


    return render(request, 'products.html', {'script': script, 'div': div})