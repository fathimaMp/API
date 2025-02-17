from django.urls import path,include
from . import views
from rest_framework.routers import SimpleRouter
app_name = "demo_app"

#Viewset
router = SimpleRouter()
router.register('students',views.StudentView)

urlpatterns = [
    # path('',views.student_list.as_view(),name='student_list'),
    # path('student_details/<int:pk>', views.student_details.as_view(), name='student_details'),
    path('',include(router.urls)),

]

