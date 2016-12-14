import logging

from .manager import DynamoDBManager

logger = logging.getLogger(__name__)


# TODO make this shit lazy AF
class QuerySet(object):

    def __init__(self, cls):
        self._cls = cls

    def _get_models(self):
        table = DynamoDBManager.get_manager().get_table(self._cls)

        logger.debug('Scanning table %s for all items' % table)

        response = table.scan()

        data = response['Items']
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])

        models = list()
        for datum in data:
            model = self._cls(from_db=True)
            for key in datum:
                value = datum[key]
                decoded = model.decoded('__%s' % key, value)
                setattr(model, key, decoded)
            models.append(model)

        return models

    def get(self, *args, **kwargs):
        print('queryset GET called with %s, %s' % (args, kwargs))
        # TODO implement this for real
        id = int(kwargs['id'])
        instance = self._cls.filter_hashkey(id)[0]
        print('found model %s' % instance)
        return instance

    def __iter__(self):
        return self._get_models().__iter__()

    def __len__(self):
        return self._get_models().__len__()

    def __getitem__(self, item):
        return self._get_models()[item]