#
# Build stage
#
FROM maven:3.8.4-jdk-8-slim AS build
COPY java/src /home/app/src
COPY java/pom.xml /home/app
RUN mvn -f /home/app/pom.xml clean package

#
# Package stage
#
FROM java:8
COPY --from=build /home/app/target/sudoku-solver-1.0-SNAPSHOT.jar /sudoku-solver/sudoku-solver.jar
COPY puzzles.txt /sudoku-solver
WORKDIR /sudoku-solver
ENTRYPOINT ["java","-jar","sudoku-solver.jar"]
