# qdesc - Quick and Easy Descriptive Analysis

## Overview
This is a package for quick and easy descriptive analysis.
Required packages include: pandas, numpy, and SciPy version 1.14.1
Be sure to run the following prior to using the "qd.desc" function:

- import pandas as pd
- import numpy as np
- from scipy.stats import anderson
- import qdesc as qd

The qdesc package provides a quick and easy approach to do descriptive analysis for quantitative data.

## qd.desc Function
Run the function qd.desc(df) to get the following statistics:
* count - number of observations
* mean - measure of central tendency for normal distribution	
* std - measure of spread for normal distribution
* median - measure of central tendency for skewed distributions or those with outliers
* MAD - measure of spread for skewed distributions or those with outliers; this is manual Median Absolute Deviation (MAD) which is more robust when dealing with non-normal distributions.
* min - lowest observed value
* max - highest observed value	
* AD_stat	- Anderson - Darling Statistic
* 5% crit_value - critical value for a 5% Significance Level	
* 1% crit_value - critical value for a 1% Significance Level

## qd.freqdist Function
Run the function qd.freqdist(df, "Variable Name") to easily create a frequency distribution for your chosen categorical variable with the following:
* Variable Levels (i.e., for Sex Variable: Male and Female)
* Counts - the number of observations
* Percentage - percentage of observations from total.

## qd.freqdist_a Function
Run the function qd.freqdist_a(df, ascending = FALSE) to easily create frequency distribution tables, arranged in descending manner (default) or ascending (TRUE), for all 
the categorical variables in your data frame. The resulting table will include columns such as:
* Variable levels (i.e., for Satisfaction: Very Low, Low, Moderate, High, Very High) 
* Counts - the number of observations
* Percentage - percentage of observations from total.

## qd.freqdist_to_excel Function
Run the function qd.freqdist_to_excel(df, "Name of file.xlsx", ascending = FALSE ) to easily create frequency distribution tables, arranged in descending manner (default) or ascending (TRUE), for all  the categorical variables in your data frame and SAVED as separate sheets in the .xlsx File. The resulting table will include columns such as:
* Variable levels (i.e., for Satisfaction: Very Low, Low, Moderate, High, Very High) 
* Counts - the number of observations
* Percentage - percentage of observations from total.

## qd.normcheck_dashboard Function
Run the function qd.normcheck_dashboard(df) to efficiently check each numeric variable for normality of its distribution. It will compute the Anderson-Darling statistic and 
create visualizations (i.e., qq-plot, histogram, and boxplots) for checking whether the distribution is approximately normal.


## Installation
pip install qdesc

## Sample use of qdesc functions

## Creating a sample dataframe
import pandas as pd
import numpy as np

## Set seed for reproducibility
np.random.seed(21)

## Create two continuous variables
var1 = np.random.normal(loc=0, scale=1, size=1000)
var2 = np.random.uniform(low=10, high=50, size=1000)

## Create DataFrame
df = pd.DataFrame({
    'Normal_Variable': var1,
    'Uniform_Variable': var2
})

## Using the qdesc function
import qdesc as qd

qd.desc(df)

## License
This project is licensed under the GPL-3 License. See the LICENSE file for more details.

## Acknowledgements
Acknowledgement of the libraries used by this package...

### Pandas
Pandas is distributed under the BSD 3-Clause License, pandas is developed by Pandas contributors. Copyright (c) 2008-2024, the pandas development team All rights reserved.
### NumPy
NumPy is distributed under the BSD 3-Clause License, numpy is developed by NumPy contributors. Copyright (c) 2005-2024, NumPy Developers. All rights reserved.
### SciPy
SciPy is distributed under the BSD License, scipy is developed by SciPy contributors. Copyright (c) 2001-2024, SciPy Developers. All rights reserved.





