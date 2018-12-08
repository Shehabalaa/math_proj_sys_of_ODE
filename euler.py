import parser
import numpy as np
from math import *
import tabulate
from sympy import integrate,Symbol

dict_to_list = lambda some_dict:[ some_dict[key] for key in sorted(some_dict.keys())]
round_list = lambda some_list,digits : [round(elem,digits) for elem in some_list]
euler = lambda x,y,ys,h,eq : y + eval(eq,ys)*h

def integrator(x,ys,h,xend,eqs,exact_integral_eqs):
    max_err_exact = 0.0
    while(1):
        if(xend -x <h):
            h = xend -x
        for i in range(len(eqs)):
            new_yi = euler(x,ys['y{0}'.format(i)],ys,h,eqs[i])
            variables = ys.copy();variables['x'] =x+h #use the current x not the previous one
            y_exact = eval(exact_integral_eqs[i],variables)
            err_exact = 100.*(y_exact - new_yi)/y_exact
            max_err_exact = err_exact if(abs(err_exact) > abs(max_err_exact)) else max_err_exact
            ys['y{0}'.format(i)] = new_yi
        x=x+h    
        if(x>= xend):
            return max_err_exact,x

def test_equations(eqs,variables):
    variables['x']=1
    try:
        for eq in eqs:
            eval(eq,variables)
    except:
        print("wrong equations or intial variables")
        exit()

def get_exact_integarl_formula(eq,intial_conditions,func):
    formula = str(integrate(eq,Symbol('x')))
    constant = intial_conditions[func] - eval(formula,intial_conditions)
    print(formula + ' + ' + str(constant))
    return formula + ' + ' + str(constant) # add constat

def read_input():
    n = int(input("Enter number of equations: "))
    print("Enter equations as python format ex: -2*x**3 + 12*x**2 -20*x + 8.5\n")
    eqs = [input("eq{0}: dy{0}/dx = ".format(i)) for i in range(n)]
    print("\nIntial values for variables")
    ys = {} # Intial values for variables
    for i in range(n):
        try:
            ys['y{0}'.format(i)] = float(input("y{0}_intial = ".format(i)))
        except: pass
    test_equations(eqs,ys.copy()) # testing input of equations
    xi = float(input("x_initial = "))
    xf = float(input("x_final = "))
    dx = float(input("calculation step size h = "))
    xout = input("show output every step (for default = h press Enter) = ")
    xout = float(xout) if xout != '' else dx
    intial_conditions=ys.copy();intial_conditions['x']=xi
    exact_integral_eqs = [get_exact_integarl_formula(eqs[i],intial_conditions,'y'+str(i)) for i in range(n)] #to calculate exact error
    return exact_integral_eqs,eqs,ys,xi,xf,dx,xout

def main():
    #TODO replace read_input with argument variables or with gui
    exact_integral_eqs,eqs,ysi,xi,xf,h,xout = read_input() # i for initial and f for final and out for output_interval
    err_exact = nan
    result_table = [xi] + dict_to_list(ysi) + [err_exact]
    while(1):
        xend = xi + xout
        if(xend > xf):
            xend = xf
        err_exact,xi = integrator(xi,ysi,h,xend,eqs,exact_integral_eqs) # ysi dictionary is passed by ref
        new_row = round_list( [xi] + dict_to_list(ysi) + [err_exact],3)
        print(new_row)
        result_table.append(new_row)
        if(xi>=xf):
            break
        

if __name__ == "__main__":
    main()