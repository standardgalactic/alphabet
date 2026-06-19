.intel_syntax noprefix
.code16
.global _start
.text
_start:
    mov ax, 0x0013
    int 0x10
    push 0xa000
    pop es
main_loop:
    mov ah, 0x01
    int 0x16
    jz draw_frame
    mov ah, 0x00
    int 0x16
    mov ax, 0x0003
    int 0x10
    mov ax, 0x4c00
    int 0x21

draw_frame:
    inc BYTE PTR [t]
    xor di, di
    mov WORD PTR [y], 0
row_loop:
    mov WORD PTR [x], 0
col_loop:
    mov bx, WORD PTR [x]
    mov dx, WORD PTR [y]
        mov al, bl
        add al, dl
        add al, BYTE PTR [t]
        and al, 15
        shl al, 4
        xor al, 42
    stosb
    inc WORD PTR [x]
    cmp WORD PTR [x], 320
    jb col_loop
    inc WORD PTR [y]
    cmp WORD PTR [y], 200
    jb row_loop
    jmp main_loop

t: .byte 0
x: .word 0
y: .word 0
