from authorization import views


from django.conf.urls import url

urlpatterns = [
    url("^register$", views.RegisterFormView.as_view(), name="register"),
    url("^login$", views.AuthForm.as_view(), name="login "),
    url("^logout$", views.LogoutView.as_view(), name="logout "),
    url("^$", views.BasicView.as_view(), name="base")

]