# Budget API

## Resources
* Users
* Auth tokens
* Envelopes
* General expenses
* Budgets
* Deposits
* Recurring expenses
* Payments

### Running the server
In the terminal, run the commands (It is necessary to install python and pipenv prior to running these commands): 
```javascript
git clone git@github.com:mcampopiano/budget-python.git
cd budget-python
pipenv shell
python3 manage.py runserver
```
The last command will start running ther server at port localhost:8000

**NOTE**
All requests will require the following header:
`'Authorization': 'Token (insert user token here)'`
all POST requests will also require the header `'Content-Type': 'application/json'`

### Envelopes
Methods supported:
* GET
* POST
* PUT
* DELETE

#### List all envelopes
Make a GET request to `http://localhost:8000/envelopes`

This will return a list of JSON strings in the following format:
```JSON
{
        "id": 1,
        "name": "Groceries",
        "user": {
            "key": "fa2eba9be8282d595c997ee5cd49f2ed31f65bed",
            "created": "2020-08-29T13:24:27.172000Z",
            "user": 1
        },
        "budget": 400.0,
        "is_active": true,
        "payment": [
            {
                "id": 1,
                "location": "Publix",
                "amount": 48.57,
                "date": "2021-03-01T14:51:39.989000Z",
                "budget": 1,
                "envelope": 1
            }
        ],
        "total": 48.57
    }
```
Notice that the returned data includes an array called "payment". This data is pulled in from the generalExpenses table, and will include all instances whose envelope id matches the current envelope. The value of the "total" property is the sum of the "amount" properties on each payment.

#### Get single envelope
Make a GET request to `http://localhost:8000/envelopes/1`, the number after `envelopes/` being the id of the desired envelopes.
However, in most cases when you would need to get a single envelope, you only want to see the total spent for a particular budget. This request will return a total for all related general payment instances, including ones attached to different budgets.
In order to get the desired data, a GET request to the following URL will return only general payment instances attached to the desired budget: `http://localhost:8000/envelopes/1?budgetId=14`
**Note** It is important that the user token in the headers matches the user for the requested envelope.

#### Create new envelope
Make a POST request to `http://localhost:8000/envelopes`
The body of the request must be in JSON format and include the name of the envelope and budget.
e.g. 
```json
{
    "name": "movies",
    "budget": 100
}
```
The returned data will look like this:
```json
{
    "id": 12,
    "name": "movies",
    "user": {
        "key": "fa2eba9be8282d595c997ee5cd49f2ed31f65bed",
        "created": "2020-08-29T13:24:27.172000Z",
        "user": 1
    },
    "budget": 100.0,
    "is_active": true,
    "payment": []
}
```
#### Edit envelope
Make a PUT request to `http://localhost:8000/envelopes/1`, the number after `envelopes/` being the id of the desired envelopes.
The body should contain the same data as the for the POST request. For example, if we were to change the budget amount from 100 to 150 for the above created movies envelope, we would make a PUT request to `http://localhost:8000/envelopes/12`

and in the body: 
```json
{
    "name": "movies",
    "budget": 150
}
```
#### Delete envelope
Make a DELETE request to `http://localhost:8000/envelopes/1`, the number after `envelopes/` being the id of the desired envelope.

### General expenses
Instances in the generalExpenses table represent purchases associated both with a particular monthly budget and a particular envelope. For example, a general expense instance could be created to record a shopping trip to the grocery store, where the associated envelope is 'Groceries' and the associate budget is 'March 2021.' There is no direct GET method supported as the individual instances are returned as part of the envelope instances they are associated with.

Methods supported:
* Post
* Delete

#### Create general expense
Make a POST request to `http://localhost:8000/envelopes/1/purchases`, the number after `envelopes/` being the id of the associated envelope.
The body should be structured as follows:
```json
{
    "budgetId": 1,
    "location": "Kroger",
    "date": "2021-03-13",
    "amount": 52.63
}
```

#### Delete general expense
Make a POST request to `http://localhost:8000/envelopes/5/purchases`, the number after `envelopes/` being the id of the desired **generalExpense** instance.

### Budgets
Methods supported:
* GET
* POST

#### Get all budgets
Make a GET request to `http://localhost:8000/budgets`. The returned data will look like this:
```json
{
        "id": 1,
        "user": {
            "key": "fa2eba9be8282d595c997ee5cd49f2ed31f65bed",
            "created": "2020-08-29T13:24:27.172000Z",
            "user": 1
        },
        "month": "03",
        "year": "2021",
        "est_income": 5000.0,
        "income": [
            {
                "id": 1,
                "source": "Paycheck",
                "amount": 1502.37,
                "date": "2021-03-01T14:51:39.989000Z",
                "budget": 1
            },
            {
                "id": 2,
                "source": "Paycheck",
                "amount": 1500.42,
                "date": "2021-03-07T14:51:39.989000Z",
                "budget": 1
            }
        ],
        "actual_inc": 3002.79,
        "total_budget": 780.0,
        "total_spent": 213.69,
        "remaining_budget": 566.31,
        "net_total": 2789.1
    },
```
The data in the *income* array is taken from the *deposits* table. *actual_in* is the sum of the *amount* property on each related deposit. *total_budget* and *total_spent* come from all envelopes (and their general expenses) related to the user whose token is in the header.

#### Get single budget
Make a GET request to `http://localhost:8000/budgets/1`, the number after `budgets/` being the id of the desired envelope. The returned data will be identical to that returned when all budgets are requested.

#### Create budget
Make a POST request to `http://localhost:8000/budgets`
The body of the request must be in JSON format and include the month, year, and estimated income of the budget.

```json
{
    "month": "03",
    "year": "1993",
    "estIncome": 2000.00
}
```
**NOTE** the values of *month* and *year* should be strings, not integers.

### Deposits
Since deposit instances are returned with their associated budgets, GET requests directly to the Deposit Table are not supported.
Methods supported:
* POST
* DELETE

#### Creating a deposit
Make a POST request to `http://localhost:8000/deposits`
The body of the request must be in JSON format and include the id of the related budget, the source (i.e., employer, birthday money, etc), amount, and date of deposit.
```json
{
    "budgetId": 1,
    "source": "Tax refund",
    "amount": "4200",
    "date": "2021-03-12"
}
```
#### Deleting a deposit
Make a POST request to `http://localhost:8000/deposits/1`, the number after `deposits/` being the id of the desired **Deposit** instance.