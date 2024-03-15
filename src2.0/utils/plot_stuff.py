# Importing necessary library for plotting. 
import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.ticker import PercentFormatter
import io 
from PIL import Image 

# Create a Function for Converting a figure to a PIL Image. 
def plt2img(plt): 
    # Getting the current figure and save it in the variable. 
    fig = plt.gcf() 

    buf = io.BytesIO() 
    fig.savefig(buf) 
    buf.seek(0) 
    img = Image.open(buf)
 
    # clear current fig
    plt.clf()

    return img 

def plot_func(profit, start, stop, file, title="Profit by Price", xlabel='price of stock at expiration', ylabel="profit of option strategy at expiration"):
    x = range(start, stop+1) 
    y = [profit(p) for p in x]

    # Plotting Line Graph 
    plt.title(title) 
    plt.xlabel(xlabel) 
    plt.ylabel(ylabel) 
    plt.plot(x, y) 
    plt.grid(True)

    # Save return image in a variable by passing 
    # plot in the created function for Converting a plot to a PIL Image. 
    img = plt2img(plt) 

    # Save image with the help of save() Function. 
    img.save(file) 

def plot_hist(dist, file, bins=None):
    plt.hist(dist, weights=np.ones(len(dist)) / len(dist), bins=bins)
    plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
    plt.title("Stock Price at Expiration pdf")
    plt.grid(True)

    average = sum(dist) / len(dist)
    plt.axvline(x=average, label="mean", ls='--', c='black')
    plt.text(average-1,0,f'    mean ({average:.1f})',rotation=90)

    img = plt2img(plt)

    img.save(file) 
    
if __name__ == "__main__":
    plot_profit(lambda x: (x < -5 and x - 1) or (x < 5 and -6) or (-11 + x), -15, 25, '/var/www/html/jn/plot.png')
    plot_hist(np.random.normal(170, 1000, 100000), '/var/www/html/jn/hist.png', 100)
