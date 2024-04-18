from typing import Any

from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import FormMixin
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
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
from .forms import ControversyForm, Data_PointForm


class IndexView(generic.ListView):
    template_name = "controversy/index.html"

    context_object_name = "controversies"

    def get_queryset(self):
        return Controversy.objects.order_by("name")


class ControversyView(FormMixin, generic.DetailView):
    model = Controversy
    template_name = "controversy/detail.html"
    form_class = Data_PointForm
    context_object_name = "controversy"

    def get_success_url(self):
        return reverse("detail")

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        obj = self.get_object()

        # factors and palette for factor_cmap function
        cfac = ["true", "false"]
        pal = ("#67a9cf", "#ef8a62")

        # the data which will be turned into a ColumnDataSource
        science_data = {
            "weight": [],
            "name": [],
            "bool": [],
            "description": [],
            "start_angle": [],
            "end_angle": [],
            "url": [],
        }

        # populating data based on the Django object of this DetailView
        for point in obj.points.all():
            if getattr(point, "data_set") == "data":
                science_data["name"].append(point.name)
                if point.boolean:
                    science_data["bool"].append("true")
                else:
                    science_data["bool"].append("false")
                science_data["description"].append(point.description)
                science_data["url"].append(point.url)
                science_data["start_angle"].append(0)
                science_data["end_angle"].append(0)
                science_data["weight"].append(0)

        # wedge angle calculations
        percent = (1 / len(science_data["name"]) if len(science_data["name"]) > 0 else 1)* 100
        for i in range(len(science_data["weight"])):
            science_data["weight"][i] = percent

        radians1 = [radians((weight / 100) * 360) for weight in science_data["weight"]]

        start_angle = [radians(0)]
        prev = start_angle[0]
        for k in radians1[:-1]:
            start_angle.append(k + prev)
            prev = k + prev

        end_angle = start_angle[1:] + [radians(0)]

        science_data["start_angle"] = start_angle
        science_data["end_angle"] = end_angle

        # make the data into a bokeh compatible resource
        source = ColumnDataSource(data=science_data)

        # plotting
        p = figure(
            height=350,
            title="Pie Chart",
            toolbar_location=None,
            tools="hover,tap",
            tooltips="@name : @description",
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

        # CHART 2 #

        # wedge angle calculations

        opinion_data = {
            "weight": [],
            "name": [],
            "bool": [],
            "description": [],
            "start_angle": [],
            "end_angle": [],
            "url": [],
        }

        for point in obj.points.all():
            if getattr(point, "data_set") == "opinion":
                opinion_data["name"].append(point.name)
                if point.boolean:
                    opinion_data["bool"].append("true")
                else:
                    opinion_data["bool"].append("false")
                opinion_data["description"].append(point.description)
                opinion_data["url"].append(point.url)
                opinion_data["start_angle"].append(0)
                opinion_data["end_angle"].append(0)
                opinion_data["weight"].append(0)

        percent = (1 / len(opinion_data["name"]) if len(opinion_data["name"]) > 0 else 1)* 100
        for i in range(len(opinion_data["weight"])):
            opinion_data["weight"][i] = percent

        radians1 = [radians((weight / 100) * 360) for weight in opinion_data["weight"]]

        start_angle = [radians(0)]
        prev = start_angle[0]
        for k in radians1[:-1]:
            start_angle.append(k + prev)
            prev = k + prev

        end_angle = start_angle[1:] + [radians(0)]

        opinion_data["start_angle"] = start_angle
        opinion_data["end_angle"] = end_angle

        # make the data into a bokeh compatible resource
        source = ColumnDataSource(data=opinion_data)

        # plotting
        p2 = figure(
            height=350,
            title="Pie Chart",
            toolbar_location=None,
            tools="hover,tap",
            tooltips="@name : @description",
            x_range=(-0.5, 1.0),
        )

        p2.wedge(
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
        taptool2 = p2.select(type=TapTool)
        taptool2.callback = OpenURL(url="@url")
        source.selected.indices = []

        p2.axis.axis_label = None
        p2.axis.visible = False
        p2.grid.grid_line_color = None

        script2, div2 = components(p2)

        context["script2"] = script2
        context["div2"] = div2

        # CHART 3 #

        # wedge angle calculations

        advice_data = {
            "weight": [],
            "name": [],
            "bool": [],
            "description": [],
            "start_angle": [],
            "end_angle": [],
            "url": [],
        }

        for point in obj.points.all():
            if getattr(point, "data_set") == "advice":
                advice_data["name"].append(point.name)
                if point.boolean:
                    advice_data["bool"].append("true")
                else:
                    advice_data["bool"].append("false")
                advice_data["description"].append(point.description)
                advice_data["url"].append(point.url)
                advice_data["start_angle"].append(0)
                advice_data["end_angle"].append(0)
                advice_data["weight"].append(0)

        percent = 1 / (len(advice_data["name"]) if len(advice_data["name"]) > 0 else 1) * 100
        for i in range(len(advice_data["weight"])):
            advice_data["weight"][i] = percent

        radians1 = [radians((weight / 100) * 360) for weight in advice_data["weight"]]

        start_angle = [radians(0)]
        prev = start_angle[0]
        for k in radians1[:-1]:
            start_angle.append(k + prev)
            prev = k + prev

        end_angle = start_angle[1:] + [radians(0)]

        advice_data["start_angle"] = start_angle
        advice_data["end_angle"] = end_angle

        # make the data into a bokeh compatible resource
        source = ColumnDataSource(data=advice_data)

        # plotting
        p3 = figure(
            height=350,
            title="Pie Chart",
            toolbar_location=None,
            tools="hover,tap",
            tooltips="@name : @description",
            x_range=(-0.5, 1.0),
        )

        p3.wedge(
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
        taptool3 = p3.select(type=TapTool)
        taptool3.callback = OpenURL(url="@url")
        source.selected.indices = []

        p3.axis.axis_label = None
        p3.axis.visible = False
        p3.grid.grid_line_color = None

        script3, div3 = components(p3)

        context["script3"] = script3
        context["div3"] = div3
        context["form"] = Data_PointForm(initial={"controversy": self.object})

        return context

    def post(self, request, *arts, **kwargs):
        controversy = self.get_object()
        form = Data_PointForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.controversy = controversy
            obj.save()
            return redirect('controversy:detail', controversy.slug)

