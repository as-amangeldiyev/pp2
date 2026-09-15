"""Examples of transforming every item with map and lambda."""


# Here is a list of temperatures in Celsius to transform into Fahrenheit.
celsius_temperatures = [0, 15, 25, 30]
fahrenheit_temperatures = list(map(lambda temperature: temperature * 9 / 5 + 32, celsius_temperatures))
print("Fahrenheit temperatures:", fahrenheit_temperatures)
