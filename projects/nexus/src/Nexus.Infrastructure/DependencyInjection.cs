using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Resilience;
using Nexus.Domain.Repositories;
using Nexus.Infrastructure.Data;
using Nexus.Infrastructure.Repositories;
using System;
using Polly;
using Polly.Retry;

namespace Nexus.Infrastructure
{
    public static class DependencyInjection
    {
        public static IServiceCollection AddInfrastructureServices(this IServiceCollection services, IConfiguration configuration)
        {
            // Database Configuration (InMemory for demo)
            services.AddDbContext<NexusDbContext>(options =>
                options.UseInMemoryDatabase("NexusDb"));

            // Repository Registrations
            services.AddScoped<IAccountRepository, AccountRepository>();

            // --- .NET 8 Resilience (Polly) ---
            services.AddResiliencePipeline("default", builder =>
            {
                builder.AddRetry(new RetryStrategyOptions
                {
                    ShouldHandle = new PredicateBuilder().Handle<Exception>(),
                    MaxRetryAttempts = 3,
                    Delay = TimeSpan.FromSeconds(2),
                    BackoffType = DelayBackoffType.Exponential,
                    UseJitter = true
                })
                .AddTimeout(TimeSpan.FromSeconds(10));
            });

            return services;
        }
    }
}
