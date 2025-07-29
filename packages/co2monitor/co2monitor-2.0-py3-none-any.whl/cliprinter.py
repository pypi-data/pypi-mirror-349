from api import EnergyData
from handler import Handler


class CliPrinter(Handler):
    def handle(self, data: EnergyData):
        date_str = data.datetime_ams.strftime("%Y-%m-%d %H:%M")
        print(f"{date_str}: {data.co2_amount * 1000:.2f}g CO2/kWh")
