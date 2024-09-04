# Use a multi-stage build to keep the final image small
# Stage 1: Build the application
FROM gradle:8.10.0-jdk17 AS build
WORKDIR /app
COPY build.gradle settings.gradle ./
# COPY src ./src
# RUN gradle build --no-daemon
COPY build/libs/foundation-component-audit-0.0.1-SNAPSHOT.jar ./build/libs/
# Stage 2: Create the final image
FROM amazoncorretto:17-alpine
# Add a non-root user
RUN addgroup -S spring && adduser -S spring -G spring
USER spring:spring

# Set the working directory
WORKDIR /app

# Copy the jar file from the build stageq
COPY --from=build /app/build/libs/*.jar app.jar

# Expose the application port
# EXPOSE 9000

# Run the application
ENTRYPOINT ["java", "-jar", "app.jar"]
