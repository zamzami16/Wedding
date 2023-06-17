from django.http import Http404
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import (
    generics,
    status,
    permissions,
    viewsets,
    authentication,
    exceptions,
)
from rest_framework.decorators import action
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response

from .models import Invitation
from .serializers import (
    InvitationSerializer,
    InvitationCreateSerializer,
    InvitationDetailSerializer,
)


class InvitationView(viewsets.ViewSet):
    authentication_classes = (
        authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    )
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request):
        queryset = Invitation.objects.all()
        serializer = InvitationSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Invitation.objects.all()
        invitation = get_object_or_404(queryset, pk=pk)
        serializer = InvitationDetailSerializer(invitation)
        return Response(serializer.data)

    def create(self, request):
        serializer = InvitationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "status": "success",
                "message": "object invitation created.",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

    def handle_exception(self, exc):
        if isinstance(exc, exceptions.ValidationError):
            return Response(
                {
                    "status": "failed",
                    "message": exc.detail,
                    "detail": exc.get_full_details(),
                },
                status=exc.status_code,
            )
        return super().handle_exception(exc)
