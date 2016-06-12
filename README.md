Vaca SQL
===================


> **UNDER DEVELOPMENT:**

> Please not that vaca is currently under development.


Think of Vaca as SQL + Python. It allows you to run SQL code into a python terminal in a very easy way. In exchange of use it you will get:
- Very easy database connection setup
- Sql helpers that will bring you light when working with date ranges.
- Transpose rows, convert a query result into a dictionary to easy manipulation.
- Save your result in json, csv or plain text.
- Print your query in a pretty mode
- Send your query result by email

Let's see an example, run `vaca` in the terminal.

    >> v.q('select * from my_table')
    >> v.show()

or run something like this to print and save your information:

    >> v.q('select * from my_table').show().save_as_json('myfile.json')

----------

How to use it? Configuration
-------------

When you run `vaca` in the terminal you will get a connection running right away, in order to do that you have to create a `config.json` file that will specify you connection and SMTP configuration. The format of the file is the following:

    {
    "connections": [
      {
        "name": "default",
        "db_name": "my db name",
        "db_port": 3306,
        "db_host": "127.0.0.1",
        "db_password": "a beautiful password",
        "db_user": "root maybe?",
        "db_type": "mysql or sqlite",
        "db_options": ""
      }
    ],
    "smtp": {
        "host": "localhost",
        "port": 25,
        "user": null,
        "password": null
    }}

please note that if you are using a ´sqlite´ database you only have to specify the db_name param,

     {
        "connections": [
          {
            "name": "default",
            "db_name": "sqlite.db",
            "db_port": "",
            "db_host": "",
            "db_password": "",
            "db_user": "",
            "db_type": "sqlite",
            "db_options": ""
          },
          .... other database names
        ],
        "smtp": {
            "host": "localhost",
            "port": 25,
            "user": null,
            "password": null
        }}

Under connection you will add the "name" key that will help you to switch the database you need it.

After creating the **config.json** file you have to create an environ variable of pass it by in the vaca command.

#### Via env variable
    VACA_CONNECTION_CONFIG=path of my config file
    VACA_DEFAULT_CONNECTION=default or another name

#### Via terminal
    vaca --config=my-config.json ----connection=default

-------

Installation
-------------
    pip install pip install -e git+https://github.com/carrerasrodrigo/vaca.git#egg=vaca

----------

Vaca API
-------------

When you run `vaca` in the terminal `v = Vaca()` instance is created and it's ready to use. After that command like

    v.q('select * from my table')

are valid. `q.q(...` created a Query instance, that has the following methods:

#### Query(String query).run()
Runs the query

    v.q('query').run()

#### Query(String query).get() or .get_raw()
It runs the query and returns a list of result if you executed a `select` or the number of modified rows in case of a `insert, delete or update`.

        rows = v.q('query').get()
        print(rows)

The difference between `.get()` and `.get_raw()` it's that the first one will add and extra row with the table titles, in case you are running a select.

#### Query(String query).show()
Print the result of the query. You can run it if the query was a `select`

        rows = v.q('query').show()

#### Query(String query).transpose()
Executes a transpose of the table.

#### Query(String query).get_map()
Returns an iterator that will convert the rows into dictionaries.

#### Query(String query).save_as_text(String name)
Saves the results of the query in a plain format.

#### Query(String query).save_as_json(String name)
Saves the results of the query in json format.

#### Query(String query).save_as_csv(String name, List cvs_args)
Saves the results of the query in csv format.  It uses the csv library of python, so you can use the csv_args param to add extra configuration when saving the file.


Helper Methods
-------------
In order to help you building your queries, there is a couple of helpers, you can import them doing `from vaca import sql`

#### sql.fdate(f=date format, d=date)

    sql.fdate()
    '2016-06-12'
    sql.fdate(f='%Y')
    '2016'

#### sql.date()
    sql.date()
    sql.date(year=2010, month=1, day=1)
    datetime.datetime(2010, 1, 1, 0, 0)


#### sql.fdatetime(f=date format, d=date)
    sql.fdatetime()
    '2016-06-12 19:05:55


#### sql.datetime_range(start, end, date_range=dict(days=1)):
    d_start = sql.date(year=2010, month=1, day=1)
    d_end = sql.date(year=2011, month=1, day=1)
    list(sql.datetime_range(d_start, d_end, date_range=dict(months=1)))

    [datetime.datetime(2010, 1, 1, 0, 0),
     datetime.datetime(2010, 2, 1, 0, 0),
     datetime.datetime(2010, 3, 1, 0, 0),
     datetime.datetime(2010, 4, 1, 0, 0),
     datetime.datetime(2010, 5, 1, 0, 0),
     datetime.datetime(2010, 6, 1, 0, 0),
     datetime.datetime(2010, 7, 1, 0, 0),
     datetime.datetime(2010, 8, 1, 0, 0),
     datetime.datetime(2010, 9, 1, 0, 0),
     datetime.datetime(2010, 10, 1, 0, 0),
     datetime.datetime(2010, 11, 1, 0, 0),
     datetime.datetime(2010, 12, 1, 0, 0),
     datetime.datetime(2011, 1, 1, 0, 0)]

`date_range` is a dictionary that accepts the following params `date_range=dict(days=1, years=1, months=1)`
