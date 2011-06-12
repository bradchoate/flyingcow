flyingcow is a no-frills way interact with database persisted objects when 
working with the Tornado framework. It's totally alpha.

It currently relies on Tornado's MySQL connection wrapper and is meant to
serve as a simple container for encapsulating and  defining models.  The 
interface sugar is around working with model objects individually, there
are no meaningful abstractions around the querying, where SQL queries
and SQL snippets are used instead.


Requirements
=======================
* Python 2.6+
* Tornado


Usage
=======================

Model definition
-----------------------
The model class corresponds to a table 'user' in the database with
the fields 'name' and 'email'.  All models assume that the corresponding
table contains a primary key field called 'id' that auto-increments.

import flyingcow

class User(flyingcow.model.Model):
    name = flyingcow.properties.Property()
    email = flyingcow.properties.Property()


Setting up a connection
-----------------------
Before using flyingcow to communicate with your database, you will need to 
establish (i.e. "register) a connection.  You only need to register the 
connection once when you start up your app, your models will have access
to it automatically.

import flyingcow

flyingcow.db.register_connection(host='localhost', name='flyingcow_tests', user='root', password='')


Save & update
-----------------------
An object can be persisted for the first time to the database by calling
save on the instance.  Calling save again on an already-persisted object
will update the record in the database.

# calling save here will perform a INSERT query.  Upon insertion, 
# user.id will be assigned with new record's primary key value' and
# user.on_create() will be called (which does nothing, but is a hook you
# can override in your Model).
user = User(name='ivan', email='myemail@email.com')
user.save()

# calling save here will perform an UPDATE query.  Upon updating
# user.on_update() will be called (which does nothing, but is a hook you
# can override in your Model).
user.name = 'newname'
user.save()


Querying objects
-----------------------
There are a couple of helper class methods for performing queries that 
return model objects.  It is recommended that any query parameters
be passed in as positional arguments, which provides a level of protection
from SQL injection.

Model.get(query_fragment, *parameters)
    Returns only one record or None if no results match the query. If more
    than one result gets returned throws a flyingcow.model.MultipleRows
    exception.
    Ex: User.get("name = %s and email = %s", 'ivan', 'myemail@email.com')

Model.where(query_fragment, *parameters)
    Returns a list of Model objects that match the query or an empty list
    if there are no matches.
    Ex: User.where("name = %s", 'ivan')

Model.where_query(query_fragment, *parameters)
    Same as Model.where, but returns a number with the count corresponding
    to number of results returned by query.

Model.object_query(full_query, *parameters)
    For more complicated queries, you can pass a fully qualified query.
    Any fields returned as part of the result will be used to construct
    model objects for the class at hand.
    Ex: User.object_query("select * from user where name = %s", 'ivan')


