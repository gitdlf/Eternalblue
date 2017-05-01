;
; Windows x64 Calculate Hash
;
; Arguments: RSI = string to hash
; Clobbers: RAX, RSI, r9
; Return: r9d = hash
;

calc_hash:
  xor r9, r9

_calc_hash_loop:
  xor eax, eax
  lodsb                                 ; Read in the next byte of the ASCII function name
  ror r9d, 13                           ; Rotate right our hash value
  or al, 0x20                           ; to lower
  add r9d, eax                          ; Add the next byte of the name
  cmp al, ah                            ; Compare AL to AH (\0)
  jne _calc_hash_loop

  ret
