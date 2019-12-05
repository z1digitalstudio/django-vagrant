from django.urls import path
from media_upload.rest_views import GetFilesView, UploadFileView

urlpatterns = [
    path("signed_url/", GetFilesView.as_view(), name="get_files"),
    path(
        "upload_file/<str:filename>/<str:token>/",
        UploadFileView.as_view(),
        name="upload_file",
    ),
]
