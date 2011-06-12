import unittest
import flyingcow

class User(flyingcow.model.Model):
    name = flyingcow.properties.Property()
    email = flyingcow.properties.Property()
    
    _for_hook_tests = ""
    
    def on_create(self):
        self._for_hook_tests = "on_create_called"
    
    def on_update(self):
        self._for_hook_tests = "on_update_called"
    

class ModelTest(unittest.TestCase):
    
    def setUp(self, *args, **kwargs):
        """
        Purge the DB between tests.
        """
        with open("tests/setup.sql") as f:
            load_query = f.read()
        flyingcow.db.connection().execute(load_query)
        super(ModelTest, self).setUp(*args, **kwargs)
    
    def test_create_with_constructor_kargs(self):
        """
        When creating object using keyword arguments in the Model constructor, 
         - All properties should be set properly except for id
         - When saved, fields should persist correctly, id should be set
        """
        user = User(name='ivan', email='myemail@email.com')
        self.assertEqual('ivan', user.name)
        self.assertEqual('myemail@email.com', user.email)
        self.assertEqual(None, user.id)
        user.save()
        result = flyingcow.db.connection().get('select * from user where email = %s', 'myemail@email.com')
        self.assertEqual('ivan', result['name'])
        self.assertEqual('myemail@email.com', result['email'])
        self.assertEqual(user.id, result['id'])

    def test_assigning_properties_directly(self):
        """
        Properties should persist correctly when assigned using
        property access syntax.
        """
        user = User()
        user.name = 'gnome'
        user.email = 'gnome@garden.com'
        self.assertEqual('gnome', user.name)
        self.assertEqual('gnome@garden.com', user.email)
        user.save()
        result = flyingcow.db.connection().get('select * from user where email = %s', 'gnome@garden.com')
        self.assertEqual('gnome', result['name'])
        self.assertEqual('gnome@garden.com', result['email'])
        self.assertEqual(user.id, result['id'])

    def test_get(self):
        """
        get should return one instance of a model if found, None if none 
        found and throw an exception if more than one found.
        """
        user = User(name='ivan', email='myemail@email.com')
        user.save()
        user = User(name='ivan', email='gnome@garden.com')
        user.save()
        user_get = User.get("email = %s", 'myemail@email.com')
        self.assertTrue(isinstance(user_get, User))
        self.assertEqual('myemail@email.com', user_get.email)
        nonexistant = User.get("email = %s", 'nonexistant')
        self.assertEqual(None, nonexistant)
        self.assertRaises(flyingcow.model.MultipleRows, User.get, "name = %s", 'ivan')

    def test_where(self):
        """
        where should return a list of the Model type or an empty list if no 
        results are found.
        """
        user = User(name='ivan', email='myemail@email.com')
        user.save()
        user = User(name='ivan', email='gnome@garden.com')
        user.save()
        users = User.where("name = %s", 'ivan')
        self.assertEqual(2, len(users))
        self.assertTrue(isinstance(users[0], User))
        no_users = User.where("name = %s", 'noonehere')
        self.assertEqual(0, len(no_users))
        self.assertTrue(isinstance(no_users, list))
    
    def test_where_count(self):
        """
        where_count should return a number with the count for
        the query passed in, or 0 if no matches.
        """
        user = User(name='ivan', email='myemail@email.com')
        user.save()
        user = User(name='ivan', email='gnome@garden.com')
        user.save()
        users = User.where_count("name = %s", 'ivan')
        self.assertEqual(2, users)
        nothere = User.where_count("name = %s", 'nothere')
        self.assertEqual(0, nothere)

    def test_object_query(self):
        """
        object_query accepts a full query and returns native model
        objects.
        """
        user = User(name='ivan', email='myemail@email.com')
        user.save()
        user = User(name='ivan', email='gnome@garden.com')
        user.save()
        users = User.object_query("select * from user where name = %s order by email desc", 'ivan')
        self.assertEqual(2, len(users))
        self.assertTrue(isinstance(users[0], User))
        self.assertEqual('ivan', users[0].name)
        self.assertEqual('myemail@email.com', users[0].email)
    
    def test_save_hooks(self):
        """
        When an object gets saved for first time, Model.on_create gets
        called for the instance.  When the object is updated, 
        Model.on_update gets called for the instance.
        
        We override these hoooks in the original User model and have them
        update a field to make sure the hooks get run correctly.
        """
        user = User(name='ivan', email='myemail@email.com')
        self.assertEqual('', user._for_hook_tests)
        user.save()
        self.assertEqual('on_create_called', user._for_hook_tests)
        user.save()
        self.assertEqual('on_update_called', user._for_hook_tests)
        user2 = User(name='ivan', email='myemail@email.com')
    
    def test_properties(self):
        """
        A model's properties should be an iterable of only the fields
        that are of the Property type.
        """
        self.assertEqual(2, len(User.properties()))
        self.assertTrue('name' in User.properties())
        self.assertTrue('email' in User.properties())

        
    