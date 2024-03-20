from openant.easy.node import Node
from openant.devices import ANTPLUS_NETWORK_KEY
from openant.devices.heart_rate import HeartRate, HeartRateData
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


def main(device_id=0):
    # Connect to InfluxDB
    client = InfluxDBClient(url="http://localhost:8086", token="r6k_FPcwxxy5i3rwOgFNKn3-mh37za2kFoJFZ8iEwbfd0UgBPJc5SMdujm2uiE2cTnQktlle9XDr8aUof3YLlg==", org="113c8128ce90e904")
    write_api = client.write_api(write_options=SYNCHRONOUS)

    node = Node()
    node.set_network_key(0x00, ANTPLUS_NETWORK_KEY)

    device = HeartRate(node, device_id=device_id)

    def on_found():
        print(f"Device {device} found and receiving")

    def on_device_data(page: int, page_name: str, data):
        if isinstance(data, HeartRateData):
            print(f"Heart rate update {data.heart_rate} bpm")

            # Create an InfluxDB point with heart rate data
            point = Point("heart_rate") \
                .tag("device_id", device_id) \
                .field("heart_rate", data.heart_rate) \
                .time(data.operating_time)  # Use the timestamp provided by the device

            # Write the point to InfluxDB
            write_api.write("garmin-james", "113c8128ce90e904", [point])

    device.on_found = on_found
    device.on_device_data = on_device_data

    try:
        print(f"Starting {device}, press Ctrl-C to finish")
        node.start()
    except KeyboardInterrupt:
        print("Closing ANT+ device...")
    finally:
        device.close_channel()
        node.stop()
        client.close()


if __name__ == "__main__":
    main()

