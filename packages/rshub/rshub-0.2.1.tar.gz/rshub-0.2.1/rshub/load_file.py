import requests
import io
import logging
from scipy.io import loadmat
from rshub.check_authenticity import return_task_path

class load_file:
    def __init__(self, token, project_name, task_name, fGHz, scenario_flag = 'snow', 
                 output_var = 'tb', inc_ang = 40, var = None):
        self.url = 'https://rshub.zju.edu.cn/'
        self.token = token
        self.project_name = project_name
        self.task_name = task_name
        self.scenario_flag = scenario_flag
        self.output_var = output_var
        self.inc_ang = inc_ang
        self.var = var
        if not isinstance(fGHz,(str)):
            fGHz=str(fGHz)
        self.fGHz = fGHz
        result = return_task_path(self.token,self.project_name,self.task_name)
        self.task_path = result['path']
        if result['error_message'] is not None and result['task_status']!="failed":
            raise ValueError(f"You cannot download the file: {result['error_message']}")
            
    def load_error_message(self):
        try:
            task_path = self.task_path
            full_url = self.url + 'projects/' + task_path + '/Job/error.txt'
            
            response = requests.get(full_url)
            
            # Raise an exception for bad HTTP responses
            response.raise_for_status()
            
            # Get the error file contents
            error_content = response.text
            
            # Return a structured error dictionary
            print(f"message: {error_content}")
    
        except requests.RequestException as e:
            # Handle different types of request errors
            print(f"Error retrieving file: {e}")
            logging.error(f"Request Error: {e}")
            return None
        
        except Exception as e:
            # Catch any other unexpected errors
            print(f"Unexpected error processing error file: {e}")
            logging.error(f"Unexpected Error: {e}")
            return None
    
    
    def load_outputs(self):
        try:
            # task_path = return_task_path(self.token,self.project_name,self.task_name)
            task_path = self.task_path
            scenario_flag = self.scenario_flag
            output_var = self.output_var
            inc_ang = self.inc_ang
        
            if not isinstance(inc_ang,(str)):
                inc_ang=str(inc_ang)
            if output_var == 'bs':
                full_url = self.url + 'projects/' + task_path + '/Result/Active_fGHz' + \
                self.fGHz + '_ob_angle'+ inc_ang + '.mat'
            else:
                if scenario_flag == 'veg':
                    full_url = self.url + 'projects/' + task_path + '/TB/TB_fGHz' + self.fGHz + '.mat'
                else:
                    full_url = self.url + 'projects/' + task_path + '/Result/Passive_fGHz' + \
                    self.fGHz + '_ob_angle'+ inc_ang + '.mat'
            #print(full_url)
            response = requests.get(full_url)

            if response.status_code == 200:
                # Use io.ByteIO to create a file-like object from the request content
                object = io.BytesIO(response.content)
                
                # load the .mat file 
                mat_data = loadmat(object)
                
                object.close()
                
                if self.var is None:
                    return mat_data
                
                variable = self.var.split()
                print("Variables Loaded")
                if len(variable) == 1 and variable in mat_data:
                    return mat_data[variable]
                
                return {var:mat_data[var] for var in variable if var in mat_data}
            else:
                print("Failed to download the file")
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return None
        except requests.exceptions.ConnectionError as conn_err:
            print(f"Connection error occurred: {conn_err}")
            return None
        except requests.exceptions.Timeout as timeout_err:
            print(f"Timeout error occurred: {timeout_err}")
            return None
        except requests.exceptions.RequestException as req_err:
            print(f"An error occurred: {req_err}")
            return None
            
    def load_veg_TB(self):
        try:
            task_path = self.task_path
            if not isinstance(task_path,dict):
                full_url = self.url + 'projects/' + task_path + '/TB/TB_fGHz' + self.fGHz + '.mat'
                # print(full_url)
                response = requests.get(full_url)

                if response.status_code == 200:
                    # Use io.ByteIO to create a file-like object from the request content
                    object = io.BytesIO(response.content)
                    
                    # load the .mat file 
                    mat_data = loadmat(object)
                    
                    object.close()
                    
                    if self.var is None:
                        return mat_data
                    
                    variable = self.var.split()
                    print("Variables Loaded")
                    if len(variable) == 1 and variable in mat_data:
                        return mat_data[variable]
                    
                    return {var:mat_data[var] for var in variable if var in mat_data}
                else:
                    print("Failed to download the file, please check the error messages")
            else:
                return task_path['error_message']
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return None
        except requests.exceptions.ConnectionError as conn_err:
            print(f"Connection error occurred: {conn_err}")
            return None
        except requests.exceptions.Timeout as timeout_err:
            print(f"Timeout error occurred: {timeout_err}")
            return None
        except requests.exceptions.RequestException as req_err:
            print(f"An error occurred: {req_err}")
            return None
        
    def load_snow_TB(self,inc_ang):
        try:
            # task_path = return_task_path(self.token,self.project_name,self.task_name)
            task_path = self.task_path
            if not isinstance(inc_ang,(str)):
                inc_ang=str(inc_ang)
            full_url = self.url + 'projects/' + task_path + '/Result/Passive_fGHz' + \
            self.fGHz + '_ob_angle'+ inc_ang + '.mat'
            #print(full_url)
            response = requests.get(full_url)

            if response.status_code == 200:
                # Use io.ByteIO to create a file-like object from the request content
                object = io.BytesIO(response.content)
                
                # load the .mat file 
                mat_data = loadmat(object)
                
                object.close()
                
                if self.var is None:
                    return mat_data
                
                variable = self.var.split()
                print("Variables Loaded")
                if len(variable) == 1 and variable in mat_data:
                    return mat_data[variable]
                
                return {var:mat_data[var] for var in variable if var in mat_data}
            else:
                print("Failed to download the file")
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return None
        except requests.exceptions.ConnectionError as conn_err:
            print(f"Connection error occurred: {conn_err}")
            return None
        except requests.exceptions.Timeout as timeout_err:
            print(f"Timeout error occurred: {timeout_err}")
            return None
        except requests.exceptions.RequestException as req_err:
            print(f"An error occurred: {req_err}")
            return None
        
    def load_snow_bc(self,inc_ang):
        try:
            # task_path = return_task_path(self.token,self.project_name,self.task_name)
            task_path = self.task_path
            if not isinstance(inc_ang,(str)):
                inc_ang=str(inc_ang)
            full_url = self.url + 'projects/' + task_path + '/Result/Active_fGHz' + \
            self.fGHz + '_ob_angle'+ inc_ang + '.mat'
            #print(full_url)
            response = requests.get(full_url)

            if response.status_code == 200:
                # Use io.ByteIO to create a file-like object from the request content
                object = io.BytesIO(response.content)
                
                # load the .mat file 
                mat_data = loadmat(object)
                
                object.close()
                
                if self.var is None:
                    return mat_data
                
                variable = self.var.split()
                print("Variables Loaded")
                if len(variable) == 1 and variable in mat_data:
                    return mat_data[variable]
                
                return {var:mat_data[var] for var in variable if var in mat_data}
            else:
                print("Failed to download the file")
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return None
        except requests.exceptions.ConnectionError as conn_err:
            print(f"Connection error occurred: {conn_err}")
            return None
        except requests.exceptions.Timeout as timeout_err:
            print(f"Timeout error occurred: {timeout_err}")
            return None
        except requests.exceptions.RequestException as req_err:
            print(f"An error occurred: {req_err}")
            return None
    def load_soil_TB(self,inc_ang):
        try:
            task_path = self.task_path
            if not isinstance(inc_ang,(str)):
                inc_ang=str(inc_ang)
            full_url = self.url + 'projects/' + task_path + '/Result/Passive_fGHz' + \
            self.fGHz + '_ob_angle'+ inc_ang + '.mat'
            #print(full_url)
            response = requests.get(full_url)

            if response.status_code == 200:
                # Use io.ByteIO to create a file-like object from the request content
                object = io.BytesIO(response.content)
                
                # load the .mat file 
                mat_data = loadmat(object)
                
                object.close()
                
                if self.var is None:
                    return mat_data
                
                variable = self.var.split()
                print("Variables Loaded")
                if len(variable) == 1 and variable in mat_data:
                    return mat_data[variable]
                
                return {var:mat_data[var] for var in variable if var in mat_data}
            else:
                print("Failed to download the file")
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return None
        except requests.exceptions.ConnectionError as conn_err:
            print(f"Connection error occurred: {conn_err}")
            return None
        except requests.exceptions.Timeout as timeout_err:
            print(f"Timeout error occurred: {timeout_err}")
            return None
        except requests.exceptions.RequestException as req_err:
            print(f"An error occurred: {req_err}")
            return None        
    def load_soil_bc(self,inc_ang):
        try:
            task_path = self.task_path
            if not isinstance(inc_ang,(str)):
                inc_ang=str(inc_ang)
            full_url = self.url + 'projects/' + task_path + '/Result/Active_fGHz' + \
            self.fGHz + '_ob_angle'+ inc_ang + '.mat'
            #print(full_url)
            response = requests.get(full_url)

            if response.status_code == 200:
                # Use io.ByteIO to create a file-like object from the request content
                object = io.BytesIO(response.content)
                
                # load the .mat file 
                mat_data = loadmat(object)
                
                object.close()
                
                if self.var is None:
                    return mat_data
                
                variable = self.var.split()
                print("Variables Loaded")
                if len(variable) == 1 and variable in mat_data:
                    return mat_data[variable]
                
                return {var:mat_data[var] for var in variable if var in mat_data}
            else:
                print("Failed to download the file")
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return None
        except requests.exceptions.ConnectionError as conn_err:
            print(f"Connection error occurred: {conn_err}")
            return None
        except requests.exceptions.Timeout as timeout_err:
            print(f"Timeout error occurred: {timeout_err}")
            return None
        except requests.exceptions.RequestException as req_err:
            print(f"An error occurred: {req_err}")
            return None        
        

        
