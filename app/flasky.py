import os
from app import create_app

app = create_app('testing')

@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == "__main__":
    app.run()

# @app.shell_context_processor
# def make_shell_context():
#     return dict()