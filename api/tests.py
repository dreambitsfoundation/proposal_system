from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from api.views import ProposalViewSet
from authentication.models import User
from rest_framework import status
from api.models import Proposal


class TestProposalAPIs(TestCase):

    proposal_id = None
    
    def setUp(self) -> None:
        u = User.objects.create(phone_number="1234567890", name="Test Name", email="EmailID")
        u.set_password("pass1234")
        u.save()

        p = Proposal.objects.create(
            proposal_name="Test Proposal", 
            proposal_date="2022-05-25", 
            description="Test Description"
        )

    def test_create_proposal(self):
        u = User.objects.get(phone_number="1234567890")
        factory = APIRequestFactory()
        request = factory.post('/api/proposal/', {
            'proposal_name': 'Test Proposal 1', 
            'proposal_date': '2022-05-25', 
            'description': 'test description'}, format='json')
        force_authenticate(request, u)
        view = ProposalViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        # Record the ID globally
        if response.status_code == status.HTTP_201_CREATED:
            self.proposal_id = response.data['id']

    def test_get_proposal(self):
        p = Proposal.objects.all().last()
        u = User.objects.get(phone_number="1234567890")
        factory = APIRequestFactory()
        request = factory.get(f'/auth/proposal/{p.pk}/')
        force_authenticate(request, u)
        view = ProposalViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=p.pk)
        self.assertEquals(response.data['id'], p.pk)

    def test_update_proposal(self):
        p = Proposal.objects.all().last()
        u = User.objects.get(phone_number="1234567890")
        factory = APIRequestFactory()
        request = factory.put(f'/auth/proposal/{p.pk}/', 
        {'description': 'Updated Description'}, format='json')
        force_authenticate(request, u)
        view = ProposalViewSet.as_view({'put': 'update'})
        response = view(request, pk=p.pk)
        
        # Check the ID if that is same.
        self.assertEquals(response.data['id'], p.pk)
        self.assertEquals(response.data['description'], 'Updated Description')

    def test_delete_proposal(self):
        p = Proposal.objects.all().last()
        u = User.objects.get(phone_number="1234567890")
        factory = APIRequestFactory()
        request = factory.delete(f'/auth/proposal/{p.pk}/')
        force_authenticate(request, u)
        view = ProposalViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=p.pk)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)


    def tearDown(self) -> None:
        User.objects.all().delete()
        Proposal.objects.all().delete()