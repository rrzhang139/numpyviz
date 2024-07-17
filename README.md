# NumpyViz

*NumpyViz is a code visualizer that renders dynamic visualizations for Numpy operations.* 

## Overview

If you've ever struggled to understand multi-dimensional array operations -- furiously keeping track of the operation names, aligning dimensions, or visualizing transformations in your head -- you've come to the right place.

While there are lots of resources and documentation about HOW to use Numpy, there surprisingly isn't a lot of content for visual learners like me. I wanted something where I could blindly paste in some arcane matrix code and magically feel these operations, playing and controlling them in real-time. 

This level of understanding and interactivity only had to come from a new tool. What was driven out of sheer need for deeper understanding led to NumpyViz.

## What is it?

In NumpyViz, you can paste in arbitrary Numpy code and it will magically parse the code and return an ordered sequence of operations, complete with visual representations of each step.

This was built with Python, Next.js/Vercel, and Manim, a math animations library, for vizualizations. 

I hope this project aims to develop a comprehensive tool for visualizing machine learning code, with the goal of providing an intuitive and educational way to see how machine learning algorithms, particularly those implemented in PyTorch or Numpy, manipulate data through various array operations.

## Features

- Real-time parsing of Numpy code
- Step-by-step visualization of matrix operations
- Support for a wide range of Numpy functions and operations
- Interactive web interface for easy code input and visualization viewing

## Getting Started
I couldn't host backend on cloud because manim animation rendering took too much memory and storage. So, just run the app locally.

### Prerequisites

- Python (version 3.9 or later)
- Node.js (version 14 or later)
- npm (usually comes with Node.js)
- Git

### Backend
1. Clone the repository:
```
git clone https://github.com/rzhang139/numpyviz.git
cd numpyviz
```

2. Set up a Python virtual environment

3. Install the required Python packages:
```
cd backend
pip install -r requirements.txt
```

4. Start the Flask server:
```
python app.py
```

The backend should now be running on `http://localhost:5000`

### Frontend
1. Open a new terminal window and navigate to the frontend directory:
```
cd frontend
```
2. Install the required npm packages:
```
npm install
```
3. Start the Next.js server:
```
npm run dev
```

The frontend should now be accessible at `http://localhost:3000`

## Future Ideas

**For anyone playing with this repo, please feel free to DM me on [twitter](https://twitter.com/rzhang139) if you run into any issues or would like to contribute**

[ ] Robust parsing module (Handle syntax edge cases)
[ ] User controls (video speed, quality, etc)
[ ] Developing more visualization intuition around some tricker operations such as np.expand_dims() or np.squeeze()
[ ] Support Pytorch operations
[ ] Support OpenGL for faster rendering