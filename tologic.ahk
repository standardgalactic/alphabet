#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

;; +-/\÷*^∋%∈∫∉√&!≈<|>≤≥=⊣⊢⊥⊤

;;≤∋÷ <≥%/∫ -|!⊣& *!⊢ ∈≥√≈> !=÷| ≤∋÷ ∉+⊤⊥ \!^


;; https://standardgalactic.github.io/alphabet/cipher.html ;;


;; Logico-Philosophicus Keyboard ;;

:*:a::{+}
:*:b::-
:*:c::/
:*:d::\
:*:e::÷ 
:*:f::*
:*:g::{^}
:*:h::∋
:*:i::%
:*:j::∈

:*:k::∫ 
:*:l::∉
:*:m::√
:*:n::&
:*:o::{!}
:*:p::≈
:*:q::<
:*:r::|
:*:s::>
:*:t::≤
:*:u::≥
:*:v::=
:*:w::⊣
:*:x::⊢
:*:y::⊥
:*:z::⊤

;; Translate to Logico

;; awk '{print tolower($0) | "tr 'a-z' '+-/\÷*^∋%∈∫∉√&!≈<|>≤≥=⊣⊢⊥⊤'"}' input-text.txt > output-cipher.txt

;; Translate Logico to Latin

;; awk '{gsub(/[+-\/\\÷\*^∋%∈∫∉√&!≈<|>\≤≥=⊣⊢⊥⊤]/, substr("abcdefghijklmnopqrstuvwxyz", match("+-/\÷*^∋%∈∫∉√&!≈<|>≤≥=⊣⊢⊥⊤", substr($0, RSTART, RLENGTH))), 1))}1' input-cipher.txt > output-text.txt



!s::Suspend ; Press Alt+s to suspend, and Alt+s again to resume
