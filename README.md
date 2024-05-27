# Page View Time Series Visualizer

This is the boilerplate for the Page View Time Series Visualizer project. Instructions for building your project can be found at https://www.freecodecamp.org/learn/data-analysis-with-python/data-analysis-with-python-projects/page-view-time-series-visualizer

# Why I changed the requirements file
Due to changes in the Numpy library underneath Seaborn 0.9.0, this version of Seaborn is raises an error when it calls an internal function that casts an Numpy array to dtype=np.float, a deprecated data type in the numpy version installed with that version of Seaborn. Hence I changed the Seaborn version to 0.13.2
