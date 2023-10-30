from pywebio.input import *
from pywebio.output import *
from flask import Flask
from pywebio.platform.flask import webio_view
from pywebio import STATIC_PATH
from pywebio.session import *

app = Flask(__name__)

user_responses = {}

def exam():
    c = 0

    put_html("<h1>Register Grievance</h1>")

    #name = input("Please enter your name to start the test", type="text", validate=validate_name)

    q1 = radio("Which government type are you addressing ?", ['Central Government', 'State Government'])
    user_responses['government'] = q1

    q2 = radio("Which Ministry/Department is involved?", ['Home Affairs', 'Housing And Urban Affairs', 'Health and Family Welfare', 'Central Board of Direct Taxes(Income Tax)', 'Labour And Employment Related', 'Posts', 'Telecommunications', 'Personnel and Training', 'Financial Services(Banking Division)', 'Financial Services(Insurance Division)'])
    user_responses['ministry'] = q2

    q3 = radio("Where is the issue located?", ['Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal', 'Andaman & Nicobar Islands', 'Chandigarh', 'Dadra & Nagar Haveli & Daman & Diu (merged)', 'Lakshadweep', 'Delhi (National Capital Territory of Delhi)', 'Puducherry'])
    user_responses['location'] = q3

    q4 = input("Q4. Please describe the problem or grievance in detail: ")
    user_responses['description'] = q4

    q5 = radio("Are you sure about registering of complaint, as per IPC-203 : Giving false information respecting an offence committed is an punishable offence. And Punishment of 2 Years of Jail or Fine or Both are may applicable ", ['Yes, I am sure', 'No'])
    if q5 == 'No':
        c += 1

    if c == 0:
        message = [style(put_html(
            "<h1 style='display:inline;border-bottom:0px'>Congratulations !! </h1>" + ", Your complaint is Submitted Successfully <b>" + "</b><br><br>"), 'color:green;'), style(put_html("<p>Status : <b>Under Process</b></p>"), 'color:green'),
                   put_html("<b>We try to solve your Grievence as soon as possible.</b>")]
        popup("Result", content=message, size='large', implicit_close=True, closable=True)
    else:
        message = [style(put_html(
            "<h1 style='display:inline;border-bottom:0px'>Oops! " + "</h1>" + ", Your complaint is not registered <b>" + "</b><br><br>"), 'color:red'), style(put_html("<p>Status : <b>FAILED</b></p>"), 'color:red'),
                   put_html("<b>Please Try to register your Complaint Again</b><br><br>"), style(put_link('Retry ↺', ""), 'color:red;align-content: center;border-radius: 5px;color:#f9faf8;padding: 5px 100px;text-align:center;align-items : center;background-color: white;\
            background-image: linear-gradient(270deg, #8cf5f5 1%, #0a43f3 100%);')]
        popup("Result", content=message, size='large', implicit_close=True, closable=True)


"""A method to validate the name entered by user"""





app.add_url_rule('/', 'webio_view', webio_view(exam), methods=['GET', 'POST', 'OPTIONS'])

if __name__ == '__main__':
    app.run(debug=True, port=5000)