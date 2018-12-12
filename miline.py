def predictor(ys,h,xs,eqs):
    predictions = []
    for i in range(len(eqs)):
        y_3 = ys[0]['y'+str(i)]
        ys[1]['x'] = xs[1]
        diff_y_2 = eval(eqs[i],globals(),ys[1])
        ys[2]['x'] = xs[2]
        diff_y_1 = eval(eqs[i],globals(),ys[2])
        ys[3]['x'] = xs[3]
        diff_y_0 = eval(eqs[i],globals(),ys[3])
        predictions.append(y_3 + 4/3*h*(2*diff_y_0 - diff_y_1 + 2*diff_y_2))
    print("Predictions")
    print(predictions)
    return predictions


def corrector(predictions,ys,h,xs,eqs,its):
    print("\nCorrections")
    result = []
    tmp={}
    for i in range(len(predictions)):
        tmp['y'+str(i)] = predictions[i]
    ys.append(tmp)
    for it in range(its):
        for i in range(len(eqs)):
            y_1 = ys[2]['y'+str(i)]
            ys[2]['x'] = xs[2]
            diff_y_1 = eval(eqs[i],globals(),ys[2])
            ys[3]['x'] = xs[3]
            diff_y_0 = eval(eqs[i],globals(),ys[3])
            ys[4]['x'] = xs[4]
            diff_y_plus1 = eval(eqs[i],globals(),ys[4])
            predictions[i] = y_1 +1./3*h*(diff_y_1+4*diff_y_0+diff_y_plus1)
            ys[4]['y'+str(i)] = predictions[i]
        print(predictions)
        result.append(predictions)
    return result
                

def test_equations(eqs,variables):
    variables['x']=1
    try:
        for eq in eqs:
            eval(eq,globals(),variables)
    except:
        print("wrong equations or intial variables")
        exit()


def read_input():
    n = int(input("Enter number of equations: "))
    print("Enter equations as python format ex: -2*x**3 + exp(x)-20*x + 8.5")
    print("Note That y0 is the name of variable 2 equations ex:\n 1-> dy0/dx = 3*x*y1 + 2y0\n 2-> dy1/dx = x + y1 + y0\n")
    eqs = [input("eq{0}: dy{0}/dx = ".format(i)) for i in range(n)]
    print("\nIntial values for variables")
    h = float(input("step size h = "))
    xf = float(input("x to solve at = "))
    xs = [xf-(4-i)*h for i in range(5)]
    ys = []
    for j in range(4):
        tmp={}
        for i in range(n):
            try:
                tmp['y'+str(i)] = float(input("y{0} at x = {1} = ".format(i,round(xs[j],3))))
            except: pass
        ys.append(tmp.copy())
    test_equations(eqs,ys[0].copy()) # testing input of equations
    its = int(input("num of iterations for correction = "))
    return eqs,ys,xs,h,its

def main():
    #TODO replace read_input with argument variables or with gui
    eqs,ys,xs,h,its = read_input() # i for initial and f for final and out for output_interval
    predictions = predictor(ys,h,xs,eqs)
    result = corrector(predictions,ys,h,xs,eqs,its)


if __name__ == "__main__":
    main()

'''
Test Case 
2
y1-x*y0
1/3*(1+x**2-2*y0)
.1
.4
1
2
1.56
2.39
3.06
1.33
2.42
.86
10
output
3.31815318 1.05004104
'''