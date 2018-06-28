from setuptools import setup

setup(name='stripe_pipeline',
      version='0.1',
      description='Simple Stripe Event data pipeline',
      url='https://github.com/bufferapp/stripe-pipeline',
      author='Michael Erasmus',
      author_email='hi@michaelerasm.us',
      license='MIT',
      packages=['stripe_pipeline'],
      install_requires=[
          'stripe',
          'sqlalchemy',
          'psycopg2',
          'python-dateutil',
          'boto3',
          'smart-open',
          'click',
          'retrying'
      ],
      entry_points={
        'console_scripts': [
            'stripe-pipeline=stripe_pipeline.cli:main'
        ]
      })
