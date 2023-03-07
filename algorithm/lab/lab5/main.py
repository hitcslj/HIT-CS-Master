from utils import createData,plot_performance_curve
from quickSort import quickSort

if __name__=='__main__':
    datasets = createData(n=11)
    plot_performance_curve(quickSort,datasets)


