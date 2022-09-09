from rest_framework import serializers

from api.models import Proposal
from authentication.models import User

class ProposalSerializer(serializers.ModelSerializer):

    proposal_name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    proposal_date = serializers.DateField(required=False)

    # Updator Variable
    updater = ""

    class Meta:
        model = Proposal
        fields = ('id', 'proposal_name', 'description', 'proposal_date', 'created_by', 'created_date', 'modified_by', 'modified_date')

    def set_updater(self, updater: User):
        self.updater = updater.name

    def create(self, validated_data):
        # To be executed when a fresh instance is created.
        proposal = Proposal(
            proposal_name=validated_data.get("proposal_name"),
            description=validated_data.get("description"),
            proposal_date=validated_data.get("proposal_date"),
            created_by=self.updater,
            modified_by=self.updater
        )
        proposal.save()
        return proposal
    
    def update(self, instance, validated_data):
        # To be executed when an existing instance is modified.
        instance.proposal_name=validated_data.get("proposal_name", instance.proposal_name)
        instance.description=validated_data.get("description", instance.description)
        instance.proposal_date=validated_data.get("proposal_date", instance.proposal_date)
        instance.modified_by=self.updater
        instance.save()
        return instance

    