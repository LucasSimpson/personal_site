import logging

from .manager import DynamoDBManager

logger = logging.getLogger(__name__)


# TODO make this shit lazy AF
class QuerySet(object):

    def __init__(self, cls):
        self._cls = cls

    def __iter__(self):
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

        return models.__iter__()

