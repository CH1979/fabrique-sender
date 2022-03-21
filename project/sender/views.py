from rest_framework import generics, mixins, viewsets

from .models import Customer, Maillist
from .serializers import (
    CustomerSerializer,
    MaillistSerializer,
    MaillistListSerializer
)


class CustomerViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()


class MaillistViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = MaillistSerializer
    queryset = Maillist.objects.all()


class MaillistListAPIView(generics.ListAPIView):
    queryset = Maillist.objects.raw('''
       SELECT  sender_maillist.id id,
                start_at,
                finish_at,
                operator_code_id,
                tag_id,
                status_pending,
                status_failed,
                status_success
        FROM    sender_maillist
        LEFT JOIN (
            SELECT maillist_id, COUNT(*) AS "status_pending"
            FROM sender_message
            GROUP BY maillist_id, status
			HAVING status LIKE "Pending"
        ) t1
        ON      sender_maillist.id=t1.maillist_id
        LEFT JOIN (
            SELECT maillist_id, COUNT(*) AS "status_success"
            FROM sender_message
            GROUP BY maillist_id, status
			HAVING status LIKE "Success"
        ) t2
        ON      sender_maillist.id=t2.maillist_id
        LEFT JOIN (
            SELECT maillist_id, COUNT(*) AS "status_failed"
            FROM sender_message
            GROUP BY maillist_id, status
			HAVING status LIKE "Failed"
        ) t3
        ON      sender_maillist.id=t3.maillist_id
    ''')
    serializer_class = MaillistListSerializer
