from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class ProductoForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired(), Length(min=2, max=100)])
    descripcion = TextAreaField("Descripción")
    precio = FloatField("Precio", validators=[DataRequired()])
    cantidad = IntegerField("Cantidad", validators=[DataRequired()])
    submit = SubmitField("Guardar")

class LoginForm(FlaskForm):
    username = StringField("Usuario", validators=[DataRequired()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    submit = SubmitField("Iniciar Sesión")
