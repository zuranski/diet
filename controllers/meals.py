import urllib2
from forms import search_form

@auth.requires_login()
def index():
    #query

    print "get", dict(request.get_vars)
    print "all", dict(request.vars)
    print "post", dict(request.post_vars)

    query=(db.Meals.id>0)
    if not request.get_vars.Person in [None,'']:
        query = query & (db.Meals.Person == request.get_vars.Person)
    if not request.get_vars.From in [None,'']:
        query = query & (db.Meals.MealDate >= request.get_vars.From)
    if not request.get_vars.To in [None,'']:
        query = query & (db.Meals.MealDate <= request.get_vars.To)

    #sort
    order = [~db.Meals.MealDate, ~db.Meals.MealTime]

    is_mobile = request.user_agent().is_mobile
    grid = SQLFORM.grid(query,
                        paginate=12,
                        csv=False,
                        searchable=True,
                        showbuttontext= not is_mobile,
                        orderby=order,
                        search_widget=search_form,
                        oncreate=getbiblequote)

    if session.reward_message is not None:
        response.flash=session.reward_message
        session.reward_message = None

    return dict(grid=grid)

def getbiblequote(form):
    if form.accepted:
        if auth.user.first_name == "Melissa":
            session.reward_message=XML(urllib2.urlopen("http://labs.bible.org/api/?passage=random").read())
        elif auth.user.first_name == "Andrzej":
            session.reward_message=XML("<a href='http://randomyoutube.net/channel/view?c=Berliner-Philharmoniker'>"
                                       "Random Berliner Philharmoniker Youtube Video</a>")