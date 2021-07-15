#!/usr/bin/env python
# coding: utf-8
import pyaoscx
from pyaoscx.session import Session
from pyaoscx.pyaoscx_factory import PyaoscxFactory
from pyaoscx.vlan import Vlan
from pyaoscx.interface import Interface
from pyaoscx.static_route import StaticRoute
from pyaoscx.vrf import Vrf
import urllib3
urllib3.disable_warnings()
# In[14]:


#get to know the pyaoscx and where it is installed.
get_ipython().system('pip show pyaoscx')


# In[12]:


# There are two approaches to workflows, both using the session.
version = '10.04'
switch_ip = '192.168.50.6'
s = Session(switch_ip, version)
s.open('admin', 'admin1')


# #  APPROACH 1: OPEN GRANULATED APPROACH VLAN

# In[ ]:



# Create Vlan object -- Not yet materialized
#Vlan is Python Class has been defined in PYTHON module pycentral.vlan
#vlan200 is a object or instance of this Class

vlan200 = Vlan(s, 200, name="VLAN 200", voice=True)


# In[ ]:


# Since object is not materialized, performs a POST request -- This method internally makes a GET request right after the POST
# Obtaining all attributes VLAN related
#If you an "Internal server error", that means the vlan is already exsisted.
vlan200.apply()


# In[ ]:


#display all Vlans


# In[ ]:


Vrf.get_all(s)


# In[ ]:


#add description for vlan200
vlan200.description = "New description, changed via pyaoscx SDK1"
vlan200.apply()

# Now vlan200 contains the description attribute
print("VLAN 200 description {}".format(vlan200.description))


# In[ ]:


# Now let's create another object, that we know already exists inside of the Switch
vlan1 = Vlan(s, 1)
# Perform a GET request to obtain all data and materialize object
vlan1.get()


# In[ ]:


# Now, we are able to modify the objects internal attributes
vlan1.voice = True
# Apply changes
changed = vlan1.apply()
# If changed is True, a PUT request was done and object was modified


# In[ ]:


# More complex example using the OPEN GRANULATED APPROACH
# Create an Interface object

lag = Interface(s, 'lag1')
lag.apply()


# In[ ]:


# Create a Vlan object

vlan_1 = Vlan(s, 1)
    # In this case, now that the VLAN exists within the Switch,
    # a GET request is called to obtain the VLAN's information.
    # The information is then added to the object as attributes.
vlan_1.get()

 


# In[ ]:


# Interfaces/Ports added to LAG
port_1_1_8 = Interface(s, '1/1/8')
port_1_1_8.get()
 # Make changes to configure LAG as L2
lag.admin = 'down'
lag.routing = False
lag.vlan_trunks = [vlan_1]
lag.lacp = "passive"
lag.other_config["mclag_enabled"] = False
lag.other_config["lacp-fallback"] = False
lag.vlan_mode = "native-untagged"
lag.vlan_tag = vlan_1
 # Add port as LAG member
lag.interfaces.append(port_1_1_8)

 # Apply changes
lag.apply()

 # ===========================================================
 # ===========================================================
 # ===========================================================


# #  APPROACH 2: IMPERATIVE FACTORY APPROACH

# pyaoscx.pyaoscx_factory provide a Factory class to instantiate all pyaoscx Modules through specific methods.
# https://github.com/aruba/pyaoscx/blob/master/pyaoscx/pyaoscx_factory.py
# 

# In[ ]:


# Create VLAN 201
# Create Factory object, passing the Session Object
factory = PyaoscxFactory(s)


# In[ ]:


# Create Vlan object
# If vlan is non-existent, Factory instantly creates it inside the switch device
vlan201 = factory.vlan(201, "NAME201")


# In[ ]:


# Same complex example using the IMPERATIVE FACTORY APPROACH
# PLUS USING IMPERATIVE METHODS

# Create the Interface object
lag2 = factory.interface('lag2')
modified = lag2.configure_l2(
        description="Created using imperative method",
        admin='up',
        vlan_mode="native-untagged",
        vlan_tag=1,
        trunk_allowed_all=True,
        native_vlan_tag=True)

# If modified is True, a PUT request was done and object was modified


# In[ ]:


# At the end, the session MUST be closed
s.close()

