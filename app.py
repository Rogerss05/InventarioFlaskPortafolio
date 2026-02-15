from flask import Flask, render_template, redirect, url_for, flash
from config import Config
from models import db, Producto, User
from forms import ProductoForm, LoginForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ------------------------
# RUTA PRINCIPAL
# ------------------------

@app.route("/")
@login_required
def index():
    if current_user.role == "admin":
        return redirect(url_for("dashboard"))

    productos = Producto.query.all()
    return render_template("productos/listar.html", productos=productos)


# ------------------------
# AGREGAR PRODUCTO
# ------------------------

@app.route("/productos/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_producto():
    if current_user.role != "admin":
        flash("No tienes permisos para agregar productos.")
        return redirect(url_for("index"))

    form = ProductoForm()
    if form.validate_on_submit():
        producto = Producto(
            nombre=form.nombre.data,
            precio=form.precio.data,
            cantidad=form.cantidad.data,
            descripcion=form.descripcion.data
        )
        db.session.add(producto)
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("productos/crear.html", form=form)

# ------------------------
# EDITAR PRODUCTO
# ------------------------

@app.route("/productos/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_producto(id):
    if current_user.role != "admin":
        flash("No tienes permisos para editar productos.")
        return redirect(url_for("index"))

    producto = Producto.query.get_or_404(id)
    form = ProductoForm(obj=producto)

    if form.validate_on_submit():
        producto.nombre = form.nombre.data
        producto.precio = form.precio.data
        producto.cantidad = form.cantidad.data
        producto.descripcion = form.descripcion.data
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("productos/editar.html", form=form)

# ------------------------
# ELIMINAR PRODUCTO
# ------------------------

@app.route("/productos/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_producto(id):
    if current_user.role != "admin":
        flash("No tienes permisos para eliminar productos.")
        return redirect(url_for("index"))

    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    return redirect(url_for("index"))

# ------------------------
# LOGIN
# ------------------------

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("index"))
        else:
            flash("Credenciales incorrectas")

    return render_template("login.html", form=form)

# ------------------------
# LOGOUT
# ------------------------

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

#------------------------
# RUTA DASHBOARD (SOLO ADMIN)
#------------------------
@app.route("/dashboard")
@login_required
def dashboard():
    if current_user.role != "admin":
        flash("No tienes permisos para acceder al dashboard.")
        return redirect(url_for("index"))

    total_productos = Producto.query.count()

    stock_bajo_lista = Producto.query.filter(Producto.cantidad < 5).all()
    stock_bajo = len(stock_bajo_lista)

    valor_total = db.session.query(
        db.func.sum(Producto.precio * Producto.cantidad)
    ).scalar() or 0

    ultimos = Producto.query.order_by(Producto.id.desc()).limit(5).all()

    return render_template(
        "dashboard.html",
        total_productos=total_productos,
        stock_bajo=stock_bajo,
        valor_total=valor_total,
        ultimos=ultimos,
        stock_bajo_lista=stock_bajo_lista
    )


# ------------------------
# CREAR TABLAS AUTOMÁTICAMENTE
# ------------------------

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
