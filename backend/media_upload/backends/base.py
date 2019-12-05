import mimetypes

from django.http import Http404


class BaseMediaUploadBackend(object):
    def get_presigned_url(self):
        # Subclasses must implement this
        raise NotImplementedError

    def process_upload(self, *args, **kwargs):
        # By default the upload is done outside our system
        raise Http404

    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs

    def _get_filename(self):
        return self.request.GET.get("filename", "data")

    def _get_content_type(self):
        filename = self._get_filename()
        content_type = self.request.GET.get(
            "contentType",
            mimetypes.guess_type(filename)[0] or "application/octet-stream",
        )
        return content_type
