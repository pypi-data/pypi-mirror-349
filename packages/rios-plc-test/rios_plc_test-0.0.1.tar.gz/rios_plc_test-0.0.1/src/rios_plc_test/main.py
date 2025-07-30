from pycomm3 import LogixDriver

with LogixDriver('192.168.1.10') as plc:
    print(plc.get_tag_list())
