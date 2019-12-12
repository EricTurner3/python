from django.shortcuts import render

from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.palettes import all_palettes, Viridis256, viridis
from bokeh.models import HoverTool, LassoSelectTool, WheelZoomTool, PointDrawTool, ColumnDataSource, LabelSet
import math
from .models import Issues

# Create your views here.

def home(request):
    issue_list = []
    count = []
    objects = Issues.objects.values()

    # iterate through and add the counts and the labels to the appropriate arrays
    for i in objects:
        if i['issue'] in issue_list:
            # find the index of the issue, and increment the same index in the count array
            index_of_issue = issue_list.index(i['issue'])
            count[index_of_issue] += 1
        else:   
            # add the the issue and count to the respective arrays
            issue_list.append(i['issue']) # add the issue text
            count.append(1)       # since it is new, will be 1

    # sort the issue_list in desc order based on the count list
    def sort_lists(labels, numbers): 
        zipped_pairs = zip(numbers, labels) 
  
        labels_sorted = [x for _, x in sorted(zipped_pairs, reverse=True)] 
        numbers_sorted = sorted(numbers, reverse=True)
      
        return labels_sorted, numbers_sorted
    
    # set the lists to the new desc order sorted lists
    issue_list, count = sort_lists(issue_list, count)



    #use a spectral color gradient
    #passing the len of issue list grabs the exact number of colors needed to display the chart
    source = ColumnDataSource(data=dict(issue_list=issue_list, count=count, color=viridis(len(issue_list))))

    # set up a plot and barchart
    plot = figure(x_range=issue_list, plot_height=800, plot_width=1000, title="Damage Counts",
           toolbar_location="right", tools="pan,wheel_zoom,box_zoom,reset, hover, tap, crosshair")
    # add the bar chart
    plot.vbar(x='issue_list', top='count', width=.4, color= "color", legend="issue_list", source=source)
    plot.legend.label_text_font_size = '14pt'
    # create labels for the bars
    labels = LabelSet(x='issue_list', y='count', text='count', level='glyph', x_offset=-13.5, y_offset=0, source=source, render_mode='canvas')
    # add the labels above the bars
    plot.add_layout(labels)
    # rotate the xaxis labels 45 degrees (check out pi radians for other angles)
    plot.xaxis.major_label_orientation = math.pi/4

    script, div = components(plot)

    return render(request, 'home.html' , {'script': script, 'div':div})