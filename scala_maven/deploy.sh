#!/usr/bin/env bash


package () {
mvn clean compile assembly:single
}

upload () {
scp target/*dependencies.jar bu:~/jars/
}
