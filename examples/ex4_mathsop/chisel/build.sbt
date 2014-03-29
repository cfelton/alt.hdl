
scalaVersion := "2.10.2"

//resolvers ++= Seq(
//  "scct-github-repository" at "http://mtkopone.github.com/scct/maven-repo"
//)
addSbtPlugin("com.github.scct" % "sbt-scct" % "0.2")

// most of the examples are small, having the *.scala source code
// at the top-level of the (complex) build directories is not too
// confusing (the opposite IMO).
//scalaSource in Compile := new File("src")

libraryDependencies += "edu.berkeley.cs" %% "chisel" % "latest.release"