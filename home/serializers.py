from rest_framework import serializers
from .models import Task, Person, Department, Employee, Skills, Foods
from decimal import Decimal
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        exclude = ['created_at', 'updated_at']

    def validate_email(self, value):
            if Person.objects.filter(email=value).exists():
                raise serializers.ValidationError("Email already exists.")
            return value

    def validate_phone_number(self, value):
            if Person.objects.filter(phone_number=value).exists():
                raise serializers.ValidationError("Phone number already exists.")
            return value

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['name']

class EmployeeSerializer(serializers.ModelSerializer):
    before_tax_salary = serializers.SerializerMethodField()
    department_serializer = DepartmentSerializer(read_only=True)
    
    class Meta:
        model = Employee
        fields = '__all__'

    def get_before_tax_salary(self, employee):
         # Assuming the tax rate is 20%
        tax_rate = Decimal('0.20')
        before_tax_salary = employee.salary / (Decimal('1') - tax_rate)
        return round(before_tax_salary, 2)

class CreateEmployeeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    joining_date = serializers.DateField(required=False, allow_null=True)

    class Meta:
        model = Employee
        fields = '__all__'

    def validate(self, data):
        return data

    def create(self, validated_data):
        print("Creating employee with data:", validated_data)
        return validated_data

# *********** Get Representation Method *********
class PersonSerializerWithRepresentation(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance) # Call the parent class's to_representation method
        data['age_in_months'] = instance.age * 12  # Add a new field for age in months
        return data

    def to_internal_value(self, data):
        # Custom logic to handle incoming data before validation
        if 'age_in_months' in data:
            data['age'] = data['age_in_months'] // 12  # Convert age in months to years
        return super().to_internal_value(data)


# ********* Authentication **************
class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField(required=False, allow_blank=True)

    def username_exists(self, username):
        return User.objects.filter(username=username).exists()

    def password_is_valid(self, password):
        return len(password) >= 8

    def create(self, validated_data):
        # Custom logic for creating a user can be added here
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name', '')

        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        user.set_password(password)  # Hash the password
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        if not User.objects.filter(username=validated_data['username']).exists():
            raise serializers.ValidationError("User does not exist.")
        return validated_data

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foods
        fields = '__all__'

    