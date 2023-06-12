from django.contrib.auth.models import User
from django.http import Http404
from rest_framework.response import Response
from rest_framework import (
    generics,
    authentication,
    permissions,
    status,
    exceptions,
)

from .serializers import BukuTamuSerializer, BukuTamuCreateSerializer
from .models import BukuTamu


class BukuTamuListView(generics.ListAPIView):
    """
    List of buku tamu data.

    endpoint: api/buku_tamu/?inviter={{username}}
        * inviter is optional,
            - if inviter exists, will return bukutamu for related user
            - if not exists, return all of buku tamu instance
    """

    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)
    serializer_class = BukuTamuSerializer
    queryset = BukuTamu.objects.all()

    def get_queryset(self):
        if "inviter" not in self.request.GET:
            return BukuTamu.objects.all()
        user_name = self.request.GET["inviter"]
        user = User.objects.get(username=user_name)
        return BukuTamu.objects.filter(inviter=user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        if len(serializer.data) == 0:
            return Response(
                {
                    "status": "success",
                    "message": "data not found",
                    "data": {},
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(
            {
                "status": "success",
                "count": len(serializer.data),
                "data": serializer.data,
            }
        )

    def handle_exception(self, exc):
        if isinstance(exc, Http404):
            return Response(
                {
                    "status": "success",
                    "message": "data not found",
                    "detail": str(exc),
                },
                status=status.HTTP_204_NO_CONTENT,
            )

        return super().handle_exception(str(exc))


class BukuTamuCreateView(generics.ListCreateAPIView):
    """
    create bukutamu instance for guest and related to User / inviter

    endpoint: api/buku_tamu/user/absen/

    fields required in request body:
        * inviter_username
        * nama
        * kehadiran:
            - Hadir = "HA"
            - Tidak Hadir = "TH"
            - Belum Tahu = "BT"
            - Insya Allah = "IA"
        * ucapan
    """

    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)
    serializer_class = BukuTamuCreateSerializer
    queryset = BukuTamu.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "status": "success",
                "message": "Data berhasil disimpan",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

    def handle_exception(self, exc):
        return Response(
            {
                "status": "failed",
                "message": "data gagal disimpan",
                "details": exc.__str__(),
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class BukuTamuDestroyView(generics.DestroyAPIView):
    """
    delete buku tamu instance for autthenticated user.

    endpoint: 'api/buku_tamu/delete/?id=bukutamuid'
        * parameter id is optional,
        * if not provided, it will delete all bukutamu instance related to user
    """

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        buku_tamu = BukuTamu.objects.filter(inviter=self.request.user)
        if "id" in self.request.GET:
            buku_tamu = BukuTamu.objects.filter(
                inviter=self.request.user, id=self.request.GET["id"]
            )
        return buku_tamu

    def destroy(self, request, *args, **kwargs):
        buku_tamu = self.get_object()
        if buku_tamu.count() == 0:
            id = self.request.GET["id"] if "id" in self.request.GET else ""
            raise exceptions.NotFound(
                f"Data buku tamu dengan id {id} tidak ditemukan."
            )
        self.perform_destroy(buku_tamu)
        return Response(status=status.HTTP_200_OK)

    def handle_exception(self, exc):
        if isinstance(exc, exceptions.AuthenticationFailed):
            return Response(
                {"status": "failed", "message": "Invalid token."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if isinstance(exc, exceptions.NotFound):
            return Response(
                {
                    "status": "failed",
                    "message": "Data tidak ditemukan.",
                    "detail": exc.detail,
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        return super().handle_exception(exc)
