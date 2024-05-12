from django.shortcuts import render, HttpResponse
from .models import Employee, Role, Department
from datetime import datetime
from django.db.models import Q

# Create your views here.
def index(request):
    return render(request, 'index.html')

def all_emp(request):
    emps = Employee.objects.all()
    context = {
        'emps' : emps
    }
    print(context) 
    return render(request, 'view_all_emp.html', context)

def add_emp(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        salary = int(request.POST['salary'])
        bonus = int(request.POST['bonus'])
        phone = int(request.POST['phone'])
        dept_name = request.POST['dept']
        role_name = request.POST['role']


        try:
            # Fetch Department instance using the department name
            dept_instance = Department.objects.get(name=dept_name)
        except Department.DoesNotExist:
            return HttpResponse("Department does not exist")
        
        try:
            # Fetch Role instance using the role name
            role_instance = Role.objects.get(name=role_name)
        except Role.DoesNotExist:
            return HttpResponse("Role does not exist")
        
        # Similarly, you may need to fetch the Role instance if needed
        
        new_emp = Employee(first_name=first_name, last_name=last_name, salary=salary, bonus=bonus, phone=phone, dept=dept_instance, role=role_instance, hire_date=datetime.now())
        new_emp.save()
        return HttpResponse('Employee added Successfully')
    elif request.method == 'GET':
        return render(request, 'add_emp.html')
    else:
        return HttpResponse("An Exception Occurred! Employee Has Not Been Added")
    




def remove_emp(request, emp_id = 0):
    if emp_id:
        try:
            emp_to_be_removed = Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return HttpResponse("Employee Removed Seccessfully")
        except:
            return HttpResponse("Please Enter A Valid EMP ID")
    emps = Employee.objects.all()
    context = {
        'emps' : emps
    }
    return render(request, 'remove_emp.html', context)

def filter_emp(request):
    if request.method == 'POST':
        name = request.POST['name']
        dept = request.POST['dept']
        role = request.POST['role']
        emps = Employee.objects.all()
        if name:
            emps = emps.filter(Q(first_name__icontains = name) | Q(last_name__icontains = name))
        if dept:
            emps = emps.filter(dept__name__icontains = dept)
        if role:
            emps = emps.filter(role__name__icontains = role)

        context = {
            'emps' : emps
        }
        return render(request, 'view_all_emp.html', context)
    
    elif request.method == 'GET' :
        return render(request, 'filter_emp.html')
    else:
        return HttpResponse('An Exception Occured') 