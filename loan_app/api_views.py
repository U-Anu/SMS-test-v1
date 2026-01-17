from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from pesanile_accounting.models import Accounts
from .models import *
from .serializers import *
from .models import *
from drf_yasg.utils import swagger_auto_schema
from accounting_engine.utils import *
from rest_framework import permissions
from pesanile_accounting.serializers import AccountsSerializer


# class LoanRegistrationAPIView(APIView):
#     permission_classes = [permissions.AllowAny]
#     serializer_class = LoanRegistrationSerializer

#     @swagger_auto_schema(request_body=LoanRegistrationSerializer)
#     def post(self, request, *args, **kwargs):
#         try:
#             print('im here.....')
#             serializer = LoanRegistrationSerializer(data=request.data)
#             if serializer.is_valid():
#                 obj = serializer.save()
#                 message = response_message('Success', message="Its Success", record_id=obj.pk)
#                 return Response(data=message, status=status.HTTP_201_CREATED)
#             return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as error:
#             message = response_message('Failed', message=f"{error}")
#             return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

class GetLoanAccountAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(responses={200: GetAccountListSerializer(many=True)})
    def get(self, request, loan_id=None, *args, **kwargs):
        try:
            if loan_id is None:
                records = Accounts.objects.filter(loan__isnull=False)
                print('records ',records.count())
                serializer = GetAccountListSerializer(records, many=True)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                records = Accounts.objects.filter(loan=loan_id)
                serializer = GetAccountListSerializer(records, many=True)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

