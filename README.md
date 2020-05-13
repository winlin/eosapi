# API Wrap for EOS

### Setup
```
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.7 -y
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python3.7 get-pip.py
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1

sudo pip3.7 install tornado ujson request
```


#### Interfaces

- get_blockid by block_num
```
curl --location --request GET 'http://localhost:50001/get_blockid?block_num=120469066'
```

RESULT:
```
{"id":"072e364a0bcf8c2824c44fd5a0e92a2e64fa6633e0df0b16fabbc29161af4404","ts":1589375558.2452514}
```
