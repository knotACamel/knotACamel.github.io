import logging
import os
import statistics
import time

from pymongo import ASCENDING, MongoClient
from pymongo.errors import PyMongoError

logger = logging.getLogger(__name__)


class AnimalShelter(object):

    def __init__(self, username=None, password=None, host=None, port=None,
                 db=None, collection=None):

        username = username or os.environ.get('AAC_USER')
        password = password or os.environ.get('AAC_PASS')
        host = host or os.environ.get('AAC_HOST', 'localhost')
        port = int(port or os.environ.get('AAC_PORT', 27017))
        db = db or os.environ.get('AAC_DB', 'aac')
        collection = collection or os.environ.get('AAC_COL', 'animals')

        if not username or not password:
            raise ValueError(
                'Database credentials are missing. Set AAC_USER and AAC_PASS '
                'in the environment, or pass them to AnimalShelter().'
            )

        uri = 'mongodb://%s:%s@%s:%d/?authSource=%s' % (
            username, password, host, port, db
        )
        self.client = MongoClient(uri)
        self.database = self.client[db]
        self.collection = self.database[collection]
        logger.info('Connected to %s.%s at %s:%d', db, collection, host, port)

    @staticmethod
    def _require_query(query, operation):
        if query is None or query == {}:
            raise ValueError(
                'A non-empty query is required for %s. An empty query would '
                'match every document in the collection.' % operation
            )
        
    # Create
    def create(self, data):
        if not data:
            logger.warning('create() called with no data; nothing was saved.')
            return False
        if not isinstance(data, dict):
            raise TypeError('create() expects a dictionary.')

        try:
            result = self.collection.insert_one(data)
            return result.inserted_id is not None
        except PyMongoError:
            logger.exception('Insert failed.')
            return False

    # Read
    def read(self, query=None, projection=None, limit=0):
        query = query if query is not None else {}
        try:
            cursor = self.collection.find(query, projection)
            if limit:
                cursor = cursor.limit(limit)
            return list(cursor)
        except PyMongoError:
            logger.exception('Query failed: %s', query)
            return []

    def get_breed_outcome_report(self, min_count=1, limit=None):
        pipeline = [
            {'$match': {'outcome_type': {'$exists': True, '$ne': None}}},

            {'$group': {
                '_id': {'breed': '$breed', 'outcome_type': '$outcome_type'},
                'total': {'$sum': 1},
            }},

            {'$match': {'total': {'$gte': int(min_count)}}},

            {'$sort': {'total': -1, '_id.breed': 1, '_id.outcome_type': 1}},

            {'$project': {
                '_id': 0,
                'breed': '$_id.breed',
                'outcome_type': '$_id.outcome_type',
                'total': 1,
            }},
        ]

        if limit:
            pipeline.append({'$limit': int(limit)})

        try:
            return list(self.collection.aggregate(pipeline))
        except PyMongoError:
            logger.exception('Breed/outcome report failed.')
            return []

    def get_outcome_totals(self):
        pipeline = [
            {'$match': {'outcome_type': {'$exists': True, '$ne': None}}},
            {'$group': {'_id': '$outcome_type', 'total': {'$sum': 1}}},
            {'$sort': {'total': -1}},
            {'$project': {'_id': 0, 'outcome_type': '$_id', 'total': 1}},
        ]

        try:
            return list(self.collection.aggregate(pipeline))
        except PyMongoError:
            logger.exception('Outcome totals report failed.')
            return []

    def get_rescue_candidate_counts(self, rescue_queries):
        counts = {}
        for name, query in (rescue_queries or {}).items():
            try:
                counts[name] = self.collection.count_documents(query)
            except PyMongoError:
                logger.exception('Count failed for profile: %s', name)
                counts[name] = 0
        return counts

    # Update
    def update_one(self, query, update_data):
        self._require_query(query, 'update_one')
        if not update_data:
            raise ValueError('update_one() requires update data.')

        try:
            result = self.collection.update_one(query, {'$set': update_data})
            return result.modified_count
        except PyMongoError:
            logger.exception('Update failed: %s', query)
            return 0

    def update_many(self, query, update_data):
        self._require_query(query, 'update_many')
        if not update_data:
            raise ValueError('update_many() requires update data.')

        try:
            result = self.collection.update_many(query, {'$set': update_data})
            return result.modified_count
        except PyMongoError:
            logger.exception('Update failed: %s', query)
            return 0

    def update(self, query, update_data):
        return self.update_many(query, update_data)

    # Delete
    def delete_one(self, query):
        self._require_query(query, 'delete_one')
        try:
            result = self.collection.delete_one(query)
            return result.deleted_count
        except PyMongoError:
            logger.exception('Delete failed: %s', query)
            return 0

    def delete_many(self, query):
        self._require_query(query, 'delete_many')
        try:
            result = self.collection.delete_many(query)
            return result.deleted_count
        except PyMongoError:
            logger.exception('Delete failed: %s', query)
            return 0

    def delete(self, query):
        return self.delete_many(query)

    DASHBOARD_INDEX_NAME = 'idx_rescue_filters'
    REPORT_INDEX_NAME = 'idx_breed_outcome'

    def create_dashboard_index(self):
        try:
            name = self.collection.create_index(
                [
                    ('breed', ASCENDING),
                    ('sex_upon_outcome', ASCENDING),
                    ('age_upon_outcome_in_weeks', ASCENDING),
                ],
                name=self.DASHBOARD_INDEX_NAME,
                background=True,
            )
            logger.info('Created dashboard index: %s', name)
            return name
        except PyMongoError:
            logger.exception('Could not create the dashboard index.')
            return None

    def create_reporting_index(self):
        try:
            name = self.collection.create_index(
                [
                    ('breed', ASCENDING),
                    ('outcome_type', ASCENDING),
                ],
                name=self.REPORT_INDEX_NAME,
                background=True,
            )
            logger.info('Created reporting index: %s', name)
            return name
        except PyMongoError:
            logger.exception('Could not create the reporting index.')
            return None

    def create_all_indexes(self):
        return [name for name in (self.create_dashboard_index(),
                                  self.create_reporting_index())
                if name]

    def drop_enhancement_indexes(self):
        dropped = []
        existing = self.list_index_names()
        for name in (self.DASHBOARD_INDEX_NAME, self.REPORT_INDEX_NAME):
            if name not in existing:
                continue
            try:
                self.collection.drop_index(name)
                dropped.append(name)
                logger.info('Dropped index: %s', name)
            except PyMongoError:
                logger.exception('Could not drop index: %s', name)
        return dropped

    def list_index_names(self):
        try:
            return list(self.collection.index_information().keys())
        except PyMongoError:
            logger.exception('Could not read index information.')
            return []

    def explain_query(self, query, projection=None):
        try:
            raw = self.collection.find(
                query or {}, projection
            ).explain()
        except PyMongoError:
            logger.exception('Explain failed for query: %s', query)
            return {}

        execution = raw.get('executionStats', {})
        winning = raw.get('queryPlanner', {}).get('winningPlan', {})

        leaf = winning
        while isinstance(leaf, dict) and 'inputStage' in leaf:
            leaf = leaf['inputStage']

        return {
            'stage': leaf.get('stage') if isinstance(leaf, dict) else None,
            'index': leaf.get('indexName') if isinstance(leaf, dict) else None,
            'docs_examined': execution.get('totalDocsExamined'),
            'keys_examined': execution.get('totalKeysExamined'),
            'docs_returned': execution.get('nReturned'),
            'millis': execution.get('executionTimeMillis'),
        }

    def time_query(self, query, projection=None, repeat=5, warmup=1):
        query = query or {}
        for _ in range(max(0, int(warmup))):
            list(self.collection.find(query, projection))

        timings = []
        document_count = 0
        for _ in range(max(1, int(repeat))):
            start = time.perf_counter()
            results = list(self.collection.find(query, projection))
            elapsed_ms = (time.perf_counter() - start) * 1000
            timings.append(elapsed_ms)
            document_count = len(results)

        return {
            'runs': len(timings),
            'best_ms': round(min(timings), 3),
            'median_ms': round(statistics.median(timings), 3),
            'mean_ms': round(statistics.fmean(timings), 3),
            'worst_ms': round(max(timings), 3),
            'docs': document_count,
        }

    def time_aggregation(self, pipeline, repeat=5, warmup=1):
        for _ in range(max(0, int(warmup))):
            list(self.collection.aggregate(pipeline))

        timings = []
        row_count = 0
        for _ in range(max(1, int(repeat))):
            start = time.perf_counter()
            results = list(self.collection.aggregate(pipeline))
            timings.append((time.perf_counter() - start) * 1000)
            row_count = len(results)

        return {
            'runs': len(timings),
            'best_ms': round(min(timings), 3),
            'median_ms': round(statistics.median(timings), 3),
            'mean_ms': round(statistics.fmean(timings), 3),
            'worst_ms': round(max(timings), 3),
            'rows': row_count,
        }
