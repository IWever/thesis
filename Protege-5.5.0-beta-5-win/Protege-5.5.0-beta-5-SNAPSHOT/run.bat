setlocal
cd /d %~dp0
jre\bin\java -Xmx500M -Xms200M -Xss16M -XX:CompileCommand=exclude,javax/swing/text/GlyphView,getBreakSpot -DentityExpansionLimit=100000000 -Dlogback.configurationFile=conf/logback-win.xml -Dfile.encoding=utf-8 -Dorg.protege.plugin.dir=plugins -classpath bundles/guava.jar;bundles/logback-classic.jar;bundles/logback-core.jar;bundles/slf4j-api.jar;bin/org.apache.felix.main.jar;bin/maven-artifact.jar;bin/protege-launcher.jar org.protege.osgi.framework.Launcher %1
