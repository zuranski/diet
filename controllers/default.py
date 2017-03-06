# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
from itertools import chain
from collections import Counter
import datetime as dt
from forms import select_form

@auth.requires_login()
def index():
    """main"""
    return dict(message="Dashboard",
                form=select_form(),
               )

def user():
    return dict(form=auth())


@cache.action()
def download():
    return response.download(request, db)


def call():
    return service()

def set_timezone():
    """Ajax call to set the timezone information for the session."""
    tz_name = request.vars.name
    from pytz import all_timezones_set
    if tz_name in all_timezones_set:
        session.user_timezone = tz_name

def plots():
    # fetch data from DB given parameters
    query=(db.Meals.id>0)
    if not request.vars.Person in [None,'']:
        query = query & (db.Meals.Person == request.vars.Person)
    if not request.vars.From in [None,'']:
        query = query & (db.Meals.MealDate >= request.vars.From)
    if not request.vars.To in [None,'']:
        query = query & (db.Meals.MealDate <= request.vars.To)

    records = [(r.MealItems,
                r.DrinkItems,
                r.MealType,
                1000 * (r.MealTime.hour * 3600 + r.MealTime.minute * 60),
                ) for r in db(query).select(db.Meals.ALL)]

    # transform data for frequency plot
    meals = list(chain.from_iterable([r[0] for r in records]))
    drinks = list(chain.from_iterable([r[1] for r in records]))
    # convert to Ascii for GAE
    meals = [item.encode('ascii') for item in meals]
    drinks = [item.encode('ascii') for item in drinks]
    # word frequencies
    freqMeals = dict(Counter(meals))
    freqDrinks = dict(Counter(drinks))
    all = dict(freqMeals, **freqDrinks)
    # sort
    Meals = sorted(freqMeals, key=freqMeals.get, reverse=True)
    Drinks = sorted(freqDrinks, key=freqDrinks.get, reverse=True)
    categories = sorted(all, key=all.get, reverse=True)

    # make frequency plot
    chart_freq = """<script
    type = "text/javascript" >
    $('#meal_freq').highcharts({
        chart: { type: 'column', zoomType: 'xy'},
        title: { text: ''},
        xAxis: {type:'category', 'categories': %s},
        plotOptions: {series: {pointWidth: 50}, column: {stacking: 'normal'}},
        tooltip: {
            formatter: function() {
                    return  '<b>' + this.key +': </b>' + this.y;
                }
        },
        yAxis: { title: { text: '' }, allowDecimals: false },
        legend: { enabled: true },
        series: [{name: "Foods", data: % s}, { name: "Drinks", data: % s}]
    })
    </script>
    """%(categories, [[m,freqMeals[m]] for m in Meals], [[m,freqDrinks[m]] for m in Drinks]) if len(freqMeals)+len(freqDrinks)>0 \
        else \
    """<script type="text/javascript">
        $('#meal_freq').text("No data for selected parameters")
        </script> """

    chart_times = """<script
    type = "text/javascript" >
    $('#meal_times').highcharts({
        chart: { zoomType: 'x', type: 'scatter', height: 200},
        title: {text: ''},
        xAxis: { type: 'datetime',    dateTimeLabelFormats : {day: '%sH:%sM'} },
        yAxis: { type: 'datetime', title: { text: '' }, labels: {enabled: false}},
        legend: { enabled: true },
        plotOptions: { scatter: { marker: {radius: 7} } },
        tooltip: {
            formatter: function() {
                    return  '<b>' + this.series.name +'</b><br/>' +
                        Highcharts.dateFormat('%sH:%sM', new Date(this.x));
                }
        },
        series: [{name: "Breakfast", data: %s},
                 {name: "Lunch", data: %s},
                 {name: "Dinner", data: %s},
                 {name: "Snack", data: %s}]
    })
    </script>
    """%('%','%','%','%',[[r[3], 0] for r in records if r[2] =='breakfast'],
         [[r[3], 0] for r in records if r[2] == 'lunch'],
         [[r[3], 0] for r in records if r[2] == 'dinner'],
         [[r[3], 0] for r in records if r[2] == 'snack']
         ) if len(records)>0 \
        else \
    """<script type="text/javascript">
        $('#meal_times').text("No data for selected parameters")
        </script> """

    table = TABLE(
        TR(TD(H3('Meal Times'))),
        TR(TD(_id="meal_times")),
        TR(TD(H3('Frequency'))),
        TR(TD(_id="meal_freq")),
        _style="width:99%"
    )

    return table + XML(chart_times) + XML(chart_freq)