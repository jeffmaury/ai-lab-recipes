
Currently, we need the fix from https://github.com/abetlen/llama-cpp-python/pull/1509 
```
pip install git+https://github.com/abetlen/llama-cpp-python.git@refs/pull/1509/head
```

get the path where the lib is installed and add the name property to line 225

/opt/app-root/lib64/python3.11/site-packages/llama_cpp/llama_types.py
