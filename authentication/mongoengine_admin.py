from flask import Blueprint, render_template, request, redirect, url_for
from mongoengine import DoesNotExist
from .models import CustomUser, VerificationToken

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/custom_users', methods=['GET', 'POST'])
def manage_custom_users():
    if request.method == 'POST':
        email = request.form.get('email')
        # Add logic to create a new CustomUser
        new_user = CustomUser(email=email)
        new_user.save()
        return redirect(url_for('admin.manage_custom_users'))

    users = CustomUser.objects()
    return render_template('admin/custom_users.html', users=users)

@admin_bp.route('/admin/verification_tokens', methods=['GET', 'POST'])
def manage_verification_tokens():
    if request.method == 'POST':
        token = request.form.get('token')
        # Add logic to create a new VerificationToken
        new_token = VerificationToken(token=token)
        new_token.save()
        return redirect(url_for('admin.manage_verification_tokens'))

    tokens = VerificationToken.objects()
    return render_template('admin/verification_tokens.html', tokens=tokens)
