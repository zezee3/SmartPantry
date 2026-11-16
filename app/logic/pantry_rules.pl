/*
   SmartPantry logic rules.
   Input is the number of days until the recorded expiration date.
   A negative number means the recorded date has passed.
   The 0-to-3 day window is a project reminder rule, not food-safety advice.
*/

:- initialization(main, main).

% Facts: project settings and the priority assigned to each status.
expiring_soon_limit(3).
priority_for_status(expired, review).
priority_for_status(expiring_soon, high).
priority_for_status(fresh, normal).
priority_for_status(no_expiry_date, normal).

% Rules: classify an item from the number of days remaining.
expiry_status(none, no_expiry_date).
expiry_status(Days, expired) :-
    Days < 0,
    !.
expiry_status(Days, expiring_soon) :-
    Days >= 0,
    expiring_soon_limit(Limit),
    Days =< Limit,
    !.
expiry_status(_, fresh).

consumption_priority(Days, Priority) :-
    expiry_status(Days, Status),
    priority_for_status(Status, Priority).

main(Arguments) :-
    maplist(classify_argument, Arguments, Results),
    maplist(writeln, Results).

classify_argument(Value, Result) :-
    to_atom(Value, Atom),
    (   Atom == none
    ->  Days = none
    ;   atom_number(Atom, Days)
    ),
    expiry_status(Days, Status),
    consumption_priority(Days, Priority),
    format(atom(Result), '~w|~w', [Status, Priority]).

to_atom(Value, Atom) :-
    (   string(Value)
    ->  atom_string(Atom, Value)
    ;   Atom = Value
    ).
