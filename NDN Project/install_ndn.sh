sudo apt -y update
sudo apt -y install build-essential pkg-config python3-minimal libboost-all-dev libssl-dev libsqlite3-dev
export PATH="${HOME}/.local/bin${PATH:+:}${PATH}"
sudo apt -y install doxygen graphviz python3-pip net-tools iperf3 moreutils
pip3 install --user sphinx sphinxcontrib-doxylink
cd
git clone https://github.com/named-data/ndn-cxx.git
cd ~/ndn-cxx
./waf configure --with-examples --with-tests
./waf
sudo ./waf install
sudo ldconfig
sudo apt -y install software-properties-common
sudo apt -y install libpcap-dev libsystemd-dev
cd
git clone --recursive https://github.com/named-data/NFD.git
cd ~/NFD
export PKG_CONFIG_PATH="~/named-data/pkgconfig:$PKG_CONFIG_PATH"
./waf configure
./waf
sudo ./waf install
sudo cp /usr/local/etc/ndn/nfd.conf.sample /usr/local/etc/ndn/nfd.conf
sudo apt -y update
sudo apt -y install nfd
sudo apt -y update
cd
git clone https://github.com/named-data/ndn-tools.git
cd ~/ndn-tools
./waf configure
./waf
sudo ./waf install
cd
mkdir ndnlogs
sudo pip3 install python-ndn
sudo apt install -y apache2 ffmpeg
wget https://nyu.box.com/shared/static/d6btpwf5lqmkqh53b52ynhmfthh2qtby.tgz -O media.tgz -o wget.log 
sudo tar -v -xzf media.tgz -C /var/www/html/ 
git clone https://github.com/pari685/AStream  
mkdir ~/NDN_STREAMING
mkdir ~/NDN_STREAMING/Files
sudo apt-get install wondershaper