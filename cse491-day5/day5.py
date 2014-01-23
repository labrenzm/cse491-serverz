def add_2_numbers(x, y):
    return x+y

def divide_2_numbers(x, y):
    f = x /float(y)
    return f

def get_3rd_value(x):
    s = x.split(',')
    value = s[2]
    return value

def get_4th_comma_plus(x):
    count = 0
    s = ""
    for i in x:
        if count >= 4:
            s+=str(i)
            
        if i == ',':
            count = count + 1
    return s

def get_lines_4_5(x):
    count = 0
    s = ""
    for i in x:
         if i == "\n":
            count = count + 1
         if (count == 3) or (count == 4):
            s+=str(i)
    return s

def get_cleaned_values_3_4(x):
    return ""
