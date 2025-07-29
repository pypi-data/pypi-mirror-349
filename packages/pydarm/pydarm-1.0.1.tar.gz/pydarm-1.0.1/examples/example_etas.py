import pydarm
import numpy as np

config = '../example_model_files/H1_20190416.ini'

darm = pydarm.darm.DARMModel(config)

# Create a frequency vector to evalute the response function
frequencies = np.logspace(np.log10(20), np.log10(2000), 10)

# Input systematic error user defined
syserr_input = [1.0000003831992847-0.0007929858798234665j,
                0.9999986255804106-0.002042969515282433j,
                0.9999869597043107-0.0052632862823899385j,
                0.9999095302557972-0.013559488366496989j,
                0.9993956411093269-0.03492779907418393j,
                0.995986356934377-0.08988999137528689j,
                0.9734269429695694-0.22996802633705743j,
                0.8267642616923517-0.5649608162253222j,
                -0.004181642663901519-1.003311656263212j,
                -0.19691508479464048+0.7796521952236531j]

# Compute impact of response function with sensing and actuation systematic error
eta_R_c, eta_R_a, eta_R = darm.compute_etas(frequencies, sensing_syserr=syserr_input)
