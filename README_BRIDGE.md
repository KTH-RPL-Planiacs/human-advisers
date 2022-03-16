# prism_bridge
A bridge from [PRISM](https://www.prismmodelchecker.org/)'s java API to python using [Py4J](https://www.py4j.org/).

## Installation

### [PRISM](https://www.prismmodelchecker.org/) or [PRISM-games](https://www.prismmodelchecker.org/games/)
You can use [PRISM](https://www.prismmodelchecker.org/) or [PRISM-games](https://www.prismmodelchecker.org/games/). 
I recommend building from source, please check the respective websites for build instructions. 

### [Py4J](https://www.py4j.org/)
Py4J is used to create a java gateway in order to access the PRISM java API from python. 
```
pip3 install py4j
```

## Usage
In order to run the bridge, first start the java PRISM handler. Make sure your classpath includes py4j 
and the PRISM-games .class files and .jars either by extending the CLASSPATH or using the -cp option.

### Extending the Class Path
While I recommend using ```javac -cp...``` to link necessary .class and .jar files, you can of course also extend 
the class path permanently. You will find the PRISM files in your PRISM directory.
The Py4J jar might be in different places, but it usually should be in ```/usr/local/share/``` after installation. 
Make sure the version number is correct.
```
export PRISM_HOME="/your/path/to/prism/prism"
export CLASSPATH="${CLASSPATH}:${PRISM_HOME}/classes"
export CLASSPATH="${CLASSPATH}:${PRISM_HOME}/lib/*"
export CLASSPATH="${CLASSPATH}:/usr/local/share/py4j/py4j0.10.9.1.jar"
export LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:${PRISM_HOME}/lib/"
```

### Compiling the .java Files
I have not tested for different JDK versions, but in theory all modern and/or open source variants should work.
```
cd prism_bridge
javac PrismEntryPoint.java
java PrismEntryPoint.java
```

Once the gateway is running, run the main code or the unittests. 
Check the [PRISM-api github](https://github.com/prismmodelchecker/prism-api) for further examples and information.
