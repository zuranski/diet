import datetime as dt
from pytz.gae import pytz
from gluon import current

# reloading modules capapbility - use only in dev
from gluon.custom_import import track_changes
track_changes(True)

#data
foods = sorted(["dairy", "bread", "beef", "chicken", "cheese", \
         "yogurt", "chocolate", "sweets", "fish", "seafood", "vegetables", \
         "fruit", "pizza", "pasta", "pastry", "burger", "soup", "carbs","eggs","pork"])
drinks = sorted(["juice","tea","coffee","milk","wine","beer","liquor"])

# timezones a la http://luca.dealfaro.org/code/web2py-recipes/utc-to-localtime-and-back-in-web2py
is_timezone_unknown = (session.user_timezone is None)
user_timezone = session.user_timezone or 'UTC'
tz=pytz.timezone(user_timezone)

#define now
now = lambda: dt.datetime.now(pytz.timezone(user_timezone)).strftime("%H:%M:00")
trepr = lambda v, r: v.strftime("%H:%M")
today = lambda: dt.datetime.now(pytz.timezone(user_timezone)).date()

#users
users = sorted([r.first_name for r in db(db.auth_user.id > 0).select()
         if auth.has_membership('users', r.id)])
current.users = users

def date_widget(f,v):
    wrapper = DIV()
    inp = SQLFORM.widgets.string.widget(f,v,_class='form-control jqdate')
    jqscr = SCRIPT("jQuery(document).ready(function(){jQuery('#%s').datepicker({dateFormat:'yy-mm-dd'});});" % inp['_id'],_type="text/javascript")
    wrapper.components.extend([inp,jqscr])
    return wrapper

db.define_table(
    "Meals",
    Field("Person",type="string", requires=IS_IN_SET(users), required=True,
        default=auth.user.first_name if auth.user is not None else None),
    Field("MealType", type="string", requires=IS_IN_SET(("breakfast", "lunch", "snack", "dinner")), \
          label="Meal Type", required=True),
    Field("MealItems", type="list:string", label="Foods", \
          requires=IS_IN_SET(foods, multiple=(0, 1000)), \
          widget=SQLFORM.widgets.checkboxes.widget),
    Field("DrinkItems", type="list:string", label="Drinks", \
          requires=IS_IN_SET(drinks, multiple=(0, 1000)), \
          widget=SQLFORM.widgets.checkboxes.widget),
    Field("MealDate", type="date", label="Date", required=True, default=today, widget=date_widget),
    Field("MealTime", type="time", label="Time", required=True, default=now, represent=trepr),
    Field("Timezone", type="string", readable=False, writable=False, default=session.user_timezone),
    Field("FeelingAfterMeal", type="string", label="Feeling After", \
          requires=IS_IN_SET(("very good", "good", "neutral", "bad", "very bad")), required=True),
    Field("Comments", type="text"),
    singular="Meal",
    plural="Meals",
)
db.Meals.id.readable=False

db.define_table(
    "Issues",
    Field("Person", type="string", requires=IS_IN_SET(users), required=True,
          default=auth.user.first_name if auth.user is not None else None),
    Field("IssueDate", type="date", label="Date", required=True, default=today, widget=date_widget),
    Field("IssueTime", type="time", label="Time", required=True, default=now, represent=trepr),
    Field("Timezone", type="string", readable=False, writable=False, default=session.user_timezone),
    Field("Description", type="text"),
    singular="Issue",
    plural="Issues"
)

db.Issues.id.readable=False


