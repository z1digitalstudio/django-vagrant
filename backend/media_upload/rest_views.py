from django.conf import settings
from django.utils.module_loading import import_string

from rest_framework import views, permissions
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response


class MediaUploadBackendMixin(object):
    def get_backend(self, request, *args, **kwargs):
        backend_class = import_string(settings.MEDIA_UPLOAD_BACKEND)
        return backend_class(request, *args, **kwargs)


class GetFilesView(MediaUploadBackendMixin, views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        presigned_url_data = self.get_backend(
            request, *args, **kwargs
        ).get_presigned_url()
        if presigned_url_data is None:
            return Response({"error": "Invalid data"}, status=400)
        return Response(presigned_url_data)


class UploadFileView(MediaUploadBackendMixin, views.APIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = (FileUploadParser,)

    def put(self, request, *args, **kwargs):
        return self.get_backend(request, *args, **kwargs).process_upload()
