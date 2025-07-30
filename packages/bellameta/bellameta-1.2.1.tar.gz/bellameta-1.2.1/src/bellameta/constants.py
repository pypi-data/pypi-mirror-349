import os

from bellameta.utils import get_config

BELLAMETA_CONFIG_PATH = os.getenv('BELLAMETA_CONFIG_PATH')
DB_PATH = os.getenv('DB_PATH')
config_data = get_config(config_path=BELLAMETA_CONFIG_PATH)
COHORTS = config_data['COHORTS']
TASKS = config_data['TASKS']
DEFAULT_TABLES = ['state', 'cohort', 'patient', 'section', 'tag', 'stain', 'task', 'subtype', 'year', 'gleason_grade']
METADATA_TABLES = DEFAULT_TABLES