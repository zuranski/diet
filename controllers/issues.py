from forms import search_form

@auth.requires_login()
def index():
    #query
    query = (db.Issues.id > 0)
    if not request.get_vars.Person in [None, '']:
        query = query & (db.Issues.Person == request.get_vars.Person)
    if not request.get_vars.From in [None, '']:
        query = query & (db.Issues.IssueDate >= request.get_vars.From)
    if not request.get_vars.To in [None, '']:
        query = query & (db.Issues.IssueDate <= request.get_vars.To)

    # sort
    order = [~db.Issues.IssueDate, ~db.Issues.IssueTime]

    is_mobile = request.user_agent().is_mobile
    grid = SQLFORM.grid(query,
                        paginate=12,
                        csv=False,
                        searchable=True,
                        showbuttontext= not is_mobile,
                        orderby=order,
                        search_widget=search_form
                        )

    return dict(grid=grid)

@auth.requires_login()
def test():
    form = FORM(INPUT(_name='Person',
                      _class='form-control'),
                INPUT(_type='submit',
                      _class='button btn btn-primary',
                      _value='Refresh'),
                )

    if form.process().accepted:
        db.Issues.insert(Person=form.vars.Person, IssueDate=today, IssueTime=now)

    return dict(form=form, data=form.vars.Person)
