brew install portaudio
brew install swig
python3 -m pip install --upgrade pip setuptools wheel
brew install cmu-pocketsphinx
brew install openal-soft
pushd .
cd /usr/local/include
sudo ln -s /usr/local/Cellar/openal-soft/1.21.1/include/AL/* .
popd
python3 -m pip install -r requirements.txt
