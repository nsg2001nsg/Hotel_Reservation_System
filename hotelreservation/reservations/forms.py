import datetime

from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, DateField
from wtforms.validators import DataRequired, InputRequired


class ReservationForm(FlaskForm):
    type = StringField("Type", validators=[DataRequired()], render_kw={"readonly": True})
    data_format = "%Y-%m-%d"
    checkin_date = DateField("Checkin Date", validators=[InputRequired()], format=data_format,
                             default=datetime.date.today() + datetime.timedelta(days=1),
                             render_kw={
                                 "min": datetime.date.today().strftime(data_format),
                                 "max": str((datetime.date.today() + datetime.timedelta(days=365)).strftime(data_format)),
                             })
    checkout_date = DateField("Checkout Date", validators=[InputRequired()], format=data_format,
                              default=datetime.date.today() + datetime.timedelta(days=2),
                              render_kw={
                                  "min": datetime.date.today().strftime(data_format),
                                  "max": str((datetime.date.today() + datetime.timedelta(days=365)).strftime(data_format)),
                              })
    guest_count = IntegerField("Guest_Count", validators=[DataRequired()],
                               default=1,
                               render_kw={
                                   "min": 1,
                                   "max": 12,
                               })
    submit = SubmitField("Book")
