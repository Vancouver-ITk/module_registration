

import os
import tkinter as tk
from tkinter.constants import DISABLED, NORMAL
import itkdb
import json
# import importlib
# import create_modules as qm # functions from QMUL scripts (author: Paul Miyagawa)
# add_batch = importlib.import_module('database-batches.add_to_batch') # functions from Liverpool scripts (author: Sven Wonsak)

from sys import path as sys_dot_path
this_file_directory = os.path.dirname(os.path.abspath(__file__))
print(this_file_directory)
sys_dot_path.insert(1, this_file_directory + '/../../database-batches/')

import add_to_batch as add_batch


# VARIABLES TO EDIT / DEFAULT VALUES
INSTITUTE = "SFU"
DEFAULT_BATCH = "PPC_SFU"
DEFAULT_LOCAL_NAME = ""

CURRENT_LONG_TAB_SHEET = "20USEVL0200221"
CURRENT_SHORT_TAB_SHEET = "20USEVS0200683"

DEFAULT_R1_TAB_JIG = "20USERT0131099"
DEFAULT_R2_TAB_JIG = "20USERT0245005"
DEFAULT_R4M0_TAB_JIG = "20USERT0442012"
DEFAULT_R4M1_TAB_JIG = "20USERT0442012"
DEFAULT_R5M0_TAB_JIG = "20USERT0510906"
DEFAULT_R5M1_TAB_JIG = "20USERT0510906"

# CONSTANTS
ENTRY_X = 100
ENTRY_Y = 20

global data, client

# read in user info
def authenticate_user():
  global client
  # lient = None  
  db_passcode_1 =  db_pass_1.get()
  db_passcode_2 =  db_pass_2.get()

  if db_passcode_1 and db_passcode_2:
    try :
        db_user_box.configure(state=NORMAL)
        user = itkdb.core.User(access_code1 = db_passcode_1, access_code2 = db_passcode_2)
        client = itkdb.Client(user=user)
        client.user.authenticate()
        user = client.get('getUser', json={'userIdentity': client.user.identity})
        db_user_box.insert('1.0', "{} {}".format(user["firstName"], user["lastName"]))
        db_user_box.configure(state=DISABLED)
        os.environ["ITKDB_ACCESS_CODE1"] = db_passcode_1
        os.environ["ITKDB_ACCESS_CODE2"] = db_passcode_2
        output_text.set("Database authorization successful!")
    except:
        output_text.set("Database credentials were entered incorrectly. Try again.")
  else: output_text.set("Passcodes weren't entered")

  return client
  # client.set(client)


def set_local_name(mod_type):
  # open file 
  file = open("PPC_local_name_numbers.txt", "r")

  content = file.readlines() 

  num_count = "0000"
  if (mod_type == "R1"):
    num_count = content[1]
  elif (mod_type == "R2"):
    num_count = content[3]
  elif (mod_type == "R4M0"):
    num_count = content[5]
  elif (mod_type == "R4M1"):
    num_count = content[7]
  elif (mod_type == "R5M0"):
    num_count = content[9]
  elif (mod_type == "R5M1"):
    num_count = content[11]

  prod_phase = DEFAULT_BATCH.split('_')[0]
  inst = DEFAULT_BATCH.split('_')[1]
  temp = inst + '_' + mod_type + '_' + prod_phase + '_' + num_count
  mod_local = str(temp)

  return mod_local 


def update_local_num(mod_type):
  # open file 
  with open('PPC_local_name_numbers.txt', 'r', encoding='utf-8') as file:
    content = file.readlines() 
    num_count = "0000"
    if (mod_type == "R1"):
      num_count = content[1]
    elif (mod_type == "R2"):
      num_count = content[3]
    elif (mod_type == "R4M0"):
      num_count = content[5]
    elif (mod_type == "R4M1"):
      num_count = content[7]
    elif (mod_type == "R5M0"):
      num_count = content[9]
    elif (mod_type == "R5M1"):
      num_count = content[11]

  # convert count to integer to increment it by 1
  num_count_int = int(num_count)
  num_count_int+=1

  # convert back to string write file line based on module type 
  if (mod_type == "R1"):
    content[1] = str(num_count_int)
  elif (mod_type == "R2"):
    content[3] = str(num_count_int) + "\n"
  elif (mod_type == "R4M0"):
    content[5] = str(num_count_int)
  elif (mod_type == "R4M1"):
    content[7] = str(num_count_int)
  elif (mod_type == "R5M0"):
    content[9] = str(num_count_int)
  elif (mod_type == "R5M1"):
    content[11] = str(num_count_int)

  with open('PPC_local_name_numbers.txt', 'w', encoding='utf-8') as file:
    file.writelines(content)
    file.close()

def register_component():

  global client

  if sensor_sn.get() == "" or module_box.curselection() == ():
    output_text.set("Please ensure that all mandatory fields are filled out.")
  else: 
    
    try: 
      module_type = module_box.get(module_box.curselection()[0])
      sensor = sensor_sn.get()
      jig = tab_jig.get()
      sheet = tab_sheet.get()
      local = local_name.get()
      batch = batch_name.get()
    

      # Verify that user is entering real componenets

      sensor_component = get_component_details(client, sensor)
      # check if sensor exists
      if sensor_component == None: 
         output_text.set("ERROR: Sensor not found in database")
         return
      
      jig_component = get_component_details(client, jig)
      # check if HV tab jig exists
      if jig_component == None: 
         output_text.set("ERROR: HV Tabbing Jig not found in database")
         return
      
      sheet_component = get_component_details(client, sheet)
      # check if HV tab sheet exists
      if sheet_component == None: 
         output_text.set("ERROR: HV Tab Sheet not found in database")
         return

      # All components exist   
      print("Sensor, HV Tabbing Jig, and HV Tab Sheet all successfully found in database. ")
    except: 
      output_text.set('ERROR: Either the sensor, HV tabbing jig or HV tab sheet were not found in the database. ')

    data={'project': "S", 
          'subproject': "SE", 
          'institution': "SFU",
          'componentType': "MODULE",
          'type': module_type,
          'properties': {'LOCALNAME': local, 'HV_TAB_ASSEMBLY_JIG': jig},
          # 'batches': {'number': "DEFAULT_BATCH", 'batchType': "MODULE_BATCH"}
          }
    

  #  'batches': [{'id': '668eff1b8e930f004302da4d', 'number': 'PPC_SFU', 
  #             'batchType': {'id': '646b881f931a9c0042134875', 'code': 'MODULE_BATCH', 'name': 'Module Batch'}, 
  #             'state': 'ready', 'stateTs': '2024-11-21T21:45:40.577Z', 'stateUserIdentity': '7986-4353-1'}]

    try: 
      component = client.post("registerComponent", json=data) 
      update_local_num(module_type)
      add_batch.main(client, component['component']['serialNumber'], batch, batch_type='MODULE_BATCH', check_prefix=True)
    except UnboundLocalError:
      print("Error: A value may have been missed, check if module type is still entered.")
    except Exception as e: 
      print(e)
      output_text.set("Error: New module could not be registered, see terminal for more details.")  
    
      # if (exc.response.json['uuAppErrorMap'][0] == "ucl-itkpd-main/assembleComponent/componentAtDifferentLocation"):
      #   output_text.set("Child sensor component is not in the same location as parent module.")
      # elif (exc.response.json['uuAppErrorMap'][0] == "ucl-itkpd-main/assembleComponent/childComponentAlreadyAssembled"):
      #   output_text.set("Sensor is already assembled to another module. (Important note: Module was still created in the database without sensor child)") 
      # else:  
      #   output_text.set("Error in registering module.")  

    try: 
      child = client.post("assembleComponent", json={'parent': component['component']['serialNumber'], 'child': sensor_component['id'], 'properties': {'HV_TAB_SHEET': sheet}})
      output_text.set("Module {0} successfully registered!".format(component['component']['serialNumber']))
    except itkdb.exceptions.BadRequest as e:
      print(e)
      output_text.set("Error: Sensor could not be attached to module, see terminal for more details. \nIMPORTANT: Module {0} was still created in the database without it's sensor child!".format(component['component']['serialNumber']))   
      
    
  # update_tab_count(client, tab_sheet)    

   

# adapted from qm script - not needed for now 
'''
def get_tab_number(tab_SN, hvtabRespJ ):
    ntabmod = 0
    for propJ in hvtabRespJ['properties']:
        if propJ['code'] == 'NUMBER_TABS_FOR_MODULES':
            if propJ['value'] is not None:
                ntabmod = propJ['value']
    ntabmod += 1
    print(ntabmod)

    tabmodJSON = {
        'component': tab_SN,
        'code': 'NUMBER_TABS_FOR_MODULES',
        'value': ntabmod
    }
    return tabmodJSON
'''
    
# next functions is adapted from QMUL scripts to update tab count - followup on this 
'''
def update_tab_count(c, tab_SN):
  uSuccess, hvtabRespJ = qm.get_component(c, tab_SN)
  tabmodJ = get_tab_number(tab_SN, hvtabRespJ)
  uSuccess, tabmodRespJ = qm.set_component_property(c, tabmodJ)
'''  

# adapted from Liverpool script - this one doesn't work with alternative IDs
def get_component_details(c, comp_sn):  
    try:
        comp = c.get("getComponent", json={"component": comp_sn})
        return comp
    except:
        return None
    

# setup up GUI input fields
root = tk.Tk()

frame = tk.Frame(root, height = 575, width = 500)
frame.pack()

db_pass_1 = tk.StringVar()
db_pass_2 = tk.StringVar()
sensor_sn = tk.StringVar()
tab_jig = tk.StringVar()
tab_sheet = tk.StringVar()
batch_name = tk.StringVar()
local_name = tk.StringVar()
output_text = tk.StringVar()

batch = DEFAULT_BATCH

title = tk.Label(frame, text = 'Module Registration GUI', font = ('calibri', 18))
title.place(x = 150, y = 10 )

#add fields 
db_pass_1_label = tk.Label(frame, text="AccessCode 1")
db_pass_1_label.place(x = ENTRY_X, y = ENTRY_Y + 50)
db_pass_1_box = tk.Entry(frame, textvariable = db_pass_1, show='*', justify = 'left', width = 15)
db_pass_1_box.place(x = ENTRY_X + 100, y = ENTRY_Y + 50)

db_pass_2_label = tk.Label(frame, text="AccessCode 2")
db_pass_2_label.place(x = ENTRY_X, y = ENTRY_Y + 80)
db_pass_2_box = tk.Entry(frame, textvariable = db_pass_2, show='*',  justify = 'left', width = 15)
db_pass_2_box.place(x = ENTRY_X + 100, y = ENTRY_Y + 80)

auth_button = tk.Button(frame, text = "Authenticate", command = lambda: authenticate_user())
auth_button.place(x = ENTRY_X + 250, y = ENTRY_Y + 65)

db_user_label = tk.Label(frame, text="User:")
db_user_label.place(x = ENTRY_X, y = ENTRY_Y + 110)
db_user_box = tk.Text(frame, font = ('calibri', 10), width = 15, height = 1, relief = 'sunken', state=DISABLED)
db_user_box.place(x = ENTRY_X + 100, y = ENTRY_Y + 110)            


sensor_label = tk.Label(frame, text="Sensor SN:")
sensor_label.place(x = ENTRY_X - 75, y = ENTRY_Y + 170)
sensor_box = tk.Entry(frame, textvariable = sensor_sn,  justify = 'left', width = 20)
sensor_box.place(x = ENTRY_X + 15, y = ENTRY_Y + 170)

module_label = tk.Label(frame, text='Module Type:')
module_label.place(x = ENTRY_X - 75, y = ENTRY_Y + 200)
module_box = tk.Listbox(frame, width = 10, relief = 'groove', height = '6')
module_box.place(x = ENTRY_X + 15, y = ENTRY_Y + 200)
module_box.insert(1,"R1")
module_box.insert(2,"R2")
module_box.insert(5,"R4M0")
module_box.insert(6,"R4M1")
module_box.insert(7,"R5M0")
module_box.insert(8,"R5M1")        


tab_jig_label = tk.Label(frame, text="HV Tabbing Jig SN:")
tab_jig_label.place(x = ENTRY_X + 175, y = ENTRY_Y + 150)
tab_jig_box = tk.Entry(frame, textvariable = tab_jig,  justify = 'left', width = 20)
tab_jig_box.place(x = ENTRY_X + 175, y = ENTRY_Y + 170)

tab_sheet_label = tk.Label(frame, text="HV Tab Sheet SN:")
tab_sheet_label.place(x = ENTRY_X + 175, y = ENTRY_Y + 200)
tab_sheet_box = tk.Entry(frame, textvariable = tab_sheet,  justify = 'left', width = 20)
tab_sheet_box.place(x = ENTRY_X + 175, y = ENTRY_Y + 220)

def autofill():
  # clear all the boxes 
  tab_jig_box.delete(0, tk.END)
  tab_jig_box.insert(0, "")
  tab_sheet_box.delete(0, tk.END)
  tab_sheet_box.insert(0, "")
  local_box.delete(0, tk.END)
  local_box.insert(0, "")

  module_type = module_box.get(module_box.curselection()[0])

  if module_type == "R1":
    tab_jig_box.insert(0, DEFAULT_R1_TAB_JIG) 
    tab_sheet_box.insert(0, CURRENT_SHORT_TAB_SHEET) 
  elif module_type == "R2":
    tab_jig_box.insert(0, DEFAULT_R2_TAB_JIG) 
    tab_sheet_box.insert(0, CURRENT_SHORT_TAB_SHEET) 
  elif module_type == "R4M0":
    tab_jig_box.insert(0, DEFAULT_R4M0_TAB_JIG) 
    tab_sheet_box.insert(0, CURRENT_SHORT_TAB_SHEET) 
  elif module_type == "R4M1":
    tab_jig_box.insert(0, DEFAULT_R4M1_TAB_JIG) 
    tab_sheet_box.insert(0, CURRENT_SHORT_TAB_SHEET)   
  elif module_type == "R5M0":
    tab_jig_box.insert(0, DEFAULT_R5M0_TAB_JIG) 
    tab_sheet_box.insert(0, CURRENT_SHORT_TAB_SHEET)
  elif module_type == "R5M1":
    tab_jig_box.insert(0, DEFAULT_R5M1_TAB_JIG) 
    tab_sheet_box.insert(0, CURRENT_LONG_TAB_SHEET)  

  local_box.insert(0, set_local_name(module_type))  


autofill_button = tk.Button(frame, text = "Autofill", command = lambda: autofill())
autofill_button.place(x = ENTRY_X + 15, y = ENTRY_Y + 320)

batch_label = tk.Label(frame, text="Batch:")
batch_label.place(x = ENTRY_X + 175, y = ENTRY_Y + 250)
batch_box = tk.Entry(frame, textvariable = batch_name,  justify = 'left', width = 20)
batch_box.insert(0, DEFAULT_BATCH)
batch_box.place(x = ENTRY_X + 175, y = ENTRY_Y + 270)

local_label = tk.Label(frame, text="Local Name (OPTIONAL):")
local_label.place(x = ENTRY_X + 175, y = ENTRY_Y + 300)
local_box = tk.Entry(frame, textvariable = local_name,  justify = 'left', width = 20)
local_box.place(x = ENTRY_X + 175, y = ENTRY_Y + 320)

reg_button = tk.Button(frame, text = "Register Module", command = lambda: register_component())
reg_button.place(x = ENTRY_X + 100, y = ENTRY_Y + 370)

output_text_box = tk.Message(frame, textvariable = output_text, font = ('calibri', 10), width = 344, relief = 'sunken', justify = 'left')
output_text_box.place(x = ENTRY_X - 30, y = ENTRY_Y + 410)
output_text.set('Please enter your DB credentials, then press \'Authenticate\' to verify user. Once you choose the correct "Module Type", press \'Autofill\' to fill in preset default Jig and Tab Sheet serial numbers. If everything looks correct, press  \'Register Module\' to register module with the child component sensor attached in database.' )

root.mainloop()