from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import FileExtensionValidator

# For each of the model, a 'created' datetime field is created, so that
# we can display to users content sorted from newest to oldest..
# Also, for the purposes of storing file uploads, we had to change
# our settings.py file accordingly.

# Extended User model with email, first and last name as required fields, 
# and also with additional (optional) fields.
class User(AbstractUser):
    email = models.EmailField("Email adress", blank=False)
    first_name = models.CharField("First Name", max_length=100, blank=False)
    last_name = models.CharField("Last Name", max_length=100, blank=False)
    name = models.CharField(max_length=200, null=True)
    photo = models.ImageField(blank=True, default="default_profile_pic.png", upload_to="photos/%Y/%m/%D/")
    bio = models.TextField(blank=True)
    twitter = models.URLField("Twitter URL(optional)", blank=True, max_length=300)
    facebook = models.URLField("Facebook URL(optional)", blank=True, max_length=300)
    instagram = models.URLField("Instagram URL(optional)", blank=True, max_length=300)
    youtube = models.URLField("YouTube URL(optional)", blank=True, max_length=300)
    amazon = models.URLField("Amazon Author's Page URL(optional)", blank=True, max_length=300)
    author = models.BooleanField(default=False)

    def save(self, *args, **kw):
        self.name = f"{self.first_name} {self.last_name}"
        super(User,self).save(*args, **kw)

    def __str__(self):
        return(f"{self.username}")

# Model for our scripts. Types and categories are hard coded since they'll not change,
# but we can imagine, that if needed this to change in the future, that we would create
# a separate model just for them. 
# Also, for simplicity, fields with whitespace in them are truncated, since that was the
# easiest way to correct error that django threw after browsing for categories and types
# with whitespace in them..
# Cover is optional, and if one isn't selected, the default cover will be applied
# .docx file, on the other hand, is a required field.
class Script(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="script")
    title = models.CharField(max_length=200)
    summary = models.TextField()
    TYPES = [
        ("Concept", "Concept"), ("Draft", "Draft"), ("ShortStory", "ShortStory")
    ]
    CATEGORIES = [
        ("Adventure", "Adventure"), ("Comedy", "Comedy"), ("Epic", "Epic"), ("Erotica", "Erotica"),("FairyTale", "FairyTale"), 
        ("Fantasy", "Fantasy"), ("HistoricalFiction", "HistoricalFiction"), ("Horror", "Horror"),
        ("Mystery", "Mystery"), ("Romance", "Romance"), ("Satire", "Satire"), ("ScienceFiction", "ScienceFiction"),
        ("Thriller", "Thriller")
    ]
    script_type = models.CharField(max_length=20, choices=TYPES)
    category = models.CharField(max_length=25, choices=CATEGORIES)
    created = models.DateTimeField(auto_now_add=True)
    upload = models.FileField("Select your script", upload_to="scripts/%Y/%m/%D/", validators=[FileExtensionValidator(allowed_extensions=['docx'])])
    cover = models.ImageField("Select your cover image(optional)", default="default_cover_pic.png", upload_to="covers/%Y/%m/%D/", blank=True)

    def __str__(self):
        return(f"{self.title}")

# Model for storing ratings. Ratings are stored as integers from 1 to 5, but the form
# itself for ratings is built with radio inputs, with the actuall input being checked
# for type (int) and value (1-5) in the view..
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rating")
    script = models.ForeignKey(Script, on_delete=models.CASCADE, related_name="rating")
    storyline_rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    characters_rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    writing_rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        avg = float((self.storyline_rating + self.writing_rating + self.characters_rating)/3)
        return(f"Rating: {avg}")

# Model for storing comments. Comments are unlimited text fields.
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
    script = models.ForeignKey(Script, on_delete=models.CASCADE, related_name="comment")
    comment = models.TextField("")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return(f"{self.user}:{self.comment[:10]}... on {self.script}")

# Model for storing suggestions. They too are unlim text fields.
class Suggestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="suggestion")
    script = models.ForeignKey(Script, on_delete=models.CASCADE, related_name="suggestion")
    suggestion = models.TextField("")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return(f"{self.user}:{self.suggestion[:10]}... on {self.script}")

# Model for storing scripts that user started reading (clicked on read button)
class Reading(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reading")
    script = models.ForeignKey(Script, on_delete=models.CASCADE, related_name="reading")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return(f"{self.user} read {self.script}.")

# Model for storing scripts that user stored in their Read Later 'library'
class ReadLater(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="read_later")
    script = models.ForeignKey(Script, on_delete=models.CASCADE, related_name="read_later")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return(f"{self.user} added {self.script} to read later.")

# Model for storing user's favorite authors.
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    created = models.DateTimeField(auto_now_add=True)

    def _str__(self):
        return(f"{self.user} added {self.author} to his favorite authors.")

# Finally, model for storing notes that user made while reading. They too are
# unlimited text fields.
class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="note")
    note = models.TextField()
    source = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return(f"{self.user}:{self.note[:10]}...")