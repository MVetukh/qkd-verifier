(* Автогенерируемый файл: coq/Generated/b92_inst.v *)

From Coq Require Import Reals Lra.
Open Scope R_scope.

Definition N : R := (100000.0000000000)%R.
Definition p_psi0 : R := (0.5000000000)%R.
Definition p_psi1 : R := (0.5000000000)%R.

Definition delta_ph_lower : R := (0.0449900000)%R.
Definition delta_ph_upper : R := (0.0450100000)%R.

Definition eps_target : R := (0.0000000010)%R.

(* На MVP-этапе эти леммы помечаем как Admitted.
   Позже заменим на проверяемые доказательства через CoqInterval/рационализацию. *)

Lemma delta_ph_bounds :
  0 <= delta_ph_lower /\ delta_ph_lower <= delta_ph_upper /\ delta_ph_upper <= 1.
Admitted.

Lemma delta_ph_nonneg : 0 <= delta_ph_upper.
Admitted.

Lemma prob_norm_ok :
  0 <= p_psi0 /\ 0 <= p_psi1 /\ p_psi0 + p_psi1 = 1.
Admitted.

Theorem b92_security_stub : 0 <= 1.
Proof. lra. Qed.