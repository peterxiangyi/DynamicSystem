import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#----------------------------------------------------------------------------#
# Page layout
## Page expands to full width
st.set_page_config(layout="wide")
#st.set_page_config(layout="centered")
#----------------------------------------------------------------------------#

# Title

st.title('Logistic Equation App')

st.markdown("""
This app simulate the iteration result of logistic equation for given growth rate, initial value and iteration steps.
""")

image = Image.open('logo.gif')
st.image(image, width=750)

#----------------------------------------------------------------------------#
# About
expander_bar = st.beta_expander("About")
expander_bar.markdown("""
* **Python libraries:** streamlit, matplotlib, PIL, numpy
* **Logistic Equation:** X(n)=r\*X(n-1)\*(1-X(n-1)), *r* is growth rate.
* **Credit:** Inspired by [Complexity Explorer website](https://www.complexityexplorer.org)
* **Bifurcation:** Source from [Complexity Explorer website](https://s3.amazonaws.com/complexityexplorer/DynamicsAndChaos/Programs/bifurcation.html)
""")

#----------------------------------------------------------------------------#
# Page layout (continued)
## Divide page to 2 columns (col1=sidebar, col2=page contents)
col1, col2 = st.beta_columns((2,1))
col1 = st.sidebar

#----------------------------------------------------------------------------#
col1.header('Set Parameters')

## Sldebar - set parameters
iteration_steps = col1.slider('The number of itereations (n)', 1, 1000, 20)
initial_value  = col1.slider('The initial value of (x0)', 0.0, 1.0, 0.4)
initial_value1  = col1.slider('The initial value of (y0)', 0.0, 1.0, 0.6)
growth_rate  = col1.slider('The growth rate (r)', 0.0, 4.0, 1.5)

# col2.header('The results of iterations')  # not align to the left
# align the header text to the left
st.markdown("<h3 style='text-align: left; color: red;'>The results of iterations</h3>", unsafe_allow_html=True)

# Show a horizontal line
#st.write('---')

#----------------------------------------------------------------------------#
# Define logistic equation and do interations
# Return three list, x, y and difference of them
def logistic_equation(steps, x0, y0, r):
    iterate_result = []
    iterate_result1 = []
    iterate_diff = []
    iterate_result.append(x0)
    iterate_result1.append(y0)
    iterate_diff.append(x0-y0)
    # start iteration
    for i in range(steps):
        x1 = r*x0*(1-x0)
        y1 = r*y0*(1-y0)
        iterate_result.append(x1)
        iterate_result1.append(y1)
        iterate_diff.append(x1-y1)
        x0 = x1
        y0 = y1

    return iterate_result, iterate_result1, iterate_diff

# This function return adjusted x-ticks for given steps automatically
def get_xticks(steps):
    if steps < 10:
        x_ticks = np.arange(0, steps+1, 1)
    elif steps < 20:
        x_ticks = np.arange(0, steps+1, 2)
    elif steps < 100:
        x_ticks = np.arange(0, steps+1, 5)
    elif steps < 200:
        x_ticks = np.arange(0, steps+1, 10)
    elif steps < 500:
        x_ticks = np.arange(0, steps+1, 25)
    else:
        x_ticks = np.arange(0, steps+1, 50)
    return x_ticks

# Get the iterated results and plot it out
iteration_result, iteration_result1, iteration_diff = logistic_equation(iteration_steps, initial_value, initial_value1, growth_rate)

## The first iteration results
f, ax = plt.subplots(figsize=(8, 4))
plt.title('Results of the first iteration', fontsize=10)
plt.plot(iteration_result, color='r', lw=0.5, marker='o', mec='r', mfc='r', ms=5)
plt.ylim(0.0, 1.0)
plt.xlim(-1, iteration_steps+1)
my_x_ticks = get_xticks(iteration_steps)
my_y_ticks = np.arange(0.0, 1.0, 0.1)
plt.xticks(my_x_ticks)
plt.yticks(my_y_ticks)
plt.xticks(fontsize=6)
plt.yticks(fontsize=6)
st.pyplot(f)

## The first and the second itereation results
f, ax = plt.subplots(figsize=(8, 4))
plt.title('Results of the first and the second iterations', fontsize=10)
plt.plot(iteration_result, color='r', lw=0.5, marker='o', mec='r', mfc='r', ms=3)
plt.plot(iteration_result1, color='b', lw=0.5, marker='D', mec='b', mfc='b', ms=3, alpha = 0.5)
plt.ylim(0.0, 1.0)
plt.xlim(-1, iteration_steps+1)
my_x_ticks = get_xticks(iteration_steps)
my_y_ticks = np.arange(0.0, 1.0, 0.1)
plt.xticks(my_x_ticks)
plt.yticks(my_y_ticks)
plt.xticks(fontsize=6)
plt.yticks(fontsize=6)
st.pyplot(f)

## The difference of two itereation results
f, ax = plt.subplots(figsize=(8, 4))
plt.title('The difference of two iterations', fontsize=10)
plt.plot(iteration_diff, color='g', lw=0.5, marker='o', mec='g', mfc='g', ms=3)
plt.ylim(-1.0, 1.0)
plt.xlim(-1, iteration_steps+1)
my_x_ticks = get_xticks(iteration_steps)
my_y_ticks = np.arange(-1.0, 1.0, 0.1)
plt.xticks(my_x_ticks)
plt.yticks(my_y_ticks)
plt.xticks(fontsize=6)
plt.yticks(fontsize=6)
st.pyplot(f)

# Output the numerical values
st.write('---')
if st.button('Show me the numbers!'):
    st.markdown("<h3 style='text-align: left; color: red;'>The numerical values of iterations</h3>", unsafe_allow_html=True)
    results = np.column_stack((iteration_result, iteration_result1, iteration_diff))
    results = pd.DataFrame(results, columns=['x', 'y','x-y'])
    st.write(results)
