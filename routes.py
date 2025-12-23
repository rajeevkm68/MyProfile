from flask import Blueprint, render_template, redirect, url_for
from extensions import db
from forms import ContactForm
import smtplib
from email.message import EmailMessage
from models import ContactMessage
import os

SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))


main_bp = Blueprint(
    "main",          # blueprint name
    __name__,
)

@main_bp.route('/')
def home():
    return render_template("index.html", show_canvas=True)

@main_bp.route("/content_about")
def content_about():
    return render_template("content_about.html")

@main_bp.route("/content_education")
def content_education():
    return render_template("content_education.html")

@main_bp.route("/content_experience")
def content_experience():
    return render_template("content_experience.html")

@main_bp.route("/content_career")
def content_career():
    return render_template("content_career.html")

@main_bp.route("/content_milestone")
def content_milestone():
    return render_template("content_milestone.html")

from flask import current_app, flash

@main_bp.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        message = form.message.data

        contact = ContactMessage(
            name=name,
            email=email,
            phone=phone,
            message=message
        )

        msg_body = (
            f"Hi {name},\n\n"
            "Thank you for your time !!!\n"
            "Sincerely appreciate the feedback !!!\n\n"
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Phone: {phone}\n"
            f"Message:\n{message}\n"
        )

        try:
            send_email(
                "Thank you for your enquiry",
                body=msg_body,
                to_emails=[email]
            )
            flash("Thank you! Your message has been sent.", "success")

        except Exception:
            # LOG the real error (this is critical)
            current_app.logger.exception("Email sending failed")

            # USER-FRIENDLY message (no scary errors)
            flash(
                "Your message was received, but email delivery failed. "
                "We will still get back to you.",
                "warning"
            )

        db.session.add(contact)
        db.session.commit()

        return redirect(url_for("main.home"))

    if form.errors:
        current_app.logger.warning("Form validation failed: %s", form.errors)

    return render_template("contact.html", form=form)


def send_email(subject, body, to_emails, from_email=None):
    if not SMTP_USER or not SMTP_PASSWORD:
        raise RuntimeError("SMTP credentials not configured")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_email or SMTP_USER
    msg["To"] = ", ".join(to_emails) if isinstance(to_emails, (list, tuple)) else to_emails
    msg.set_content(body)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as smtp:
        smtp.starttls()
        smtp.login(SMTP_USER, SMTP_PASSWORD)
        smtp.send_message(msg)

