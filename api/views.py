import datetime
import re
import os
import csv
from drf_yasg.utils import swagger_auto_schema
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import status, mixins, generics
from rest_framework.views import APIView
from api.models import Proposal
from api.serializer import ProposalSerializer
from rest_framework.pagination import PageNumberPagination

from authentication.serializer import UserAccountSerializer
from authentication.models import User
import logging

logger = logging.getLogger('__name__')

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProposalViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Proposal.objects.all()
    pagination_class = LargeResultsSetPagination
    serializer_class = ProposalSerializer

    def list(self, request):
        serializer = ProposalSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        item = get_object_or_404(self.queryset, pk=pk)
        serializer = ProposalSerializer(item)
        return Response(serializer.data)

    def create(self, request):
        serializer = ProposalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.set_updater(request.user)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """
        Update the Porposal
        """
        # Fetch user account
        proposal = Proposal.objects.filter(pk=pk).last()
        if not proposal:
            raise APIException("No Proposal with the provided ID was found.")
        
        proposal = ProposalSerializer(proposal, request.data)
        proposal.is_valid(raise_exception=True)
        proposal.set_updater(request.user)
        proposal.save()

        return Response(data=proposal.data)

    def destroy(self, request, pk=None):
        """
        Delete a single proposal
        """
        # Fetch user account
        proposal = Proposal.objects.filter(pk=pk).last()
        if not proposal:
            raise APIException("No Proposal with the provided ID was found.")
        
        proposal.delete()

        return Response(data={
            "message": "Proposal was deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)


class UserSearch(mixins.ListModelMixin, mixins.CreateModelMixin,generics.GenericAPIView):

    permission_classes = [IsAuthenticated,]
    serializer_class = UserAccountSerializer
    pagination_class = LargeResultsSetPagination
    http_method_names = ['get']
    query_email = None

    def get_queryset(self):
        return User.objects.filter(email=self.query_email).order_by('-id')

    def get(self, request, *args, **kwargs):
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+') 
        
        self.query_email = request.GET.get('email', None)
        if not self.query_email or not re.fullmatch(regex, self.query_email):
            raise APIException("A valid Email was not provided in the search")
        return self.list(request, *args, **kwargs)


class ProposalSearch(mixins.ListModelMixin, mixins.CreateModelMixin,generics.GenericAPIView):

    permission_classes = [IsAuthenticated,]
    serializer_class = ProposalSerializer
    pagination_class = LargeResultsSetPagination
    http_method_names = ['get']
    query_name = None

    def get_queryset(self):
        return Proposal.objects.filter(proposal_name__contains=self.query_name).order_by('id')

    def get(self, request, *args, **kwargs):
        self.query_name = request.GET.get('name', None)
        if not self.query_name:
            logger.error("Proposal Name was not porvided in the query")
            raise APIException("Proposal Name was not provided in the search")
        return self.list(request, *args, **kwargs)


class DownloadMonthlyReport(APIView):
    """
    This is used to generate report for a based on duration
    """
    permission_classes = [IsAuthenticated]

    def validate(self, date_text, date_type):
        try:
            datetime.datetime.strptime(date_text, '%Y-%m-%d')
        except ValueError:
            raise APIException(f"Incorrect data format for {date_type}, should be YYYY-MM-DD")

    @swagger_auto_schema(operation_description="Download the report based on duration scope.")
    def post(self, request):
        # Read the start and end date from request
        try:
            start_date = request.data.get("start_date")
            end_date = request.data.get("end_date")
        except:
            raise APIException("start_date or end_date values are not provided")
        
        # Validate the provided date format
        self.validate(start_date, "start_date")
        self.validate(end_date, "end_date")

        queryset = Proposal.objects.filter(proposal_date__range=[start_date, end_date])
        
        """
        We'll create a temp csv file with all the data related to the extracted proposals
        and store it in the memory. This file will get changed with every new API call
        but since Django server is queue based, so the change in file will not effect
        the upcoming or former requests. This execise will also help us clear CSV files 
        in the next request that are already served.
        
        Though the ideal approach would be to use a scheduler to run a background job 
        and prepare the file, then email/store it in a bucket and share the download URL.
        But my server infrastructure will not support multiple instances in the same
        account under the free plan. So, I am keeping it simple.
        """


        try:
            f = open('temp_file.csv', 'w' )

            # create the csv writer
            writer = csv.writer(f)

            # Write the heading row
            writer.writerow([
                'ID', 
                'Porposal Name', 
                'Proposal Date', 
                'Description',
                'Created By',
                'Date',
            ])

            for row in queryset:
                writer.writerow([
                    row.pk, 
                    row.proposal_name, 
                    row.proposal_date, 
                    row.description, 
                    row.created_by, 
                    row.created_date.strftime("%m/%d/%Y, %H:%M:%S")
                ])

            # close the file
            f.close()

            data = open('temp_file.csv','r').read()
            resp = HttpResponse(data)
            resp['Content-Disposition'] = 'attachment;filename=report.csv'
            #resp['Content-Type'] = 'application/x-download'
            return resp
        except Exception as e:
            f.close()
            os.remove('temp_file.csv')
            raise APIException(f"Error: {e}")


