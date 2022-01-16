import sys
import json

array = [{"cliente": "jony", "modelo": 2424}, {"cliente": "adad", "modelo": "kangoo"}]

jason = json.dumps(array)

print(jason)