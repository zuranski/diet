from gluon import current, OPTION, FORM, DIV, SELECT, INPUT, A, SPAN, SCRIPT

def search_form(self,url):


    input_style='height:36px; width:180px'
    hide_style=""

    vars = current.request.get_vars
    if all([vars[var]==None for var in vars]):
        # if there are no request params, hide the search query
        hide_style="display:none"

    #options for select
    persons = [OPTION('Select Person',_value='')] +\
              [OPTION(user, _value=user) for user in current.users]

    form = FORM(
        A(
            SPAN(_class='icon magnifier icon-zoom-in glyphicon glyphicon-zoom-in'),
            SPAN(' Filter', _class='buttontext button'),
            _class='button btn btn-default',
            _onclick="jQuery('#SearchForm').slideToggle()",
            _style='vertical-align:top'
        ),
        DIV(FORM(
            SELECT(persons,
                   _id="Person",
                   _class='form-control',
                   _name="Person",
                   _style=input_style,
                   value=vars.Person),' ',
            INPUT(_id='From',
                  _name="From",
                  _value=vars.From,
                  _class='form-control jqdate',
                  _placeholder="From",
                  _style=input_style),
            SCRIPT("jQuery(document).ready(function(){jQuery('#From').datepicker({dateFormat:'yy-mm-dd'});});",
                   _type="text/javascript"),
            ' ',
            INPUT(_id='To',
                  _name="To",
                  _value=vars.To,
                  _class='form-control jqdate',
                  _placeholder="To",
                  _style=input_style),
            SCRIPT("jQuery(document).ready(function(){jQuery('#To').datepicker({dateFormat:'yy-mm-dd'});});",
                   _type="text/javascript"),
            INPUT(_type='submit',
                  _class='btn btn-info',
                  _value='Submit',
                  ),
            INPUT(_type='button',
                  _class='btn btn-default',
                  _value='Clear',
                  _onclick="jQuery('#Person').val(''); "
                           "jQuery('#From').val('');"
                           "jQuery('#To').val('');"
                           "jQuery('#form').submit()"),
        ), _class='form-inline', _id="SearchForm", _style=hide_style),
        _method="GET",
        _action=url
    )
    return form

def select_form():

    vars = current.request.get_vars
    persons = [OPTION(user, _value=user) for user in current.users]

    form = FORM(
            SELECT(persons,
                   _name="Person",
                   _class='form-control',
                   value=vars.Person if vars.Person is not None else '',
                   ), ' ',
            INPUT(_class='form-control jqdate',
                  _name="From",
                  _id="From",
                  _value=vars.From,
                  _placeholder=" From",
                  ),

        ' ',        SCRIPT("jQuery(document).ready(function(){jQuery('#From').datepicker({dateFormat:'yy-mm-dd'});});",
               _type="text/javascript"),
            INPUT(_name="To",
                  _id="To",
                  _value=vars.To,
                  _class='form-control jqdate',
                  _placeholder=" To",
                  ),
        SCRIPT("jQuery(document).ready(function(){jQuery('#To').datepicker({dateFormat:'yy-mm-dd'});});",
               _type="text/javascript"), ' ',
            INPUT(_type='submit',
                  _class='button btn btn-primary',
                  _value='Refresh',
                  ),
     _id="form",
     _method="POST",
     _class='form-inline'
    )

    return form