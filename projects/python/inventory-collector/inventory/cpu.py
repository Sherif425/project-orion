import os

def get_cpu_info():
    return {
        
        "logical_cores": os.cpu_count() 
    }