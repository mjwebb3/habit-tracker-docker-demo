import os
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from db import db, User, Habit


def seed_demo_data():
    admin_email = "admin@demo.com"
    admin_password = "PruebaTestA"

    demo_email = "user@demo.com"
    demo_password = "PruebaTestE"

    existing_admin = User.query.filter_by(email=admin_email).first()
    if not existing_admin:
        admin_user = User(
            username="admin",
            email=admin_email,
            password_hash=generate_password_hash(admin_password),
            is_admin=True,
        )
        db.session.add(admin_user)
        db.session.commit()

    existing_demo = User.query.filter_by(email=demo_email).first()
    if not existing_demo:
        demo_user = User(
            username="demo",
            email=demo_email,
            password_hash=generate_password_hash(demo_password),
            is_admin=False,
        )
        db.session.add(demo_user)
        db.session.commit()

        demo_habits = [
            Habit(name="Learn Docker", streak=3, user_id=demo_user.id),
            Habit(name="Study AWS", streak=5, user_id=demo_user.id),
            Habit(name="Practice Linux", streak=2, user_id=demo_user.id),
            Habit(name="Build a containerized app", streak=1, user_id=demo_user.id),
            Habit(name="Finish Students Community Day Lab", streak=0, user_id=demo_user.id),
        ]
        db.session.add_all(demo_habits)
        db.session.commit()


def reset_demo_only():
    demo_user = User.query.filter_by(email="user@demo.com").first()

    if demo_user:
        Habit.query.filter_by(user_id=demo_user.id).delete()
        db.session.delete(demo_user)
        db.session.commit()

    new_demo = User(
        username="demo",
        email="user@demo.com",
        password_hash=generate_password_hash("PruebaTestE"),
        is_admin=False,
    )
    db.session.add(new_demo)
    db.session.commit()

    demo_habits = [
        Habit(name="Learn Docker", streak=3, user_id=new_demo.id),
        Habit(name="Study AWS", streak=5, user_id=new_demo.id),
        Habit(name="Practice Linux", streak=2, user_id=new_demo.id),
        Habit(name="Build a containerized app", streak=1, user_id=new_demo.id),
        Habit(name="Finish Students Community Day Lab", streak=0, user_id=new_demo.id),
    ]
    db.session.add_all(demo_habits)
    db.session.commit()


def admin_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("login"))
        if not current_user.is_admin:
            flash("Admin access required.", "error")
            return redirect(url_for("dashboard"))
        return view_func(*args, **kwargs)
    return wrapped_view


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-change-me")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////app/data/habits.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    os.makedirs("/app/data", exist_ok=True)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    with app.app_context():
        db.create_all()

        # simple migration for old DBs without is_admin column
        try:
            User.query.first()
        except Exception:
            db.drop_all()
            db.create_all()

        seed_demo_data()

    @app.route("/")
    def root():
        if current_user.is_authenticated:
            return redirect(url_for("dashboard"))
        return redirect(url_for("login"))

    @app.route("/dashboard")
    @login_required
    def dashboard():
        return render_template(
            "index.html",
            username=current_user.username,
            is_admin=current_user.is_admin
        )

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for("dashboard"))

        if request.method == "POST":
            username = request.form.get("username", "").strip()
            email = request.form.get("email", "").strip().lower()
            password = request.form.get("password", "")

            if not username or not email or not password:
                flash("All fields are required.", "error")
                return render_template("register.html")

            existing_user = User.query.filter(
                (User.username == username) | (User.email == email)
            ).first()

            if existing_user:
                flash("Username or email already exists.", "error")
                return render_template("register.html")

            user = User(
                username=username,
                email=email,
                password_hash=generate_password_hash(password),
                is_admin=False,
            )
            db.session.add(user)
            db.session.commit()

            flash("Account created successfully. Please sign in.", "success")
            return redirect(url_for("login"))

        return render_template("register.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("dashboard"))

        if request.method == "POST":
            email = request.form.get("email", "").strip().lower()
            password = request.form.get("password", "")

            user = User.query.filter_by(email=email).first()

            if not user or not check_password_hash(user.password_hash, password):
                flash("Invalid email or password.", "error")
                return render_template("login.html")

            login_user(user)
            return redirect(url_for("dashboard"))

        return render_template("login.html")

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash("You have been logged out.", "success")
        return redirect(url_for("login"))

    @app.route("/habits", methods=["GET"])
    @login_required
    def get_habits():
        habits = Habit.query.filter_by(user_id=current_user.id).order_by(Habit.created_at.desc()).all()
        return jsonify([
            {
                "id": habit.id,
                "name": habit.name,
                "streak": habit.streak,
            }
            for habit in habits
        ])

    @app.route("/habits", methods=["POST"])
    @login_required
    def add_habit():
        data = request.get_json(silent=True) or {}
        name = (data.get("name") or "").strip()

        if not name:
            return jsonify({"error": "Habit name is required."}), 400

        habit = Habit(name=name, user_id=current_user.id)
        db.session.add(habit)
        db.session.commit()

        return jsonify({"status": "ok"}), 201

    @app.route("/habits/<int:habit_id>/check", methods=["POST"])
    @login_required
    def check_habit(habit_id):
        habit = Habit.query.filter_by(id=habit_id, user_id=current_user.id).first()

        if not habit:
            return jsonify({"error": "Habit not found."}), 404

        habit.streak += 1
        db.session.commit()

        return jsonify({"status": "ok"})

    @app.route("/habits/<int:habit_id>", methods=["DELETE"])
    @login_required
    def delete_habit(habit_id):
        habit = Habit.query.filter_by(id=habit_id, user_id=current_user.id).first()

        if not habit:
            return jsonify({"error": "Habit not found."}), 404

        db.session.delete(habit)
        db.session.commit()

        return jsonify({"status": "ok"})

    @app.route("/health")
    def health():
        return {"status": "ok"}, 200

    @app.route("/admin")
    @admin_required
    def admin_panel():
        users = User.query.order_by(User.created_at.desc()).all()
        user_data = []

        for user in users:
            user_data.append({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_admin": user.is_admin,
                "habit_count": Habit.query.filter_by(user_id=user.id).count(),
                "created_at": user.created_at.strftime("%Y-%m-%d %H:%M"),
            })

        return render_template("admin.html", users=user_data)

    @app.route("/admin/reset-password", methods=["POST"])
    @admin_required
    def admin_reset_password():
        user_id = request.form.get("user_id")
        new_password = request.form.get("new_password", "").strip()

        if not user_id or not new_password:
            flash("User and new password are required.", "error")
            return redirect(url_for("admin_panel"))

        user = db.session.get(User, int(user_id))
        if not user:
            flash("User not found.", "error")
            return redirect(url_for("admin_panel"))

        user.password_hash = generate_password_hash(new_password)
        db.session.commit()

        flash(f"Password updated for {user.email}.", "success")
        return redirect(url_for("admin_panel"))

    @app.route("/admin/reset-demo", methods=["POST"])
    @admin_required
    def admin_reset_demo():
        reset_demo_only()
        flash("Demo user and habits reset successfully.", "success")
        return redirect(url_for("admin_panel"))

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)