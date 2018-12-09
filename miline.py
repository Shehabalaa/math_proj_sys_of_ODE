def predictor(ys,h,xs,eqs):
    predictions = []
    for i in range(len(eqs)):
        y_3 = ys[0]['y'+str(i)]
        ys[1]['x'] = xs[1]
        diff_y_2 = eval(eqs[i],ys[1].copy())
        ys[2]['x'] = xs[2]
        diff_y_1 = eval(eqs[i],ys[2].copy())
        ys[3]['x'] = xs[3]
        diff_y_0 = eval(eqs[i],ys[3].copy())
        predictions.append(y_3 + 4./3*h*(2*diff_y_0 - diff_y_1 + 2*diff_y_2))
    return predictions


def corrector(predictions,ys,h,xs,eqs,its):
    result = []
    tmp={}
    for i in range(len(predictions)):
        tmp['y'+str(i)] = predictions[i]
    ys.append(tmp)
    for it in range(its):
        for i in range(len(eqs)):
            y_1 = ys[2]['y'+str(i)]
            ys[2]['x'] = xs[2]
            diff_y_1 = eval(eqs[i],ys[2].copy())
            ys[3]['x'] = xs[3]
            diff_y_0 = eval(eqs[i],ys[3].copy())
            ys[4]['x'] = xs[4]
            diff_y_plus1 = eval(eqs[i],ys[4].copy())
            predictions[i] = y_1 +1./3*h*(diff_y_1+4*diff_y_0+diff_y_plus1)
            ys[4]['y'+str(i)] = predictions[i]
            print(predictions)
        result.append(predictions)
    return result
                

def test_equations(eqs,variables):
    variables['x']=1
    try:
        for eq in eqs:
            eval(eq,variables)
    except:
        print("wrong equations or intial variables")
        exit()


def read_input():
    n = int(input("Enter number of equations: "))
    print("Enter equations as python format ex: -2*x**3 + 12*x**2 -20*x + 8.5\n")
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
        