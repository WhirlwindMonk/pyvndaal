from pyvndaal import *

vndaal = VNDAAL()
vndaal.open_connection()
vndaal.login()
vn = vndaal.get_vn_by_name("Dies Irae")
vndaal.close_connection()
print(vn.data['title'] + " - " + vn.data['description'])