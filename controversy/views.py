from typing import Any

from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import generic
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.forms.models import model_to_dict

import pandas as pd
from math import pi, radians
import numpy as np

from bokeh.plotting import figure, show
from bokeh.models import (
    OpenURL,
    TapTool,
    AnnularWedge,
    ColumnDataSource,
    CustomJS,
    Legend,
    LegendItem,
    Plot,
    Range1d,
    HoverTool,
)
from bokeh.transform import cumsum, factor_cmap
from bokeh.palettes import Category20c, magma
from bokeh.embed import components

from .models import Controversy, Data_Point


class IndexView(generic.ListView):
    template_name = "controversy/index.html"

    context_object_name = "controversies"

    def get_queryset(self):
        return Controversy.objects.order_by("name")


class ControversyView(generic.DetailView):
    model = Controversy
    template_name = "controversy/detail.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        obj = self.get_object()

        # factors and palette for factor_cmap function
        cfac = ["true", "false"]
        pal = ("#ef8a62", "#67a9cf")

        # the data which will be turned into a ColumnDataSource
        data = {
            "weight": [],
            "name": [],
            "bool": [],
            "start_angle": [],
            "end_angle": [],
            "url": [],
        }

        # populating data based on the Django object of this DetailView
        for point in obj.points.all():
            data["name"].append(point.name)
            if point.boolean:
                data["bool"].append("true")
            else:
                data["bool"].append("false")
            data["url"].append(point.url)
            data["start_angle"].append(0)
            data["end_angle"].append(0)
            data["weight"].append(0)

        # wedge angle calculations
        percent = 1 / len(data["name"]) * 100
        for i in range(len(data["weight"])):
            data["weight"][i] = percent

        radians1 = [radians((weight / 100) * 360) for weight in data["weight"]]

        start_angle = [radians(0)]
        prev = start_angle[0]
        for k in radians1[:-1]:
            start_angle.append(k + prev)
            prev = k + prev

        end_angle = start_angle[1:] + [radians(0)]

        data["start_angle"] = start_angle
        data["end_angle"] = end_angle

        # make the data into a bokeh compatible resource
        source = ColumnDataSource(data=data)

        # plotting
        p = figure(
            height=350,
            title="Pie Chart",
            toolbar_location=None,
            tools="hover,tap",
            tooltips="@name \n @url",
            x_range=(-0.5, 1.0),
        )

        p.wedge(
            x=0,
            y=1,
            radius=0.4,
            start_angle="start_angle",
            end_angle="end_angle",
            line_color="white",
            fill_color=factor_cmap("bool", pal, factors=cfac),
            legend_field="name",
            source=source,
        )

        # enable taptool
        taptool = p.select(type=TapTool)
        taptool.callback = OpenURL(url="@url")
        source.selected.indices = []
        

        p.axis.axis_label = None
        p.axis.visible = False
        p.grid.grid_line_color = None

        script, div = components(p)

        context["script"] = script
        context["div"] = div
        return context
