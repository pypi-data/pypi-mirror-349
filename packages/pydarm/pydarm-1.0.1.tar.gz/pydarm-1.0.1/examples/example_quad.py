import pydarm
import numpy as np

# --------------------------------------------------------------------
# Example with two darm models (there are other ways to make 2 models)

# Don't forget to change the configuration file so that the parameter cal_data_root
# points to the directory where you have all the data files.
config = '../example_model_files/myH1_20190416.ini'

# The two models are identical except for the coupled cavity pole frequency.
D1 = pydarm.darm.DARMModel(config)
D2 = pydarm.darm.DARMModel(config)
D2.sensing.coupled_cavity_pole_frequency = 150

freq = np.logspace(1, 4, 100)

# Pretend that you have a 10% uncertainty in one of the models for demonstration.
unc_D1 = np.abs(D1.compute_darm_olg(freq))*0.1

# Declare your quad plot.
qplot = pydarm.plot.QuadPlot(title='The title of this quad plot')
# Plot the models on the quad plot.
# First two arguments are tuples that should include freq,tf or freq,tf,unc.
qplot.plot((freq, D1.compute_darm_olg(freq), unc_D1), (freq, D2.compute_darm_olg(freq)))
# If you want to add more data/lines in your quad plot, simply call plot again.
qplot.plot((freq, D2.compute_darm_olg(freq)), (freq, D1.compute_darm_olg(freq)))
# Now you are done plotting data, you may start messing with how it looks.
qplot.legend(label=['Test1', 'Test2'])
# By default everything you change will be applied to all 4 plots.
# If you don't want that, you may use quadrant=[] to specify which of the four
# quadrants you want to affect. bl=bottom left, tr=top right, etc. You may also
# use numbers: tl=1, tr=2, bl=3, br=4.
qplot.legend(label=['Test10', 'Test20'], quadrant=['bl'])
qplot.xlim(20, 3000)
qplot.ylim(1e-10, 1e10, quadrant=['tl'])
qplot.ylim(-60, 60, quadrant=['bl'])
qplot.vlines(300)
qplot.vlines(400, quadrant=[3, 2])
qplot.text(200, 2, 'testing')
qplot.show()
qplot.save('qplot_test.pdf')
