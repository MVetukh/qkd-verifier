(* coq/Theories/Core/Prelude.v *)
From Coq Require Import Reals Lra.
(* Здесь позже появятся определения плотностных матриц, CPTP, etc. *)

(* Минимальная лемма, чтобы файл точно компилировался *)
Lemma core_prelude_ok : 0 <= 1.
Proof. lra. Qed.