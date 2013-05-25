# a web app for calculating molar mass
# using the web.py framework
import web
from chem_lex import calc_mass
from lex import LexError

urls = ('/', 'Index')

page = web.template.frender("main.html")
form = web.form.Form(web.form.Textbox("Formula"),
                     web.form.Button("Calculate"))

class Index:

    def GET(self):
        return page("", form)

    def POST(self):
        user_input = web.input().Formula

        try:
            result = calc_mass(user_input)
            answer = "Molecular Mass of %s: %.5f g/mol" % (user_input, result)

        except:
            answer = "Invalid Input"

        return page(answer, form)

app = web.application(urls, globals())
app = app.wsgifunc()