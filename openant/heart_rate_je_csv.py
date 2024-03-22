import csv
import os
import time
from datetime import datetime
from openant.easy.node import Node
from openant.devices import ANTPLUS_NETWORK_KEY
from openant.devices.heart_rate import HeartRate, HeartRateData

def main(device_id=0):
    node = Node()
    node.set_network_key(0x00, ANTPLUS_NETWORK_KEY)

    device = HeartRate(node, device_id=device_id)
    
    folder_name = 'csv-logs'

    # Generate the CSV filename with the current timestamp
    #timestamp = int(time.time())
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] # Get milliseconds without trailing zeros
    csv_filename = os.path.join(folder_name, f"hr_data_{timestamp}.csv")

    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(["timestamp","device_id", "page_specific", "beat_time", "beat_count", "heart_rate", "operating_time",
                         "manufacturer_id_lsb", "serial_number", "previous_heart_beat_time", "battery_percentage"])

        def on_device_data(page: int, page_name: str, data):
            if isinstance(data, HeartRateData):
                # Write the data to the CSV file
                writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
                		  device_id,
                                 data.page_specific, data.beat_time, data.beat_count, data.heart_rate,
                                 data.operating_time, data.manufacturer_id_lsb, data.serial_number,
                                 data.previous_heart_beat_time, data.battery_percentage])
                print(f"Heart rate: {data.heart_rate} bpm, Operating Time: {data.operating_time} seconds")

        device.on_device_data = on_device_data

        try:
            print(f"Starting {device}, press Ctrl-C to finish")
            node.start()
        except KeyboardInterrupt:
            print("Closing ANT+ device...")
        finally:
            device.close_channel()
            node.stop()

if __name__ == "__main__":
    main(device_id=40436)
