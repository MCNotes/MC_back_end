#!/bin/bash
export CONDA_CACHED=1
if [[ "$TRAVIS_OS_NAME" == "linux" ]];
then
  export OS=Linux;
elif [[ "$TRAVIS_OS_NAME" == "osx" ]];
then
  export OS=MacOSX; brew install pandoc;
else echo "Cannot support MacOSX";
  exit 1;
fi;

if [[ $TRAVIS_PYTHON_VERSION == "2.7" ]];
then
  wget https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh -O miniconda.sh;
elif [[ $TRAVIS_PYTHON_VERSION == 3* ]];
then
  wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh;
else echo "Could not find the specified Python version";
  exit 1;
fi;

if [ ! -d $HOME/download/ ];
then
  mkdir $HOME/download/;
fi;

if [ ! -d $HOME/install/ ];
  then mkdir $HOME/install/;
fi;

export MINICONDA_FILE=$MINICONDA-latest-$OS-x86_64-$PYTHON_VERSION
export MINCONDA_CACHE_FILE=$HOME/download/$MINICONDA_FILE.sh
export MINICONDA_INSTALL=$HOME/install/$MINICONDA_FILE

if [ ! -f $MINCONDA_CACHE_FILE ];
then
  export CONDA_CACHED=0;
  wget http://repo.continuum.io/miniconda/$MINICONDA-latest-$OS-x86_64.sh -O $MINCONDA_CACHE_FILE;
  bash $MINCONDA_CACHE_FILE -b -p $MINICONDA_INSTALL;
fi;

export PATH="$MINICONDA_INSTALL/bin:$PATH";
