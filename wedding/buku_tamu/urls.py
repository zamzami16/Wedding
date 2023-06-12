from django.urls import path

from .views import BukuTamuListView, BukuTamuCreateView, BukuTamuDestroyView


urlpatterns = [
    path("", BukuTamuListView.as_view(), name="buku_tamu_user"),
    path("user/absen/", BukuTamuCreateView.as_view(), name="mengisi buku tamu"),
    path("delete/", BukuTamuDestroyView.as_view(), name="hapus buku tamu"),
    path(
        "delete/<int:pk>/",
        BukuTamuDestroyView.as_view(),
        name="hapus buku tamu",
    ),
]
