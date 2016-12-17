from pyvndaal import *

vndaal = VNDAAL()
vndaal.open_connection()
vndaal.login()
vn_list = vndaal.get_vns_by_name('jaoiejaifjeajoefij')
if vn_list == "ERROR: NO RESULTS FOUND":
	print(vn_list)
vndaal.close_connection()
for vn in vn_list:
	print(vn.data['title'] + " - " + vn.get_vndb_link())