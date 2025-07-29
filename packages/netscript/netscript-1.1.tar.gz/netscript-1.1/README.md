# NetScript

A simple python script to host a flask server to run python scripts and output over a network.


### URL's

- /start
- stop
- log

### Usage

```python

from netscript.script_server import ScriptServer

py_exec = "venv/bin/python3.12"
py_script = "active/NetScript/netscript/netscript/tests/script_1.py"
app = ScriptServer(py_exec, py_script, "script_out.txt", 3000)
app.run()

```


### Example Script

- Website
- HTML example download