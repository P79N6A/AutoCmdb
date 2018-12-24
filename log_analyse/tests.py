from django.test import TestCase

# Create your tests here.
from log_analyse.services.getIP import get_ip

ip_list = ["210.22.175.114",
           "218.95.245.90",
           "27.19.200.202",
           "222.67.132.201",
           "180.158.32.146",
           "122.227.206.246",
           "180.157.221.23",
           "120.244.121.133",
           "60.190.25.222",
           "101.88.108.82"]






for i in ip_list:
    z = get_ip(i)
    print(z)