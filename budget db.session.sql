SELECT "budgetapi_envelope"."id", "budgetapi_envelope"."user_id", "budgetapi_envelope"."name", "budgetapi_envelope"."budget", "budgetapi_envelope"."is_active" FROM "budgetapi_envelope";


SELECT "budgetapi_generalexpense"."id", "budgetapi_generalexpense"."budget_id", "budgetapi_generalexpense"."envelope_id", "budgetapi_generalexpense"."location", "budgetapi_generalexpense"."amount", "budgetapi_generalexpense"."date" FROM "budgetapi_generalexpense" WHERE "budgetapi_generalexpense"."envelope_id" = 2