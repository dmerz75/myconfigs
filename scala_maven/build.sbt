name := "RunEpsilon"
version := "1.0"
organization := "com.pg.bigdata"
//scalaVersion := "2.11.12" // 2.11.12, 2.10.7
scalaVersion := "2.12.4"
crossScalaVersions := Seq("2.11.12", "2.12.4")
val sparkVersion = "2.3.2"

libraryDependencies ++= Seq(
  "org.apache.spark" %% "spark-sql" % sparkVersion,
  "org.apache.spark" %% "spark-core" % sparkVersion,
  "org.apache.spark" %% "spark-streaming" % sparkVersion,
  "org.apache.spark" %% "spark-streaming-twitter" % sparkVersion
)

//import javax.naming.spi.Resolver

/*
lazy val commonSettings = Seq(
  name := "RunEpsilon",
  version := "1.0",
  organization := "com.pg.bigdata",
  scalaVersion := "2.10.7", // 2.11.12, 2.10.7
  sparkVersion := "2.2.0"
  //  scalaVersion in ThisBuild := "2.10.7"
//  sparkVersion := "2.2.0", // tried: 2.3.2
//  sparkComponents ++= Seq("sql", "streaming", "mllib")
)
// assemblySettings: base?
Seq(baseAssemblySettings: _*)

lazy val app  = (project in file ("release"))
  .settings(commonSettings)
  .settings(mainClass in assembly := Some("com.pg.bigdata"))
*/




//// Resolvers:
//resolvers += Resolver.url("jb-bintray", url("http://dl.bintray.com/jetbrains/sbt-plugins"))(Resolver.ivyStylePatterns)

//libraryDependencies ++= Seq(
//  "org.jetbrains" %% "sbt-structure-core" % "7.0.0" // % "2018.2.1"
//  "org.apache.spark" %% "spark-core" % "2.2.0", // 2.3.2
//  "org.apache.spark" %% "spark-sql" % "2.2.0"

  // was not found with 1.2.7
  //  "org.scala-lang" % "scala-library" % "2.11.12",

  //  "org.codehaus.jackson" % "jackson-core-asl" % "1.9.13"
  // %% vs %
  //    libraryDependencies += "org.scala-tools" % "scala-stm_2.11" % "0.3"
  //    libraryDependencies += "org.scala-tools" %% "scala-stm" % "0.3"
//)


//  .enablePlugins(SbtPlugin)



//assemblyMergeStrategy in assembly := (assemblyMergeStrategy in assembly) {
//  case PathList("META-INF", "MANIFEST.MF") => MergeStrategy.discard
//}

//assemblyMergeStrategy in assembly := (assemblyMergeStrategy in assembly) {
//  (old) =>
//  {
//    case PathList("META-INF", "MANIFEST.MF") => MergeStrategy.discard
//    //    case PathList("javax", "servlet", xs @ _*)         => MergeStrategy.first
//    //    case PathList(ps @ _*) if ps.last endsWith ".html" => MergeStrategy.first
//    case "MANIFEST.MF"     => MergeStrategy.discard
//    case x => old(x)
//  }
//}

//assemblyMergeStrategy in assembly := MergeStrategy.discard
//assemblyMergeStrategy in assembly := (assemblyMergeStrategy in assembly) {
//  case PathList("META-INF", "MANIFEST.MF") => MergeStrategy.discard
//}

/*
  old => {
//    case PathList("javax", "servlet", xs @ _*)         => MergeStrategy.first
//    case PathList(ps @ _*) if ps.last endsWith ".html" => MergeStrategy.first
//    case "application.conf" => MergeStrategy.concat
//    case "unwanted.txt"     => MergeStrategy.discard
    case PathList("META-INF", "MANIFEST.MF") => MergeStrategy.discard
    case x => old(x)
  }
}
*/

////assemblyMergeStrategy in assembly := MergeStrategy.discard
//assemblyMergeStrategy in assembly <<= (assemblyMergeStrategy in assembly) {
//  //  case old => {
//  case PathList("META-INF", "MANIFEST.MF") => MergeStrategy.discard
//}

/*
  .settings(
  // more settings here ...
      assemblyMergeStrategy in assembly <<= (assemblyMergeStrategy in assembly) {
      //  case old => {
      case PathList("META-INF", "MANIFEST.MF") => MergeStrategy.discard
      //  case PathList("javax", "xml", xs @ _*) => assemblyMergeStrategy.first
      //  case PathList("org", "w3c", "dom", "TypeInfo.class") => assemblyMergeStrategy.first
      //  case x => old(x)
      //  }
    }

  )
*/
//  .scalaVersions("2.11.12")
//  .enablePlugins(sbt-assembly)
//  .dependsOn(commonSettings)
//  .settings(commonSettings)


/*
libraryDependencies ++= Seq(
  "org.scala-lang" % "scala-library" % "2.11.12",
  "org.apache.spark" %% "spark-core" % "2.3.2", // use 2.3.2 with 2.11.12
  "org.apache.spark" %% "spark-sql" % "2.3.2",
  "org.apache.log4j" %% "log4j.Logger",
  "org.apache.log4j" %% "log4j.Level",
  "org.slf4j" % "slf4j-api" % "1.7.26",
  "org.slf4j" % "slf4j-simple" % "1.6.2",
  "org.apache.logging.log4j" % "log4j-api" % "2.11.2",
  "org.apache.logging.log4j" % "log4j-core" % "2.11.2"
  // https://mvnrepository.com/artifact/org.scala-lang/scala-library
  // https://mvnrepository.com/artifact/org.apache.spark/spark-core
  //    "org.apache.spark" %% "spark-core" % "1.2.1",
  //import org.apache.spark.sql.SparkSession
  //  "org.apache.log4j" %% "Logger" % "2.0"
  //  "org.apache.logging.log4j" %% "log4j-core" % "2.0"
  // not found
  // http request
  // logging
)

lazy val app = (project in file("Epsilon")).
  settings(commonSettings: _*).
  settings(
    // your settings here
  )

//import AssemblyKeys._
//
//AssemblyKeys
//seq(assemblySettings: _*)
//enablePlugins(AssemblyPlugin)

//name := "nas_epsilon"
//organization := "com.pg.bigdata"
//version := "0.3"
//scalaVersion := "2.11.12"

/*
traceLevel in run := 0
fork in run := true
scalacOptions ++= Seq("-optimize")

// The following is the class that will run when the jar is compiled!
//mainClass in assembly := Some("Epsilon")
*/

*/
