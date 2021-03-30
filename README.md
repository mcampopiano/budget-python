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
The body of the request must be in JSON format, include the name of the envelope and budget.
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
Make a DELETE request to `http://localhost:8000/envelopes/1`, the number after `envelopes/` being the id of the desired envelopes.
