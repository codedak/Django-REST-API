from django.urls import path, re_path, include
from .views import ListSchoolsView, ListFilteredSchoolsView, addDataToDB


urlpatterns = [
    re_path('(?P<version>(v1|v2))/schools/', ListSchoolsView.as_view(), name="schools-all"),
    re_path('(?P<version>(v1|v2))/filter/', ListFilteredSchoolsView.as_view(), name="schools-filtered"),
    path('add-data-to-db/', addDataToDB, name="add-data"),
]
