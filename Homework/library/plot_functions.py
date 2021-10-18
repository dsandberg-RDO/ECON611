from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
import numpy as np
import pandas_datareader.data as web
import datetime
import matplotlib.pyplot as plt
import os

import matplotlib.ticker as mticker

# Hoepefullly resolving the "UserWarning: FixedFormatter should only be used together with FixedLocator" 
# Resolving source: https://programmersought.com/article/96489082118/

# label_format = '{:,.1f}'  # Create a floating point format. 1F a decimal
# xlabels = ax_main.get_xticks().tolist()
# ax_main.xaxis.set_major_locator(mticker.FixedLocator(xlabels))  # Position the x-axis of the scatter plot
# ax_main.set_xticklabels([label_format.format(x) for x in xlabels])  # Use the list deduced loop to convert the scale into floating point
# plt.show()

def gather_data(data_codes, start, end = datetime.datetime.today(), freq = "M"):
    isDF = 0
    for key, val in data_codes.items():
        if isDF == 0:
            df = web.DataReader(val, "fred", start, end).resample(freq).mean()
            df.rename(columns = {val:key}, inplace = True) 
            isDF = 1
        else:
            # If dataframe already exists, add new column
            df[key] = web.DataReader(val, "fred", start, end).resample(freq).mean()
    return df

def bil_to_mil(series):
    return series * 10 ** 3

def plot_lines(df,
              title = "",
              lw = 1,   #linewidth
              figsize = (40,30),
              secondary_y = None,
              legend = True,
              pp = None,   # pdf pages
              #save_fig = False,
              legend_columns = 2):
    fig, ax = plt.subplots(figsize = figsize)
    df.dropna(axis=0, how="all").plot.line(
            linewidth = lw,
            secondary_y = secondary_y,
            legend = legend,
            ax = ax)
    
    ax.set_title(title)
    ax.legend(ncol = legend_columns)
    
    # remove ticklines
    ax.tick_params("both", length=0, which="both")
    
    # format axis labels
    ax.tick_params(axis="x", rotation = 90)
    label_format = '{:,.1f}'  # Create a floating point format. 1F a decimal
       
    # renaming y-axis labels
    vals = ax.get_yticks()
    #ax.set_yticklabels([round(x,2) for x in vals])
    ax.set_yticklabels([label_format.format(x) for x in vals]) 
    
    #Format file name
    characters = "[]:$'\\"
    filename = str(list(df.keys()))
    for char in characters:
        filename = filename.replace(char,"")

    if pp != None:
        try:
            os.mkdir("plots")
            pp.savefig(fig)
        except:
            pass
        pp.savefig(fig)
            
        
#     if save_fig:
#         try:
#             os.mkdir("plots")
#         except:
#             pass
#         # bbox_inches = "tight" rfers to formatting...

#         plt.figure.savefig("plots/" + filename[:50] + "lines.png",
#                    bbox_inches = "tight")
        
#         if pp!= None: pp.figure.savefig(fig, bbox_inches = "tight")    

def plot_stacked_lines(df, 
                       plot_vars, 
                       lw = 2, 
                       figsize = (40,20), 
                       pdf = None, 
                       total_var = False,
                       legend_columns = 2):
    fig, ax = plt.subplots(figsize = figsize)
    df[plot_vars].plot.area(stacked = True, 
                            linewidth = lw,
                            ax = ax)
    # change y vals from mil to tril
    
    if total_var != False:
        df[total_var].plot.line(
            linewidth = lw, 
            ax = ax, 
            c = "k",
            label = total_var, 
            ls = "--")
        
    ax.legend(loc=2, ncol = legend_columns)
    

def plot_ts_scatter(data
                    , point_size = 75
                    , figsize = (40, 20)
                    , save_fig = False
                    , pp = None):
    df = data.copy()
    for var1 in df:
        for var2 in df:
            if var1 != var2:
                fig, ax = plt.subplots(figsize = figsize)
                
                # if 'Year' is not present in keys, create list of years from index (date)
                if "Year" not in df.keys():
                    df["Year"] = [int(str(ind)[:4]) for ind in df.index] 
                
                df.plot.scatter(x = var1
                                , y = var2
                                , s = point_size
                                , ax = ax
                                , c = "Year"
                                , cmap = "viridis")
                
                # Axis formatting
                ax.tick_params(axis='x', rotation=90)
                ax.tick_params('both', length=0, which='both')

                # PDF 
                if save_fig:
                    try:
                        os.mkdir("plots")
                    except:
                        pass
                    plt.savefig("plots/" + str(list(df.keys())).replace("[", "").replace("]","")[:40] + " scatter.png",
                            bbox_inches = "tight")
                    if pp != None:
                        pp.savefig(fig, bbox_inches = "tight")
                        

def corr_matrix_heatmap(data, pp):  
    #Create a figure to visualize a corr matrix  
    fig, ax = plt.subplots(figsize=(20,20))  
    # use ax.imshow() to create a heatmap of correlation values  
    # seismic mapping shows negative values as blue and positive values as red  
    im = ax.imshow(data, norm = plt.cm.colors.Normalize(-1,1), cmap = "seismic")  
    # create a list of labels, stacking each word in a label by replacing " "  
    # with "\n"  
    labels = data.keys()  
    num_vars = len(labels)  
    tick_labels = [lab.replace(" ", "\n") for lab in labels]  
    # adjust font size according to the number of variables visualized  
    tick_font_size = 120 / num_vars  
    val_font_size = 200 / num_vars  
    plt.rcParams.update({'font.size': tick_font_size}) 
    # prepare space for label of each column  
    x_ticks = np.arange(num_vars)  
    # select labels and rotate them 90 degrees so that they are vertical  
    plt.xticks(x_ticks, tick_labels, fontsize = tick_font_size, rotation = 90)  
    # prepare space for label of each row  
    y_ticks = np.arange(len(labels))  
    # select labels  
    plt.yticks(y_ticks, tick_labels, fontsize = tick_font_size)  
    # show values in each tile of the heatmap  
    for i in range(len(labels)):  
        for j in range(len(labels)):  
            text = ax.text(i, j, str(round(data.values[i][j],2)),  
                           fontsize= val_font_size, ha="center",   
                           va="center", color = "w")  
    #Create title with Times New Roman Font  
    title_font = {"fontname":"Times New Roman"}  
    plt.title("Correlation", fontsize = 50, **title_font)  
    # Call scale to show value of colors 
    cbar = fig.colorbar(im)
    plt.show()
    # pp.figure.savefig(fig, bbox_inches="tight")
    plt.close()

