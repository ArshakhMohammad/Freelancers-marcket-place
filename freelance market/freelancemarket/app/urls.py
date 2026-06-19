from django.urls import path,include
from . import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

path('',views.landing,name='landing'),
path('freelancerreg/',views.freelancer_reg,name='freelancer_reg'),
path('freelancerlogin/',views.freelancer_login,name='freelancer_login'),
path('freelancerdashboard/',views.freelancer_dashboard,name='freelancer_dashboard'),
path('freelancerlogout/',views.freelancer_logout,name='freelancer_logout'),
path('freelancerprofile/<int:freelancer_id>',views.freelancer_profile,name=f'freelancer_profile'),
path("profile/<int:freelancer_id>/",views.profile,name="profile"),
path("clientreg/", views.client_reg, name="client_reg"),
path("clientlogin/", views.client_login, name="client_login"),
path("clientdashboard/",views.client_dashboard,name="client_dashboard"),
path("clientlogout/",views.client_logout,name="client_logout"),
path("postjob/",views.post_job,name="post_job"),
path("jobs/",views.job_list,name="job_list"),
path("apply/<int:job_id>/", views.apply_job, name="apply_job"),
path("applications/<int:job_id>/", views.job_applications, name="job_applications"),
path("apply/<int:job_id>/",views.apply_job,name="apply_job"),
path("application/accept/<int:app_id>/",views.accept_application,name="accept_application"),
path("application/reject/<int:app_id>/",views.reject_application,name="reject_application"),
path("my-applications/",views.my_applications,name="my_applications"),
path("cancel-application/<int:job_id>/", views.cancel_application, name="cancel_application"),
path("mark-completed/<int:job_id>/",views.mark_completed,name="mark_completed"),
path("approve-completion/<int:job_id>/", views.approve_completion, name="approve_completion"),
path("reject-completion/<int:job_id>/", views.reject_completion, name="reject_completion"),
path("admin-login/", views.admin_login, name="admin_login"),
path("admin-panel/", views.admin_panel, name="admin_panel"),

path("client/block/<int:client_id>/", views.block_client, name="block_client"),
path("client/unblock/<int:client_id>/", views.unblock_client, name="unblock_client"),
path("client/warn/<int:client_id>/", views.warn_client, name="warn_client"),

path("freelancer/block/<int:freelancer_id>/", views.block_freelancer, name="block_freelancer"),
path("freelancer/unblock/<int:freelancer_id>/", views.unblock_freelancer, name="unblock_freelancer"),
path("freelancer/warn/<int:freelancer_id>/", views.warn_freelancer, name="warn_freelancer"),
path('adminlogout/', views.admin_logout, name='admin_logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
