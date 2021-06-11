# Monitor Flask Postgres with Elastic APM

This project is based on https://github.com/Azure-Samples/docker-flask-postgres

The objective was to get a very simple project in Flask PostgreSQL, and inset Elastic APM to take a look at what is happening with each request to the app, specially what queries are made to the database.

I've created some bad routes to have interesting data on Elastic APM dashboard
```
# bad query
@APP.route('/bad_query')
def view_registered_guests_bad_query():
    for _ in range(20):
        guests = Guest.query.all()
    return render_template('guest_list.html', guests=guests)
    
# error message
@APP.route('/hello')
def apm_message_hello():
    apm.capture_message('hello, world!')
    return render_template('apm_hello.html')

# Error
@APP.route('/error')
def apm_error():
    try:
        1 / 0
    except ZeroDivisionError:
        apm.capture_exception()
    return render_template('apm_error.html')

# Unhandled error
@APP.route('/fatal_error')
def apm_fatal_error():
    1 / 0
    return render_template('apm_error.html')
```

Using a HTTP load generator I've generated some load on the server and Elastic APM quickly showed me where to look, I attach some screenshots

## General Overview
![Screenshot 2021-06-11 at 13 08 23](https://user-images.githubusercontent.com/43767/121685118-75da5180-cab7-11eb-826a-238bef3c56da.png)

## GET to / (simple query)
![Screenshot 2021-06-11 at 13 08 36](https://user-images.githubusercontent.com/43767/121685211-8e4a6c00-cab7-11eb-98f0-02192bcfe3a2.png)

## GET to /bad_query (bad query)
![Screenshot 2021-06-11 at 13 08 58](https://user-images.githubusercontent.com/43767/121685252-9c988800-cab7-11eb-8ecb-0bb2169ea466.png)

## GET to /fatal_error (Unhandled division by zero)
![Screenshot 2021-06-11 at 13 09 30](https://user-images.githubusercontent.com/43767/121685290-a91ce080-cab7-11eb-8da8-80cce41ddb7e.png)

## Auto generated Service Map
![Screenshot 2021-06-11 at 13 10 22](https://user-images.githubusercontent.com/43767/121685571-0022b580-cab8-11eb-9ed4-a7cf3ea81950.png)
