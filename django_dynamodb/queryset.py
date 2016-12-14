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

    # given a set of kwargs (ex {'id': '4'}) filters the queryset for only matching items
    # TODO return new queryset. This isnt super trivial - there are cache issues with storing the models that have to be
    # figured out :(
    def filter(self, **filter_args):
        models = self._get_models()
        filtered = list()

        for model in models:
            matches = True
            for attr, value in filter_args.items():
                field = self._cls.get_model_field(attr)
                if field.cast(value) != getattr(model, attr):
                    matches = False

            if matches:
                filtered.append(model)

        return filtered

    # return first instance matching kwargs
    def get(self, *args, **kwargs):
        return self.filter(**kwargs)[0]

    def __iter__(self):
        return self._get_models().__iter__()

    def __len__(self):
        return self._get_models().__len__()

    def __getitem__(self, item):
        return self._get_models()[item]