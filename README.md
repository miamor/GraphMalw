# Constructing behavior graphs from Cuckoo reports

### About
Similar to [HAN-sec](https://github.com/miamor/HAN-sec), but handling `Ldr[...]` APIs and modules.  
When a process calls `Ldr[...]` APIs, it's actually retrieving address/module/path to call that function (eg. `LdrGetProcedureAddress` will get the address of a function name and call that function).  
Refer to `utils/rep2graph.py` for more details.  

[Example graph](img/0a63152a4c21e43985366350101547e5a7eaf27bdacbf6f91c5bb39275e4197a__VirusShare_8879094e5aa077947123cd62d6051302__4301.json.dot.svg)

There is a mechanism to map an address with a filepath/regkey to know which file/registry key the API is interacting on. But the path is too long for rendering, so the output graph only displays the address of the file/key handle.  
The block code for rendering full path or address here: (in `utils/rep2graph.py`)
```python
            #? Graphviz graph
            # n_txt = f'{node_idx} {node_identifier_str}'
            n_txt = '{} {}'.format(node_idx, node['address']) if 'handle' in node['type'] else f'{node_idx} {node_identifier_str}'
            self.g_codes['nodes'][node_idx] = f'node [shape="{n_shape}" style="{n_style}" color="{n_color}" fontcolor="{n_fontcolor}" fillcolor="{n_fillcolor}"] {node_idx} [label="{n_txt}"]
```

### Types of nodes
```python
    n_types = [
        'proc',     #? process
        'api',      #? api call
        'handle',   #? a handle. thread_handle, file_handle, key_handle (registry), module_handle
        'key_handle',
        'file_handle',
        'module',   #? a module address, which is the actual function that the api calls (when api is LdrLoadDll or LdrGetProcedureAddress)
    ]
```

### Types of connections
```python
    e_types = [
        'proc-api',     #? connects a process to an api, shows that this process makes the first call to this api
        'api-proc',     #? connects an api to the same process that calls it, shows that this api is doing something with this process (normally sees this with NtCreateThreadEx, NtAllocateVirtualMemory, NtMapViewOfSection, NtResumeThread, ...)
        'api-nproc',    #? connects an api to another process, shows that this api spawns a new process (this proc)
        'api-api',      #? connects 2 api, creates a sequence of api calls
        'api-handle',   #? connects an api to a handle, shows that the api affects the handle
        'handle-api',   #? connects an api with a handle, shows that the api get info from the handle to affect other handle
        'api-key_handle',
        'key_handle-api',
        'api-file_handle',
        'file_handle-api',
        'api-module',    #? connects an api to a module, when an api gets the address of a dll
        'module-api'    #? connects a module to an api, when an api uses the address of a loaded dll to get the address of a function to use that function
    ]
```
