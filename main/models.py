from django.db import models


class Information(models.Model):
    comp_name = models.CharField(max_length=60)
    logo = models.ImageField(upload_to="BannerImg")
    address = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    working_time = models.CharField(max_length=255)
    about = models.TextField()
    fb = models.URLField()
    tg = models.URLField()
    insta = models.URLField()

    def str(self):
        return self.comp_name


class Banner(models.Model):
    img = models.ImageField(upload_to='BannerIMG')
    title = models.CharField(max_length=255)
    mid_title = models.CharField(max_length=255)
    typ_education = models.CharField(max_length=255)


class About(models.Model):
    img = models.ImageField(upload_to='AboutIMG')
    quantity = models.IntegerField(default=0)
    title = models.CharField(max_length=255)


class Language(models.Model):
    name = models.CharField(max_length=255)
    registered = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Faculty(models.Model):
    name = models.CharField(max_length=255)
    img = models.ImageField(upload_to='FacultyIMG')
    registered = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class AboutMe(models.Model):
    img = models.ImageField(upload_to='AboutMeIMG')
    title = models.CharField(max_length=255)


class ContactUs(models.Model):
    phone_number = models.CharField(max_length=25)


class Degree(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=5)

    def __str__(self):
        return self.name


class UnivGallery(models.Model):
    img = models.ImageField(upload_to='UnivGalleryIMG')


class Region(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Sessions(models.Model):
    name = models.CharField(max_length=255)


class University(models.Model):
    name = models.CharField(max_length=255)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    city = models.CharField(max_length=255)
    date = models.DateField()
    img = models.ImageField(upload_to='UniversityIMG')
    banner = models.ImageField(upload_to='UniversityBanner')
    address = models.CharField(max_length=255)
    about = models.TextField()
    rating = models.IntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=5)
    process = models.CharField(max_length=255)
    control = models.CharField(max_length=255)
    gallery = models.ManyToManyField(UnivGallery)
    motto = models.CharField(max_length=255)
    degree = models.ManyToManyField(Degree)
    faculty = models.ManyToManyField(Faculty)
    language = models.ManyToManyField(Language)
    teachers = models.IntegerField()
    sessions = models.ManyToManyField(Sessions)
    registered = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Manager(models.Model):
    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    bio = models.TextField()
    phone_number = models.CharField(max_length=25)
    email = models.EmailField()

    def __str__(self):
        return self.full_name


class Student(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    img = models.ImageField(upload_to='StudentIMG')
    passport = models.FileField(upload_to='StudentPassport')
    certificate = models.FileField(upload_to='StudentCertificate')
    ielts = models.FloatField(default=0)
    gpa = models.FloatField(default=0)
    phone = models.CharField(max_length=25)
    email = models.EmailField()
    bio = models.TextField()
    banner = models.ImageField(upload_to='StudentBannerIMG', null=True, blank=True)
    university = models.ForeignKey(University, on_delete=models.CASCADE, null=True, blank=True)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    contract = models.FileField(upload_to='StudentContractFile', null=True, blank=True)
    date = models.DateField(auto_now=True)
    gender = models.IntegerField(choices=(
        (1, 'Man'),
        (2, 'Woman')
    ), default=1)

    def __str__(self):
        return self.first_name


class Testimonials(models.Model):
    Student = models.ForeignKey(Student, on_delete=models.CASCADE)
    comment = models.TextField()


class Registration(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    passport = models.FileField(upload_to='RegisPast')
    certificate = models.FileField(upload_to='RegisCertificate')
    lifetime = models.DateField()
    answer = models.CharField(max_length=255, null=True, blank=True)
    status = models.IntegerField(choices=(
        (1, 'received'),
        (2, 'cancelled'),
        (3, 'in_progres')
    ), default=3)
