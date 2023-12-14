from urllib.parse import urlparse

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from django.utils import timezone

from .models import VisitedLink
from .serializer import TimeStampSerializer, VisitedLinkSerializer 


class VisitedLinkViewSet(viewsets.GenericViewSet):
    queryset = VisitedLink.objects.all()
    serializer_class = VisitedLinkSerializer

    @action(
        detail=False, methods=('post',), url_path='visited-links', permission_classes=(IsAuthenticated,),
    )
    def visited_links(self, request: Request, **kwargs):
        data = {}
        serializer = self.get_serializer(data=request.data)
        response_status = status.HTTP_400_BAD_REQUEST
        if serializer.is_valid():
            visited_at = timezone.now()
            VisitedLink.objects.bulk_create([VisitedLink(
                    **{
                        'visited_at': visited_at,
                        'link': link,
                        'domain': urlparse(link).netloc,
                    }
                ) for link in serializer.validated_data['links']
            ])
            data['status'] = 'ok'
            response_status = status.HTTP_201_CREATED
        else:
            data['status'] = serializer.errors

        return Response(data=data, status=response_status)

    @action(
        detail=False, methods=('get',), url_path='visited-domains', permission_classes=(IsAuthenticated,),
        serializer_class=TimeStampSerializer,
    )
    def visited_domains(self, request: Request, **kwargs):
        data = {}
        serializer = self.get_serializer(
            data={
                'from_date': request.query_params.get('from'),
                'to_date': request.query_params.get('to'),
            }
        )
        response_status = status.HTTP_400_BAD_REQUEST
        if serializer.is_valid():
            domains = self.get_queryset().filter(
                visited_at__range=[serializer.validated_data['from_date'], serializer.validated_data['to_date']]
            ).distinct('domain').values_list('domain', flat=True)
            data['domains'] = domains
            data['status'] = 'ok'
            response_status = status.HTTP_200_OK
        else:
            data['status'] = serializer.errors

        return Response(data=data, status=response_status)
