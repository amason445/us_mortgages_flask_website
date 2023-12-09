"""
This app serves as the main entry point when initiliazing the flask app.
It also contains a function that allows initiliazition and unit testing.
Unit testing is initialized from the console command "flask test"
To start the web site use the console command "flask run"
"""

from app import create_app

# initializes app in the testing environment
app = create_app('testing')

# a flask function that allows unit tests to be ran from the tests folder
@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == "__main__":
    app.run()