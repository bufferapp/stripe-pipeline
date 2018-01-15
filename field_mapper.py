from datetime import datetime


def format_datetime(date):
    if date:
        return date.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]


def format_date(timestamp):
    if timestamp:
        return format_datetime(datetime.fromtimestamp(timestamp))


class FieldMapper:
    def __init__(self, input, output, prefix=None):
        self.input = input
        self.output = output
        self.prefix = prefix

    def map(self, input_name, output_name=None, output_transform=None):
        if not output_name:
            output_name = input_name
        if self.prefix:
            output_name = '{}_{}'.format(self.prefix, output_name)

        if output_transform:
            self.output[output_name] = output_transform(
                self.input.get(input_name))
        else:
            self.output[output_name] = self.input.get(input_name)

        return self

    def map_ts(self, input_name):
        if not input_name.endswith('_at'):
            output_name = '{}_at'.format(input_name)
        else:
            output_name = input_name

        return self.map(input_name, output_name, format_date)

    def map_id(self, input_name):
        if not input_name.endswith('_id'):
            output_name = '{}_id'.format(input_name)
        else:
            output_name = input_name

        return self.map(input_name, output_name)
