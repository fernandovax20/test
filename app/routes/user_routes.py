from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.user import User
from app.dtos.user_dto import UserDTO

main = Blueprint("main", __name__)


@main.route("/")
def index():
    query = request.args.get("q", "").strip()
    if query:
        users = User.search(query)
    else:
        users = User.all()
    users_dto = [UserDTO.from_model(u) for u in users]
    return render_template("users.html", users=users_dto, query=query)


@main.route("/users/create", methods=["POST"])
def create_user():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()

    if not name or not email:
        flash("Nombre y email son obligatorios.", "error")
        return redirect(url_for("main.index"))

    if User.find_by_email(email):
        flash("El email ya está registrado.", "error")
        return redirect(url_for("main.index"))

    User.create(name, email)
    flash("Usuario creado exitosamente.", "success")
    return redirect(url_for("main.index"))


@main.route("/users/<int:user_id>/edit")
def edit_user(user_id):
    user = User.find(user_id)
    if not user:
        flash("Usuario no encontrado.", "error")
        return redirect(url_for("main.index"))

    users = User.all()
    users_dto = [UserDTO.from_model(u) for u in users]
    editing_dto = UserDTO.from_model(user)
    return render_template("users.html", users=users_dto, editing=editing_dto)


@main.route("/users/<int:user_id>/update", methods=["POST"])
def update_user(user_id):
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()

    if not name or not email:
        flash("Nombre y email son obligatorios.", "error")
        return redirect(url_for("main.edit_user", user_id=user_id))

    existing = User.find_by_email(email)
    if existing and existing.id != user_id:
        flash("El email ya está registrado por otro usuario.", "error")
        return redirect(url_for("main.edit_user", user_id=user_id))

    user = User.find(user_id)
    if user:
        user.update(name, email)
    flash("Usuario actualizado exitosamente.", "success")
    return redirect(url_for("main.index"))


@main.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    user = User.find(user_id)
    if user:
        user.delete()
    flash("Usuario eliminado exitosamente.", "success")
    return redirect(url_for("main.index"))
