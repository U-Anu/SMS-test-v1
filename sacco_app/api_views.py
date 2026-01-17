from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from pesanile_accounting.models import CommonRegistration, Accounts,AccountEntry
from .serializers import *
from .models import *
from drf_yasg.utils import swagger_auto_schema
from accounting_engine.utils import *
from rest_framework import permissions

class CategoryTypeAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CategoryTypeSerializer

    @swagger_auto_schema(responses={200: CategoryTypeSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        try:
            records = CategoryType.objects.all()
            serializer = CategoryTypeSerializer(records, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=CategoryTypeSerializer)
    def post(self, request, *args, **kwargs):
        try:
            print('im here.....')
            serializer = CategoryTypeSerializer(data=request.data)
            if serializer.is_valid():
                obj = serializer.save()
                message = response_message('Success', message="Its Success", record_id=obj.pk)
                return Response(data=message, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)



class CategoryAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CategorySerializer

    @swagger_auto_schema(responses={200: CategorySerializer(many=True)})
    def get(self, request, *args, **kwargs):
        try:
            category_type = request.GET.get('category_type', None)
            if category_type is not None:
                records = Category.objects.filter(category_type_id=category_type)
                serializer = CategorySerializer(records, many=True)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            records = Category.objects.all()
            serializer = CategorySerializer(records, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=CategorySerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = CategorySerializer(data=request.data)
            if serializer.is_valid():
                obj = serializer.save()
                message = response_message('Success', message="Its Success", record_id=obj.pk)
                return Response(data=message, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)



class DefaultAccountSetupAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = DefaultAccountSetUpSerializer

    @swagger_auto_schema(responses={200: DefaultAccountSetUpSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        try:
            print('In here...')
            records = DefaultAccountSetUp.objects.all()
            serializer = DefaultAccountSetUpSerializer(records, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            print('error ',error)
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=DefaultAccountSetUpSerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = DefaultAccountSetUpSerializer(data=request.data)
            if serializer.is_valid():
                obj = serializer.save()
                message = response_message('Success', message="Its Success", record_id=obj.pk)
                return Response(data=message, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)


class GetAccountDetailsAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(responses={200: CategorySerializer(many=True)})
    def get(self, request, register_id, *args, **kwargs):
        try:
            obj = CommonRegistration.objects.filter(register_id=register_id)
            if obj.exists():
                cr_id = obj.first().pk
                acc_obj = Accounts.objects.filter(cr_id_id=cr_id)
                serializer = GetAccountRecordSerializer(acc_obj, many=True)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                message = response_message('Failed', message=f"Record Not Found")
                return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)



class GetAccountDetailsByBankidAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, code, *args, **kwargs):
        try:
            obj = Accounts.objects.filter(bank__code=code)
            if obj.exists():
                serializer = GetAccountRecordSerializer(obj, many=True)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                message = response_message('Failed', message=f"Record Not Found")
                return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)


class GetAccountEntryListAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, code, *args, **kwargs):
        try:
            account = Accounts.objects.get(account_number=code)
            obj=AccountEntry.objects.filter(account_number=account.account_id)
            if obj.exists():
                serializer = GetAccountEntrySerializer(obj, many=True)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                message = response_message('Failed', message=f"Record Not Found")
                return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
