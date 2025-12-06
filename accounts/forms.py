# accounts/forms.py
from collections import defaultdict
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import AccountType, CompletionRevisionFeedback, CustomUser, Department, Document, DocumentComment, DocumentFile, AnnualReport, ExtensionActivity, Linkage
from django.forms import ModelForm, DateField, ModelMultipleChoiceField, SelectDateWidget
from .models import  CustomUser
from django.utils import timezone
from .models import QuarterlyReport, ExtensionProject
from collections import defaultdict
from django.forms import ModelMultipleChoiceField
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model

# Custom user creation form for general users (admin, staff, etc.)
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'full_name', 'email', 'contact_number', 'gender', 'password1', 'password2', 'account_type', 'profile_image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        excluded = [
            AccountType.DEPARTMENT_COORDINATOR,
            AccountType.EXTENSIONIST,
        ]

        self.fields['account_type'].choices = [
            (key, label) for key, label in self.fields['account_type'].choices
            if key not in excluded
        ]


User = get_user_model()
# Form for updating existing users (for admins or self-admin)
class UserEditForm(forms.ModelForm):
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=False,
        label='Department'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'full_name', 'contact_number', 'gender', 'profile_image', 'department']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Only show department field if user is Coordinator or Extensionist
        if self.instance and self.instance.account_type not in [
            AccountType.DEPARTMENT_COORDINATOR,
            AccountType.EXTENSIONIST
        ]:
            self.fields.pop('department')
        else:
            # Pre-select the current department if exists
            if self.instance and self.instance.department:
                self.fields['department'].initial = self.instance.department

    def clean_username(self):
        username = self.cleaned_data['username']
        qs = User.objects.filter(username=username)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("A user with that username already exists.")
        return username




class DepartmentCoordinatorRegistrationForm(UserCreationForm):
    department = forms.ModelChoiceField(queryset=Department.objects.none(), required=True, label='Department')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'full_name', 'contact_number', 'gender', 'department', 'profile_image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].queryset = Department.objects.all()


class ExtensionistRegistrationForm(UserCreationForm):
    department = forms.ModelChoiceField(
        queryset=Department.objects.none(),
        required=False,                # <-- Make NOT required (important)
        label='Department'
    )

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'password1', 'password2',
            'full_name', 'contact_number', 'gender', 'department'
        )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)   # <-- receive current user
        super().__init__(*args, **kwargs)

        self.fields['department'].queryset = Department.objects.all()

        # If a coordinator is creating an extensionist
        if user and hasattr(user, 'department') and user.department:
            self.fields['department'].initial = user.department
            self.fields['department'].widget.attrs['readonly'] = True
            self.fields['department'].widget.attrs['style'] = (
                'pointer-events:none; background:#eee;'
            )


class DocumentCommentForm(forms.ModelForm):
    class Meta:
        model = DocumentComment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Write a comment...',
                'class': 'form-control w-100'  # Ensures full width and Bootstrap styling
            }),
        }


class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['name', 'Activity_Proposal', 'Work_and_Financial_Plan', 'Plan_of_Activities', 'doc4', 'doc5', 'doc6', 'doc7', 'doc8']
        


class CompletionUploadForm(forms.ModelForm):
    class Meta:
        model = DocumentFile
        fields = ['completion_doc1', 'completion_doc2', 'completion_doc3', 'completion_doc4', 'completion_doc5', 'completion_doc6', 'completion_doc7', 'completion_doc8']

from django import forms
from collections import defaultdict
from django.forms import ModelMultipleChoiceField
from .models import  CustomUser
from django.utils import timezone

# ✅ Step 1: Define this FIRST
class GroupedModelMultipleChoiceField(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.username

    def _get_choices(self):
        if hasattr(self, '_choices'):
            return self._choices

        choices = []
        from collections import defaultdict
        grouped = defaultdict(list)

        # Group users by their department
        for user in self.queryset.select_related('department').order_by('department__name', 'last_name'):
            dept = user.department.get_name_display() if user.department else "No Department"
            grouped[dept].append((user.pk, self.label_from_instance(user)))

        for dept, users in grouped.items():
            choices.append((dept, users))

        self._choices = choices
        return self._choices

    # Make choices a read-only property
    choices = property(_get_choices)

class AnnualReportForm(forms.ModelForm):
    class Meta:
        model = AnnualReport
        fields = ['year', 'google_drive_link']

class ExtensionActivityForm(forms.ModelForm):
    class Meta:
        model = ExtensionActivity
        fields = ['activity', 'extensionist', 'no_of_beneficiaries', 'partner_agency']
        
class LinkageForm(forms.ModelForm):
    class Meta:
        model = Linkage
        fields = ['agency', 'nature']
class QuarterlyReportForm(forms.ModelForm):
    class Meta:
        model = QuarterlyReport
        fields = ['year', 'quarter']
        widgets = {
            'quarter': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quarter'].empty_label = "Select Quarter"

class ExtensionProjectForm(forms.ModelForm):
    class Meta:
        model = ExtensionProject
        fields = [
            'title', 'date', 'duration_hours', 'sector',
            'target_no', 'actual_male', 'actual_female',
            'location', 'persons_responsible', 'budget_allocation', 'remarks'
        ]
        
# accounts/forms.py
# accounts/forms.py
from django import forms
from .models import Media

class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['title', 'media_type', 'file', 'description']

from django import forms
from .models import PhotoAlbum, Photo

class PhotoAlbumForm(forms.ModelForm):
    class Meta:
        model = PhotoAlbum
        fields = ['title', 'description', 'cover_photo']

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']  # Only one field, we'll handle multiple files in the view
from .models import Template

class TemplateForm(forms.ModelForm):
    class Meta:
        model = Template
        fields = ['title', 'description', 'file']
        
        

from .models import DocumentDay, DayTrainingReport

class DocumentDayForm(forms.ModelForm):
    class Meta:
        model = DocumentDay
        fields = ["title", "date"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"})
        }


class DayTrainingReportForm(forms.ModelForm):
    class Meta:
        model = DayTrainingReport
        fields = ["file"]

# forms.py
from django import forms
from .models import DocumentDayFile

class DocumentDayFileForm(forms.ModelForm):
    class Meta:
        model = DocumentDayFile
        fields = ["doc1", "doc2", "doc3", "doc4", "doc5"]
# forms.py
from django import forms
from .models import DocumentRevisionFeedback

class RevisionFeedbackForm(forms.ModelForm):
    class Meta:
        model = DocumentRevisionFeedback
        fields = ['comment', 'image']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Add a revision comment...'}),
        }
from django import forms
from .models import DayRevisionFeedback

class DayRevisionFeedbackForm(forms.ModelForm):
    class Meta:
        model = DayRevisionFeedback
        fields = ["comment", "image"]
        widgets = {
            "comment": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Write your comment..."
            }),
            "image": forms.ClearableFileInput(attrs={"class": "form-control", "accept": "image/*"}),
        }
from django import forms

class CompletionRevisionFeedbackForm(forms.ModelForm):
    class Meta:
        model = CompletionRevisionFeedback
        fields = ['comment', 'image']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter revision comment'}),
        }
        
from django import forms
from .models import MOAResource

class MOAResourceForm(forms.ModelForm):
    class Meta:
        model = MOAResource
        fields = ['title', 'logo', 'pdf_file']
