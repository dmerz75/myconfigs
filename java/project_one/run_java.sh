#!/bin/bash


run_java ()
{

    javac $1.java
    java $1

}

# Example:
# javac StringExample.java
# java StringExample
#      -- without the .class extension
run_java $1
