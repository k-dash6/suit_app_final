from django.contrib.auth.decorators import user_passes_test


admin_required = user_passes_test(
    lambda user: user.is_admin,
    login_url='home',
    redirect_field_name=None,
)