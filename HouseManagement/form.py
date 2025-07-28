from django import forms
from .models import HouseFeatureAssignment, AdditionalFeatures

from django.core.exceptions import ObjectDoesNotExist

from .models import AdditionalFeatures  # Make sure this is the correct model for 'feature'

class HouseFeatureAssignmentForm(forms.ModelForm):
    class Meta:
        model = HouseFeatureAssignment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        feature = None

        # Try to get the instance or resolve it from initial using the feature ID
        try:
            feature = getattr(self.instance, 'feature', None)

            if not feature and 'feature' in self.initial:
                feature_id = self.initial['feature']
                feature = AdditionalFeatures.objects.get(pk=feature_id)

        except (ObjectDoesNotExist, AdditionalFeatures.DoesNotExist):
            feature = None

        # Safely access show_available_number only if feature is a real instance
        if feature and not getattr(feature, 'show_available_number', None):
            self.fields['available_number'].widget = forms.HiddenInput()
        else:
            self.fields['available_number'].required = False

