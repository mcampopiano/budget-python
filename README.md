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

### Envelopes
Methods supported:
* GET
* POST
* PUT
* DELETE

In order to get a list of all envelopes, make a get request to `http://localhost:8000/envelopes`

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
