# MS17-010
MS17-010 is the Microsoft security bulletin which fixes several remote code execution vulnerabilities in the SMB service on Windows systems.

There are numerous things about MS17-010 that make it esoteric, such as manipulating the Windows kernel pool heap allocations, running remote Windows ring 0 shellcode, and the intricacies of the different SMB protocol versions.

We previously improved the ExtraBacon exploit. https://github.com/RiskSense-Ops/CVE-2016-6366

## Scanners
There is a Metasploit scanner and a Python port. The scanners are able to use uncredentialed information leakage to determine if the MS17-010 patch is installed on a host. If it is not installed, it will also check for a DoublePulsar infections.

The Metasploit scanner can take a network range, while the Python script is single target. You can use shell scripting to get a range:

**Linux**
```
for i in `seq 254` ; do python smb_ms17_010.py 192.168.1.$i ; done
```

**Windows**
```
FOR /L %i IN (1,1,254) DO python smb_ms17_010.py 192.168.1.%i 
```

## Exploits
There is an ETERNALBLUE fully ported Metasploit exploit module and an earlier Python PoC.

Currently, support includes:

- Windows 7 SP0 x64
- Windows 7 SP1 x64
- Windows 2008 R2 SP1 x64

Support for Windows XP and x86 platforms is underway.

## Payloads
Windows ring 0 shellcode has been crafted so that instead of DoublePulsar, the transition from ring 0 to ring 3 and running usermode payloads, directly with or without DLL, is done in a single step. The size of the code has also being reworked, as the original shellcode appears to be compiler output, in order to accomodate more complex userland payloads in the first stage.

The improved payload is approximately 15-20% of the original size.

## Resources 
- https://zerosum0x0.blogspot.com/2017/04/doublepulsar-initial-smb-backdoor-ring.html
- https://countercept.com/our-thinking/analyzing-the-doublepulsar-kernel-dll-injection-technique/
- https://www.rapid7.com/db/modules/auxiliary/scanner/smb/smb_ms17_010

## Disclaimer
This code serves an important business purpose for penetration testers and others to show impact to organizations, without having to run NSA malware binaries. We must ask that you use these tools for their intended, lawful purposes, and only with consent of targets.

### License
Apache 2.0 and MSF

### Credits
- @zerosum0x0
- @jennamagius
- @The_Naterz
- @Aleph___Naught
- @nixawk
- @JukeLennings (Countercept)

### Acknowledgements
- Shadow Brokers
- Equation Group
- skape
- Stephen Fewer
