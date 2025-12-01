# accounts/models.py
import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from datetime import datetime
from django.utils.timezone import now

class AccountType(models.TextChoices):
    SUPER_ADMIN = 'Super Admin', 'Campus Dean'
    CAMPUS_ADMIN = 'Campus Admin', 'Campus Extension Coordinator'
    STAFF_EXTENSIONIST = 'Staff Extensionist', 'Staff Extensionist'
    DEPARTMENT_COORDINATOR = 'Department Coordinator', 'Department Coordinator'
    EXTENSIONIST = 'Extensionist', 'Extensionist'

class Department(models.Model):
    name = models.CharField(max_length=100, choices=[
        ('DCS', 'DCS (IT-CS)'),
        ('DMS (HM)', 'DMS (HM)'),
        ('DMS (BM)', 'DMS (BM)'),
        ('DC', 'DC (Criminology)'),
        ('DAS', 'DAS (Psychology)'),
        ('DTE', 'DTE (Education)')
    ])
    
    def __str__(self):
        return self.get_name_display()

class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    account_type = models.CharField(
        max_length=50,
        choices=AccountType.choices,
    )
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL)
    full_name = models.CharField(max_length=150)
    contact_number = models.CharField(max_length=15)
    profile_image = models.ImageField(upload_to='documents/profile_images/', null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True, default='Female')  # 👈 New field

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.full_name




from django.db import models
from django.conf import settings
from django.utils.timezone import now

class Document(models.Model):
    DOCUMENT_STATUS = [
        ('pending', 'Pending'),
        ('recommended', 'Recommended'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('completion_processing', 'Completion Reviewing'),
        ('completion_recommended', 'Completion Recommended'),
    ]

    name = models.CharField(max_length=255)
    department = models.ForeignKey('accounts.Department', on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=30, choices=DOCUMENT_STATUS, null=True, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    status_updated_at = models.DateTimeField(default=now)

    # Initial docs
    Activity_Proposal = models.FileField(upload_to='documents/', null=True, blank=False)
    Activity_Proposal_status = models.CharField(max_length=20, default="normal")  # NEW

    Work_and_Financial_Plan = models.FileField(upload_to='documents/', null=True, blank=True)
    Work_and_Financial_Plan_status = models.CharField(max_length=20, default="normal")  # NEW

    Plan_of_Activities = models.FileField(upload_to='documents/', null=True, blank=True)
    Plan_of_Activities_status = models.CharField(max_length=20, default="normal")  # NEW

    doc4 = models.FileField(upload_to='documents/', null=True, blank=True)
    doc4_status = models.CharField(max_length=20, default="normal")  # NEW

    doc5 = models.FileField(upload_to='documents/', null=True, blank=True)
    doc5_status = models.CharField(max_length=20, default="normal")  # NEW

    doc6 = models.FileField(upload_to='documents/', null=True, blank=True)
    doc6_status = models.CharField(max_length=20, default="normal")  # NEW

    doc7 = models.FileField(upload_to='documents/', null=True, blank=True)
    doc7_status = models.CharField(max_length=20, default="normal")  # NEW

    doc8 = models.FileField(upload_to='documents/', null=True, blank=True)
    doc8_status = models.CharField(max_length=20, default="normal")  # NEW


    is_archived = models.BooleanField(default=False)

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    uploaded_by_name = models.CharField(max_length=150, blank=True)  # fallback name

    recommended_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='recommended_documents'
    )
    recommended_by_name = models.CharField(max_length=150, blank=True)  # fallback

    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='approved_documents'
    )
    approved_by_name = models.CharField(max_length=150, blank=True)  # fallback

    def save(self, *args, **kwargs):
        # Store fallback names
        if self.uploaded_by:
            self.uploaded_by_name = self.uploaded_by.get_full_name() or self.uploaded_by.username
        if self.recommended_by:
            self.recommended_by_name = self.recommended_by.get_full_name() or self.recommended_by.username
        if self.approved_by:
            self.approved_by_name = self.approved_by.get_full_name() or self.approved_by.username

        # Update status timestamp if status changes
        if self.pk:  # means this is an update, not a new record
            old_status = Document.objects.filter(pk=self.pk).values_list('status', flat=True).first()
            if old_status != self.status:
                self.status_updated_at = now()
        else:
            self.status_updated_at = now()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class DocumentComment(models.Model):
    document = models.ForeignKey('Document', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    user_name_snapshot = models.CharField(max_length=150, blank=True)

    def save(self, *args, **kwargs):
        if self.user and not self.user_name_snapshot:
            self.user_name_snapshot = self.user.get_full_name() or self.user.username
        super().save(*args, **kwargs)

    def __str__(self):
        name = self.user.get_full_name() if self.user else self.user_name_snapshot or "Unknown User"
        return f"{name} on {self.document.name}"

    
class DocumentFile(models.Model):
    document = models.ForeignKey(Document, related_name='files', on_delete=models.CASCADE)
    completion_doc1 = models.FileField(upload_to='documents/completion/', null=True, blank=True)# Required file input for completion_doc1
    completion_doc1_status = models.CharField(max_length=20, default="normal")
    completion_doc1_label = models.CharField(max_length=100, default="attendace")  
    completion_doc2 = models.FileField(upload_to='documents/completion/', null=True, blank=True) # Required file input for completion_doc2
    completion_doc2_status = models.CharField(max_length=20, default="normal")  
    completion_doc3 = models.FileField(upload_to='documents/completion/', null=True, blank=True) # Required file input for completion_doc3
    completion_doc3_status = models.CharField(max_length=20, default="normal")  
    completion_doc4 = models.FileField(upload_to='documents/completion/', null=True, blank=True)  # Optional file input for completion_doc4
    completion_doc4_status = models.CharField(max_length=20, default="normal")  
    completion_doc5 = models.FileField(upload_to='documents/completion/', null=True, blank=True)  # Optional file input for completion_doc5
    completion_doc5_status = models.CharField(max_length=20, default="normal")  
    completion_doc6 = models.FileField(upload_to='documents/completion/', null=True, blank=True)  # Optional file input for completion_doc6
    completion_doc6_status = models.CharField(max_length=20, default="normal")  
    completion_doc7 = models.FileField(upload_to='documents/completion/', null=True, blank=True)  # Optional file input for completion_doc7
    completion_doc7_status = models.CharField(max_length=20, default="normal")  
    completion_doc8 = models.FileField(upload_to='documents/completion/', null=True, blank=True) 
    completion_doc8_status = models.CharField(max_length=20, default="normal")  
    

from django.contrib.auth import get_user_model

User = get_user_model()

from django.conf import settings

class ChatMessage(models.Model):
    document = models.ForeignKey('Document', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    sender_name_snapshot = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='read_messages', blank=True)

    def __str__(self):
        return f'{self.sender_name_snapshot} ({self.document}): {self.message}'




    
class AnnualReport(models.Model):
    year = models.PositiveIntegerField()
    google_drive_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Annual Report {self.year}"

class ExtensionActivity(models.Model):
    report = models.ForeignKey(AnnualReport, on_delete=models.CASCADE, related_name='activities')
    activity = models.TextField()
    extensionist = models.CharField(max_length=255, blank=True)
    no_of_beneficiaries = models.CharField(max_length=100)
    partner_agency = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.activity
    
class Linkage(models.Model):
    report = models.ForeignKey(AnnualReport, related_name='linkages', on_delete=models.CASCADE)
    agency = models.CharField(max_length=255)
    nature = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.agency} - {self.nature}"
    
from django.db import models

class QuarterlyReport(models.Model):
    QUARTER_CHOICES = [
        ('Q1', 'January to March'),
        ('Q2', 'April to June'),
        ('Q3', 'July to September'),
        ('Q4', 'October to December'),
    ]

    year = models.PositiveIntegerField()
    quarter = models.CharField(
    max_length=2,
    choices=QUARTER_CHOICES,
    default='Q1',
)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Quarterly Report {self.get_quarter_display()} {self.year}"


class ExtensionProject(models.Model):
    report = models.ForeignKey(QuarterlyReport, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=255)
    date = models.DateField()
    duration_hours = models.PositiveIntegerField()

    sector = models.CharField(max_length=100)
    target_no = models.PositiveIntegerField()
    actual_male = models.PositiveIntegerField()
    actual_female = models.PositiveIntegerField()

    location = models.CharField(max_length=255)
    persons_responsible = models.CharField(max_length=255)
    budget_allocation = models.DecimalField(max_digits=12, decimal_places=2)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
    
    
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

def validate_video_file(value):
    valid_extensions = ['.mp4', '.mov', '.avi', '.mkv']  # allowed video formats
    import os
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError(f'Unsupported file extension. Allowed: {", ".join(valid_extensions)}')

class Media(models.Model):
    MEDIA_TYPES = [
        ('video', 'Video')
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(
        blank=True, 
        null=True, 
        help_text="Optional: Add a brief description or details about the video."
    )
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES, default='video')
    file = models.FileField(upload_to='media_uploads/', validators=[validate_video_file])
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"{self.title} ({self.media_type})"

from django.db import models
from django.conf import settings

class PhotoAlbum(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    cover_photo = models.ImageField(upload_to='album_covers/', blank=True, null=True)  # 👈 allow empty
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.title

    @property
    def cover_url(self):
        """Return the cover photo URL or fallback to default image."""
        if self.cover_photo:
            return self.cover_photo.url
        from django.templatetags.static import static
        return static('image/no-image.png')


class Photo(models.Model):
    album = models.ForeignKey(PhotoAlbum, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='album_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.image.name if self.image else f"Photo {self.id}"

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        from django.templatetags.static import static
        return static('image/no-image.png')

class Template(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='templates/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
  

class DocumentDay(models.Model):
    document = models.ForeignKey("Document", on_delete=models.CASCADE, related_name="days")
    title = models.CharField(max_length=255)  # e.g. "Day 1", "Orientation Day"
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return f"{self.title} ({self.date}) - {self.document.name}"


class DayTrainingReport(models.Model):
    day = models.ForeignKey("DocumentDay", on_delete=models.CASCADE, related_name="training_reports")
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="day_training_reports/")
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"{self.title} - {self.day.name} ({self.day.document.name})"

# accounts/models.py
from django.db import models
from django.conf import settings

class DayTrainingEntry(models.Model):
    report = models.ForeignKey(
        "DayTrainingReport",
        on_delete=models.CASCADE,
        related_name="entries"
    )

    # uploader info
    department = models.CharField(max_length=255, blank=True)
    contact_person = models.CharField(max_length=255, blank=True)
    number_email = models.CharField(max_length=255, blank=True)
    
    coordinator_name = models.CharField(max_length=255, blank=True, null=True)
    coordinator_email = models.EmailField(blank=True, null=True)
    # core fields
    project_no = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=255, blank=True)
    title = models.TextField(blank=True)
    date_conducted_text = models.CharField(max_length=255, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    number_of_days = models.IntegerField(null=True, blank=True)
    number_of_days_label = models.CharField(max_length=20, blank=True, null=True)

    # sex
    male_participants = models.IntegerField(null=True, blank=True)
    female_participants = models.IntegerField(null=True, blank=True)
    total_participants = models.IntegerField(null=True, blank=True)

    # by category
    student = models.IntegerField(null=True, blank=True)
    farmer = models.IntegerField(null=True, blank=True)
    fisherfolk = models.IntegerField(null=True, blank=True)
    agricultural_technician = models.IntegerField(null=True, blank=True)
    government_employee = models.IntegerField(null=True, blank=True)
    private_employee = models.IntegerField(null=True, blank=True)
    other_category = models.IntegerField(null=True, blank=True)
    total_by_category = models.IntegerField(null=True, blank=True)

    # total persons trained
    total_persons_trained = models.IntegerField(null=True, blank=True)

    # TVL-only
    tvl_solo_parent = models.IntegerField(null=True, blank=True)
    tvl_4ps = models.IntegerField(null=True, blank=True)
    tvl_pwd = models.IntegerField(null=True, blank=True)
    tvl_pwd_type = models.CharField(max_length=255, blank=True)

    # survey
    total_trainees_surveyed = models.IntegerField(null=True, blank=True)

    # ratings
    relevance_counts = models.JSONField(default=dict, blank=True)
    relevance_average = models.FloatField(null=True, blank=True)

    quality_counts = models.JSONField(default=dict, blank=True)
    quality_average = models.FloatField(null=True, blank=True)

    timeliness_counts = models.JSONField(default=dict, blank=True)
    timeliness_average = models.FloatField(null=True, blank=True)

    # computed weights
    weight_multiplier = models.FloatField(null=True, blank=True)
    weighted_persons = models.FloatField(null=True, blank=True)


    # extra info
    collaborating_agencies = models.TextField(blank=True)
    amount_charged_to_cvsu = models.CharField(max_length=255, blank=True, default='0')
    amount_charged_to_partner_agency = models.CharField(max_length=255, blank=True, default='0')
    venue = models.TextField(blank=True)
    related_curricular_offering = models.CharField(max_length=255, blank=True, null=True)

    # computed fields
    total_score = models.FloatField(null=True, blank=True)
    overall_average = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title[:60]} — {self.department}"
    
# models.py
class DocumentDayFile(models.Model):
    day = models.ForeignKey("DocumentDay", on_delete=models.CASCADE, related_name="day_files")

    # allow up to 5 document uploads
    doc1 = models.FileField(upload_to="day_documents/", null=True, blank=True)
    doc2 = models.FileField(upload_to="day_documents/", null=True, blank=True)
    doc3 = models.FileField(upload_to="day_documents/", null=True, blank=True)
    doc4 = models.FileField(upload_to="day_documents/", null=True, blank=True)
    doc5 = models.FileField(upload_to="day_documents/", null=True, blank=True)

    # NEW status fields
    doc1_status = models.CharField(max_length=20, default="normal")
    doc2_status = models.CharField(max_length=20, default="normal")
    doc3_status = models.CharField(max_length=20, default="normal")
    doc4_status = models.CharField(max_length=20, default="normal")
    doc5_status = models.CharField(max_length=20, default="normal")
    # track who uploaded and when
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"Day Files for {self.day.name} ({self.day.document.name})"
# models.py
class DocumentRevisionFeedback(models.Model):
    document = models.ForeignKey('Document', on_delete=models.CASCADE)
    slot_name = models.CharField(max_length=100)  # e.g., "Activity_Proposal" or "day_doc1"
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    image = models.ImageField(upload_to='revision_feedback/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
from django.db import models
from django.conf import settings  # ✅ import this

class DayRevisionFeedback(models.Model):
    document = models.ForeignKey("Document", on_delete=models.CASCADE, related_name="day_revision_feedbacks")
    day = models.ForeignKey("DocumentDay", on_delete=models.CASCADE, related_name="revision_feedbacks")
    slot_name = models.CharField(max_length=50)  # e.g., day_doc1, day_doc2, etc.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # ✅ fixed line
    comment = models.TextField()
    image = models.ImageField(upload_to="day_revision_feedbacks/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.day} - {self.slot_name} ({self.user})"

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class CompletionRevisionFeedback(models.Model):
    document = models.ForeignKey('Document', on_delete=models.CASCADE)
    completion_file = models.ForeignKey('DocumentFile', on_delete=models.CASCADE, related_name='completion_feedbacks')
    slot_name = models.CharField(max_length=50)  # e.g., "completion_doc1"
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    image = models.ImageField(upload_to='documents/completion/revision/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

from django.db import models

class MOAResource(models.Model):
    title = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='moa_logos/')
    pdf_file = models.FileField(upload_to='moa_pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


from django.db import models

class ShowcaseImage(models.Model):
    image = models.ImageField(upload_to="showcase/")
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['position']  # Show ordered images

