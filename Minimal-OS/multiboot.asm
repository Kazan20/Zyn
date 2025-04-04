; multiboot.asm
[bits 32]
[global multiboot_header]

section .multiboot
multiboot_header:
    dd 0x1BADB002  ; magic number
    dd 0x00        ; flags
    dd - (0x1BADB002 + 0x00)  ; checksum
