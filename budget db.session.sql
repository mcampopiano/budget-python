SELECT "budgetapi_envelope"."id", "budgetapi_envelope"."user_id", "budgetapi_envelope"."name", "budgetapi_envelope"."budget", "budgetapi_envelope"."is_active" FROM "budgetapi_envelope";


SELECT "budgetapi_generalexpense"."id", "budgetapi_generalexpense"."budget_id", "budgetapi_generalexpense"."envelope_id", "budgetapi_generalexpense"."location", "budgetapi_generalexpense"."amount", "budgetapi_generalexpense"."date" FROM "budgetapi_generalexpense" WHERE "budgetapi_generalexpense"."envelope_id" = 2;

SELECT "budgetapi_envelope"."id", "budgetapi_envelope"."user_id", "budgetapi_envelope"."name", "budgetapi_envelope"."budget", "budgetapi_envelope"."is_active" FROM "budgetapi_envelope" WHERE ("budgetapi_envelope"."is_active" AND "budgetapi_envelope"."user_id" = fa2eba9be8282d595c997ee5cd49f2ed31f65bed);

SELECT 
"budgetapi_envelope"."id", 
"budgetapi_envelope"."user_id", 
"budgetapi_envelope"."name", 
"budgetapi_envelope"."budget", 
"budgetapi_envelope"."is_active" 
FROM "budgetapi_envelope" 
WHERE ("budgetapi_envelope"."is_active" 
AND "budgetapi_envelope"."user_id" = "fa2eba9be8282d595c997ee5cd49f2ed31f65bed");