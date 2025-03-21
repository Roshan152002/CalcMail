from .models import Arithmatic

def handle_calculation(a,b,string,user):
    if string == 'add':
            r1 = a + b
    elif string == 'mul':
        r1 = a * b
    elif string == 'sub':
        r1 = a - b
    elif string == 'div': 
        r1 = a / b

    calculate = Arithmatic(a=a,b=b,operation_type=string,operation=r1,USER=user)
    calculate.save()
    return r1