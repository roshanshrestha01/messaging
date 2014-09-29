BROKER_URL = 'redis://localhost:6379/0'

# List of modules to import when celery starts.
CELERY_IMPORTS = ('msgin.models', )

## Using the database to store task state and results.
CELERY_RESULT_BACKEND = 'redis://localhost'

CELERY_ANNOTATIONS = {'tasks.add': {'rate_limit': '10/s'}}
