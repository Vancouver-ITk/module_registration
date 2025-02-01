# module_registration
Python script/GUI that EC sites can use to register their modules after HV-tabbing


# Installation

Install dependencies (tk and itkdb). 

Windows:

```
pip install tk itkdb
```

MAC:

```
pip3 install tk itkdb
```

CENTOS: 

```
yum install python3-tkinter

pip3 install itkdb --user
```



This GUI depends on database-batches (written by Sven Wonsak). Therefore, to download this repository, please use a recursive download command to ensure that a copy of (database-batches) is also downloaded:

```
git clone --recursive  https://github.com/Vancouver-ITk/module_registration.git
```



# Edits

At the top of the script there are a few variables that can be preset to reduce the amount of fields the user needs to enter in the GUI. These are:

```
# VARIABLES TO EDIT / DEFAULT VALUES
INSTITUTE = "SFU"
DEFAULT_BATCH = "PPC_SFU"

CURRENT_LONG_TAB_SHEET = "20USEVL0200221"
CURRENT_SHORT_TAB_SHEET = "20USEVS0200683"

DEFAULT_R1_TAB_JIG = "20USERT0131099"
DEFAULT_R2_TAB_JIG = "20USERT0245005"
DEFAULT_R4M0_TAB_JIG = "20USERT0442012"
DEFAULT_R4M1_TAB_JIG = "20USERT0442012"
DEFAULT_R5M0_TAB_JIG = "20USERT0510906"
DEFAULT_R5M1_TAB_JIG = "20USERT0510906"
```

INSTITUTE: This is mandatory to set. This is the user's institute code.

DEFAULT_BATCH: This is optional to set, if you leave it empty (eg. "") then the user will have enter it in the GUI. If populated, then when opening the GUI, the batch field will be autofilled with value specified above (eg. "PPC_SFU"). This can be overwritten in GUI if necessary.

CURRENT_x_TAB_SHEET: This is optional to set, if you leave it empty (eg. "") then the user will have enter it in the GUI. If set, then after choosing the module type and then pressing 'Autofill', the Tab Sheet field will be autofilled with value specified above (eg. "20USEVS0200683" for modules that use short tabs). This can be overwritten in GUI if necessary.

DEFAULT_x_TAB_JIG: This is optional to set, if you leave it empty (eg. "") then the user will have enter it in the GUI. If set, then after choosing the module type and then pressing 'Autofill', the Tab Jig field will be autofilled with value specified above (eg. "20USERT0131099" for R1 module). This can be overwritten in GUI if necessary.


# Running

To run the file, open a terminal and navigate to the folder containing this program and enter the following command:

Windows:

```
python module_registration.py
```

Linux/MAC:

```
python3 module_registration.py
```

The GUI will pop up and you will have to sign into the database, enter the parameters for the module you are registering, and then a module with it's specified sensor will be registered in the ITkPD. 

