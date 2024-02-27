from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Information, Banner, About, Faculty, AboutMe, ContactUs, Region, University, Student, Testimonials, Registration

from .serializer import InformationSerializer, BannerSerializer, AboutSerializer, FacultySerializer, AboutMeSerializer, ContactUsSerializer, \
    LanguageSerializer, UniversitySerializer, StudentSerializer, TestimonialsSerializer, RegistrationSerializer, MangerSerializer


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def information_view(request):
    information = Information.objects.last()
    ser_data = InformationSerializer(information).data
    return Response(ser_data, status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_banner(request):
    banner = Banner.objects.last()
    ser_data = BannerSerializer(banner).data
    return Response(ser_data, status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def filter_university(request):
    university = University.objects.all()
    if request.GET.get('region'):
        university = University.objects.filter(region__name=request.GET.get('region'))
        ser_data = UniversitySerializer(university, many=True).data
    if request.GET.get('degree'):
        university = university.filter(degree__name=request.GET.get('degree'))
        ser_data = UniversitySerializer(university, many=True).data
    if request.GET.get('faculty'):
        university = university.filter(faculty__name=request.GET.get('faculty'))
        ser_data = UniversitySerializer(university, many=True).data
    return Response(ser_data, status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_about(request):
    about = About.objects.all().order_by('-id')[:4]
    ser_data = AboutSerializer(about, many=True).data
    return Response(ser_data, status.HTTP_200_OK)


@api_view(['GEt'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def popular_university(request):
    university = University.objects.all().order_by('rating')[:6]
    ser_data = UniversitySerializer(university, many=True).data
    return Response(ser_data, status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def popular_faculty(request):
    faculty = Faculty.objects.all().order_by('-registered')[:9]
    ser_data = FacultySerializer(faculty, many=True).data
    return Response(ser_data, status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_about_me(request):
    about_me = AboutMe.objects.all().order_by('-id')[:6]
    ser_data = AboutMeSerializer(about_me, many=True).data
    return Response(ser_data, status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_testimonials(request):
    testimonials = Testimonials.objects.all().order_by('-id')[:12]
    ser_data = TestimonialsSerializer(testimonials, many=True).data
    return Response(ser_data, status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_contact(request):
    try:
        phone_number = request.POST.get('phone_number')
        contact_us = ContactUs.objects.create(phone_number=phone_number)
        contact_us.save()
        data = {
            'success': True,
            'message': ContactUsSerializer(contact_us).data
        }
        status_code = status.HTTP_201_CREATED
    except Exception as e:
        data = {
            'success': False,
            'message': f'{e}'
        }
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return Response(data, status_code)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def university_details(request, pk):
    university = University.objects.get(id=pk)
    ser_data = UniversitySerializer(university).data
    return Response(ser_data, status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def student_cabinet(request, pk):
    student = Student.objects.get(id=pk)
    ser_data = StudentSerializer(student).data
    return Response(ser_data, status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def student_university(request, pk):
    university = Registration.objects.filter(student_id=pk).order_by('-id')
    ser_data = RegistrationSerializer(university, many=True).data
    return Response(ser_data, status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def student_university_single(request, pk):
    university = Registration.objects.get(student_id=pk)
    ser_data = RegistrationSerializer(university).data
    return Response(ser_data, status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def personal_manager(request, pk):
    student = Student.objects.get(id=pk)
    manager = student.manager
    ser_data = MangerSerializer(manager).data
    return Response(ser_data, status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def university_admin_panel(request, pk):
    university = University.objects.get(id=pk)
    total_students = Student.objects.filter(university_id=pk).count()
    register = Registration.objects.filter(university_id=pk).count()
    registers = Registration.objects.filter(university_id=pk)
    received = registers.filter(status=1).count()
    cancelled = registers.filter(status=2).count()
    students = Student.objects.filter(university_id=pk)
    male = students.filter(gender=1).count()
    female = students.filter(gender=2).count()
    faculty = university.faculty.all().order_by('-registered')[:4]
    language = university.language.all().order_by('-registered')[:3]
    data = {
        'university': UniversitySerializer(university).data,
        'total_students': total_students,
        'register': register,
        'received': received,
        'cancelled': cancelled,
        'gender': {
            'male': male,
            'female': female,
        },
        'faculty': FacultySerializer(faculty, many=True).data,
        'language': LanguageSerializer(language, many=True).data,
    }
    return Response(data, status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def university_students(request, pk):
    students = Student.objects.filter(university_id=pk)
    ser_data = StudentSerializer(students, many=True).data
    if request.GET.get('first_name'):
        searched_student = students.filter(first_name=request.GET.get('first_name'))
        ser_data = StudentSerializer(searched_student, many=True).data
    if request.GET.get('start_date') and request.GET.get('end_date'):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        filtered_objects = students.filter(date__gte=start_date, date__lte=end_date)
        ser_data = StudentSerializer(filtered_objects, many=True).data
    return Response(ser_data, status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def university_registered_students(request, pk):
    registered = Registration.objects.filter(university_id=pk, status=3)
    ser_data = RegistrationSerializer(registered, many=True).data
    if request.GET.get('first_name'):
        searched_registered = registered.filter(student__first_name=request.GET.get('first_name'))
        ser_data = RegistrationSerializer(searched_registered, many=True).data
    if request.GET.get('start_date') and request.GET.get('end_date'):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        filtered_objects = registered.filter(student__date__gte=start_date, student__date__lte=end_date)
        ser_data = RegistrationSerializer(filtered_objects, many=True).data
    return Response(ser_data, status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def university_registered_student_single(request, pk):
    registered = Registration.objects.get(student_id=pk)
    ser_data = RegistrationSerializer(registered).data
    return Response(ser_data, status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def university_registered_student_answer(request, pk):
    registered = Registration.objects.get(student_id=pk)
    registered.status = request.GET.get('status')
    registered.save()
    if registered.status == '1':
        student = Student.objects.get(id=pk)
        student.university = registered.university
        student.save()
        data = {
            'success': True,
            'message': 'You have been successfully received'
        }
    elif registered.status == '2':
        data = {
            'success': False,
            'message': 'You have been cancelled'
        }
    return Response(data, status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def university_cabinet(request, pk):
    university = University.objects.get(id=pk)
    ser_data = UniversitySerializer(university).data
    return Response(ser_data)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def dashboard(request):
    students = Student.objects.all().count()
    university = University.objects.all().count()
    region = Region.objects.all().count()
    faculty = Faculty.objects.all().count()
    male = Student.objects.filter(gender=1).count()
    female = Student.objects.filter(gender=2).count()
    context = {
        'students': students,
        'university': university,
        'region': region,
        'faculty': faculty,
        'male': male,
        'female': female
    }
    return Response(context)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def dashboard_university(request):
    university = University.objects.all().order_by('-id')
    ser_data = UniversitySerializer(university, many=True).data
    if request.GET.get('region'):
        university = University.objects.filter(region__name=request.GET.get('region'))
        ser_data = UniversitySerializer(university, many=True).data
    if request.GET.get('city'):
        university = university.filter(city=request.GET.get('city'))
        ser_data = UniversitySerializer(university, many=True).data
    if request.GET.get('start_date') and request.GET.get('end_date'):
        university = university.filter(date__gte=request.GET.get('start_date'), date__lte=request.GET.get('end_date'))
        ser_data = UniversitySerializer(university, many=True).data
    return Response(ser_data)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def dashboard_university_single(request, pk):
    university = University.objects.get(id=pk)
    ser_data = UniversitySerializer(university).data
    return Response(ser_data)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def dashboard_student(request):
    student = Student.objects.all().order_by('-id')
    ser_data = StudentSerializer(student, many=True).data
    if request.GET.get('first_name'):
        searched_student = Student.objects.filter(first_name=request.GET.get('first_name'))
        ser_data = StudentSerializer(searched_student, many=True).data
    if request.GET.get('start_date') and request.GET.get('end_date'):
        filter_student = Student.objects.filter(date__gte=request.GET.get('start_date'), date__lte=request.GET.get('end_date'))
        ser_data = StudentSerializer(filter_student, many=True).data
    return Response(ser_data)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def dashboard_student_single(request, pk):
    student = Student.objects.get(student_id=pk)
    ser_data = StudentSerializer(student).data
    return Response(ser_data)

