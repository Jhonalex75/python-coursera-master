# -----------------------------------------------------------------------------
# Purpose: Fit a 2-parameter Weibull distribution to failure data and display results.
# Application: Reliability engineering, failure analysis.
# Dependencies: reliability, matplotlib
# Usage: Run the script to fit the Weibull model and show the plot.
# -----------------------------------------------------------------------------

from reliability.Fitters import Fit_Weibull_2P
import matplotlib.pyplot as plt
data = [58,75,36,52,63,65,22,17,28,64,23,40,73,45,52,36,52,60,13,55,82,55,34,57,23,42,66,35,34,25] # made using Weibull Distribution(alpha=50,beta=3)
wb = Fit_Weibull_2P(failures=data)
plt.show()

'''
Results from Fit_Weibull_2P (95% CI):
Analysis method: Maximum Likelihood Estimation (MLE)
Optimizer: TNC
Failures / Right censored: 30/0 (0% right censored)

Parameter  Point Estimate  Standard Error  Lower CI  Upper CI
    Alpha          51.858         3.55628   45.3359   59.3183
     Beta         2.80086         0.41411   2.09624   3.74233

Goodness of fit    Value
 Log-likelihood -129.063
           AICc   262.57
            BIC  264.928
             AD 0.759805
'''