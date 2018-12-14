import numpy as np
import matplotlib.pyplot as plt
round_list = lambda some_list,digits : [round(elem,digits) for elem in some_list]

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
    print(round_list(predictions,5))
    return predictions


def corrector(predictions,ys,h,xs,eqs,its,stopping_err):
    print("Corrections and maximum approximate error %")
    result = []
    tmp={}
    for i in range(len(predictions)):
        tmp['y'+str(i)] = predictions[i]
    ys.append(tmp)
    approx_errs = [100.]*len(predictions)
    it=0
    while((it<its or its==-1) and (max(approx_errs)>stopping_err or stopping_err==-1)):
        for i in range(len(eqs)):
            y_1 = ys[2]['y'+str(i)]
            ys[2]['x'] = xs[2]
            diff_y_1 = eval(eqs[i],globals(),ys[2])
            ys[3]['x'] = xs[3]
            diff_y_0 = eval(eqs[i],globals(),ys[3])
            ys[4]['x'] = xs[4]
            diff_y_plus1 = eval(eqs[i],globals(),ys[4])
            new_y =  y_1 +1./3*h*(diff_y_1+4*diff_y_0+diff_y_plus1)
            approx_errs[i]=(new_y-predictions[i])/new_y*100
            predictions[i] = new_y
            ys[4]['y'+str(i)] = predictions[i]
        it+=1
        print(round_list(predictions + [max(approx_errs)],5))

        result.append(predictions + [max(approx_errs)])
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
    print("Note That y0 is the name of variable 2 equations ex:\n 1-> dy0/dx = 3*x*y1 + 2*y0\n 2-> dy1/dx = x + y1 + y0\n")
    eqs = [input("eq{0}: dy{0}/dx = ".format(i)) for i in range(n)]
    print("\nIntial values for variables")
    h = float(input("step size h = "))
    xi = float(input("start form x = "))
    xf = float(input("till reach x = "))
    xs = [xi+i*h for i in range(5)]
    ys = []
    for j in range(4):
        tmp={}
        for i in range(n):
            try:
                tmp['y'+str(i)] = float(input("y{0} at x = {1} = ".format(i,round(xs[j],3))))
            except: pass
        ys.append(tmp.copy())
    test_equations(eqs,ys[0].copy()) # testing input of equations
    its = input("num of iterations for correction (if not defined press Enter) = ")
    its = int(its) if its != '' else -1
    stopping_err = input("Presantage of relative stopping error (if not defined press Enter) = ")
    stopping_err = float(stopping_err) if stopping_err != '' else -1
    if(its==-1 and stopping_err==-1):
        print("No stopping criteria defined Set iterations to default 10")
        its = 10
    return eqs,ys,xs,h,its,xf,stopping_err


def plot_points(points):
    legends = []
    for i in range(len(points[0])-1):
        plt.scatter(points[:,0],points[:,i+1])
        legends.append('y'+str(i))
    plt.legend(legends, loc='upper left')
    plt.show()

def main():
    #TODO replace read_input with argument variables or with gui
    eqs,ys,xs,h,its,xf,stopping_err = read_input() # i for initial and f for final and out for output_interval
    points=[]
    for i in range(4):
        points.append(round_list([xs[i]] + [ys[i]['y'+str(j)] for j in range(len(eqs))],5))
    while(xs[-1]<=xf):
        print("\nSolve at x = {0}".format(xs[-1]))
        predictions = predictor(ys,h,xs,eqs)
        result = corrector(predictions,ys,h,xs,eqs,its,stopping_err)
        points.append(round_list([xs[-1]] + result[-1][:-1],5))
        #shifting problem one step
        xs.append(xs[-1]+h)
        xs.pop(0)
        tmp={}
        for i in range(len(eqs)):
            tmp['y'+str(i)] = predictions[i]
        ys.append(tmp)
        ys.pop(0)
        print('')

    print("All pooints x ,y0 ,y1 ...")
    points=np.array(points)
    print(points)
    plot_points(points)

if __name__ == "__main__":
    main()

'''
Test Case 
2
y1-x*y0
1/3*(1+x**2-2*y0)
.1
0
.7
1
2
1.56
2.39
3.06
1.33
2.42
.86
5
output
3.31815318 1.05004104
'''