# d-OR-plan

Desktop OR Planner. A desktop wrapper for applications based on the Cornflow-client format. Check out the [Cornflow project](https://github.com/baobabsoluciones/cornflow).
[Here is a guide](https://baobabsoluciones.github.io/cornflow/guides/deploy_solver_new.html) on how to configure an app in the right format.

Another option is just to check the tests/data/graph_coloring example that comes inside the project. 

## Installation

Running uv or pip should work:

Using uv:

```
uv install dorplan
```

Using pip
```
python -m pip install dorplan
```

## Testing

If you want to test the example app, run:

```commandline
python -m unittest dorplan.tests.test_app.AppTest.test_open_app
```

## Functionality

* Import and export data (in json format and Excel).
* Load example data.
* Solve an instance.
* Show interactive logs in the GUI.
* Stop a running solver, if the correct callback is implemented.
* Generate report, if a quarto report is available.
* Open the report in a new browser tab.