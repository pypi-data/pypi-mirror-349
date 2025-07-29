# Mviewer Plotly/Dash React Component

Dash contains a very large number of components for data display and UI configuration.  However, specialized display and interaction components are sometimes needed to fill discipline-specific roles.  All Dash components are written using React, a JavaScript library for building user interfaces, written and maintained by Facebook. 

mviewer is a Dash React component, part of an interactive astronomical image viewer written as part of the Montage toolkit (http://montage.ipac.caltech.edu).  mviewer really only handles the display window and functions like zooming and panning.  It is the front-end for Python-based Dash apps which control what data gets displayed. The Dash app also handles the processing of "pick" and "draw box" events from mviewer.

Even the Dash app does not itself render the image/overlay graphics that get display.  For that it relys on a Python-callable Montage library.
All of this is covered in more detail at http://montage.ipac.caltech.edu/docs/mViewer_DASH .


## Building mviewer

mviewer is a standard React component, but to make sure it is built right Dash provides a boilerplate template (https://github.com/plotly/dash-component-boilerplate.git) that can be used with Python "cookiecutter" to configure a directory tree for the build.  For all the details on this, see https://dash.plotly.com/react-for-python-developers .  The configuration will even result in a README.md (this file), though it usually needs to be reworked after the fact.
