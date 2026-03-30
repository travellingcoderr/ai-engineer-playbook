using Microsoft.EntityFrameworkCore;
using Nexus.Application;
using Nexus.Infrastructure;
using Nexus.Infrastructure.Data;
using OpenTelemetry.Metrics;
using OpenTelemetry.Trace;
using Azure.Monitor.OpenTelemetry.AspNetCore;

var builder = WebApplication.CreateBuilder(args);

// --- OpenTelemetry Configuration ---
var otelBuilder = builder.Services.AddOpenTelemetry();

otelBuilder.WithTracing(tracing =>
{
    tracing.AddAspNetCoreInstrumentation()
           .AddHttpClientInstrumentation()
           .AddConsoleExporter();
});

otelBuilder.WithMetrics(metrics =>
{
    metrics.AddAspNetCoreInstrumentation()
           .AddHttpClientInstrumentation()
           .AddConsoleExporter();
});

if (!string.IsNullOrWhiteSpace(builder.Configuration["APPLICATIONINSIGHTS_CONNECTION_STRING"]))
{
    otelBuilder.UseAzureMonitor();
}
// -----------------------------------

// Add Services from Layers (Clean Architecture Pattern)
// Repository & Service DI (Dependency Injection)
// Infrastructure DI (SOLID - D)
builder.Services.AddInfrastructureServices(builder.Configuration);
// Application DI (SOLID - L)
builder.Services.AddApplicationServices();

// Api Layer Services
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();

    // Data Seeding
    using (var scope = app.Services.CreateScope())
    {
        var services = scope.ServiceProvider;
        var context = services.GetRequiredService<NexusDbContext>();
        DbInitializer.Initialize(context);
    }
}

app.UseHttpsRedirection();
app.UseAuthorization();
app.MapControllers();

app.Run();
