using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Resilience;
using Nexus.Domain.Repositories;
using Nexus.Infrastructure.Data;
using Nexus.Infrastructure.Repositories;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.IdentityModel.Tokens;
using System.Text;
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

            // --- Security Services (JWT) ---
            services.AddSecurityServices(configuration);

            return services;
        }

        private static IServiceCollection AddSecurityServices(this IServiceCollection services, IConfiguration configuration)
        {
            var jwtSettings = configuration.GetSection("JwtSettings");
            var secretKey = jwtSettings.GetValue<string>("SecretKey") ?? "YourSuperSecretKey123!ThatIsAtLeast32CharsLong";

            services.AddAuthentication(options =>
            {
                options.DefaultAuthenticateScheme = JwtBearerDefaults.AuthenticationScheme;
                options.DefaultChallengeScheme = JwtBearerDefaults.AuthenticationScheme;
            })
            .AddJwtBearer(options =>
            {
                options.TokenValidationParameters = new TokenValidationParameters
                {
                    ValidateIssuer = true,
                    ValidateAudience = true,
                    ValidateLifetime = true,
                    ValidateIssuerSigningKey = true,
                    ValidIssuer = jwtSettings.GetValue<string>("Issuer") ?? "NexusAPI",
                    ValidAudience = jwtSettings.GetValue<string>("Audience") ?? "NexusClients",
                    IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(secretKey))
                };
            });

            services.AddAuthorization();

            return services;
        }
    }
}
