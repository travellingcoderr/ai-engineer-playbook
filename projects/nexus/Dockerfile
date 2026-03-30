# Build Stage
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /app

# Copy csproj and restore
COPY src/Nexus.sln ./Nexus.sln
COPY src/Nexus.Domain/Nexus.Domain.csproj ./Nexus.Domain/
COPY src/Nexus.Application/Nexus.Application.csproj ./Nexus.Application/
COPY src/Nexus.Infrastructure/Nexus.Infrastructure.csproj ./Nexus.Infrastructure/
COPY src/Nexus.Api/Nexus.Api.csproj ./Nexus.Api/
RUN dotnet restore

# Copy everything else and build
COPY src/ ./
RUN dotnet publish Nexus.Api/Nexus.Api.csproj -c Release -o out

# Runtime Stage
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS runtime
WORKDIR /app
COPY --from=build /app/out ./
ENTRYPOINT ["dotnet", "Nexus.Api.dll"]
