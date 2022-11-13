from json import load

from django.core.management.base import BaseCommand
from inventory.models import Stock


class Command(BaseCommand):
    help = "Loads stock data from file"

    variable_name_mapping = dict(
        type="stock_type", isEnabled="is_enabled", iexId="iex_id"
    )

    def add_arguments(self, parser):
        parser.add_argument("file")

    def handle(self, *args, **options):
        with open(options["file"], "r") as fp:
            data = load(fp)

        stocks = []
        for record in data:
            mapped_keys = (
                self.variable_name_mapping[k] if k in self.variable_name_mapping else k
                for k in record.keys()
            )
            stocks.append(
                Stock(
                    **dict(
                        zip(
                            mapped_keys,
                            record.values(),
                        ),
                    )
                )
            )
        Stock.objects.bulk_create(stocks)
