from django.urls import path
from .import views

urlpatterns = [
    path("about/", views.about),
    path("home/",views.home,name="Home"), 
    path("login/",views.loginPage, name="login"),
    path("register/",views.registerPage, name="register"),
    path("logout/", views.logOutUser, name="logout"),
    path("user/", views.userPage, name="user-page"),
    path('accounts/', views.accounts_view, name='accounts'),
    path('success/', views.success_page, name='success'),
    # path('sister_profile/<str:username>/', views.sister_profile, name='sister_profile'),
    path('<int:user_id>/summary/', views.patient_summary, name='patient_summary'),
    path('<int:user_id>/account/', views.patient_account, name='patient_account'),
    path('<int:user_id>/vitals/', views.patient_vitals, name='patient_vitals'),
    path('doctor/<int:doctor_id>/', views.doctor_interface, name='doctor_interface'),
    path('doctor/<int:doctor_id>/patients/', views.doctor_patient, name='doctor_patient'),
    path('<int:user_id>/bookappointment/', views.book_appointment, name="Book_Appointment"),
    path('doctor-action/<int:user_id>/', views.doctor_action, name='doctor_action'),
    path('vital_visual/',views.vital_visualization,name="Vital_Visual"),
    path('<int:user_id>/hospital-map/', views.hosp_map, name='hospital_map'),
    # path('vis/', views.visualize, name='visualize'),
    path('sympform/', views.symp_predict, name='sympform'),
    path('predict/', views.pred_value, name='predict'),
    path('index/',views.index, name='index'),
]
