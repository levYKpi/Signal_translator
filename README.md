# Signal_translator
Транслятор паскалеподібної мови на мову асемблера (Python)
Курсова робота (3 курс) з основ проектування транслятора


граматика мови:
1. <signal-program> --> <program>
2. <program> --> PROGRAM <procedure-identifier> ;
			<block>. |
			PROCEDURE <procedure-identifier><parameters-list> ;
				 <block> ;
3. <block> --> <declarations> BEGIN <statementslist> END
4. <declarations> --> <constant-declarations><variable-declarations>
     <math-functiondeclarations><procedure-declarations>
5. <constant-declarations> --> CONST <constantdeclarations-list>|
				      <empty>
6. <constant-declarations-list> --> <constantdeclaration><constant-declarationslist>|
				         <empty>
7. <constant-declaration> --> <constantidentifier> = <constant>;
8. <constant> --> <complex-constant> |
		     <unsigned-constant> |
                             - <unsigned-constant>
9. <variable-declarations> --> VAR <declarationslist>|
                                                 <empty>
10. <declarations-list> --> <declaration>
                                           <declarations-list> |
                                           <empty>
11. <declaration> --><variableidentifier><identifiers-list>: <attribute><attributes-list> ;
12. <identifiers-list> --> , <variable-identifier> <identifiers-list> |
                                        <empty>
13. <attributes-list> --> <attribute> <attributeslist> |
                                      <empty>
14. <attribute> --> SIGNAL |
                              COMPLEX |
                              INTEGER |
                              FLOAT |
                              BLOCKFLOAT |
                              EXT |
                              [<range><ranges-list>]
15. <ranges-list> --> ,<range> <ranges-list> |
                                  <empty>
16. <range> --> <unsigned-integer> .. <unsignedinteger>
17. <math-function-declarations> --> DEFFUNC <function-list> |
                                                             <empty>
18. <function-list> --> <function> function-list> |
                                     <empty>
19. <function> --> <function-identifier> = <expression><function-characteristic> ;
20. <function-characteristic> --> \ <unsignedinteger>, <unsigned-integer>
21. <procedure-declarations> --> <procedure> <procedure-declarations> |
                                                      <empty>
22. <procedure> --> PROCEDURE <procedureidentifier> <parameters-list> ;
23. <parameters-list> --> ( <declarations-list> ) |
                                         <empty>
24. <statements-list> --> <statement> <statementslist> |
                                        <empty>
25. <statement> --> LINK <variable-identifier> , <unsigned-integer> ; |
                                 IN <unsigned-integer>; |
                                 OUT <unsigned-integer>;
26. <complex-constant> --> '<complex-number>'
27. <unsigned-constant> --> <unsigned-number>
28. <complex-number> --> <left-part> <right-part>
29. <left-part> --> <expression> |
                               <empty>
30. <right-part> --> ,<expression> |
                                $EXP( <expression> ) |
                                <empty>
31. <constant-identifier> --> <identifier>
32. <variable-identifier> --> <identifier>
33. <procedure-identifier> --> <identifier>
34. <function-identifier> --> <identifier>
35. <identifier> --> <letter><string>
36. <string> --> <letter><string> |
                          <digit><string> |
                          <empty>
37. <unsigned-number> --> <integerpart><fractional-part>
38. <integer-part> --> <unsigned-integer>
39. <fractional-part> --> #<sign><unsigned-integer>|
                                        <empty>
40. <unsigned-integer> --> <digit><digits-string>
41. <digits-string> --> <digit><digits-string> |
                                     <empty>
42. <sign> --> + |
                         - |
                        <empty>
43. <digit> --> 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
44. <letter> --> A | B | C | D | ... | Z
