#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

#SingleInstance force


;; need to install a font with Phoenician unicode such as
;; Noto Sans Phoenician
;; https://fonts.google.com/noto/specimen/Noto+Sans+Phoenician


;; return to Phoenician ;; alt+r , to run Phoenicianizer 

::phoen::Phoenician 
::Phoenecian::Phoenician
::phoneician::Phoenician

;;adfsdf
;;  𐤃𐤎𐤃𐤅 𐤄𐤕𐤉𐤓𐤁𐤀𐤎𐤃𐤅𐤃𐤎𐤃𐤅𐤅𐤅𐤉𐤏𐤅𐤏𐤉𐤊𐤋𐤉𐤋𐤀𐤃𐤅𐤆𐤅

;; 𐤀𐤁𐤂𐤃𐤄𐤅𐤆𐤇𐤈𐤉𐤊𐤋𐤌𐤍𐤎𐤏𐤐𐤑𐤒𐤓𐤔𐤕;;
;; abgde vzhty klmns opw qrxj

;;𐤀𐤁𐤂𐤃𐤄𐤅𐤄𐤕𐤉𐤊𐤋𐤌𐤍𐤎𐤏𐤐𐤑𐤒𐤓𐤔𐤈

;; correct ;;

;;𐤀𐤁𐤂𐤃𐤄𐤅𐤆𐤇𐤈𐤉𐤊𐤋𐤌𐤍𐤎𐤏𐤐𐤑𐤒𐤓𐤔𐤕

;; Phoenician ;;

;; alf, bet, gaml,delt, he
;;wau, zai,het,tet,yod
;; kaf, lamd, mem, nun, semk
;; ain, pe, tsadik, qof, rosh, shin, tau

:*:a::𐤀
:*:b::𐤁
:*:c::𐤂
:*:d::𐤃
:*:e::𐤄
:*:f::𐤅
:*:g::𐤂
:*:h::𐤇
:*:i::𐤉
:*:j::𐤕
:*:k::𐤊
:*:l::𐤋
:*:m::𐤌
:*:n::𐤍
:*:o::𐤏
:*:p::𐤐
:*:q::𐤒
:*:r::𐤓
:*:s::𐤎
:*:t::𐤈
:*:u::𐤅
:*:v::𐤅
:*:w::𐤑
:*:x::𐤔
:*:y::𐤉
:*:z::𐤆

;; note w for weapon -- tsadik
;; 𐤔 (shin) looks like a double-u but type it with an x like Mexica (Meshica)


;; don't need

;;  :C*:T::𐤈
;:C*:t::𐤕


!r::Suspend ; Press Alt+r to suspend, and Alt+r again to resume 

