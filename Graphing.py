import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import seaborn as sns
from time import localtime, strftime
from FirebaseDW import FirebaseApplication as fb


class Graphing(object):
    # to change token and secret when data is ready
    def __init__(self, url = None, token = None):
        # Testing data
        # self.temp_data = np.random.uniform(18,40,[4,4])
        # self.hum_data = np.random.uniform(0,1,[4,4])
        # fb.get('./heatmap')
        #self.temp_data = np.array([[11,12,13,14],
        #                          [21,22,23,24],
        #                          [31,32,33,34],
        #                          [41,42,43,44]])
        #self.hum_data = np.array([[11,12,13,14],
        #                          [21,22,23,24],
        #                          [31,32,33,34],
        #                          [41,42,43,44]])

        # get data from firebase
        f = fb(url,token)
        hum = f.get('/heatmap/hum')
        self.hum_data = np.array(hum)
        self.url = url

        temp = f.get('/heatmap/temp')
        self.temp_data = np.array(temp)

    def gen_temp_graph(self):
        """
        generate temperature graph
        """
        fig, ax = plt.subplots()

        data = self.temp_data

        # add axis to cbar to tweak numbers
        cbar_ax = fig.add_axes([0.92,0.3,0.02,0.4])

        # Color map
        colors = ["#EF4E00"]

        my_cmap = mpl.colors.ListedColormap(sns.light_palette("green",9)+sns.color_palette(colors).as_hex())

        # Seaborn heat map
        sns.heatmap(data,
                    robust = True,
                    ax = ax,
                    cmap = my_cmap,
                    cbar_ax = cbar_ax,
                    annot = True,
                    vmin = 18.0,
                    vmax = 32.0)

        changed_val1 = ">" + cbar_ax.get_yticklabels()[-1].get_text()

        labels = [x.get_text() for x in cbar_ax.get_yticklabels()[:-1]]+[changed_val1]

        cbar_ax.set_yticklabels(labels)

        # Add Title and give it a time stamp
        timenow = strftime("%Y-%m-%d %H:%M:%S", localtime())
        ax.set_title('Temperature, {}\nOrange tile indicates that the area requires watering'.format(timenow))
        ax.set(xlabel='url: {}'.format(self.url))
        #plt.show()
        plt.savefig("temp.png")

    def gen_hum_graph(self):
        """
        generate humidity graph
        """

        fig, ax = plt.subplots()

        data = self.hum_data

        # add axis to cbar to tweak numbers
        cbar_ax = fig.add_axes([0.92,0.3,0.02,0.4])

        # Color map
        colors = ["#EF4E00"]

        my_cmap = mpl.colors.ListedColormap(sns.color_palette(colors).as_hex() + sns.light_palette("blue",9))

        # Seaborn heat map
        sns.heatmap(data,
                    robust = True,
                    ax = ax,
                    cmap = my_cmap,
                    cbar_ax = cbar_ax,
                    annot = True,
                    vmin = 0.4,
                    vmax = 1.0)

        changed_val1 = "<" + cbar_ax.get_yticklabels()[0].get_text()

        labels = [changed_val1]+[x.get_text() for x in cbar_ax.get_yticklabels()[1:]]

        cbar_ax.set_yticklabels(labels)

        # Add Title and give it a time stamp
        timenow = strftime("%Y-%m-%d %H:%M:%S", localtime())
        ax.set_title('Humidity, {}\nOrange tile indicates that the area requires watering'.format(timenow))
        ax.set(xlabel='url: {}'.format(self.url))
        #plt.show()
        plt.savefig("humidity.png")

if __name__ == "__main__":
    url = 'https://my-awesome-project-3e36c.firebaseio.com'
    token = 'AxddRZLLd4QR55sNCMXt832N0v759EvheBnWBshR'
    g = Graphing(url, token)
    g.gen_temp_graph()
    g.gen_hum_graph()
